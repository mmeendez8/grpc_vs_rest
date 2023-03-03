import asyncio
import base64
from time import time
import sys
import cv2
import grpc
import numpy as np
from httpx import AsyncClient, Timeout
from grpc_stubs import inference_pb2_grpc, inference_pb2

ITERATIONS = [10]
CONCURRENCY = [20]
IMAGE_SIZES = [(360, 640, 3), (720, 1280, 3), (1080, 1920, 3)]

MODEL_NAME = "densenet161"

async def grpc_request(stub, image):
    return await stub.Predictions(inference_pb2.PredictionsRequest(
        model_name=MODEL_NAME,
        input={"data": image},
    ))


async def send_grpc_requests(n_requests, concurrent_request, request_callable, *args):
    grpc_times = []
    for _ in range(n_requests):
        tasks = [request_callable(*args) for _ in range(concurrent_request)]
        start = time()
        results = await asyncio.gather(*tasks)
        end = time() - start
        grpc_times.append(end)

        for result in results:
            assert result is not None

        print(f"GRPC call took \t: {end}")

    return grpc_times


async def send_rest_requests(n_requests, concurrent_request, client, rest_url, data):
    rest_times = []
    for _ in range(n_requests):

        tasks = []
        for _ in range(concurrent_request):
            if isinstance(data, bytes):
                tasks.append(asyncio.create_task(client.post(url=rest_url, data=data)))
            else:
                tasks.append(asyncio.create_task(client.post(url=rest_url, json=data)))
        start = time()
        results = await asyncio.gather(*tasks)
        end = time() - start
        rest_times.append(end)

        for result in results:
            assert result.status_code == 200, f"Error, status code: {result.status_code}"
        print(f"REST call took \t: {end}")

    return rest_times


def get_binary_request(image_size):
    image = (np.random.rand(*image_size) * 255).astype(np.uint8)
    return cv2.imencode(".jpg", image)[1].tobytes()


def get_base64_request(image_size):
    image = get_binary_request(image_size)
    return base64.b64encode(image).decode("utf-8")


async def benchmark(rest_url, grpc_url, image_size, iterations, concurrency):
    channel = grpc.aio.insecure_channel(grpc_url)
    stub = inference_pb2_grpc.InferenceAPIsServiceStub(channel)

    client = AsyncClient(timeout=Timeout(timeout=30.0))

    print(f"\nResults for Image Size: {image_size} - Iterations: {iterations} - Concurrency: {concurrency}\n")

    # Send BASE64 REST request
    print("\nREST B64:\n" + 100 * "=")
    b64_request = get_base64_request(image_size)
    rest_b64_times = await send_rest_requests(iterations, concurrency, client, rest_url, b64_request)

    # Send BASE64 REST request
    print("\nREST Binary:\n" + 100 * "=")
    binary_request = get_binary_request(image_size)
    rest_binary_times = await send_rest_requests(iterations, concurrency, client, rest_url, binary_request)

    print("\nGRPC Binary:\n" + 100 * "=")
    grpc_binary_times = await send_grpc_requests(iterations, concurrency, grpc_request, stub, binary_request)

    print(f"\nResults for Image Size: {image_size} - Iterations: {iterations} - Concurrency: {concurrency}\n" + 20 * "=")
    print(f"REST Base64 Mean time \t: {np.mean(np.array(rest_b64_times))}\n")
    print(f"REST Binary Mean time \t: {np.mean(np.array(rest_binary_times))}\n")
    print(f"GRPC Binary Mean time \t: {np.mean(np.array(grpc_binary_times))}\n")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide REST URL and GRPC URL as arguments")
        exit()
    
    rest_url, grpc_url = sys.argv[1:]

    rest_url += f"/predictions/{MODEL_NAME}"

    for image_size in IMAGE_SIZES:
        for iterations in ITERATIONS:
            for concurrency in CONCURRENCY:
                asyncio.run(benchmark(rest_url, grpc_url, image_size, iterations, concurrency))
