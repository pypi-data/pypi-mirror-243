from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='openconnectome',
    version='0.0.11',
    description='Brain Graph Management and Numerical Model Simulations on Brains',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Stefano Bianchi',
    author_email='stefanobianchi314@gmail.com',
    url='https://github.com/Stefano314/OpenConnectome',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23',
        'matplotlib>=3.5.2',
        'pandas>=1.4.2',
        'networkx>=2.8.5',
        'scipy>=1.8.1',
        'tqdm>=4.64.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    license='CC BY-NC 4.0'
)