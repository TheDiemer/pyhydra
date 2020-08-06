import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhydra",
    version="0.2.0",
    author="Eric Rich",
    author_email="erich@redhat.com",
    description="Python API for interacting with Hydra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheDiemer/pyhydra",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3"
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
