import json
import os
import argparse
import subprocess
import datetime
import time
import torch
import re
import copy
import shutil

GLOBAL_ARGS = None

def parse_str_range(str_range:str):
    str_range_list = str_range.split(',')
    print(str_range_list)
    int_range = []
    for each in str_range_list:
        integers = re.findall(r'\d+', each)
        if '-' in each:
            start = int(integers[0])
            end = int(integers[1])+1
            int_range += list(range(start, end))
        else:
            int_range.append(int(integers[0]))
    return int_range

def logging(msg):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{formatted_time}] {msg}")
    with open("history.cof", "a+") as file:
        file.write(f"[{formatted_time}] {msg}\n")

device_name_map={
    'NVIDIA GeForce GTX 1080 Ti': '1080Ti',
    'NVIDIA A40': '40A',
    'NVIDIA GeForce RTX 3090': '3090RTX'
}

def auto_exec():
    if GLOBAL_ARGS.test:
        print("cofrun test done")
        logging(f"{GLOBAL_ARGS.config_file} test done")
        return
    
    print("executing tasks. we strongly recommend to leverage tmux: \n\
                                                tmux new -s cof\n\
                                                tmux attach -t cof\n\
                                                Ctrl+b d\n\
          if process hangs up during batch mode, you can input \"pkill python\" to skip the current task\n")
    if GLOBAL_ARGS.output is not None:
        # check if output directory exists or not
        if not os.path.exists(GLOBAL_ARGS.output):
            os.mkdir(GLOBAL_ARGS.output)
        now = datetime.datetime.now()
        gpu_name = torch.cuda.get_device_properties(torch.device("cuda")).name
        def extract_gpu_info(name):
            if name in device_name_map.keys():
                return device_name_map[name]
            else:
                return ''
        formatted_time = now.strftime("%m%d%H%M%S")
        # mkdir
        log_dir = os.path.join(GLOBAL_ARGS.output, extract_gpu_info(gpu_name)+formatted_time)
        os.mkdir(log_dir)
        # write config file
        with open(GLOBAL_ARGS.config_file) as fp:
            config_list = json.load(fp)
        
        # save config json file
        with open(f'{log_dir}/config.json', "w") as fp:
            json.dump(config_list,fp=fp, indent=4, separators=(',', ': '))
        # save template bash script
        shutil.copy(GLOBAL_ARGS.template, f'{log_dir}/run.sh')
        # launch task
        print("launch task and current time: ", extract_gpu_info(gpu_name)+formatted_time)
        with open(f'{log_dir}/log', 'w') as fp:
            try: 
                result = subprocess.run(['bash', 'cof_workspace/launch-all.sh'], stdout=fp, stderr=subprocess.STDOUT, text=True)
                logging(f"process return code: {result.returncode}")
            except KeyboardInterrupt:
                logging(f"process killed by users")
        if os.path.exists('/tmp/target.nsys-rep'):
            shutil.copy('/tmp/target.nsys-rep', f'{log_dir}/target.nsys-rep')
        else:
            logging('/tmp/target.nsys-rep not exist!')
    else:
        subprocess.run(['bash','cof_workspace/launch-all.sh'])

def auto_gen():
    host_file_name="cof_workspace/hostfile"
    launch_file_name="cof_workspace/launch-all.sh"
    script_file_name=f'cof_workspace/target.sh'
    cluster_ip_list=list()

    def autogen_from_template(config_table, template_file, ipx):
        def compile(line:str, table):
            line = line.strip('\n')
            key_list = line.split('%')
            re_table = table
            for key in key_list:
                if key:
                    re_table=re_table[key]
            key_list
            return '_'.join(key_list)+f"={re_table}\n"
                
        with open(template_file, 'r') as file:
            lines = file.readlines()

        modified_lines = [compile(line, config_table) if line.startswith('%') else line for line in lines]
        modified_lines = [ '_'.join(line.strip('\n').split('&'))+f"={ipx}\n"if line.startswith('&') else line for line in modified_lines]
        return ''.join(modified_lines)

    with open(GLOBAL_ARGS.config_file) as f:
        config_list = json.load(f)
    config_table = {k:v for each in config_list for k,v in each.items()}
    cluster_ip_list = [each for each in config_table["CLUSTER_IPS"].split(" ") if each]
    
    ##########################################
    # generate launch-all.sh!
    ##########################################
    NNODES = config_table['NNODES']
    
    current_dir = os.getcwd()
    nsys_cmd = 'pkill nsys; nsys start --stop-on-exit=false -c cudaProfilerApi -f true -o /tmp/target ;nsys launch --trace=cuda,nvtx '
    launch_all_content = f'{nsys_cmd if GLOBAL_ARGS.nsys else ""}mpirun -np {NNODES} \\\n\
    --hostfile {current_dir}/cof_workspace/hostfile  \\\n\
    -bind-to none -map-by slot \\\n\
    --allow-run-as-root \\\n\
    -x LD_LIBRARY_PATH -x PATH \\\n\
    bash /tmp/target.sh \n\
second_return_code=$?\n\
if [ $second_return_code -ne 0 ]; then \n\
    exit 1 \n\
fi \n\
exit 0'
    if not os.path.exists("cof_workspace/"):
        os.mkdir("cof_workspace/")

    with open(launch_file_name,"w") as fp:
        fp.write(launch_all_content)
    for host_idx,host_ip in enumerate(cluster_ip_list[:NNODES]):
        script_content = autogen_from_template(config_table, GLOBAL_ARGS.template, host_idx)
        with open(script_file_name,'w') as f:
            f.write(script_content)
        dispatch_cmd=f'scp {script_file_name} {host_ip}:/tmp/'
        return_code=os.system(dispatch_cmd)
        return_code="successfully" if return_code==0 else "failed"
        print(f"{dispatch_cmd}------------{return_code}")
    if return_code!="successfully":
        print("failed to dispatch tasks")
        return -1
    else:
        print("successfully dispatch tasks")
        
    ##########################################
    # generate hostfile!
    ##########################################

    with open(host_file_name,"w") as fp:
        for each_ip in cluster_ip_list[:NNODES]:
            fp.write(each_ip + " slots=1\n")
    return 0

def process_file():
    assert auto_gen()==0
    start = time.time()
    auto_exec()
    print(f"{GLOBAL_ARGS.config_file} done execution time: {time.time()-start:.2f}s")
    logging(f"{GLOBAL_ARGS.config_file} done execution time: {time.time()-start:.2f}s")

def process_batched_files():
    global GLOBAL_ARGS
    assert os.path.exists(GLOBAL_ARGS.input), GLOBAL_ARGS.input+" not exist"
    config_file_list = []
    for _, _, files in os.walk(GLOBAL_ARGS.input):
        for file in files:
            config_file_list.append(os.path.join(GLOBAL_ARGS.input, file))
    config_file_list.sort()

    if GLOBAL_ARGS.list:
        print("="*25)
        print("     Print Log List")
        print("="*25)

        print(f"log num: {len(config_file_list)}")
        print("id         name")
        for id, dir in enumerate(config_file_list):
            print(f"{id}    {dir}")

        print("-"*25)
        logging("list input files done")
    else:
        
        candidate_config_file_list = [config_file_list[each] for each in parse_str_range(GLOBAL_ARGS.range)] if GLOBAL_ARGS.range is not None else config_file_list
        for id, config_file in enumerate(candidate_config_file_list):
            print(f"{id+1}/{len(candidate_config_file_list)} executing: {config_file}")
            logging(f"{id+1}/{len(candidate_config_file_list)} executing: {config_file}")
            GLOBAL_ARGS.config_file = config_file
            process_file()

def task_setup():
    global GLOBAL_ARGS
    logging(f"task setup ...")
    if GLOBAL_ARGS.input is not None:
        process_batched_files()
    else:
        def check_inner_list(config_file):
            json_gen_dir = 'cof-gen/'
            with open(config_file) as f:
                config_list = json.load(f)

            def find_lists_and_generate_combinations(config_list, setting_lists):
                # setting_lists = []
                setting_num = 1
                waited_to_visit = [each for each in config_list]
                for config in waited_to_visit:
                    for key, value in config.items():
                        if isinstance(value, dict):
                            waited_to_visit.append(value)
                        elif isinstance(value, list):
                            if value:
                                if not setting_lists:
                                    setting_lists = [[v] for v in value]
                                else:
                                    setting_lists = [s + [v] for s in setting_lists for v in value]
                                setting_num *= len(value)
                                config[key] = []
                            else:
                                config[key] = setting_lists.pop(0)

                return setting_lists, setting_num
            setting_lists = []
            setting_lists, setting_num = find_lists_and_generate_combinations(config_list, setting_lists)
            if setting_lists:
                if os.path.exists(json_gen_dir):
                    shutil.rmtree(json_gen_dir)
                os.mkdir(json_gen_dir)

                for idx in range(setting_num):
                    config_copy = copy.deepcopy(config_list)
                    _, _ = find_lists_and_generate_combinations(config_copy, setting_lists[idx])
                    with open(f'{json_gen_dir}/config-{str(idx).zfill(len(str(setting_num)))}'+".json", "w") as fp:
                        json.dump(config_copy, fp=fp, indent=4, separators=(',', ': '))
            return bool(setting_lists)

        if check_inner_list(GLOBAL_ARGS.file):
            GLOBAL_ARGS.input = 'cof-gen/'
            process_batched_files()
        else:
            process_file()

def main():
    global GLOBAL_ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-f', type=str, default="config-template.json", help="config file path, default is ./config-template.json")
    parser.add_argument('--input', '-i', type=str, default=None, help="run experiments in batch mode. all config files are placed in input directory")
    parser.add_argument('--template','-T', type=str, default=None, help='provide the path of template .sh file')
    parser.add_argument('--output','-o', type=str, default=None,
                       help='write execution output to specific path')
    parser.add_argument('--test','-t', action='store_true',
                        help='use cof run in test mode -> just generate bash script')
    parser.add_argument('--nsys','-n', action='store_true',
                        help='use nsys to profile your cuda programme')
    parser.add_argument('--list','-l', action='store_true',
                        help='list id of all input files, only available when input dir is provided')
    parser.add_argument('--range','-r', type=str, default=None,
                        help='support 3 formats: [int | int,int,int... | int-int], and int value must be > 0')
    GLOBAL_ARGS = parser.parse_args()
    
    logging("-"*10+"cofrun begin"+"-"*10)
    args_str = "\n"

    # find the longest var name
    max_arg_length = max(len(arg) for arg in vars(GLOBAL_ARGS))

    # alignment
    for arg in vars(GLOBAL_ARGS):
        args_str += f"{arg.ljust(max_arg_length)}: {getattr(GLOBAL_ARGS, arg)}\n"
    logging(args_str)


    task_setup()
    logging("="*10 + "All submitted cofrun tasks done" + "="*10)

if __name__ == "__main__":
    main()