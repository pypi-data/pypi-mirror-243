import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lightflask",
    version="1.0.0",
    author="Ekin Varli",
    author_email="ekinnos@tutanota.com",
    description="Lightweight Markdown Router for Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eknvarli/lightflask",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.8',
    install_requires=["Flask","markdown2"]
)
