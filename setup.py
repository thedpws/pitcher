import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()



authors_string = ', '.join(sorted(["Caleb Wong", "Aeyzechiah Vasquez", "Vinicius Martinson", "Jacob Menke", "Brian McDowell"], key= lambda n: n.split()[1]))



with open("requirements.txt", "r") as fh:
    requirements = fh.read().split('\n')

print(requirements)
input('Do these requirements look okay?')

setuptools.setup(
    name="pitchr",
    version="0.1.5",
    author=authors_string,
    author_email="azvasquez99@gmail.com",
    description="A Python library and framework for composing and playing music.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thedpws/pitcher",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
