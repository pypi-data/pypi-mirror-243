from setuptools import setup, find_packages

setup(
    name='JinxxObbSearch',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        'tqdm==4.66.1',
    ],
    entry_points={
        'console_scripts': [
            'JinxxObbSearch = JinxxObbSearch.search:main',
        ],
    },
)
