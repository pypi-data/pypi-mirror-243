from setuptools import setup, find_packages

setup(
    name='tnsa-gplbt',  # Replace with your desired package name
    version='1.3.2',  # Replace with your desired version
    packages=find_packages(),
    install_requires=[
        # Your dependencies go here
    ],
    entry_points={
        'console_scripts': [
            'your_command_name = your_package.module:main',
        ],
    },
)
