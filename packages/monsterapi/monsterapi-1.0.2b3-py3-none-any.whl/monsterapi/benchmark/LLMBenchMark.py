import random
import asyncio
import aiohttp
from typing import Literal
from time import perf_counter

class QuickServeBenchmark:
    def __init__(self, client):
        self.client = client

    async def generate(self, model, payload):
        start_time = perf_counter()
        response = await self.client.generate(model, payload)
        end_time = perf_counter()
        response['latency'] = end_time - start_time
        return response

    async def benchmark(self, model, payload, num_iterations=10):
        tasks = []
        for _ in range(num_iterations):
            task = asyncio.create_task(self.generate(model, payload))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

    def run_benchmark(self, model: Literal["quickserve-llm","custom-image"], prompts, max_tokens, temperature=0.6, stream=False, num_iterations=10):
        prompt = random.choice(prompts)
        payload = {
            'input_variables': {"system": "You are a friendly chatbot who always responds with utmost respect using sir",
                                'prompt': prompt},
            'max_tokens': max_tokens,
            'temperature': temperature,
            'stream': stream
        }
        responses = asyncio.run(self.benchmark(model, payload, num_iterations))
        latencies = [resp['latency'] for resp in responses if 'latency' in resp]
        return {
            'average_latency': sum(latencies) / len(latencies) if latencies else 0,
            'max_latency': max(latencies) if latencies else 0,
            'min_latency': min(latencies) if latencies else 0,
            'total_requests': len(latencies),
            'total_time': sum(latencies)
        }

