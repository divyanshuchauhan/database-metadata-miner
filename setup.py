import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demo_meta_miner",
    version="0.0.19",
    author="Divyanshu",
    author_email="divyanshuchauhan0208@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divyanshuchauhan/database-metadata-miner",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'AristotleDbTools = demo_meta_miner.AristotleDbTools:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click~=6.0",
        "sqlalchemy~=1.2.0",
        "requests~=2.19.0",
        "psycopg2~=2.7.0",
        "mysqlclient~=1.3.0"
        
    ]
)
