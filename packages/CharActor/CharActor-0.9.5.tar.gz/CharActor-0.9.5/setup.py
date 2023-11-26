from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='CharActor',
    version='0.9.5',
    description='A module for creating and managing rpg characters.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/CharActor',
    packages=find_packages(),
    install_requires=[
        'dicepy', 
        'entyty',
        'CharObj', 
        'getch', 
        'pyglet', 
        'pymunk'],
    python_requires='>=3.8',
    keywords='rpg character dnd d&d dungeons and dragons dungeons & dragons player character actor charactor',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
        ],
    include_package_data=True,
    package_data={'CharActor': ['_charactor/dicts/*.json']}
)