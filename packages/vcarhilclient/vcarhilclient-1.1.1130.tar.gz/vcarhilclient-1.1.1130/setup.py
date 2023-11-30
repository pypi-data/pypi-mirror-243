# -*- coding: utf-8 -*-
import json
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("version.json","r", encoding="utf-8") as vf:
    v = json.load(vf)
    version = v["version"]

setuptools.setup(
    name="vcarhilclient",  # 包名
    version=version,
    author="vcarsystem",
    author_email="service@vcarsystem.com",
    description="vcarhilclient",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires = ["bitstring"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
# Python setup.py sdist bdist_wheel
# python -m twine upload -u luyulei -p kunyitest --repository pypi dist/*
# Python -m twine upload --repository pypi dist/*


