import setuptools

with open('README.md' , 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-upsrtc",
    version="0.0.1",
    author="Mohd Sabahat",
    author_email="mohdsabahat123@gmail.com",
    description="An unofficial python wrapper for UPSRTC internal API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://replit.com/@Mohdsabahat/python-upsrtc#README.md",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)