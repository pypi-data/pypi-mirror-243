from setuptools import setup, find_packages

setup(
    name='shieldb',
    version='0.4.7',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy~=2.0.23',
        'psycopg2-binary~=2.9.1',
        'nltk~=3.8.1',
        'inquirerpy~=0.3.4',
        'setuptools~=60.2.0'
    ],
    data_files=[('', ['src/app.py', 'README.md', 'requirements.txt'])],
    entry_points={
        'console_scripts': [
            'shieldb=src.app:main',
        ],
    },
)
