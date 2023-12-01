"""Setup PIP package"""


from codecs import open as codecs_open
from pathlib import Path
from setuptools import setup, find_packages


BASE_PATH = Path(__file__).parent


with codecs_open((BASE_PATH / "README.md"), encoding="utf-8") as readme_file:
    readme_content = "\n" + readme_file.read()


VERSION = "0.0.1"
DESCRIPTION = "A tool to create a command-line interface for your app using python"
LONG_DESCRIPTION = readme_content


# Setting up
setup(
    name="betterargs",
    version=VERSION,
    author="Daniel Muringe",
    author_email="<danielmuringe@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme_content,
    packages=find_packages(),
    install_requires=[
        "pyyaml",
    ],
    keywords=[
        "python arguments",
        "create arguments easily",
        "easy arguments",
        "yaml arguments",
        "create arguments",
        "better arguments",
        "argument parser",
        "boilerplate",
        "yaml",
        "command-line",
        "command-line-tool",
        "argparse",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
)
