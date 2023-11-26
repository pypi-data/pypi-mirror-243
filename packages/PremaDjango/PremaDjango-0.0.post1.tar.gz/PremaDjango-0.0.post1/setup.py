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

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PremaDjango',
    # version='0.1.9',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
        'Django',  # Add other default libraries here
    ],
    author="Premanath",
    author_email="talamarlapremanath143@gmail.com",
    description="My Short Description",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
