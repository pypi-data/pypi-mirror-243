# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# -*- coding: UTF-8 -*-
from typing import Any
from aselenium.chromium.options import ChromiumOptions
from aselenium.chromium.service import ChromiumService
from aselenium.chromium.session import ChromiumSessionContext
from aselenium.webdriver import ChromiumBaseWebDriver

__all__ = ["Chromium"]


# Chromium Webdriver ------------------------------------------------------------------------------
class Chromium(ChromiumBaseWebDriver):
    """The webdriver for Chromium."""

    def __init__(
        self,
        executable: str,
        service_timeout: int = 10,
        *service_args: Any,
        **service_kwargs: Any
    ) -> None:
        """The webdriver for Chromium.

        :param executable: `<str>` The absolute path to the webdriver executable file.
        :param service_timeout: `<int/float>` Timeout in seconds for starting/stopping the webdriver service. Defaults to `10`.
        :param service_args: `<Any>` Additional arguments for the webdriver service.
        :param service_kwargs: `<Any>` Additional keyword arguments for the webdriver service.
        """
        super().__init__(
            executable,
            ChromiumOptions,
            ChromiumService,
            service_timeout,
            *service_args,
            **service_kwargs,
        )

    @property
    def options(self) -> ChromiumOptions:
        """Access the webdriver options for the browser `<ChromiumOptions>`."""
        return self._options

    def acquire(self) -> ChromiumSessionContext:
        """Acquire a new browser session `<ChromiumSession>`.

        ### Example:
        >>> async with driver.acquire() as session:
                await session.load("https://www.google.com")
                # . some automated tasks
        """
        return ChromiumSessionContext(
            self._options,
            self._service_cls(
                self._executable,
                self._service_timeout,
                *self._service_args,
                **self._service_kwargs,
            ),
        )
