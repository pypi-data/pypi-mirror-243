

from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name="pixel_perfect",
    version="3.1.0",
    description='A versatile Python package leveraging machine learning model for efficient image comparisons.',
    author='Etenrnal Tech Systems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
     install_requires=[
        "numpy",
        "tensorflow",
        "opencv-python",
        "selenium",
    ],
)
