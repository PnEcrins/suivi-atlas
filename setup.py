import setuptools
from pathlib import Path


root_dir = Path(__file__).absolute().parent
with (root_dir / "VERSION").open() as f:
    version = f.read().strip()
with (root_dir / "README.md").open() as f:
    long_description = f.read()


setuptools.setup(
    name="app",
    description="TODO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Théo Lechémia",
    url="https://github.com/PnX-SI/GeoNature/",
    python_requires=">=3.9",
    version=version,
    packages=setuptools.find_packages("./"),
    package_dir={"": "."},
    install_requires=[
        "flask",
        "sqlalchemy",
        "flask-sqlalchemy",
        "toml",
        "psycopg2",
        "flask-admin",
        "babel",
        "Flask-Babel"
    ],
    extras_require={
        "tests": [
            "pytest",
            "pytest-flask",
            "pytest-cov",
            "jsonschema",
        ],
    },
    classifiers=[
        "Framework :: Flask",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
