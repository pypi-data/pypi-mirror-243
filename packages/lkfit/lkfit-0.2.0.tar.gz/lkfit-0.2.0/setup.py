import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lkfit",
    version="0.2.0",
    author="Lukas Kontenis",
    author_email="dse.ssd@gmail.com",
    description="A Python library for fitting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy', 'matplotlib>=2.1.0', 'scipy>=1.5.4', 'lkcom>=0.2.0',
    ],
    python_requires='>=3.6'
)
