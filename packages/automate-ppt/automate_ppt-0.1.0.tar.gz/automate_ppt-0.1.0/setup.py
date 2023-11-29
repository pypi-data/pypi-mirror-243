from setuptools import setup, find_packages


setup(
    name="automate_ppt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的库所需的其他Python包
        "python-docx==1.1.0",
        "python-pptx==0.6.23"
    ],

    author="Sun Meng",
    author_email="clivesun@163.com",
    description="Offic自动化工具-自用，在原有包的基础上二次开发",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="",
    url="",
    classifiers=[
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # 开发的目标用户
        "Intended Audience :: Developers",
        # 属于什么类型
        "Topic :: Software Development :: Build Tools",
        # 许可证信息
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)