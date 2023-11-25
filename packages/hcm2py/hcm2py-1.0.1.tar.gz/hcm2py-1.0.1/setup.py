from setuptools import setup, find_packages

with open('README.md', "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hcm2py',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'requests',
        'PyOpenGL',
        'pygame',
    ],
    author="Hawk King",
    author_email="dbadbplayz@gmail.com",
    description="This is a registry generator for the Roblox game Circuit Maker 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    keywords=['registry', 'Circuit Maker 2', 'Roblox'],
    python_requires='>=3.6',
)