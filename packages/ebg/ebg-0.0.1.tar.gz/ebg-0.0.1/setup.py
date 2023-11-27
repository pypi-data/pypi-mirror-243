from setuptools import setup, find_packages

setup(
    name="ebg",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['ebg = EBG.__main__:main']
    },
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
        "ete3",
        "biopython",
        "networkx",
        "scipy",
        "lightgbm"

    ],
    package_data={
        'ebg': ['EBG/Models/*.pkl'],
    },
)
