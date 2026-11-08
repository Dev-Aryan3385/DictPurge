from setuptools import setup, find_packages

setup(
    name="DictPurge",
    version="1.0",
    description="An advanced dictionary manipulation & wordlist merging tool.",
    author="Aryan Kumar Shrivastav",
    py_modules=["dictpurge", "termcolor"],
    package_data={
        "": ["doc/*", "txt/*"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "DictPurge=dictpurge:main",
            "dictpurge=dictpurge:main",
        ],
    },
    python_requires=">=3.6",
)

