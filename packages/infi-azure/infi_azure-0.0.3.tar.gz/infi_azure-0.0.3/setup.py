from setuptools import find_packages, setup

setup(
    name='infi_azure',
    packages=find_packages(),
    version='0.0.3',
    description='Azure python package for infinity team',
    author='Infinity Team',
    install_requires=['azure.storage.blob==12.19.*', 'pytest==7.4.*'],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
