from setuptools import setup, find_packages

VERSION = "0.3.6"
DESCRIPTION = "python project_utils tools"
setup(
    name="project-utils-2023",
    version=VERSION,
    author="mylx2014",
    author_email="mylx2014@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['loguru', 'dbutils', 'pymysql'],
    keywords=['python', 'utils', 'project utils'],
    data_files=[],
    entry_points={},
    license="MIT",
    url="https://gitee.com/mylx2014/project-utils.git",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ]
)
