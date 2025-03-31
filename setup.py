import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monnify-python",
    version="1.0.0",
    author="Marvelous-Benji",
    author_email="integration-support@monnify.com",
    description="Python library for the Monnify API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Monnify/pymonnify",
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'marshmallow',],
    tests_require=['pytest','black'],
    test_suite='tests',
)