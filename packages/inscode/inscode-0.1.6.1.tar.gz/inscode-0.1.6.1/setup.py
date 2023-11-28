from setuptools import setup

VERSION = '0.1.6.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('requirements.txt') as f:
#     requirements = [l for l in f.read().splitlines() if l]
requirements = open('requirements.txt').readlines()

setup(
    name='inscode',  # package name
    version=VERSION,  # package version
    description='Inscode SDK',  # package description
    long_description=long_description,  # 长简介 这里使用的 readme 内容
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=['inscode'],
    # package_dir={"": "inscodek"},
    zip_safe=False,
    python_requires='>=3'
)
