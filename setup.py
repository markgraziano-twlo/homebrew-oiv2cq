from setuptools import setup, find_packages

setup(
    name="oiv2cq",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "termcolor",
        "cookiecutter",
    ],
    entry_points={
        "console_scripts": [
            "oiv2cq=oiv2cq.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="CLI tool to automate prerequisites setup and plugin template creation for Twilio CloudQuery.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/markgraziano-twlo/oiv2cq",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
