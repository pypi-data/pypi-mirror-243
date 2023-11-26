from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as req:
    requires = req.read().split('\n')[:-1]

setup_params = dict(
    name =          'pysqream_log_analyzer',
    version =       '0.0.3',
    description =   'The log analyzer has the ability to help us find the correct logs faster and in a more intuitive way.',
    long_description = long_description,
    url = "https://github.com/SQream/pysqream_log_analyzer",
    author = "SQream",
    author_email = "info@sqream.com",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.9',
    install_requires=requires
)

if __name__ == '__main__':
    setup(**setup_params)
