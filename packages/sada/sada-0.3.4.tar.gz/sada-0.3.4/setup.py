from setuptools import find_packages, setup

setup(
    name="sada",
    version="0.3.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.0",
    ],
    author="Sarmad Gulzar",
    author_email="xarmad@hotmail.com",
    description="A Django package to handle SadaBiz payment links.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ixarmad/sada",
    license="MIT",
)
