import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quos",
    version="0.0.12",
    author="Lalit Patel",
    author_email="LLSR@att.net",
    description="Quos package simplifies plotting and simulating a quantum computing circuit employing oscillatory qudits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lapyl/quos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["matplotlib","pandas"],
    package_data={"quos": ["*.html","*.xlsm","icons/*","icons/w/*"],},
)