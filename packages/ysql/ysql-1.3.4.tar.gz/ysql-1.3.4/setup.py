import setuptools

with open("README_pypi.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ysql",
    version="1.3.4",
    author="dfqxhhh",
    author_email="dfqxhhh@163.com",
    description="a more efficient and concise SQLite framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/darlingxyz/ysql",
    packages=['ysql'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)



