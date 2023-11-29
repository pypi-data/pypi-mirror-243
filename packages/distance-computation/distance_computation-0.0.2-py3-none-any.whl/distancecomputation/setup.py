from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('src/distance_computation/requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='distance-computation',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=required_packages,
    entry_points={
        'console_scripts': [
            'compute_distance = distance_computation.cli:main',
        ],
    },
)
