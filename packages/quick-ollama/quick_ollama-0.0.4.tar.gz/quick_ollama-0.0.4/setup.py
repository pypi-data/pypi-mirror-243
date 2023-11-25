from setuptools import find_packages, setup


with open("VERSION", "r") as f:
    VERSION = f.read().strip()


DESCIPTION = "fast startup ollama server"


with open("requirements.txt", "r") as requirements_file:
    REQUIREMENTS = requirements_file.readlines()


setup(
    name="quick_ollama",
    version=VERSION,
    author="axdjuraev",
    author_email="<axdjuraev@gmail.com>",
    description=DESCIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)

