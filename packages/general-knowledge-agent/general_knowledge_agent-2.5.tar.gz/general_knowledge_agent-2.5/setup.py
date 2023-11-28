from setuptools import find_packages, setup

# Setup custom import schema
# cortex_cli.cli
# cortex_cli.core
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)

from general_knowledge_agent import __version__

setup(
    name="general_knowledge_agent",
    version=__version__,
    packages=find_packages(exclude=['tests*']),
    author='Nearly Human',
    author_email='support@nearlyhuman.ai',
    description='Nearly Human General Knowledge Agent dependency for creating functional client specific agents.',
    keywords='nearlyhuman, nearly human, agent',

    python_requires='>=3.10',
    # long_description=open('README.txt').read(),
    install_requires=[
        'cortex-cli',
        'scikit-learn==1.2.2',
        'openai==0.28.0',
        'langchain==0.0.330',
        'chromadb==0.4.15',
        'tiktoken',
        'pydantic==1.10.11'
    ]
)