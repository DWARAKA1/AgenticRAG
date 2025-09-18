from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AgenticRAG",
    version="0.1",
    author="Dwarakanadha Reddy",
    packages=find_packages(),
    install_requires = requirements,
)