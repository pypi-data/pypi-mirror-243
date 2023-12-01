from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="Topsis-Amit-102003053",
	version='1.0.0',
	author='Amit Kumar',
	author_email='amtsinh164@gmail.com',
	description='Topsis package for MCDM problems',
	long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires = ['pandas'],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	)