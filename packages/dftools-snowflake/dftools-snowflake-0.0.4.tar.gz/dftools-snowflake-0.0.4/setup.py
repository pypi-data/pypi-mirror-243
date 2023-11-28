import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='dftools-snowflake',
    packages=setuptools.find_namespace_packages(include=['dftools_snowflake', 'dftools_snowflake.database']),
    version='0.0.4',
    description='DF-Tools Snowflake',
    author='Data Flooder',
    author_email="lirav.duvshani@dataflooder.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache',
    install_requires=[
        'snowflake-connector-python'
        , 'dftools-core>=0.0.12'
    ],
    python_requires=">=3.7.9",
)