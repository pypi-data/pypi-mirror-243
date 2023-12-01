from setuptools import setup, find_packages
import pathlib

setup(
    name='scuttlebuddy',
    version='0.0.1',
    requires=[],
    description="External Scripting Framework for developers who play League of Legends.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://discord.gg/huywRMDEmE",
    author="Business",
    author_email="",
    license="The Unlicense",
    project_urls={
        "Discord": "https://discord.gg/huywRMDEmE"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires=">=3.10,<3.12",
    install_requires=[
        "requests",
        "numpy",
        "pywin32"
    ],
    extras_require={},
    packages=find_packages(),
    include_package_data=True
)