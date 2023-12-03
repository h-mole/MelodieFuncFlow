import setuptools


setuptools.setup(
    name="ModuleTemplate",
    version="0.0.1",
    description="Template for module",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/ABM4ALL/Melodie",
    author="Songmin Yu",
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
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    project_urls={
        "Documentation": "http://docs.abm4all.com",
    },
    packages=setuptools.find_namespace_packages(
        include=["ModuleTemplate", "ModuleTemplate.*"]
    ),
    install_requires=[
        "pandas",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
