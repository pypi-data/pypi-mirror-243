from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    install_requires=required_packages,
    entry_points={
        'console_scripts': [
            'my_package_cli = my_package.cli:main',
        ],
    },
)
