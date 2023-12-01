
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="add-test-20231130",
    version="1.0.0",
    packages=find_packages(),
    py_modules=['add_test_20231130'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'add_test_20231130 = add_test_20231130:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
