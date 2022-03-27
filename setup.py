from setuptools import find_namespace_packages, setup

VERSION_FILE = "src/app/version.py"


def get_version():
    locals_vars = {}
    with open(VERSION_FILE) as inf:
        exec(inf.read(), {}, locals_vars)
    return locals_vars["__version__"]


setup(
    name="flask-open-api-example",
    version=get_version(),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    package_data={
        "app": ["py.typed"],
    },
    install_requires=[
        "Flask",
        "flask-smorest",
        "gunicorn",
        "marshmallow_dataclass",
        "structlog",
        "werkzeug",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "mypy",
            "pylint",
            "python-dotenv",
            "pytest",
            "rich",
        ]
    },
)
