import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WSA-Sideloader",
    version="1.1.7",
    author="infinitepower18",
    description="Easily sideload Android apps on Windows Subsystem for Android on Windows 11",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infinitepower18/WSA-Sideloader",
    project_urls={
        "Bug Tracker": "https://github.com/infinitepower18/WSA-Sideloader/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
    ],
    entry_points={
    'console_scripts': [
        'wsa-sideloader=wsasideloader.sideloader:startpypi',
    ],
    },
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["PySimpleGUI==4.57.0", "jproperties==2.1.1","plyer==2.0.0"],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)