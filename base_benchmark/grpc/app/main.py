import asyncio

import random
from typing import Dict, List, Tuple

import grpc

from grpc_stubs import benchmark_pb2
from grpc_stubs.benchmark_pb2_grpc import (
    GrpcBenchmarkApiService,
    add_GrpcBenchmarkApiServiceServicer_to_server,
)

RESPONSE_SIZE = 100


class GrpcBenchmarkApiServiceHandler(GrpcBenchmarkApiService):
    async def BenchmarkBasicRequest(
            self, request: benchmark_pb2.BasicRequest, context: grpc.aio.ServicerContext, **kwargs
    ) -> benchmark_pb2.BasicResponse:
        print("Received basic request")

        prediction1, prediction2 = self.generate_random_response()

        return benchmark_pb2.BasicResponse(
            prediction1=prediction1,
            prediction2=prediction2,
        )

    async def BenchmarkB64Image(
            self, request: benchmark_pb2.ImageBase64Request, context: grpc.aio.ServicerContext, **kwargs
    ) -> benchmark_pb2.BasicResponse:
        print("Received b64 image request")

        prediction1, prediction2 = self.generate_random_response()

        return benchmark_pb2.BasicResponse(
            prediction1=prediction1,
            prediction2=prediction2,
        )

    async def BenchmarkBinaryImage(
            self, request: benchmark_pb2.ImageBinaryRequest, context: grpc.aio.ServicerContext, **kwargs
    ) -> benchmark_pb2.BasicResponse:
        print(f"Received binary image request")

        prediction1, prediction2 = self.generate_random_response()

        return benchmark_pb2.BasicResponse(
            prediction1=prediction1,
            prediction2=prediction2,
        )

    @classmethod
    def generate_random_response(cls) -> Tuple[List[float], Dict[str, int]]:
        prediction1 = [random.random() for _ in range(RESPONSE_SIZE)]
        prediction2 = {f"{i}": i for i in range(RESPONSE_SIZE)}

        return prediction1, prediction2


async def serve():
    server = grpc.aio.server()
    add_GrpcBenchmarkApiServiceServicer_to_server(GrpcBenchmarkApiServiceHandler(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Server running...")
    await server.wait_for_termination()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve())
