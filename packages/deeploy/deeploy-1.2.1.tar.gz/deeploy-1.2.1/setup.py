import re

import setuptools

with open("docs/pypi.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSIONFILE = "deeploy/_version.py"
VERSIONRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
version_string = open(VERSIONFILE, "rt").read()
mo = re.search(VERSIONRE, version_string, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    name="deeploy",
    version=version,
    description="The official Deeploy client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tim Kleinloog",
    author_email="opensource@deeploy.ml",
    packages=setuptools.find_packages(),
    package_data={"": ["*.j2", "*.bst", "*.dill", "*.json"]},
    include_package_data=True,
    url="https://gitlab.com/deeploy-ml/deeploy-python-client",
    project_urls={
        "Documentation": "https://deeploy-ml.gitlab.io/deeploy-python-client/",
        "Deeploy website": "https://deeploy.ml",
    },
    install_requires=[
        "pydantic>=1.8.2",
        "gitpython==3.1.23",
        "requests>=2.26.0",
        "joblib==1.3.2",
        "dill==0.3.6",
        "ipython>=7.26.0",
        "nbconvert>=6.0.7",
        "torch-model-archiver==0.3.1",
        "kserve[storage]==0.11.0",
        "nest-asyncio~=1.4.0",
        "click",
        "Jinja2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["deeploy = deeploy.cli.deeploycli:main"]},
)
