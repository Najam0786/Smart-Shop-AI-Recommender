from setuptools import setup, find_packages
from typing import List

# A constant for the requirements file
REQUIREMENTS_FILE = "requirements.txt"

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements file and returns a list of packages.
    This function filters out comments and blank lines.
    """
    requirements = []
    with open(file_path) as f:
        for line in f.read().splitlines():
            # Filter out comments, blank lines, and non-package lines
            if line and not line.startswith('#'):
                requirements.append(line)
    return requirements

setup(
    name="shop-smart-ai-recommender",
    version="0.0.1",
    author="Nazmul Farooquee",
    author_email="nazmulfarooquee@gmail.com",  # Add your email here
    description="An AI-powered product recommendation system using LLMs and RAG.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ShopSmartAIRecommender",  # Add your repo URL
    packages=find_packages(),
    install_requires=get_requirements(REQUIREMENTS_FILE),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # It's good practice to choose a license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)