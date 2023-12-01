from setuptools import setup

setup(
    name="catgpt",
    version="0.0.7",
    description="A simple cli tool to generate text using GPT-turbo",
    author="tom <tom@gmail.com>",
    install_requires=[
        "codefast>=23.4.18", "python-dotenv>=1.0.0", "sseclient-py>=1.7.2"
    ],
    tests_require=["pytest>=5.2"],
)
