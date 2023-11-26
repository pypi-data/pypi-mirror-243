#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'wait-for-message',
        version = '0.1.8',
        description = 'A simple client server utility that blocks until a message is received on a TCP/IP socket connection',
        long_description = '[![build+test](https://github.com/soda480/wait-for-message/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/wait-for-message/actions/workflows/main.yml)\n[![complexity](https://img.shields.io/badge/complexity-A-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/wait-for-message.svg)](https://badge.fury.io/py/wait-for-message)\n[![python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-teal)](https://www.python.org/downloads/)\n# wait-for-message\n\nA simple client server utility that blocks until a message is received on a TCP/IP socket connection; useful for synchronizing interdependent networked jobs.\n\n## Installation\n```bash\npip install wait-for-message\n```\n\n## `w4m` Usage\n```bash\nusage: w4m [-h] {send,wait} ...\n\nA simple client server utility that blocks until a message is received on a TCP/IP socket connection\n\npositional arguments:\n  {send,wait}\n    send       send message to tcp/ip connection until acknowledged or maximum attempts\n    wait       wait for message on tcp/ip connection until received or timeout\n\noptional arguments:\n  -h, --help   show this help message and exit\n```\n\n### `w4m send`\n\nsend message to tcp/ip connection until acknowledged or maximum attempts\n\n```bash\nusage: w4m send [-h] --ip-address IP_ADDRESS --port-number PORT_NUMBER --message MESSAGE_TO_SEND [--delay DELAY] [--attempts MAX_ATTEMPTS]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --ip-address IP_ADDRESS\n                        the ip address of the server\n  --port-number PORT_NUMBER\n                        the port number the server is listening on\n  --message MESSAGE_TO_SEND\n                        the message to send\n  --delay DELAY         number of seconds to delay between retries; default 10\n  --attempts MAX_ATTEMPTS\n                        maximum retry attempts; default 6\n```\n\n### `w4m wait`\n\nwait for message on tcp/ip connection until received or timeout - if message received and if it contains a body print it to stdout\n\n```bash\nusage: w4m wait [-h] [--ip-address IP_ADDRESS] --port-number PORT_NUMBER --message MESSAGE_TO_WAIT_FOR [--timeout TIMEOUT]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --ip-address IP_ADDRESS\n                        the ip address to bind to; default 0.0.0.0\n  --port-number PORT_NUMBER\n                        the port number to listen on\n  --message MESSAGE_TO_WAIT_FOR\n                        the message to wait for\n  --timeout TIMEOUT     number of seconds to wait for message; default 900 (i.e. 15 minutes)\n```\n\n## Example\n\n### wait\n\nOn a Linux machine, start tcp/ip socket listening on port 8080 and wait for message. Note the script blocks until the expected message is received. If the message is not received a timeout error will be thrown. If the message received contains a body it is printed to stdout.\n\n```bash\nw4m wait --port-number 8080 --message "ready to proceed"\n```\n\n### send\n\nOn an other machine (this example we used a Windows machine), connect tcip/ip socket to the ip:port for the server and send several messages. Send will resend message until an acknowledgement is received. If no acknowledgement is received after max attempts a MaxAttemptsError is thrown.\n\n```bash\nw4m send --ip-address 192.168.1.199 --port-number 8080 --message "a message"\nw4m send --ip-address 192.168.1.199 --port-number 8080 --message "another message"\nw4m send --ip-address 192.168.1.199 --port-number 8080 --message "ready to proceed:message body"\n```\n\n![example1](https://raw.githubusercontent.com/soda480/wait-for-message/main/docs/images/execution.gif)\n\n## Development\n\nBuild the Docker image:\n```bash\ndocker image build \\\n-t w4m:latest .\n```\n\nRun the Docker container:\n```bash\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\n-p:8080:8080 \\\nw4m:latest \\\nbash\n```',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/wait-for-message',
        project_urls = {},

        scripts = [],
        packages = ['wait_for_message'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'console_scripts': ['w4m = wait_for_message.cli:main']
        },
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
