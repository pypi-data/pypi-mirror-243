import setuptools
from setuptools import find_packages

with open("requirements.txt", "rt") as f:
    install_requires = [line.strip() for line in f.readlines()]

setuptools.setup(
    name="moval",
    version="0.0.3",
    author="Zeju Li",
    author_email="lizeju8@gmail.com",
    description="Model evalutation without manual label",
    install_requires=install_requires,
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
)
