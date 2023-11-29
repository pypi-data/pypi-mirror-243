import subprocess
import os

try:
  from setuptools import setup, find_packages
except ImportError:
  subprocess.call(["pip", "install", "setuptools"])
  from setuptools import setup, find_packages

try:
  with open((os.path.dirname(__file__)+"/README.md"), 'r') as f:
      pypi_text = f.read()
except:
  pypi_text = ""

setup(
    name='tir-cli',
    version='0.1.1',
    description="This a E2E CLI tool for TIR AI-ML",
    author="Aman",
    packages=find_packages(),
    install_requires=['prettytable', 'e2enetworks', 'requests', 'setuptools', 'chardet'],

    long_description_content_type="text/markdown",
    long_description=pypi_text,

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'tir=e2e_gpu.main:run_main_class'
        ]
    },
)
