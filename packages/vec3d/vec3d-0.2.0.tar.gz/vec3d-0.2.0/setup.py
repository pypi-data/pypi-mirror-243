from setuptools import setup

with open("README.md", encoding="utf-8") as file:
    read_me_description = file.read()

setup(
    name="vec3d",
    version="0.2.0",
    author="Sergio F. Gonzalez",
    author_email="sergio.f.gonzalez@gmail.com",
    description="Maths and graph functions for vectors in the 3D space",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergiofgonzalez/vec3d",
    packages=["vec3d/graph", "vec3d/math"],
    include_package_data=True,
    install_requires=["matplotlib", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
