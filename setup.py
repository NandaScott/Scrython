from setuptools import setup

setup(
    name="scrython",
    packages=["scrython", "scrython.cards", "scrython.sets", "scrython.bulk_data"],
    version="2.0.0",
    description="A wrapper for using the Scryfall API.",
    long_description="https://github.com/NandaScott/Scrython/blob/master/README.md",
    url="https://github.com/NandaScott/Scrython",
    download_url="https://github.com/NandaScott/Scrython/archive/0.1.0.tar.gz",
    author="Nanda Scott",
    author_email="nanda1123@gmail.com",
    license="MIT",
    keywords=["Scryfall", "magic", "the gathering", "scrython", "wrapper"],
    python_requires=">=3.10",
    install_requires=[
        # No runtime dependencies - uses Python standard library only
    ],
    extras_require={
        "dev": [
            "black>=24.0.0",
            "ruff>=0.1.0",
            "mypy>=1.8.0",
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pre-commit>=3.6.0",
        ],
    },
)
