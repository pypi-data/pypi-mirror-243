from setuptools import setup, find_packages
setup(
    name='jaguardb-http-client',
    version='3.4.0.1',
    author = 'JaguarDB',
    description = 'Http client for Jaguar vector database',
    url = 'http://www.jaguardb.com',
    license = 'Apache 2.0',
    python_requires = '>=3.0',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('jaguardb', ['jaguardb-http-client/LICENSE', 'jaguardb-http-client/README-http.md', 'jaguardb-http-client/JaguarHttpClient.py'])
    ],
)
