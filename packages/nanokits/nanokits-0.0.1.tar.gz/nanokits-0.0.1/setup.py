
import os
import sys
import setuptools

# Get the Python version
major_v = sys.version_info.major
minor_v = sys.version_info.minor

# Get the compatible .pyd files
package_dir = os.path.join(os.getcwd(), "nanokits")
if not os.path.exists(package_dir):
    package_dir = os.getcwd()
    print("Package directory not found. Using current directory instead.")
    
pyd_list = [os.path.join(root, file) for root, dirs, files in os.walk(package_dir)
            for file in files if file.endswith(".pyd") and f"cp{major_v}{minor_v}" in file]

# Get the content of the README.md file
with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

# Set up the package using setuptools
setuptools.setup(
    name = "nanokits",
    version = "0.0.1",
    author = "Shen Pengju",
    author_email = "spjace@sina.com",
    description = "A small package for python",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/spjace/nanokits",
    packages = setuptools.find_packages(),
    install_requires=["packaging"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=f"~={major_v}.{minor_v}",
    include_package_data=True,
    package_data={"nanokits": pyd_list},
)
