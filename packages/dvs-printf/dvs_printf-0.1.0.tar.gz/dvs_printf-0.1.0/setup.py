import pathlib, setuptools

setuptools.setup(
    name="dvs_printf",
    version="0.1.0",
    description="types of printing animetion styles, that gives spark on your project",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/dhruvan-vyas/dvs_printf",
    author="Dhruvan_vyas",
    author_email="dhruvanvyas1@gmail.com",
    license="MIT License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities"],

    python_requires=">=3.8",
    packages=setuptools.find_packages(),
    include_package_data=True,
)