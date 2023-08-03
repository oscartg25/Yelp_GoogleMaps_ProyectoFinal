from setuptools import setup, find_packages

setup(
    name='my_dataflow_pipeline',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'apache-beam',
        'google-cloud-storage',
    ],
)
