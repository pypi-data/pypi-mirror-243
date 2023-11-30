# -*- coding: utf-8 -*-

# (C) Copyright 2023 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


import os

from setuptools import setup

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
with open(README_PATH) as readme_file:
    README = readme_file.read()

# NOTE: The lists below require each requirement on a separate line,
# putting multiple requirements on the same line will prevent qiskit-bot
# from correctly updating the versions for the qiskit packages.
requirements = ["qiskit==0.45.0", "backoff"]

setup(
    name="qiskit-transpiler-service",
    version="0.1.0",
    description="A custom Qiskit transpiler plugin that uses IBM AI Transpiler services",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service",
    author="Data & Intelligence team, IBM Quantum",
    author_email="",
    license="Apache 2.0",
    py_modules=[],
    packages=["qiskit_transpiler_service"],
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
    ],
    keywords="qiskit ai transpiler plugin",
    install_requires=requirements,
    project_urls={
        "Bug Tracker": "https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service/issues",
        "Documentation": "https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service",
        "Source Code": "https://github.ibm.com/IBM-Q-Software/qiskit-transpiler-service",
    },
    include_package_data=True,
    python_requires=">=3.8",
    entry_points={
        "qiskit.synthesis": [
            "clifford.ai = qiskit_transpiler_service.ai:CliffordAISynthesizer",
            "linear_function.ai = qiskit_transpiler_service.ai:LinearFunctionAISynthesizer",
            "permutation.ai = qiskit_transpiler_service.ai:PermutationAISynthesizer",
        ]
    },
)
