from setuptools import setup, find_packages
setup(
    name='jaguardb-socket-client',
    version='3.4.0',
    author = 'JaguarDB',
    description = 'Socket client for Jaguar vector database',
    url = 'http://www.jaguardb.com',
    license = 'Apache 2.0',
    python_requires = '>=3.0',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('jaguardb', ['jaguardb-socket-client/LICENSE', 'jaguardb-socket-client/README.md', 'jaguardb-socket-client/libJaguarClient.so', 'jaguardb-socket-client/jaguarpy.so', 'jaguardb-socket-client/JaguarSocketClient.py'])
    ],
)
