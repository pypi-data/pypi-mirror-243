from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="simple-justwatch-python-api",
    packages=["simplejustwatchpythonapi"],
    package_dir={"simplejustwatchpythonapi": "src/simplejustwatchpythonapi"},
    version="0.1",
    license="GPLv3",
    description="A simple JustWatch Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Electronic Mango",
    author_email="78230210+Electronic-Mango@users.noreply.github.com",
    url="https://github.com/Electronic-Mango/simple-justwatch-python-api",
    download_url="https://github.com/Electronic-Mango/simple-justwatch-python-api/releases/",
    keywords=["justwatch", "api", "graphql"],
    install_requires=["httpx"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
