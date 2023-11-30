from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

'''
# 学习了这篇文章：https://zhuanlan.zhihu.com/p/276461821
# 总结一下就是先写个 setup.py 文件，然后按照下面步骤操作：
# python3 setup.py register
# python3 setup.py sdist upload
'''
# 更新了打包步骤：https://blog.csdn.net/xcntime/article/details/115189401
# python3 setup.py sdist
# twine check dist/*
# twine upload dist/*
setup(
    name='berttextclassification',
    version='0.0.7',
    author='may.xiaoya.zhang',
    author_email='may.xiaoya.zhang@gmail.com',
    url='https://pypi.org/user/May.xiaoya.zhang/',
    description='训练/使用Bert分类模型',
    packages=find_packages(),

    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/berttextclassification 的可执行文件
    # 该文件入口指向 berttextclassification/bert_lawlaw.py 的main 函数
    entry_points={
        'console_scripts':[
            'berttextclassification = berttextclassification.bert_lawlaw:main'
        ]
    },

    long_description=long_description,
    long_description_content_type='text/markdown'
)
