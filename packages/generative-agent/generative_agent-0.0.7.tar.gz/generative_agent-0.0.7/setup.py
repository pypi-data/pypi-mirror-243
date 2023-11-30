import setuptools
from pkg_resources import parse_requirements

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generative_agent",
    version="0.0.7",
    author="Donnaphat Trakulwaranont",
    author_email="donnaphat_tr@dtgo.com",
    description="A package for generative agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MQDC-Tech/bel-generative-agents",
    packages=setuptools.find_packages(),
    package_data={
        "generative_agent": [
            "prompt/*",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.8",
)
