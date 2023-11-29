from setuptools import setup, find_packages

setup(
    name="testprojvis",
    version="0.0.4",
    author="vismaya",
    author_email="muruganvichunni@gmail.com",
    url="https://github.com/VismayaM-2003/Pack.git",
    description="An application that informs you of the time in different locations and timezones",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["cloudquicklabs1 = src.main:main"]},
)