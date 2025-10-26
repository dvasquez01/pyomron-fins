from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyomron-fins",
    version="1.0.0",
    author="PyOmron FINS Contributors",
    author_email="",
    description="Python wrapper for OMRON FINS protocol communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dvasquez01/pyomron-fins",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies - uses only standard library
    ],
    keywords="omron plc fins ethernet automation industrial",
    project_urls={
        "Bug Reports": "https://github.com/dvasquez01/pyomron-fins/issues",
        "Source": "https://github.com/dvasquez01/pyomron-fins",
        "Documentation": "https://github.com/dvasquez01/pyomron-fins/blob/main/README.md",
    },
)