import setuptools

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of the requirements file
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="v2srt",
    version="2.3.0",
    author="abysmli", 
    author_email="abysmli@gmail.com", 
    description="AI-Powered Subtitle Transcription and Translation Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abysmli/v2srt",
    project_urls={
        "Bug Tracker": "https://github.com/abysmli/v2srt/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: Linguistic",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "v2srt=main:main",
        ],
    },
)
