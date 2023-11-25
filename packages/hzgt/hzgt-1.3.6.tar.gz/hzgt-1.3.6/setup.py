from setuptools import setup, find_packages

from hzgt import version

setup(
    name="hzgt",
    # 包的分发名称
    version=version,
    # 包的版本
    author="HZGT",
    # 包的作者
    author_email="2759444274@qq.com",
    # 包的作者的邮箱

    description="",
    # 用于介绍包的总结
    long_description="This library is used for personal testing",
    # 包的详细说明
    long_description_content_type="""
    This library is used for personal testing.
    
    Only WIN.
    """,
    # 索引类型长描述
    url="",
    # 项目主页的URL

    packages=find_packages(),
    data_files=['README.md', 'LICENSE',
                r'hzgt\download\book118\book118download.exe'],
    install_requires=[''],
    # 需要安装的依赖包
    python_requires='>=3.7',
    # python版本限制

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 元数据
)

