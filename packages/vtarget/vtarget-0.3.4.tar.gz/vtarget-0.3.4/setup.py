from setuptools import __version__, setup

with open("./README.md", "r") as f:
    readme = f.read()

with open("./requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="vtarget",
    packages=[
        "vtarget",
        "vtarget.dataprep",
        "vtarget.dataprep.nodes",
        "vtarget.handlers",
        "vtarget.utils",
        "vtarget.utils.database_connection",
    ],
    version="0.3.4",
    description="vtarget lib",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="vTarget Team",
    author_email="contact@vtarget.ai",
    keywords=["vtarget", "dataprep"],
    classifiers=[],
    license="BSD",
    install_requires=requirements,
    include_package_data=False,
    python_requires=">=3.9.10,<3.11.0",
)
