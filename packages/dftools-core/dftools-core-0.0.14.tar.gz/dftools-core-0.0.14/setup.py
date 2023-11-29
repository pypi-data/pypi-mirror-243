import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='dftools-core',
    packages=setuptools.find_namespace_packages(include=['dftools']),
    version='0.0.14',
    description='Data Flooder Tools - Core Package',
    author='Lirav DUVSHANI',
    author_email="lirav.duvshani@dataflooder.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache',
    install_requires=[
        'StrEnum>=0.4.10'
        , 'regex>=2023.8.8'
        , 'pandas>=1.5.3'
        , 'jinja2>=3.1.2'
        , 'ordered_set>=4.1.0'
    ],
    python_requires=">=3.7.9",
)