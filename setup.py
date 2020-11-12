from setuptools import setup
import io

install_requires = open("requirements.txt").readlines()

setup(
    
    install_requires = install_requires,
    author = "zhaomeng",
    author_email = "780027387@qq.com",
    name='sanic_admin_api',
    version='1.0',
    packages = ['sanic_admin_api'],
    url = "https://github.com/mrzhao666/sanic_admin_api",

)