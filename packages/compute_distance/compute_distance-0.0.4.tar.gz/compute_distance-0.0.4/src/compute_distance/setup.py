from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('src/compute_distance/requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='compute_distance',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=required_packages,
    entry_points={
        'console_scripts': [
            'compute_distance = compute_distance.cli:main',
        ],
    },
)
