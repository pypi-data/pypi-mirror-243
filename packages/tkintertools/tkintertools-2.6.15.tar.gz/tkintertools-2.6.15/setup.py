"""
上传 PyPI
---------
1. __init__.py 的版本号
2. setup.py 的版本号
3. CHANGELOG.md 日志文件
4. README.md 自述文件
5. Python3.8.* 兼容性测试【稳定版】
6. Ubuntu22.04 跨平台测试【稳定版】
7. 确认上传的文件有哪些并上传
8. 删除多余文件
"""

import setuptools

setuptools.setup(
    name="tkintertools",
    version="2.6.15",
    description="The tkintertools module is an auxiliary module of the tkinter module.",
    long_description=open("README.md", encoding="utf-8").read(),
    author="Xiaokang2022",
    author_email="2951256653@qq.com",
    maintainer="Xiaokang2022",
    maintainer_email="2951256653@qq.com",
    url="https://github.com/Xiaokang2022/tkintertools",
    packages=setuptools.find_packages(),
    license="MulanPSL-2.0",
    keywords=["tkinter", "tkintertools", "GUI"],
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)",
        "Operating System :: OS Independent",
    ],
)

# python -m pip install --user --upgrade setuptools wheel [检查更新]

# python setup.py sdist bdist_wheel [打包]
# python -m twine upload dist/* [上传]

# pip install -U pypistats [数据分析]

# pypistats overall tkintertools [数据分析]
# pypistats recent tkintertools
# pypistats system tkintertools
# pypistats python_minor tkintertools
# pypistats python_major tkintertools
