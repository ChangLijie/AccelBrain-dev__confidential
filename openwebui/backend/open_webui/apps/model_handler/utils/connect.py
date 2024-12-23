import logging
from typing import Dict, Optional, Union

import aiohttp
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from open_webui.env import AIOHTTP_CLIENT_TIMEOUT
from starlette.background import BackgroundTask

log = logging.getLogger(__name__)


async def check_url(url):
    timeout = aiohttp.ClientTimeout(total=60)
    try:
        async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    log.info(f"Model handler is alive: {url}")
                    return url
                else:
                    log.error(f"Connect model_handler error: {response.status}")
                    return None
    except Exception as e:
        log.error(f"Connect model_handler error: {e}")
        return None


async def cleanup_response(
    response: Optional[aiohttp.ClientResponse],
    session: Optional[aiohttp.ClientSession],
):
    if response:
        response.close()
    if session:
        await session.close()


async def streaming_url(
    url: str,
    payload: Optional[Dict[str, Union[str, UploadFile]]] = None,
    method: str = "GET",
    stream: bool = True,
    headers: Optional[Dict[str, str]] = None,
    form_data: bool = False,
    content_type: Optional[str] = None,
):
    r = None
    try:
        session = aiohttp.ClientSession(
            trust_env=True,
            timeout=aiohttp.ClientTimeout(total=AIOHTTP_CLIENT_TIMEOUT),
        )

        data = None
        if payload:
            if form_data:
                data = aiohttp.FormData()
                for key, value in payload.items():
                    data.add_field(
                        name=key,
                        value=value.file,
                        filename=value.filename,
                        content_type=value.content_type,
                    )

            else:
                data = payload

        default_headers = {"Content-Type": "application/json"} if not form_data else {}
        if headers:
            default_headers.update(headers)
        if method.upper() == "GET" and not payload:
            default_headers.pop("Content-Type", None)
        r = await session.request(
            method=method.upper(),
            url=url,
            data=data,
            headers=default_headers,
        )
        r.raise_for_status()
        if stream:
            headers = dict(r.headers)
            if content_type:
                headers["Content-Type"] = content_type
            return StreamingResponse(
                r.content,
                status_code=r.status,
                headers=headers,
                background=BackgroundTask(
                    cleanup_response, response=r, session=session
                ),
            )
        else:
            res = await r.json()
            await cleanup_response(r, session)
            return res

    except Exception as e:
        error_detail = "Model_handler: Server Connection Error"
        if r is not None:
            try:
                res = await r.json()
                if "error" in res:
                    error_detail = f"Model_handler: {res['error']}"
            except Exception:
                error_detail = f"Model_handler: {e}"

        raise HTTPException(
            status_code=r.status if r else 500,
            detail=error_detail,
        )


async def fetch_url(url):
    timeout = aiohttp.ClientTimeout(total=60)
    try:
        async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(url) as response:
                return await response.json()
    except Exception as e:
        # Handle connection error here
        log.error(f"Connection error: {e}")
        return None


async def forward_upload(file: UploadFile, url: str):
    timeout = aiohttp.ClientTimeout(total=5)  # 設定超時為 5 秒
    try:
        file_content = await file.read()

        form_data = aiohttp.FormData()
        form_data.add_field(
            "model",
            file_content,
            filename=file.filename,
            content_type=file.content_type,
        )

        async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.post(url, data=form_data) as response:
                return await response.json()
    except Exception as e:
        log.error(f"Error forwarding upload to {url}: {e}")
        return None


async def post_model_creation(url: str, model: str, model_name_on_ollama: str):
    params = {"model": model, "model_name_on_ollama": model_name_on_ollama}
    timeout = aiohttp.ClientTimeout(total=60)

    try:
        async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.post(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    log.info(f"Response: {data}")
                    return data
                else:
                    log.error(f"Request failed with status {response.status}")
                    return None
    except Exception as e:
        log.error(f"Connection error: {e}")
        return None
