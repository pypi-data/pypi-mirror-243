from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mathstropy", # Replace with your own username
    version="4.0.4",
    author="Richard Hamilton",
    author_email="richard.ha@mathstronauts.ca",
    description="Python library with functions to make learning more efficient",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mathstronauts/mathstropy",
    packages=find_packages(),
    install_requires=[
        "pygame==2.5.2",
        "opencv-python-headless==4.8.1.78",
        "numpy==1.26.2",
        "pandas==1.3.5",
        "scikit-learn>=1.3.1"

    ],
    extras_require={
        "dev": [
            "build",
            "twine",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
