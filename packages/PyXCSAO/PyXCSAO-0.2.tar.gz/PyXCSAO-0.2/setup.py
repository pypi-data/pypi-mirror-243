import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="PyXCSAO",
    version="0.2",
    author="Marina Kounkel",
    author_email="marina.kounkel@vanderbilt.edu",
    description="Replicates functionality of IRAF XCSAO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkounkel/pyxcsao",
    packages=['pyxcsao'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['astropy','numpy','scipy','specutils','PyAstronomy'],
    python_requires='>=3.6',
)
