from setuptools import find_packages, setup

with open("README.rst", "r") as readme:
    long_description = readme.read()

setup(
    name = 'uwVIKOR',
    packages = find_packages(include=['uwVIKOR']),
    version = '1.0.0',
    author = 'Aaron Lopez-Garcia',
    author_email='logara8@alumni.uv.es',
    description = 'Unweighted VIKOR method',
    long_description=long_description,
    license = 'MIT',
    url='https://github.com/Aaron-AALG/uwVIKOR',
    download_url = 'https://github.com/Aaron-AALG/uwVIKOR/releases/tag/uwVIKOR_1.0.0',
    install_requires=['numpy >= 1.19',
                      'scipy >= 1.6.3'],
    classifiers=["Programming Language :: Python :: 3.8",
	         "License :: OSI Approved :: MIT License"],
)
