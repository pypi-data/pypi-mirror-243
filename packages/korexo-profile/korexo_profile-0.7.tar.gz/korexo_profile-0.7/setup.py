from setuptools import setup

setup(
    name="korexo_profile",
    packages=["korexo_profile"],
    use_scm_version={'version_scheme': 'post-release'},
    setup_requires=["setuptools_scm"],
    description="Read KorEXO sonde profile CSV files",
    long_description=open("README.md", mode="r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dew-waterscience/korexo_profile",
    author="DEW Water Science (Kent Inverarity)",
    author_email="kent.inverarity@sa.gov.au",
    license="All rights reserved",
    classifiers=["Programming Language :: Python :: 3"],
    keywords="science",
    install_requires=(
        "pandas",
        "numpy",
        "scipy",
        "lasio",
    ),
    entry_points={},
)