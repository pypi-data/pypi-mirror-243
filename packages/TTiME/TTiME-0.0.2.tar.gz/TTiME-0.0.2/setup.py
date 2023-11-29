from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="TTiME",
    version="0.0.2",
    author="Leonhard X. Driever",
    author_email="ttime.python@gmail.com",
    description="Tensor Trains in Mathematics and Engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['coverage',
                        'numpy',
                        'tqdm',
                        'scipy',
                        'numba',
                        'setuptools',
                        'matplotlib'],
)
