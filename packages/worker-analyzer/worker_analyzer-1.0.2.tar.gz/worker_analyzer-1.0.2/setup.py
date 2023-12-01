from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='worker_analyzer',
    version='1.0.2',
    description='Package for analyze and monitoring worker performance',
    author='Claudio Vinicius Oliveira',
    author_email='claudio.datascience@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.5,<1.26.2',
        'pandas>=1.1.5,<2.1.3',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'tzdata==2023.3'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)