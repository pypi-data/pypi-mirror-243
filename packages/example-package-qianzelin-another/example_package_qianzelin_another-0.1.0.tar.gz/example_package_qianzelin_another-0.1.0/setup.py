from setuptools import setup, find_packages

setup(
    name="example_package_qianzelin_another",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 'numpy',
        # 'matplotlib',
        # 'torch',# 在这里列出你的库所需的其他Python包, 这不是requirements
    ],

    author="Zelin Qian",
    author_email="qzl22@mails.tsinghua.edu.cn",
    description="testttt",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ZelinQian/SPIDER",
    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: MIT License",
    #     "Programming Language :: Python",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.6",
    #     "Programming Language :: Python :: 3.7",
    #     "Programming Language :: Python :: 3.8",
    #     "Programming Language :: Python :: 3.9",
    # ],
    python_requires=">=3.6"
)
