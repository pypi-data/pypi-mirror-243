#!/usr/bin/env python

# Copyright 2023 Monster Street Systems LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# NB: This is a generated file; any changes will be lost.

from typing import Optional, Set


class Contact:
    name: str
    url: str
    email: str

    def __init__(self, name: str, url: str, email: str):
        self.name = name
        self.url = url
        self.email = email


class License:
    name: str
    url: str

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url


class ExternalDocs:
    description: str
    url: str

    def __init__(self, description: str, url: str):
        self.description = description
        self.url = url


class Server:
    url: str
    description: str
    variables: dict[str, str]
    tags: Set[str]

    def __init__(self, url: str, description: str, variables: dict[str, str], tags: Set[str]):
        self.url = url
        self.description = description
        self.variables = variables
        self.tags = tags


class Config:
    title: str
    version: str
    description: str
    terms_of_service: str
    contact: Contact
    license: License
    external_docs: ExternalDocs
    servers: Set[Server]

    def __init__(
        self,
        title: str = "Vements REST API",
        version: str = "1.0.3",
        description: str = "This specification describes the Vements REST API, its endpoints, and  the data structures used to communicate with it.",
        terms_of_service: str = "https://vements.io/terms",
        contact: Contact = Contact(
            name="Vements Support Contact",
            url="https://vements.io",
            email="support@vements.io",
        ),
        license: License = License(
            name="MIT",
            url="https://opensource.org/license/mit/",
        ),
        external_docs: ExternalDocs = ExternalDocs(
            description="Vements REST API Documentation",
            url="https://vements.io/docs",
        ),
        servers: Set[Server] = {
            Server(
                url="https://a.vements.io/{basePath}",
                description="Production Server",
                variables={
                    "basePath": "api/rest/v1.0.3/",
                },
                tags={
                    "production",
                },
            ),
            Server(
                url="http://api.localtest.me/{basePath}",
                description="Development Server (Host)",
                variables={
                    "basePath": "api/rest/v1.0.3/",
                },
                tags={
                    "development",
                    "host",
                    "full",
                },
            ),
            Server(
                url="http://localhost:9000/{basePath}",
                description="Development Server (Host Substitute)",
                variables={
                    "basePath": "api/rest/v1.0.3/",
                },
                tags={
                    "development",
                    "host",
                    "substitute",
                },
            ),
            Server(
                url="http://api-server-a:8080/{basePath}",
                description="Development Server (Container)",
                variables={
                    "basePath": "api/rest/v1.0.3/",
                },
                tags={
                    "development",
                    "container",
                    "full",
                },
            ),
            Server(
                url="http://substitute-server:9000/{basePath}",
                description="Development Server (Container Substitute)",
                variables={
                    "basePath": "api/rest/v1.0.3/",
                },
                tags={
                    "development",
                    "container",
                    "substitute",
                },
            ),
        },
    ):
        self.title = title
        self.version = version
        self.description = description
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license = license
        self.external_docs = external_docs
        self.servers = servers

    def server_url(self, matching: Set[str]) -> Optional[str]:
        servers = [server for server in self.servers if server.tags >= matching]
        if not servers:
            return
        url = servers[0].url
        for key, value in servers[0].variables.items():
            url = url.replace("{" + key + "}", value)
        return url

