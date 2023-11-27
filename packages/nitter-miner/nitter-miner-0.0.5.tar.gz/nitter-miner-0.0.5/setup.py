from setuptools import setup, find_packages

with open("long_desc.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nitter-miner",
    version="0.0.5",
    author="hashirkz",
    author_email="hashir.khan@mail.mcgill.ca",
    description="cli utility for data mining https://nitter.net/serach",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hashirkz/nitter_scraper",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'nitter = __nitter__.nitter:app',
        ],
    },
    install_requires=[
        'numpy==1.24.3',
        'pandas==2.0.2',
        'bs4==0.0.1',
        'requests==2.28.1',
        'tabulate==0.9.0',
        'langdetect==1.0.9',
        'emoji==1.7.0',
        'text2emotion==0.0.5',
        'nltk==3.8.1',
        'transformers==4.30.2',
        'xformers==0.0.20',
        'torch==2.0.1',
        'pip-system-certs==4.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
    ],
)
