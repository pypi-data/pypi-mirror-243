from setuptools import find_packages, setup

setup(
    name='mfio',
    version='1.3.5',
    description='自用文件读写检索匹配工具',
    url='https://github.com/MrRabbit2MissCat/mmfio',
    author='yunhgu',
    author_email='1508777473@qq.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'loguru',
        'xlrd==1.2.0',
        'xlwt',
        'numpy',
        'opencv_python',
        'xmltodict',
        "pyyaml",
        "requests",
        "openpyxl",
        "rich",
    ],
    python_requires='>=3.7',
)
