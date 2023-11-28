from setuptools import find_packages, setup

setup(
    name="dev_yet_another_colorful_logger",
    version="0.0.10",
    author="Wagner Cotta",
    description="Just another Colorful Logger with my personal customizations to be used in any python script.",
    url="https://github.com/wagnercotta/dev_yet_another_colorful_logger",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["colorlog"],
    license="GNU",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
