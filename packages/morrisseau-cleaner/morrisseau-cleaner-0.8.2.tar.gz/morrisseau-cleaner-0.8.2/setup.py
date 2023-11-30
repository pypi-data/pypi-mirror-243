import setuptools
import versioneer

with open("README.rst", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="morrisseau-cleaner",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Ali Shajari",
    author_email="ali0shajari@gmail.com",
    description="A Python library to clean data for Morrisseau Project",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'morrisseau-cleaner = morrisseau_cleaner.morrisseau_cleaner:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
