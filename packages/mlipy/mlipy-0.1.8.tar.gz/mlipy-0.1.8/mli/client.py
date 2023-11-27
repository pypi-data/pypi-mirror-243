__all__ = ['SyncMLIClient', 'AsyncMLIClient', 'LangchainMLIClient']

import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

import os
import json
import time
import threading
from typing import Iterator, AsyncIterator, Mapping, Any, Optional, Unpack, Callable

from aiohttp import ClientSession, WSMsgType
from langchain.callbacks.manager import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.schema.output import GenerationChunk

from .server import LLMParams
from .params import LlamaCppParams, CandleParams, LLMParams


DEBUG = int(os.getenv('DEBUG', 0))
DONE = object()


def _async_to_sync_iter(loop: Any, async_iter: AsyncIterator, queue: asyncio.Queue) -> Iterator:
    t = threading.Thread(target=_run_coroutine, args=(loop, async_iter, queue))
    t.start()

    while True:
        if queue.empty():
            time.sleep(0.001)
            continue

        item = queue.get_nowait()

        if item is DONE:
            break

        yield item

    t.join()


def _run_coroutine(loop, async_iter, queue):
    loop.run_until_complete(_consume_async_iterable(async_iter, queue))


async def _consume_async_iterable(async_iter, queue):
    async for item in async_iter:
        await queue.put(item)

    await queue.put(DONE)


def async_to_sync_iter(async_iter: AsyncIterator) -> Callable:
    queue = asyncio.Queue()
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError as e:
        loop = asyncio.new_event_loop()

    return _async_to_sync_iter(loop, async_iter, queue)


class BaseMLIClient:
    endpoint: str
    ws_endpoint: str


    def __init__(self, endpoint: str, ws_endpoint: str | None=None):
        # endpoint
        if not (endpoint.startswith('http://') or endpoint.startswith('https://')):
            # check if IPv4 address
            if endpoint.replace('.', '').replace(':', '').isnumeric():
                endpoint = 'http://' + endpoint
            else:
                endpoint = 'https://' + endpoint

        self.endpoint = endpoint

        # ws_endpoint
        if ws_endpoint is None:
            if endpoint.startswith('http://'):
                ws_endpoint = 'ws://' + endpoint[len('http://'):]
            elif endpoint.startswith('https://'):
                ws_endpoint = 'wss://' + endpoint[len('https://'):]
        
        self.ws_endpoint = ws_endpoint


class SyncMLIClient(BaseMLIClient):
    def __init__(self, endpoint: str, ws_endpoint: str | None=None):
        super().__init__(endpoint, ws_endpoint)
        self.async_client = AsyncMLIClient(endpoint, ws_endpoint)


    def text(self, **kwargs: Unpack[LLMParams]) -> str:
        data = asyncio.run(self.async_client.text(**kwargs))
        return data


    def chat(self, **kwargs: Unpack[LLMParams]) -> str:
        data = asyncio.run(self.async_client.chat(**kwargs))
        return data


    def iter_text(self, **kwargs: Unpack[LLMParams]) -> Iterator[str]:
        for chunk in async_to_sync_iter(self.async_client.iter_text(**kwargs)):
            yield chunk


    def iter_chat(self, **kwargs: Unpack[LLMParams]) -> Iterator[str]:
        for chunk in async_to_sync_iter(self.async_client.iter_chat(**kwargs)):
            yield chunk


class AsyncMLIClient(BaseMLIClient):
    async def text(self, **kwargs: Unpack[LLMParams]) -> str:
        url: str = f'{self.endpoint}/text/completions'

        async with ClientSession() as session:
            async with session.post(url, json=kwargs) as resp:
                data = await resp.json()

        return data


    async def chat(self, **kwargs: Unpack[LLMParams]) -> str:
        url: str = f'{self.endpoint}/chat/completions'

        async with ClientSession() as session:
            async with session.post(url, json=kwargs) as resp:
                data = await resp.json()

        return data


    async def iter_text(self, **kwargs: Unpack[LLMParams]) -> AsyncIterator[str]:
        url: str = f'{self.ws_endpoint}/text/completions'
        
        async with ClientSession() as session:
            async with session.ws_connect(url) as ws:
                await ws.send_json(kwargs)

                async for msg in ws:
                    if msg.type == WSMsgType.PING:
                        await ws.pong(msg.data)
                    elif msg.type == WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        yield data['chunk']
                    elif msg.type == WSMsgType.ERROR:
                        print(f'[ERROR] websocket closed with exception: {ws.exception()}')
                        break


    async def iter_chat(self, **kwargs: Unpack[LLMParams]) -> AsyncIterator[str]:
        url: str = f'{self.ws_endpoint}/chat/completions'
        
        async with ClientSession() as session:
            async with session.ws_connect(url) as ws:
                await ws.send_json(kwargs)

                async for msg in ws:
                    if msg.type == WSMsgType.PING:
                        await ws.pong(msg.data)
                    elif msg.type == WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        yield data['chunk']
                    elif msg.type == WSMsgType.ERROR:
                        print(f'[ERROR] websocket closed with exception: {ws.exception()}')
                        break


class LangchainMLIClient(LLM):
    endpoint: str = 'http://127.0.0.1:5000/api/1.0'
    streaming: bool = False

    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return 'LangchainMLIClient'

    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            'endpoint': self.endpoint,
        }


    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Unpack[LLMParams],
    ) -> str:
        """Run the LLM on the given prompt and input."""
        print('_call', self)
        sync_client = SyncMLIClient(self.endpoint)

        if self.streaming:
            output: list[str] | str = []

            for chunk in self._stream(prompt=prompt, stop=stop, run_manager=run_manager, **kwargs):
                output.append(chunk.text)

            output = ''.join(output)
        else:
            res: dict = sync_client.text(prompt=prompt, stop=stop, **kwargs)
            output: str = res['output']
        
            logprobs = None

            if run_manager:
                run_manager.on_llm_new_token(
                    token=output,
                    verbose=self.verbose,
                    log_probs=logprobs,
                )

        return output


    async def _acall(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Unpack[LLMParams],
    ) -> str:
        """Run the LLM on the given prompt and input."""
        print('_acall', self)
        async_client = AsyncMLIClient(self.endpoint)

        if self.streaming:
            output: list[str] | str = []

            async for chunk in self._astream(prompt=prompt, stop=stop, run_manager=run_manager, **kwargs):
                output.append(chunk.text)

            output = ''.join(output)
        else:
            res: dict = await async_client.text(prompt=prompt, stop=stop, **kwargs)
            output: str = res['output']
            logprobs = None

            if run_manager:
                await run_manager.on_llm_new_token(
                    token=output,
                    verbose=self.verbose,
                    log_probs=logprobs,
                )

        return output


    def _stream(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Unpack[LLMParams],
    ) -> Iterator[GenerationChunk]:
        """Yields results objects as they are generated in real time.

        It also calls the callback manager's on_llm_new_token event with
        similar parameters to the LLM class method of the same name.
        """
        print('_stream', self)
        sync_client = SyncMLIClient(self.endpoint)
        logprobs = None

        for text in sync_client.iter_text(prompt=prompt, stop=stop, **kwargs):
            chunk = GenerationChunk(
                text=text,
                generation_info={'logprobs': logprobs},
            )

            yield chunk

            if run_manager:
                run_manager.on_llm_new_token(
                    token=chunk.text,
                    verbose=self.verbose,
                    log_probs=logprobs,
                )


    async def _astream(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Unpack[LLMParams],
    ) -> AsyncIterator[GenerationChunk]:
        """Yields results objects as they are generated in real time.

        It also calls the callback manager's on_llm_new_token event with
        similar parameters to the LLM class method of the same name.
        """
        print('_astream', self)
        async_client = AsyncMLIClient(self.endpoint)
        logprobs = None

        async for text in async_client.iter_text(prompt=prompt, stop=stop, **kwargs):
            chunk = GenerationChunk(
                text=text,
                generation_info={'logprobs': logprobs},
            )

            yield chunk

            if run_manager:
                await run_manager.on_llm_new_token(
                    token=chunk.text,
                    verbose=self.verbose,
                    log_probs=logprobs,
                )
