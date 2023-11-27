from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Managing context as a set of variables for executing a digital assistant script'
LONG_DESCRIPTION = 'Managing context as a set of variables for executing a digital assistant script'
with open('./README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="digital-assistant-context",
    version=VERSION,
    author="Aleksandr Belov",
    author_email="a.belov@asbelon.ru",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['digital assistant'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
