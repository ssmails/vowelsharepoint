import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vowelsharepoint", #same repo-name and package-folder-name
    version="0.0.1",
    author="Sushama Shroff",
    author_email="sushroff@cisco.com",
    description="Library to interface with Sharepoint APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'wheel',
        'certifi==2023.11.17',
        'cffi==1.16.0',
        'charset-normalizer==3.3.2',
        'cryptography==41.0.7',
        'idna==3.6',
        'msal==1.24.1',
        'pycparser==2.21',
        'PyJWT==2.8.0',
        'pyspnego==0.10.2',
        'pytz==2021.1',
        'requests==2.31.0',
        'requests-ntlm==1.2.0',
        'typing_extensions==4.9.0',
        'Office365-REST-Python-Client==2.5.5',
        'urllib3==2.1.0',
        'python-dotenv~=1.0.0',
    ],
)
