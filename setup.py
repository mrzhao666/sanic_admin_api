from setuptools import find_packages,setup
install_requires = open("requirements.txt").readlines()

setup(
    license = "MIT License",
    long_description=open("README.md", encoding="utf-8").read(),
    install_requires = install_requires,
    author = "zhaomeng",
    author_email = "780027387@qq.com",
    name='sanic_admin_api',
    version='1.0',
    packages = find_packages(),
    url = "https://github.com/mrzhao666/sanic_admin_api",
    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: SQL",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',


)