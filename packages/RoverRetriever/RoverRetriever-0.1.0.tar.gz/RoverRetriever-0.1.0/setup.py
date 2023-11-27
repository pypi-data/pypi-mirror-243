from setuptools import setup

setup(
    name='RoverRetriever',
    version='0.1.0',
    url='https://github.com/yourusername/RoverRetriever',
    author='Tyler Talaga',
    author_email='ttalaga@wgu.edu',
    description='A lightweight Python wrapper for the Dog CEO API',
    packages=['RoverRetriever'],
    install_requires=['requests >= 2.25.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
