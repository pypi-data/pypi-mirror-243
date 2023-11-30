import setuptools
from pathlib import Path

setuptools.setup(
    name='moki_panda',                   #  项目名称
    version='0.0.2',                    #  项目版本
    description='An OpenAI Gym Env for Panda',            #  项目描述
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include='moki_panda*'),
    install_requires=['gym']   #   依赖库，这些库会在pip install的时候自动安装
)