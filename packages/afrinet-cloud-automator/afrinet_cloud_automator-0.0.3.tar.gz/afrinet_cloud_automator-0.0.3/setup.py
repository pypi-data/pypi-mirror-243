from setuptools import setup, find_packages

# Project metadata
name = "afrinet_cloud_automator"
version = "0.0.3"
description = "Cloud Automation for All Platforms - Streamline and optimize your cloud operations with our comprehensive cloud automation solutions. Whether on AWS, Azure, Google Cloud, or other platforms, our tools empower you to automate tasks, enhance efficiency, and ensure seamless management of your cloud infrastructure."
long_description = "In the rapidly evolving landscape of cloud computing, effective management and orchestration of resources across diverse cloud platforms are imperative. Our Cloud Automation solution is designed to provide a unified and comprehensive approach to automate processes, workflows, and tasks across various cloud environments, including but not limited to AWS, Azure, Google Cloud, and more."
author = "Afrinet Devs"
author_email = "support_admin@afrinet.com"

# Package dependencies (add your project-specific dependencies here)
install_requires = [
    "requests",
    "numpy",
    "pandas",
    # Add more dependencies as needed
]

# License information
license = "MIT"

# Additional classifiers for your package (customize as needed)
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

# Entry point scripts (if applicable)
entry_points = {
    "console_scripts": [
        "my_script = afrinet_cloud_automator.module:main",
    ],
}

# Package information
packages = find_packages()

# Package setup
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url="https://github.com/yourusername/yourproject",  # Replace with your project's URL
    packages=packages,
    install_requires=install_requires,
    license=license,
    classifiers=classifiers,
    entry_points=entry_points,
)
