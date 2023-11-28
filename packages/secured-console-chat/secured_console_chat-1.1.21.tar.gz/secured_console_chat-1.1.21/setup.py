import setuptools
  
with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()
  
setuptools.setup(
    name="secured_console_chat",
    version="1.1.21",
    author="dinosaurtirex",
    author_email="sneakybeaky18@gmail.com",
    packages=[
        "cmd_chat", 
        "cmd_chat/client",
        "cmd_chat/client/core",
        "cmd_chat/client/core/abs",
        "cmd_chat/server"
    ],
    description="Secured console chat with RSA & Fernet",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/dinosaurtirex/cmd-chat",
    license='MIT',
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'cmd_chat = cmd_chat:main'
        ]
    },
    install_requires=[
        "sanic",
        "requests",
        "rsa",
        "cryptography",
        "colorama",
        "pydantic",
        "websocket-client"
    ]
)