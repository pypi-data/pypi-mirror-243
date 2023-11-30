from setuptools import setup, find_packages

setup(
    name='sandeep_keyword_generator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'langchain',
        'torch',
        'einops',
        'accelerate',
        'bitsandbytes',
        # Add any other dependencies your package needs
    ],
    description='Keyword extraction using LLMs',
    author='Your Name',
    author_email='your.email@example.com',
)
