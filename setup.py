from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="youtube_api_project",
    version="0.1",
    author="cakir",
    packages=find_packages(),
    install_requires = requirements
)