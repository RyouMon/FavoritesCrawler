from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = [line.rstrip() for line in f.readlines()]

setup(
    install_requires=requirements
)
