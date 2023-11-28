from setuptools import setup, find_packages

setup(
    name='dbt-purview',
    version='0.52',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'apache-airflow',
    ],
    entry_points={
        'console_scripts': [
            'dbtpurview = dbtpurview.main:dbtpurview',
        ],
    },
)