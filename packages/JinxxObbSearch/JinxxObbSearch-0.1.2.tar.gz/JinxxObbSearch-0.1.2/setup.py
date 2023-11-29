# setup.py

from setuptools import setup, find_packages

setup(
    name='JinxxObbSearch',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'tqdm==4.62.2',
    ],
    entry_points={
        'console_scripts': [
            'search = Jinxx66ObbTool.search:main',  # Adjust the entry point
        ],
    },
)
