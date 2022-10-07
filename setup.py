from setuptools import setup, find_packages


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2.28.1,<2.29"]

setup(
    name="pyonlyoffice",
    version="0.0.3",
    author="3v01ut10n",
    author_email="arxonix7@gmail.com",
    description="Package for working with OnlyOffice API.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/3v01ut10n/pyonlyoffice/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
