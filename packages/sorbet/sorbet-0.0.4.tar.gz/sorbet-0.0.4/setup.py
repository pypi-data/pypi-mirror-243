from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "A better printing experience in the console."
LONG_DESCRIPTION = "Sorbet is a Python package designed to enhance the printing experience in the console."

# Setting up
setup(
    name="sorbet",
    version=VERSION,
    author="Himeji",
    author_email="<himejidev@proton.me>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["executing", "asttokens"],
    keywords=["python", "print", "icecream", "log", "debug", "console", "sorbet"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
