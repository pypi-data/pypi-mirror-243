from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

exec(open('multislsqp/_version.py').read()) # get version number

setup(
    name='multislsqp',
    version=__version__,
    author='Rhydian Lewis',
    author_email='rhydian.lewis@swansea.ac.uk',
    description='MultiSLSQP is an extension of the SLSQP algorithm used in scipy.optimize.minimize which supports multiple initial starting points.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/RhydianL/multislsqp',    
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['scipy>=1.4']
)