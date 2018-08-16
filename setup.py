import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demo_meta_miner",
    version="0.0.9",
    author="Divyanshu",
    author_email="divyanshuchauhan0208@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divyanshuchauhan/database-metadata-miner",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'miner = demo_meta_miner.miner:demo',
            'execute_saved_req = demo_meta_miner.execute_saved_req:execute_migration',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click",
        "SQLAlchemy"
    ]
)
