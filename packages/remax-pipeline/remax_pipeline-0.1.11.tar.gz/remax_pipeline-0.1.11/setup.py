from setuptools import find_packages, setup


def read_requirements():
    with open("requirements.txt") as req:
        return req.read().splitlines()


setup(
    name="remax_pipeline",
    author="Aymen Rumi",
    author_email="aymen.rumi@mail.mcgill.ca",
    description="Python package to scrape data from remax (can be used locally). Package is also meant to install to deploy web scraping ETL workers in Celery and for calling pipeline jobs to celery worker server.",
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type="text/markdown",
    url="https://github.com/AymenRumi/remax-data-pipeline",  # Your project's homepage
    packages=find_packages(),
    version="0.1.11",
    # cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose the appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version requirement
    install_requires=read_requirements(),  # Include the requirements from the requirements.txt file
)
