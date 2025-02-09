from setuptools import setup, find_packages

setup(
    name="kafka-stream-processor",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "kafka-python-ng>=2.2.2",
        "pytz",
        "prometheus-client"
    ],
)
