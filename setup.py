from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='imagedeskew',
    version='1.0',
    author='Benoit Cayla',
    author_email='benoit@datacorner.fr',
    url='https://github.com/datacorner/blueprism-deskew-skill',
    license='LICENSE.txt',
    description='A Web service which deskew images.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )