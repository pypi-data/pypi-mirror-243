from setuptools import setup, find_packages
import versioneer

setup(
    name="streetaddress",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A Python port of the Perl address parser.",
    long_description="README",
    long_description_content_type="text/markdown",
    author="Mike Jensen",
    url="https://github.com/ArcadiaPower/python-streetaddress",
    keywords="streetaddress",
    packages=find_packages(),
    install_requires=["regex>=2021.10.8"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
    ],
)
