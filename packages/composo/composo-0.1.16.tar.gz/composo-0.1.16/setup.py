from setuptools import setup, find_packages

setup(
    name="composo",
    version="0.1.16",
    description="Composo Python Package",
    author="Luke Markham",
    author_email="luke@composo.ai",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "colorama>=0.4.4",
        "pydantic<2.0.0,>=1.9.0"
        
    ],
    python_requires=">=3.8",
)
