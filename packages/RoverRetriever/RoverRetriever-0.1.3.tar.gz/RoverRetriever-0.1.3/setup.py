from setuptools import setup
from os import path

currrent_direct = path.abspath(path.dirname(__file__))
with open(path.join(currrent_direct, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RoverRetriever',
    version='0.1.3',
    url='https://github.com/tyler-tee/RoverRetriever',
    author='Tyler Talaga',
    author_email='ttalaga@wgu.edu',
    packages=['RoverRetriever'],
    install_requires=['requests >= 2.25.1'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description='RoverRetriever is a lightweight Python wrapper written to facilitate interaction with the Dog CEO API.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
