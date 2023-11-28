# coding:utf-8

from setuptools import setup, find_packages
from volcengine import VERSION

setup(
    name="vop-sdk",
    version=VERSION,
    keywords=["pip", "vop", "vop-sdk-python"],
    description="The Vop SDK for Python",
    license="MIT Licence",

    url="https://github.com/Volcengine/volc-sdk-python",
    author="Vop SDK",
    author_email="liangqing.leon@bytedance.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "retry", "pytz", "pycryptodome", "protobuf", "google", "six", "lz4a"]
)
