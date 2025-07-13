from setuptools import setup, find_packages

setup(
    name="reddit-abuse-tracker",
    version="1.0.0",
    description="A system to detect and track abusive language in Reddit posts",
    packages=find_packages(),
    install_requires=[
        "praw>=7.7.1",
        "pandas>=2.0.3",
        "numpy>=1.24.3",
        "scikit-learn>=1.3.0",
        "python-dotenv>=1.0.0",
        "flask>=2.3.2",
        "sqlalchemy>=2.0.17",
        "pytest>=7.4.0",
    ],
    python_requires=">=3.8",
)
