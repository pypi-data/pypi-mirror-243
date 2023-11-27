import setuptools

from hina.sdk import SDK_VERSION

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="HinaCloudSDK",
    version=SDK_VERSION,
    author="hina",
    author_email="admin@hinadt.com",
    description="This is the official Python SDK for Hina Analytics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hinadt/hina-cloud-python-sdk.git",
    packages=setuptools.find_packages(),
)
