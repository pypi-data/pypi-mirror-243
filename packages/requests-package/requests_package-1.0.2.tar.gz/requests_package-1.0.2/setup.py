from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_desctiption = f.read()

setup(
    name='requests_package',
    packages=find_packages(),
    long_description=long_desctiption,
    long_description_content_type="text/markdown",
    description='Request with retry configurated',
    version='1.0.2',
    url='https://github.com/edmachina/requests_package',
    author='Ezequiel Marcel',
    author_email='ezequiel.marcel@edmachina.com',
    keywords=['pip','requests','retry'],
    install_requires=["requests"],
    python_requires='>=3.9',
)
