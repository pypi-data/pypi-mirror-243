from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='storage-tool',
    version='0.1.0',
    description='Package for manager files in differents storages',
    author='Claudio Vinicius Oliveira',
    author_email='claudio.datascience@gmail.com',
    packages=find_packages(),
    install_requires=[
        'boto3==1.29.6',
        'botocore==1.32.6',
        'jmespath==1.0.1',
        'numpy>=1.19.5,<1.26.2',
        'pandas>=1.1.5,<2.1.3',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'tzdata==2023.3',
        's3transfer==0.7.0',
        'pyarrow==14.0.1',
        'urllib3==1.26.18',

    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)