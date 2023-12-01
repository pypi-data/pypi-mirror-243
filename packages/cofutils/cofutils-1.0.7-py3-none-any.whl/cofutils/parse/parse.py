#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Parse the SQLite3 database from NVprof or Nsight and print a dictionary for every kernel.
"""

import sys
import os
import argparse
from tqdm import tqdm

from .db import DB
from .kernel import Kernel
from .nvvp import NVVP
from .nsight import Nsight
from collections import defaultdict
from cofutils import cofcsv

def parseArgs():
    parser = argparse.ArgumentParser(description="Parse SQLite3 DB from NVprof or Nsight.")
    parser.add_argument("--file", '-f', type=str, default=None, help="SQLite3 database.")
    parser.add_argument("--csv", '-c', type=str, default=None, help="SQLite3 database.")
    parser.add_argument("--start", '-s', type=float, default=None, help="profile begin time(s)")
    parser.add_argument("--end", '-e', type=float, default=None, help="profile end time(s)")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        raise parser.error("No such file '{}'.".format(args.file))

    return args


def dbIsNvvp(db):
    cmd = "SELECT * FROM sqlite_master where type='table' AND name='StringTable'"
    result = db.select(cmd)
    return True if len(result) == 1 else False


def main():
    args = parseArgs()

    db = DB(args.file)

    prof_start = -1 if args.start is None else args.start*1e9
    prof_end = float('inf') if args.end is None else args.end*1e9



    nvvp = None
    if dbIsNvvp(db):
        nvvp = NVVP(db)
    else:
        nvvp = Nsight(db)

    kInfo = nvvp.getKernelInfo()
    if len(kInfo) == 0:
        print("Found 0 kernels. Exiting.", file=sys.stderr)
        db.close()
        sys.exit(0)
    else:
        print("Found {} kernels. Getting info for each kernel.".format(len(kInfo)), file=sys.stderr)

    nvvp.createMarkerTable()

    prevSeqId = -1
    prevSubSeqId = -1
    prevOp = "na"

    Kernel.profStart = nvvp.getProfileStart()

    if args.csv:
        table = cofcsv(args.csv)
    else:
        table = None

    fwd_stream_time_dict = defaultdict(int)
    bwd_stream_time_dict = defaultdict(int)

    for i in tqdm(range(len(kInfo)), ascii=True):
        info = kInfo[i]
        k = Kernel()

        #Calculate/encode object ID
        nvvp.encode_object_id(info)

        #Set kernel info
        k.setKernelInfo(info)
        #Get and set marker and seqid info
        info = nvvp.getMarkerInfo(k.objId, k.kStartTime, k.kEndTime)
        k.setMarkerInfo(info)
        if k.kStartTime < prof_start or k.kEndTime > prof_end or k.device != 0:
            continue
        



        #If the seqId contains both 0 and non zero integers, remove 0.
        if any(seq != 0 for seq in k.seqId) and (0 in k.seqId):
            k.seqId.remove(0)

        #Set direction (it uses seq id)
        k.setDirection()

        #Set op
        k.setOp()

        #The following code is based on heuristics.
        #TODO: Refactor.
        #Assign subSeqId, adjust seqId and altSeqId
        #seqId can be 0.
        #A kernel can have multiple seqIds both in fprop and bprop.
        #In bprop, seqIds might not decrease monotonically. I have observed a few blips.
        if len(k.seqId):
            assert (k.dir in ["fprop", "bprop"])
            if (k.dir == "fprop"):
                #Check if there is a sequence id larger than the previous
                inc = (k.seqId[-1] > prevSeqId)
                if inc:
                    currSeqId = [x for x in k.seqId if x > prevSeqId][0]
                else:
                    currSeqId = prevSeqId
            else:
                currSeqId = k.seqId[0]

            #if ((currSeqId == prevSeqId) and (k.op == prevOp)):
            if ((currSeqId == prevSeqId) and (k.op == prevOp)) or ((k.op[0] == "forward") and (k.op == prevOp) and
                                                                   (k.mod[0] in ["LSTMCell", "GRUCell", "RNNCell"])):
                #The second condition is to trap cases when pytorch does not use cudnn for a LSTMCell.
                k.subSeqId = prevSubSeqId + 1

            prevSeqId = currSeqId
            prevSubSeqId = k.subSeqId
            prevOp = k.op

            #Keep currSeqId in k.seqId, move everything else to k.altSeqId
            for s in k.seqId:
                if s != currSeqId:
                    k.seqId.remove(s)
                    k.altSeqId.append(s)

            for s in k.altSeqId:
                if s == currSeqId:
                    k.altSeqId.remove(s)

            k.altSeqId = list(set(k.altSeqId))
            if (len(k.altSeqId)):
                (k.altSeqId).sort()

        kernel_info = k.print()
        
        nvtx = kernel_info['op'][0] if len(kernel_info['op'])>0 else None
        if table:
            table.write({'stream': kernel_info['stream'], 'Name': kernel_info['kLongName'], 'time(ms)': kernel_info['kDuration']/float(1e6), 'start(s)': kernel_info['kStartTime']/float(1e9), 'end(s)': kernel_info['kEndTime']/float(1e9), 'nvtx': nvtx})

        if nvtx is not None and 'forward' in nvtx:
            fwd_stream_time_dict[kernel_info['stream']] += kernel_info['kDuration']/float(1e6)
        elif nvtx is not None and  'backward' in nvtx:
            bwd_stream_time_dict[kernel_info['stream']] += kernel_info['kDuration']/float(1e6)
    def print_dict(kernel_dict):
        sorted_keys = sorted(kernel_dict.keys())
        for key in sorted_keys:
            print(f"stream-{key}: {kernel_dict[key]} ms")
    print("forward stage: ")
    print_dict(fwd_stream_time_dict)
    print("backward stage: ")
    print_dict(bwd_stream_time_dict)
    if table:
        cofcsv.save('.')
    db.close()


if __name__ == '__main__':
    main()
