
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="greet-name-test2",
    version="1.0.2",
    packages=find_packages(),
    py_modules=['greet_name'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'greet_name = greet_name:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
