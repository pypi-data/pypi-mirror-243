from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pydivar',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Ali Ardakani',
    author_email='aliardakani78@gmail.com',
    description='Python library for crawling and extracting data from Divar',
    url='https://github.com/ali-ardakani/pydivar.git',
    license='MIT',
)
