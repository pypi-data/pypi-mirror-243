
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="greeting-test1",
    version="1.0",
    packages=find_packages(),
    py_modules=['greeting_test1'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'greeting_test1 = greeting_test1:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
