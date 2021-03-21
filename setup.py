import setuptools

setuptools.setup(
    name="covid19",
    version="0.0.1",
    author="mantovanig",
    description="Covid-19 stats - Italy",
    scripts=["src/covid19.py"],
    install_requires=["pyfiglet", "termcolor", "requests", "tabulate"],
)