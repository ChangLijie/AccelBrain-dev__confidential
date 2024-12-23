import json
import logging
from typing import Optional
from urllib.parse import urljoin

from fastapi import FastAPI, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from open_webui.config import CORS_ALLOW_ORIGIN, MODEL_HANDLER_URL, AppConfig
from open_webui.env import SRC_LOG_LEVELS

from .schema.error import ResponseErrorHandler
from .schema.main import CreateModel, DeleteModel, UploadModel
from .utils.connect import check_url, streaming_url

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODEL_HANDLER"])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.config = AppConfig()

app.state.config.MODEL_HANDLER_URL = MODEL_HANDLER_URL


@app.on_event("startup")
async def on_startup():
    valid_url = await check_url(MODEL_HANDLER_URL)
    if valid_url:
        app.state.config.MODEL_HANDLER_URL = valid_url
        log.info(f"MODEL_HANDLER_URL is set to: {valid_url}")
    else:
        raise ConnectionError(f"MODEL_HANDLER_URL is invalid: {MODEL_HANDLER_URL}")


@app.get("/model", tags=["Get models list"])
async def get_models():
    error_handler = ResponseErrorHandler()
    try:
        url = urljoin(app.state.config.MODEL_HANDLER_URL, "model")

        return await streaming_url(url=url, method="get")

    except Exception as e:
        error_handler.add(
            type=error_handler.ERR_UNEXPECTED,
            loc=[error_handler.LOC_UNEXPECTED],
            msg=str(e),
            input=dict(),
        )
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json.dumps(error_handler.errors),
            media_type="application/json",
        )


@app.post("/upload", tags=["Upload model."])
async def upload(model: Optional[UploadFile] = None):
    error_handler = ResponseErrorHandler()
    try:
        request = UploadModel(model=model)
        log.info(f"Uploading file: {request.model.filename}")
        url = urljoin(app.state.config.MODEL_HANDLER_URL, "upload")
        payload = {"model": request.model}

        return await streaming_url(
            url=url, payload=payload, method="post", form_data=True
        )

    except Exception as e:
        error_handler.add(
            type=error_handler.ERR_UNEXPECTED,
            loc=[error_handler.LOC_UNEXPECTED],
            msg=str(e),
            input=dict(),
        )
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json.dumps(error_handler.errors),
            media_type="application/json",
        )


@app.delete("/model", tags=["Delete Innodisk Model"])
async def delete_model(
    request: DeleteModel,
):
    error_handler = ResponseErrorHandler()
    try:
        url = urljoin(app.state.config.MODEL_HANDLER_URL, "model")
        payload = {**request.model_dump(exclude_none=True), "insecure": True}

        return await streaming_url(
            url=url, payload=json.dumps(payload), method="delete"
        )

    except Exception as e:
        error_handler.add(
            type=error_handler.ERR_UNEXPECTED,
            loc=[error_handler.LOC_UNEXPECTED],
            msg=str(e),
            input=dict(),
        )
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json.dumps(error_handler.errors),
            media_type="application/json",
        )


@app.post("/model/create", tags=["Create Model on Ollama"])
async def create_model(
    request: CreateModel,
):
    error_handler = ResponseErrorHandler()
    try:
        url = urljoin(app.state.config.MODEL_HANDLER_URL, "create")
        payload = {**request.model_dump(exclude_none=True), "insecure": True}

        return await streaming_url(url=url, payload=json.dumps(payload), method="post")

    except Exception as e:
        error_handler.add(
            type=error_handler.ERR_UNEXPECTED,
            loc=[error_handler.LOC_UNEXPECTED],
            msg=str(e),
            input=dict(),
        )
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json.dumps(error_handler.errors),
            media_type="application/json",
        )
