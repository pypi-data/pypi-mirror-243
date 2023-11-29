import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="verumverify",
    version="0.0.2",
    author="Ethosymn",
    author_email="ethosymn.verum.service@gmail.com",
    description=("Verifies the authenticity of content published "
                 "on the Verum Journo portal."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ethosym/verumverify",
    install_requires=[
        'cryptography',
        'rfc3161ng',
        'click',
        'requests',
        'pymaybe'
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'verumverify = verumverify.main:main',
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
