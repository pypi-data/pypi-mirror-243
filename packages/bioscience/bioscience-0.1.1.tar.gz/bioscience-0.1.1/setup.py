from setuptools import setup, Extension, Command, find_packages
import os
import sys
import shutil
import platform
import importlib
from os import path
from os.path import join
import bioscience._dependencies as dependencies

this_directory = path.abspath(path.dirname(__file__))

DISTNAME = "bioscience"
VERSION = "0.1.1"
AUTHOR = "Aurelio Lopez-Fernandez"
AUTHOR_EMAIL = "alopfer1@upo.es"
DESCRIPTION="bioScience: A new Python science library for High-Performance Computing Bioinformatics Analytics"
LONG_DESCRIPTION_CONTENT_TYPE="text/x-rst"
URL = "https://github.com/aureliolfdez/bioscience"
DOWNLOAD_URL = "https://pypi.org/project/bioscience/#files"
LICENSE = "BSD License"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/aureliolfdez/bioscience/issues",
    "Documentation": "https://bioscience.readthedocs.io/en/latest/",
    "Source Code": "https://github.com/aureliolfdez/bioscience",
}


class CleanCommand(Command):
    description = "Remove build artifacts from the source tree"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        if os.path.exists("build"):
            shutil.rmtree("build")
        
        if os.path.exists("dist"):
            shutil.rmtree("dist")
            
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")
        
        if os.path.exists("bioscience.egg-info"):
            shutil.rmtree("bioscience.egg-info")
            
        for dirpath, dirnames, filenames in os.walk("bioscience"): 
            for dirname in dirnames:
                if dirname == "__pycache__":
                    shutil.rmtree(os.path.join(dirpath, dirname))

# read the contents of README.rst
def readme():
    with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
        return f.read()

cmdclass = {
    "clean": CleanCommand,
}
# Setting up
def setup_package():
    python_requires = ">=3.10"
    required_python_version = (3, 10)
    metadata = dict(
        name=DISTNAME,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        description=DESCRIPTION,    
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        long_description=readme(),
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
        ], 
        cmdclass=cmdclass, 
        python_requires=python_requires,
        packages=find_packages(),
        install_requires=dependencies.tag_to_packages["install"],
        keywords=['python', 'data-science', 'data-mining', 'bioinformatics','high-performance-computing','data-analysis'],        
    ) 
    
    commands = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if not all(
        command in ("egg_info", "dist_info", "clean", "check") for command in commands
    ):
        if sys.version_info < required_python_version:
            required_version = "%d.%d" % required_python_version
            raise RuntimeError(
                "bioScience requires Python %s or later. The current Python version is %s installed in %s." % (required_version, platform.python_version(), sys.executable)
            )

    setup(**metadata)

       
if __name__ == "__main__":
    setup_package()