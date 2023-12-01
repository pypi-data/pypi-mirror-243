import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "readme.md").read_text()

# This call to setup() does all the work
setup(
    name="mmobs_logger",
    version="0.2",
    description="Python software to generate a user interface for marine mammal observation logging and GPS tracking for visual surveys of marine mammal abundance.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://zenodo.org/doi/10.5281/zenodo.10228669",
    author="Sebastian Menze",
    author_email="sebastian.menze@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["PyQt5","pynmea2","pyserial","pandas"])
    # entry_points={
    #     "console_scripts": [
    #         "pase=pase.__main__:main",
        # ]
    # },
# )
