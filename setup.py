import setuptools



setuptools.setup(
    name="TensorLogic",
    version="0.0.1",
    author="Jesus Sesma",
    author_email="jesus.sesma@hotmail.com",
    description="A small tensorlogic package",
    url="https://github.com/BoxRight/TensorLogic",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
