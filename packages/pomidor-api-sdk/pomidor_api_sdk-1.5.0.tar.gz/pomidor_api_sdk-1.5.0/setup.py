#  https://github.com/SuSLiK-bozhe/pomidor_api_sdk/blob/main/README.md
from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()

setup(name='pomidor_api_sdk',
version='1.5.0',
author='SuSLiK',
description='SDK for easy contact with https://api.pomidorproject',
long_description=readme(),
long_description_content_type='text/markdown',
url='https://t.me/pomidorik_sus',
packages=find_packages(),
install_requires=['requests>=2.25.1'],
classifiers=['Programming Language :: Python :: 3.11','License :: OSI Approved :: MIT License','Operating System :: OS Independent'],
python_requires='>=3.7')