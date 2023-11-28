import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="composer_notebook",
    version="0.1.6",
    author="Exa",
    author_email="exa@exponent.ai",
    description="interactive demo for composer application on Jupyter notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["composer"],
    package_dir={'composer': '.'},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.10',
    install_requires= required,
)

