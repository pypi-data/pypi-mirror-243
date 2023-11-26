from setuptools import setup, find_packages

setup(
    name="winautostart",
    version="0.2",
    packages=find_packages(),
    license="MIT",
    description="Manage your Windows autostarts",
    long_description="README at https://github.com/infernox-dev/winautostart",
    long_description_content_type="text/markdown",
    author="infernox.dev",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[],
    python_requires=">=3.6",
)
