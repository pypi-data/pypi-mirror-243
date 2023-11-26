import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="joestock", # Replace with your own username
    version="0.0.2",
    author="joenjoy",
    author_email="kim_junhan@naver.com",
    description="Joe Utils Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://blog.naver.com/joendjoy",
    packages=setuptools.find_packages(exclude = []),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)