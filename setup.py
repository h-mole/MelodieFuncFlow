import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="MelodieFuncFlow",
    version="0.3.0",
    description="Functional programming extension of Melodie",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hzyrc6011/MelodieFuncFlow",
    author="Zhanyi Hou",
    author_email="abm4all@outlook.com",
    license="MIT",
    # For classifiers, refer to:
    # https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    project_urls={
        "Documentation": "https://github.com/hzyrc6011/MelodieFuncFlow",
    },
    packages=setuptools.find_namespace_packages(
        include=["MelodieFuncFlow", "MelodieFuncFlow.*"]
    ),
    install_requires=[],
    python_requires=">=3.8",
    include_package_data=True,
)
