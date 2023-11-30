from setuptools import setup
from setuptools import find_packages

setup(
    name='ergondata-executions',
    version='1.2.2',
    description="Collection of methods to connect and interact with Ergondata's Execution API",
    author_email="daniel.vossos@ergondata.com.br",
    author='Daniel Anzanello Vossos',
    url='',
    packages=find_packages(),
    install_requires=["requests", "typing_extensions", "pydantic"],
    license="MIT",
    keywords="executions"
)
