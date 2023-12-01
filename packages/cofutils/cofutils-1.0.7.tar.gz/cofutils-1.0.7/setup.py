from setuptools import setup
import setuptools
from cofutils.package_info import (
    __description__,
    __contact_names__,
    __url__,
    __keywords__,
    __license__,
    __package_name__,
    __version__,
)

from distutils.cmd import Command
import os
import shutil
class CleanCommand(Command):
    description = "Clean up build and temporary files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        here = os.path.abspath(os.path.dirname(__file__))
        build_dir = os.path.join(here, 'build')
        dist_dir = os.path.join(here, 'dist')
        egg_info_dir = os.path.join(here, 'cofutils.egg-info')

        print("Cleaning up...")
        for d in [build_dir, dist_dir, egg_info_dir]:
            if os.path.exists(d):
                print(f"Removing {d}")
                shutil.rmtree(d)


with open("README.md", "r") as fh:
    long_description = fh.read()
def req_file(filename):
    with open(filename) as f:
        content = f.readlines()
    return [x.strip() for x in content]
install_requires = req_file("requirements.txt")
entry_points = {
    'console_scripts': [
        'cofrun = cofutils.dispatch:main',
    ]
}

setup(
        name=__package_name__,
        version=__version__,
        description=__description__,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=__url__,
        author=__contact_names__,
        maintainer=__contact_names__,
        license=__license__,
        python_requires='>=3.6',
        packages=setuptools.find_packages(),
        entry_points=entry_points,
        install_requires=install_requires,
        cmdclass={
            'clean': CleanCommand,
        },
        package_data={'cofutils':['*.pyi']})