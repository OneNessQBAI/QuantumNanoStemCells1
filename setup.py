from setuptools import setup, find_packages

setup(
    name="quantum_nanobot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit>=1.24.0',
        'cirq>=1.2.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'pytest>=7.4.0',
        'matplotlib>=3.7.0',
        'scipy>=1.10.0',
        'plotly>=5.13.0'
    ],
    author="Open Quantum Technologies",
    author_email="jerry@openquantum.ca",
    description="Quantum Cell Reprogramming & Nanobot Delivery System",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://www.openquantum.ca",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
