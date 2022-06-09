from setuptools import setup

with open("README.rst") as README:
    long_description = README.read()
    long_description = long_description[long_description.index("Description") :]

setup(
    name="wos",
    version="0.2.7",
    description="Web of Science client using API v3.",
    long_description=long_description,
    install_requires=[
        "limit",
        'suds;python_version<"3.0"',
        'suds-py3;python_version>="3.0"',
    ],
    url="http://github.com/enricobacis/wos",
    author="Enrico Bacis",
    author_email="enrico.bacis@gmail.com",
    license="MIT",
    packages=["wos"],
    scripts=["scripts/wos"],
    keywords="wos isi web of science knowledge api client",
)
