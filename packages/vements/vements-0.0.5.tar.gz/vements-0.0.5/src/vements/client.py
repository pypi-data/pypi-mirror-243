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

from os import environ
from requests import Response, delete, get, post, put
from typing import Optional, Set

from vements.config import Config


class ClientConfig:
    api_key: str
    config: Config
    server_url: str

    def __init__(
        self,
        api_key: Optional[str] = None,
        tags: Set[str] = set(),
        config: Optional[Config] = None,
    ):
        self.api_key = str(api_key or "") or environ["API_KEY"]
        self.config = config or Config()
        env_tags = set()
        if environ.get("SERVER_TAGS", None):
            env_tags = set(environ["SERVER_TAGS"].split(","))
        tags = (
            set(tags)
            or env_tags
            or {
                "production",
            }
        )
        server_url = self.config.server_url(tags)
        if not server_url:
            raise NotImplementedError("no server_url available; tags: " + str(tags))
        self.server_url = server_url


class Client:
    _client_config: ClientConfig

    def __init__(self, client_config: ClientConfig):
        self._client_config = client_config

    @property
    def api_key(self) -> str:
        return self._client_config.api_key

    @property
    def config(self) -> Config:
        return self._client_config.config

    @property
    def headers(self) -> dict:
        return {"x-api-key": self.api_key}

    def url(self, path) -> str:
        return self._client_config.server_url + path[1:]

    def put(self, path, params) -> Response:
        return put(self.url(path), json=params, headers=self.headers)

    def get(self, path, params=None) -> Response:
        return get(self.url(path), params=params or {}, headers=self.headers)

    def post(self, path, params) -> Response:
        return post(self.url(path), json=params, headers=self.headers)

    def delete(self, path) -> Response:
        return delete(self.url(path), headers=self.headers)
