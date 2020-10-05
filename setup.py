import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nalapi",
    version="0.0.1",
    author="Vibby",
    author_email="contact@vibby.fr",
    description="Expose some NLTK tools to an API over HTTP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vibby/nalapi",
    packages=['nalapi'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
