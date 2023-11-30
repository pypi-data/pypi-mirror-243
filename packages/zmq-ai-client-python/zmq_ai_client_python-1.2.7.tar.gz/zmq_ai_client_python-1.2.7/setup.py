from setuptools import setup, find_packages

setup(
    name="zmq_ai_client_python",
    version="1.2.7",
    packages=find_packages(),
    package_data={'zmq_ai_client_python': ['schema/*']},
    author="Fatih GENÇ",
    author_email="f.genc@qimia.de",
    description="A ZMQ client interface for llama server",
    long_description="A ZMQ client interface for llama server",
    url="https://github.com/zmq-ai-client-python",
    python_requires=">=3.9",
    install_requires=[
        "pyzmq>=25.1.1",
        "msgpack>=1.0.7",
        "dacite>=1.8.1"
    ],
    extras_require={
        'tests': [
            'pytest>=7.4.3',
            "polyfactory>=2.5.0",
        ]
    }
)
