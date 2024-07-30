import os
import re
import sys

from setuptools import setup, find_packages


def get_requirements_to_install():
    __curr_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    requirements_txt_file_as_str = f"{__curr_location__}/requirements.txt"
    with open(requirements_txt_file_as_str, 'r') as req_file:
        libs = req_file.readlines()
        for i in range(len(libs)):
            libs[i] = libs[i].replace('\n', '')
    return libs


def get_description() -> str:
    __curr_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    rst_txt_file_as_str = f'{__curr_location__}/README.rst'
    with open(rst_txt_file_as_str, 'r') as rst_file:
        desc = rst_file.read()
    return desc


def get_version():
    version_pattern = re.compile(r'^\d+\.\d+\.\d+$')
    version = '0.1.0'  # default version
    if '--version' in sys.argv:
        version_index = sys.argv.index('--version') + 1
        if version_index < len(sys.argv):
            version = sys.argv[version_index]
            if not version_pattern.match(version):
                raise ValueError("Version must be in the format X.Y.Z (e.g., 0.0.1)")
            sys.argv.pop(version_index)  # Remove version value
            sys.argv.pop(version_index - 1)  # Remove --version flag
        else:
            raise ValueError("--version flag requires a version argument")
    return version


setup(
    name='loguru-cli',
    version=get_version(),
    description='An interactive commandline interface that brings intelligence to your logs.',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    install_requires=get_requirements_to_install(),
    author='Amith Koujalgi',
    author_email='koujalgi.amith@gmail.com',
    project_urls={
        'Repository': 'https://github.com/Loguru-AI/Loguru-CLI'
    },
    packages=find_packages(
        include=[
            'loguru',
            'loguru.*',
        ]),
    py_modules=[
        'loguru',
    ],
    entry_points={
        'console_scripts': [
            'loguru = loguru.cli:main'
        ],
    },
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Environment :: Console'
    ],
)
