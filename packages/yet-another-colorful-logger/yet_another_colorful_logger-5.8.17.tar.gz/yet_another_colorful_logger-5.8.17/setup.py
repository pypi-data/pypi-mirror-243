import json

import setuptools

version_value = [
    values.split("=")[1]
    for values in open(".version", "r").read().splitlines()
    if values != " "
]

setuptools.setup(
    name="yet_another_colorful_logger",
    version=f"{version_value[0]}.{version_value[1]}.{version_value[2]}",
    author="Wagner Cotta",
    description="Just another Colorful Logger with my personal customizations to be used in any python script.",
    package_dir={"": "src"},
    url="https://github.com/wagnercotta/yet_another_colorful_logger",
    packages=setuptools.find_packages(where="src"),
    install_requires=["colorlog"],
    license="GNU",
    data_files=[("", [".version"])],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
