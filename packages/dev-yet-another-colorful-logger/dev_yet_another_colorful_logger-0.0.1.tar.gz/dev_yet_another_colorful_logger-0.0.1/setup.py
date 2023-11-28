from setuptools import find_packages, setup

version_value = [
    values.split("=")[1]
    for values in open(".version", "r").read().splitlines()
    if values != " "
]

setup(
    name="dev_yet_another_colorful_logger",
    version=f"{version_value[0]}.{version_value[1]}.{version_value[2]}",
    author="Wagner Cotta",
    description="Just another Colorful Logger with my personal customizations to be used in any python script.",
    url="https://github.com/wagnercotta/dev_yet_another_colorful_logger",
    packages=find_packages(),
    install_requires=["colorlog"],
    license="GNU",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
