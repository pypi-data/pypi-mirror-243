import setuptools

with open("VERSION") as freader:
    VERSION = freader.readline().strip()

with open("README.md") as freader:
    README = freader.read()

install_requirements = [
    "midas-util>=1.1.1",
    "mosaik_api",
    "matplotlib",
    "numpy",
    "pandas",
    "tables",
    "wget",
]

development_requirements = [
    "flake8==6.1.0",
    "pytest",
    "coverage",
    "black==23.11.0",
    "setuptools",
    "twine",
    "wheel",
    "mosaik",
]

extras = {"dev": development_requirements}

setuptools.setup(
    name="midas-weather",
    version=VERSION,
    description="A MIDAS module for weather datasets.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Stephan Balduin",
    author_email="stephan.balduin@offis.de",
    url="https://gitlab.com/midas-mosaik/midas-weather",
    packages=["midas.modules.weather", "midas.modules.weather.model"],
    # include_package_data=True,
    install_requires=install_requirements,
    extras_require=extras,
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)
