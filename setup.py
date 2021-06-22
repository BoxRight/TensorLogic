import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TensorLogic",
    version="0.0.1",
    author="Jesus Sesma",
    author_email="jesus.sesma@hotmail.com",
    description="A small tensorlogic package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BoxRight/TensorLogic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
