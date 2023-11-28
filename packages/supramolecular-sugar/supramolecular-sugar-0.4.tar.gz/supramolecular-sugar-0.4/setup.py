import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supramolecular-sugar",
    version="0.4",
    author="Zidi Wang",
    author_email="",
    description="SUpramolecular recoGnition prediction in porous moleculAR materials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chemwzd/sugar",
    packages=setuptools.find_packages(),
    install_requires=['networkx', 'matplotlib', 'rdkit-pypi==2022.3.5',
    'numpy==1.22.4', 'scipy==1.7.1', 'MDAnalysis==2.4.3', 'pyvoro==1.3.2'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.8'
)
