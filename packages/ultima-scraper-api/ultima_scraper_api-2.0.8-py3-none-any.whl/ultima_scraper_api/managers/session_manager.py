from __future__ import annotations

import asyncio
import hashlib
import json
import random
import string
import time
from random import randint
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

import aiohttp
import python_socks
import requests
from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientOSError,
    ClientPayloadError,
    ClientResponseError,
    ContentTypeError,
    ServerDisconnectedError,
)
from aiohttp_socks import ProxyConnectionError, ProxyConnector, ProxyError, ProxyInfo

import ultima_scraper_api
import ultima_scraper_api.apis.api_helper as api_helper

if TYPE_CHECKING:
    auth_types = ultima_scraper_api.auth_types
EXCEPTION_TEMPLATE = (
    ClientPayloadError,
    ContentTypeError,
    ClientOSError,
    ServerDisconnectedError,
    ProxyConnectionError,
    ConnectionResetError,
    asyncio.TimeoutError,
)


class ProxyManager:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.proxies = [
            ProxyInfo(*python_socks.parse_proxy_url(proxy)) for proxy in self.session_manager.proxies  # type: ignore
        ]
        self.current_proxy_index = 0

    def create_connection(self, proxy: ProxyInfo | None = None):
        if proxy is None:
            proxy = self.proxies[0]
        return ProxyConnector(**proxy._asdict())  # type: ignore

    def get_current_proxy(self):
        return self.proxies[self.current_proxy_index]

    def add_proxy(self, proxy: str):
        self.proxies.append(ProxyInfo(*python_socks.parse_proxy_url(proxy)))  # type: ignore

    async def proxy_switcher(self):
        if self.proxies:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(
                self.proxies
            )
            await self.session_manager.active_session.close()
            self.session_manager.active_session = (
                self.session_manager.create_client_session(
                    False, self.get_current_proxy()
                )
            )


class SessionManager:
    def __init__(
        self,
        auth: ultima_scraper_api.authenticator_types,
        headers: dict[str, Any] = {},
        proxies: list[str] = [],
        max_threads: int = -1,
        use_cookies: bool = True,
    ) -> None:
        max_threads = api_helper.calculate_max_threads(max_threads)
        self.semaphore = asyncio.BoundedSemaphore(max_threads)
        self.max_threads = max_threads
        self.max_attempts = 10
        self.kill = False
        self.headers = headers
        self.proxies: list[str] = (
            proxies if proxies else auth.api.config.settings.network.proxies
        )
        self.proxy_manager = ProxyManager(self)
        self.dynamic_rules = None
        from ultima_scraper_api.apis.onlyfans.classes.extras import (
            OnlyFansAuthenticator,
        )

        if isinstance(auth, OnlyFansAuthenticator):
            self.dynamic_rules = auth.api.dynamic_rules
        self.auth = auth
        self.use_cookies: bool = use_cookies
        self.active_session = self.create_client_session()
        self.request_count = 0
        # self.last_request_time: float | None = None
        # self.rate_limit_wait_minutes = 6
        self.lock = auth.api.lock
        self.rate_limit_check = False
        self.is_rate_limited = None
        self.time2sleep = 0
        asyncio.create_task(self.check_rate_limit())

    def get_cookies(self):
        from ultima_scraper_api.apis.fansly.fansly import FanslyAuthenticator

        if isinstance(self.auth, FanslyAuthenticator):
            final_cookies: dict[str, Any] = {}
        else:
            final_cookies = self.auth.auth_details.cookie.format()
        return final_cookies

    def add_proxies(self, proxies: list[str] = []):
        for proxy in proxies:
            self.proxy_manager.add_proxy(proxy)

    def test_proxies(self, proxies: list[str] = []):
        final_proxies: list[str] = []

        session = requests.Session()
        proxies = proxies if proxies else self.proxies
        for proxy in proxies:
            url = "https://checkip.amazonaws.com"
            temp_proxies = {"https": proxy}
            try:
                resp = session.get(url, proxies=temp_proxies)
                ip = resp.text
                ip = ip.strip()
                final_proxies.append(proxy)
            except Exception as _e:
                continue
        return final_proxies

    def create_client_session(
        self, test_proxies: bool = True, proxy: ProxyInfo | None = None
    ):
        limit = 0
        if test_proxies and self.proxies:
            self.proxies = self.test_proxies()
            if not self.proxies:
                raise Exception("Unable to create session due to invalid proxies")
        connector = (
            self.proxy_manager.create_connection(proxy)
            if self.proxies
            else aiohttp.TCPConnector(limit=limit)
        )
        final_cookies = self.get_cookies()
        # Had to remove final_cookies and cookies=final_cookies due to it conflicting with headers
        # timeout = aiohttp.ClientTimeout(None)
        timeout = aiohttp.ClientTimeout(
            total=None, connect=10, sock_connect=10, sock_read=60
        )
        client_session = ClientSession(
            connector=connector, cookies=final_cookies, timeout=timeout
        )
        return client_session

    def get_proxy(self) -> str:
        proxies = self.proxies
        proxy = self.proxies[randint(0, len(proxies) - 1)] if proxies else ""
        return proxy

    # async def limit_rate(self):
    #     if self.auth.api.site_name == "OnlyFans":
    #         # [OF] 1,000 requests every 5 minutes
    #         # Can batch  =< 5,000 amount of requests, but will get rate limited and throw 429 error
    #         MAX_REQUEST_LIMIT = 900  # 900 instead of 1,000 to be safe
    #         rate_limit_wait_minutes = self.rate_limit_wait_minutes
    #         RATE_LIMIT_WAIT_TIME = 60 * rate_limit_wait_minutes
    #         if self.request_count >= MAX_REQUEST_LIMIT:
    #             # Wait until 5 minutes have elapsed since last request
    #             if self.last_request_time is not None:
    #                 elapsed_time = time.time() - self.last_request_time
    #                 if elapsed_time < RATE_LIMIT_WAIT_TIME:
    #                     time2sleep = RATE_LIMIT_WAIT_TIME - elapsed_time
    #                     print(time2sleep)
    #                     await asyncio.sleep(time2sleep)
    #             # Reset counter and timer
    #             self.request_count = 0
    #             self.last_request_time = None
    #         self.request_count += 1
    #         if self.last_request_time is None:
    #             self.last_request_time = time.time()

    async def check_rate_limit(self):
        while True:
            rate_limit_count = 1
            async with self.lock:
                while self.rate_limit_check:
                    try:
                        url = "https://onlyfans.com/api2/v2/init"
                        headers = await self.session_rules(url)
                        headers["accept"] = "application/json, text/plain, */*"
                        headers["Connection"] = "keep-alive"
                        proxy_manager = self.proxy_manager
                        if proxy_manager.proxies:
                            await proxy_manager.proxy_switcher()
                            print(proxy_manager.get_current_proxy().host)

                        result = await self.active_session.get(url, headers=headers)
                        result.raise_for_status()
                        self.rate_limit_check = False
                        self.is_rate_limited = None
                        break
                    except EXCEPTION_TEMPLATE as _e:
                        continue
                    except ClientResponseError as _e:
                        if _e.status == 429:
                            # Still rate limited, wait 5 seconds and retry
                            self.is_rate_limited = True
                            rate_limit_count += 1
                    except Exception as _e:
                        pass
                    await asyncio.sleep(self.time2sleep)
                await asyncio.sleep(5)

    async def request(
        self,
        url: str,
        method: str = "GET",
        data: Any = {},
        premade_settings: str = "json",
        custom_cookies: str = "",
    ):
        while True:
            if self.rate_limit_check:
                await asyncio.sleep(5)
                continue
            headers = {}
            if premade_settings == "json":
                headers = await self.session_rules(url)
                headers["accept"] = "application/json, text/plain, */*"
                headers["Connection"] = "keep-alive"
            if custom_cookies:
                headers = await self.session_rules(url, custom_cookies=custom_cookies)
                pass

            # await self.limit_rate()
            result = None
            try:
                match method.upper():
                    case "GET":
                        result = await self.active_session.get(url, headers=headers)
                    case "POST":
                        result = await self.active_session.post(
                            url, headers=headers, data=data
                        )
                    case "DELETE":
                        result = await self.active_session.delete(url, headers=headers)
                    case _:
                        raise Exception("Method not found")
            except EXCEPTION_TEMPLATE as _e:
                continue
            except Exception as _e:
                continue
            try:
                assert result
                result.raise_for_status()
                return result
            except EXCEPTION_TEMPLATE as _e:
                # Can retry
                continue
            except ClientResponseError as _e:
                match _e.status:
                    case 400 | 401 | 403 | 404:
                        assert result
                        return result
                    case 429:
                        pass
                        if self.is_rate_limited is None:
                            self.rate_limit_check = True
                        continue
                    case 500 | 502 | 503 | 504:
                        continue
                    case _:
                        raise Exception(
                            f"Infinite Loop Detected for unhandled status error: {_e.status}"
                        )
            except Exception as _e:
                pass

    async def bulk_requests(self, urls: list[str]) -> list[ClientResponse | None]:
        return await asyncio.gather(*[self.request(url) for url in urls])

    async def json_request(self, url: str, method: str = "GET"):
        while True:
            response = await self.request(url, method)
            json_resp: dict[Any, Any] = {}
            try:
                if response.status == 200:
                    json_resp = await response.json()
                else:
                    json_resp["error"] = {
                        "code": response.status,
                        "message": getattr(response, "reason"),
                    }
                return json_resp
            except EXCEPTION_TEMPLATE as _e:
                continue

    async def bulk_json_requests(self, urls: list[str]) -> list[dict[Any, Any]]:
        return await asyncio.gather(*[self.json_request(url) for url in urls])

    async def json_request_2(
        self,
        link: str,
        session: ClientSession | None = None,
        method: str = "GET",
        stream: bool = False,
        json_format: bool = True,
        payload: dict[str, str | bool] | str = {},
        _handle_error_details: bool = True,
    ) -> Any:
        import ultima_scraper_api.apis.fansly.classes as fansly_classes
        import ultima_scraper_api.apis.onlyfans.classes as onlyfans_classes

        async with self.semaphore:
            headers = {}
            custom_session = False
            if not session:
                custom_session = True
                session = self.create_client_session()
            headers = await self.session_rules(link)
            headers["accept"] = "application/json, text/plain, */*"
            headers["Connection"] = "keep-alive"
            if isinstance(payload, str):
                temp_payload = payload.encode()
            else:
                temp_payload = payload.copy()

            request_method = None
            result = None
            if method == "HEAD":
                request_method = session.head
            elif method == "GET":
                request_method = session.get
            elif method == "POST":
                request_method = session.post
                headers["content-type"] = "application/json"
                if isinstance(payload, str):
                    temp_payload = payload.encode()
                else:
                    temp_payload = json.dumps(payload)
            elif method == "DELETE":
                request_method = session.delete
            else:
                return None
            while True:
                try:
                    response = await request_method(
                        link, headers=headers, data=temp_payload
                    )
                    if method == "HEAD":
                        result = response
                    else:
                        if json_format and not stream:
                            # qwsd = list(response.request_info.headers.items())
                            result = await response.json()
                            if "error" in result:
                                extras: dict[str, Any] = {}
                                extras["auth"] = self.auth
                                extras["link"] = link
                                if isinstance(
                                    self.auth, onlyfans_classes.auth_model.AuthModel
                                ):
                                    handle_error = onlyfans_classes.extras.ErrorDetails
                                else:
                                    handle_error = fansly_classes.extras.ErrorDetails

                                result = await handle_error(result).format(extras)
                                if _handle_error_details:
                                    await api_helper.handle_error_details(result)
                        elif stream and not json_format:
                            result = response
                        else:
                            result = await response.read()
                    break
                except (ClientConnectorError, ProxyError):
                    break
                except (
                    ClientPayloadError,
                    ContentTypeError,
                    ClientOSError,
                    ServerDisconnectedError,
                    ProxyConnectionError,
                    ConnectionResetError,
                ) as _exception:
                    continue
                except Exception as _exception:
                    pass
            if custom_session:
                await session.close()
            return result

    async def session_rules(
        self, link: str, signed_headers: dict[str, Any] = {}, custom_cookies: str = ""
    ) -> dict[str, Any]:
        import ultima_scraper_api.apis.fansly.classes as fansly_classes
        import ultima_scraper_api.apis.onlyfans.classes as onlyfans_classes

        headers: dict[str, Any] = {}
        headers |= self.headers
        match self.auth.auth_details.__class__:
            case onlyfans_classes.extras.AuthDetails:
                if "https://onlyfans.com/api2/v2/" in link:
                    dynamic_rules = self.dynamic_rules
                    final_cookies = self.auth.auth_details.cookie.convert()
                    headers["app-token"] = dynamic_rules["app_token"]
                    headers["cookie"] = final_cookies
                    if self.auth.guest:
                        headers["x-bc"] = "".join(
                            random.choice(string.digits + string.ascii_lowercase)
                            for _ in range(40)
                        )
                    headers2 = self.create_signed_headers(link)
                    headers |= headers2
                    # t2s does not set for cdn links yet
                    self.time2sleep = 5
                elif ".mpd" in link:
                    headers["cookie"] = custom_cookies
                else:
                    if "/files/" not in link:
                        pass
                    dynamic_rules = self.dynamic_rules
                    final_cookies = (
                        self.auth.auth_details.cookie.convert() + custom_cookies
                    )
                    headers["cookie"] = final_cookies
            case fansly_classes.extras.AuthDetails:
                if "https://apiv3.fansly.com" in link:
                    headers["authorization"] = self.auth.auth_details.authorization
                    self.is_rate_limited = False
            case _:
                pass
        return headers

    def create_signed_headers(
        self, link: str, auth_id: int = 0, time_: int | None = None
    ):
        # Users: 300000 | Creators: 301000
        headers: dict[str, Any] = {}
        final_time = str(int(round(time.time()))) if not time_ else str(time_)
        path = urlparse(link).path
        query = urlparse(link).query
        if query:
            auth_id = (
                self.auth.auth_details.id if self.auth.auth_details.id else auth_id
            )
            headers["user-id"] = str(auth_id)
        path = path if not query else f"{path}?{query}"
        dynamic_rules = self.dynamic_rules
        a = [dynamic_rules["static_param"], final_time, path, str(auth_id)]
        msg = "\n".join(a)
        message = msg.encode("utf-8")
        hash_object = hashlib.sha1(message)
        sha_1_sign = hash_object.hexdigest()
        sha_1_b = sha_1_sign.encode("ascii")
        checksum = (
            sum([sha_1_b[number] for number in dynamic_rules["checksum_indexes"]])
            + dynamic_rules["checksum_constant"]
        )
        headers["sign"] = dynamic_rules["format"].format(sha_1_sign, abs(checksum))
        headers["time"] = final_time
        return headers
