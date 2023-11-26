# from setuptools import setup, find_packages
#
# setup(
#     name='PremaDjango',
#     use_scm_version=True,
#     setup_requires=['setuptools_scm'],
#     packages=find_packages(),
#     install_requires=[
#         # List your dependencies here
#     ],
# )
#

from setuptools import setup, find_packages
from setuptools_scm import get_version

from update_version import update_version

print("Version:", get_version())
print("Version:", update_version())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PremaDjango',
    version=update_version(),  # Dynamically determine version
    # use_scm_version=True,
    # setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
        'Django',
        'setuptools_scm'
    ],
    author="Premanath",
    author_email="talamarlapremanath143@gmail.com",
    description="My Short Description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prema1432/premadjango/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    license="MIT",
)
