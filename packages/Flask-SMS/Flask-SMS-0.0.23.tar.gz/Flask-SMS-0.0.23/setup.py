"""
 Flask-SMS
 # ~~~~~~~~~~~~~~
 flask 短信 扩展
 Flask SMS extension
 :copyright: (c) 2023.11 by 浩.
 :license: GPL, see LICENSE for more details.
"""

from os import path
from codecs import open
from setuptools import setup


basedir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-SMS',  # 包名称
    version='0.0.23',  # 版本
    url='',
    license='MIT',
    author='浩',
    author_email='',
    description='flask-sms',
    long_description=long_description,
    long_description_content_type='text/markdown',  # 默认渲染格式为 rst
    platforms='any',
    packages=['flask_sms'],  # 包含的包列表，包括子包，可用find_pakages()
    zip_safe=False,
    test_suite='test_flask_share',  # 测试包或模块
    include_package_data=True,
    install_requires=['Flask', 'alibabacloud_dysmsapi20170525==2.0.24',"redis"],  # 安装依赖
    keywords='flask extension development sms',  # 项目关键词
    classifiers=[  # 分类词， 在 PyPI 中设置分类
        "Programming Language :: Python :: 3",
      ]
)
