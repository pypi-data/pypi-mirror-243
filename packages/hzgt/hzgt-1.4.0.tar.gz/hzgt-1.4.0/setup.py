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
    long_description="This library is used for personal",
    # 包的详细说明
    long_description_content_type="""
    This library is used for personal.
    And if anyone wants to use it, they can also use it.
    
    WIN and Linux.
    """,
    # 索引类型长描述
    url="",
    # 项目主页的URL

    packages=find_packages(),
    data_files=['README.md', 'VersionReadme.md', 'LICENSE', ],
    # 指定打包的文件
    install_requires=['tqdm', 'requests', 'you-get'],
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

