from setuptools import find_packages, setup


def read_requirements():
    with open("requirements.txt") as req:
        return req.read().splitlines()


setup(
    name="remax_pipeline",
    author="Aymen Rumi",
    author_email="aymen.rumi@mail.mcgill.ca",
    description="A Python package designed for scraping data from Remax, enabling local use and integration with Celery for deploying ETL workers. It supports multiple multithreaded pipeline tasks for efficient data processing on Celery worker servers.",
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type="text/markdown",
    url="https://github.com/AymenRumi/remax-data-pipeline",  # Your project's homepage
    packages=find_packages(),
    version="0.1.13",
    # cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose the appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version requirement
    install_requires=read_requirements(),  # Include the requirements from the requirements.txt file
)
