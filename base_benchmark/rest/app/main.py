import random
from typing import Dict, List

from fastapi import FastAPI, Request
from pydantic import BaseModel

RESPONSE_LIST_SIZE = 10

app = FastAPI()


class BasicRequest(BaseModel):
    field1: str
    field2: str
    field3: int
    field4: Dict[str, int]


class ImageBase64Request(BaseModel):
    image: str


class ImageBinaryRequest(BaseModel):
    image: bytes


class BasicResponse(BaseModel):
    prediction1: List[float]
    prediction2: Dict[str, int]


app = FastAPI()


@app.post("/basic")
async def basic(basic_request: BasicRequest):
    return BasicResponse(
        prediction1=[random.random() for _ in range(100)], prediction2={str(i): i for i in range(RESPONSE_LIST_SIZE)}
    )


@app.post("/base64")
async def base64(base64_request: ImageBase64Request):
    return BasicResponse(
        prediction1=[random.random() for _ in range(100)], prediction2={str(i): i for i in range(RESPONSE_LIST_SIZE)}
    )


@app.post("/binary")
async def binary(request: Request):
    image: bytes = await request.body()
    return BasicResponse(
        prediction1=[random.random() for _ in range(100)], prediction2={str(i): i for i in range(RESPONSE_LIST_SIZE)}
    )
