__all__ = [
    'MLIServer',
]

import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

import os
import json
import shlex
import argparse
# import traceback
from weakref import WeakKeyDictionary
from typing import AsyncIterator, TypedDict, Optional, Required, Unpack

from aiohttp import web, WSMsgType
from huggingface_hub import try_to_load_from_cache

from .params import LlamaCppParams, CandleParams, LLMParams


DEBUG = int(os.getenv('DEBUG', 0))


class MLIServer:
    host: str
    port: int
    timeout: float
    candle_path: str
    llama_cpp_path: str
    app: web.Application
    lock: asyncio.Lock
    ws_proc_map: WeakKeyDictionary


    def __init__(self,
                 host: str='0.0.0.0',
                 port=5000,
                 timeout: float=90.0,
                 candle_path: str | None=None,
                 llama_cpp_path: str | None=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.candle_path = candle_path
        self.llama_cpp_path = llama_cpp_path
        self.app = web.Application()
        self.lock = asyncio.Lock()
        self.ws_proc_map = WeakKeyDictionary()


    def _format_llama_cpp_cmd(self, kind: str, **kwargs: Unpack[LlamaCppParams]) -> str:
        cmd: list[str] | str = []
        
        if kind == 'main':
            prompt: str = kwargs['prompt']
            model: str = kwargs['model']
            model_id: str | None = kwargs.get('model_id')
            chatml: bool | None = bool(kwargs.get('chatml', False))
            n_predict: int = int(kwargs.get('n_predict', '-1'))
            ctx_size: int = int(kwargs.get('ctx_size', '2048'))
            batch_size: int = int(kwargs.get('batch_size', '512'))
            temp: float = float(kwargs.get('temp', '0.8'))
            n_gpu_layers: int = int(kwargs.get('n_gpu_layers', '0'))
            top_k: int = int(kwargs.get('top_k', '40'))
            top_p: float = float(kwargs.get('top_p', '0.9'))
            
            # shell_prompt
            shell_prompt: str = shlex.quote(prompt)

            # model_path
            if model_id:
                model_path = try_to_load_from_cache(repo_id=model_id, filename=model)
            else:
                model_path = model

            cmd.extend([
                f'{self.llama_cpp_path}/{kind}',
                '--model', model_path,
            ])

            if chatml:
                cmd.extend([
                    '--chatml',
                ])

            cmd.extend([
                '--n-predict', n_predict,
                '--ctx-size', ctx_size,
                '--batch-size', batch_size,
                '--temp', temp,
                '--n-gpu-layers', n_gpu_layers,
                '--top-k', top_k,
                '--top-p', top_p,
                '--simple-io',
                '--log-disable',
                '--prompt', shell_prompt,
            ])
        else:
            raise ValueError(f'Unsupported kind: {kind}')

        cmd = ' '.join(str(n) for n in cmd)
        return cmd


    def _format_candle_cmd(self, kind: str, **kwargs: Unpack[CandleParams]) -> str:
        cmd: list[str] | str = []
        
        if kind == 'phi':
            prompt: str = kwargs['prompt']
            model: str = kwargs['model']
            cpu: bool = bool(kwargs.get('cpu', False))
            temperature: int = float(kwargs.get('temperature', '0.8'))
            top_p: int = float(kwargs.get('top_p', '0.9'))
            sample_len: int = int(kwargs.get('sample_len', '100'))
            quantized: bool = bool(kwargs.get('quantized', False))

            # shell_prompt
            shell_prompt: str = shlex.quote(prompt)
            
            cmd.extend([
                f'{self.candle_path}/target/release/examples/phi',
            ])

            if cpu:
                cmd.extend([
                    '--cpu',
                ])

            cmd.extend([
                '--model', model,
                '--temperature', temperature,
                '--top-p', top_p,
                '--sample-len', sample_len,
            ])
            
            if quantized:
                cmd.extend([
                    '--quantized',
                ])

            cmd.extend([
                '--prompt', shell_prompt,
            ])
        elif kind == 'stable-lm':
            prompt: str = kwargs['prompt']
            model_id: str = kwargs.get('model_id', 'lmz/candle-stablelm-3b-4e1t')
            cpu: bool = bool(kwargs.get('cpu', False))
            temperature: int = float(kwargs.get('temperature', '0.8'))
            top_p: int = float(kwargs.get('top_p', '0.9'))
            sample_len: int = int(kwargs.get('sample_len', '100'))
            quantized: bool = bool(kwargs.get('quantized', False))
            use_flash_attn: bool = bool(kwargs.get('use_flash_attn', False))

            # shell_prompt
            shell_prompt: str = shlex.quote(prompt)
            
            cmd.extend([
                f'{self.candle_path}/target/release/examples/stable-lm',
            ])

            if cpu:
                cmd.extend([
                    '--cpu',
                ])

            cmd.extend([
                '--model-id', model_id,
                '--temperature', temperature,
                '--top-p', top_p,
                '--sample-len', sample_len,
            ])
            
            if quantized:
                cmd.extend([
                    '--quantized',
                ])
            
            if use_flash_attn:
                cmd.extend([
                    '--use-flash-attn',
                ])

            cmd.extend([
                '--prompt', shell_prompt,
            ])
        elif kind == 'llama':
            prompt: str = kwargs['prompt']
            model_id: str = kwargs.get('model_id')
            cpu: bool = bool(kwargs.get('cpu', False))
            temperature: int = float(kwargs.get('temperature', '0.8'))
            top_p: int = float(kwargs.get('top_p', '0.9'))
            sample_len: int = int(kwargs.get('sample_len', '100'))
            use_flash_attn: bool = bool(kwargs.get('use_flash_attn', False))

            # shell_prompt
            shell_prompt: str = shlex.quote(prompt)

            cmd.extend([
                f'{self.candle_path}/target/release/examples/llama',
            ])

            if cpu:
                cmd.extend([
                    '--cpu',
                ])

            if model_id:
                cmd.extend([
                    '--model-id', model_id
                ])

            cmd.extend([
                '--temperature', temperature,
                '--top-p', top_p,
                '--sample-len', sample_len,
            ])
            
            if use_flash_attn:
                cmd.extend([
                    '--use-flash-attn',
                ])

            cmd.extend([
                '--prompt', shell_prompt,
            ])
        elif kind == 'mistral':
            prompt: str = kwargs['prompt']
            model_id: str = kwargs.get('model_id')
            cpu: bool = bool(kwargs.get('cpu', False))
            temperature: int = float(kwargs.get('temperature', '0.8'))
            top_p: int = float(kwargs.get('top_p', '0.9'))
            sample_len: int = int(kwargs.get('sample_len', '100'))
            quantized: bool = bool(kwargs.get('quantized', False))
            use_flash_attn: bool = bool(kwargs.get('use_flash_attn', False))

            # shell_prompt
            shell_prompt: str = shlex.quote(prompt)

            cmd.extend([
                f'{self.candle_path}/target/release/examples/mistral',
            ])

            if cpu:
                cmd.extend([
                    '--cpu',
                ])

            if model_id:
                cmd.extend([
                    '--model-id', model_id
                ])

            cmd.extend([
                '--temperature', temperature,
                '--top-p', top_p,
                '--sample-len', sample_len,
            ])
            
            if quantized:
                cmd.extend([
                    '--quantized',
                ])

            if use_flash_attn:
                cmd.extend([
                    '--use-flash-attn',
                ])

            cmd.extend([
                '--prompt', shell_prompt,
            ])
        elif kind == 'quantized':
            prompt: str = kwargs['prompt']
            model: str = kwargs['model']
            model_id: str | None = kwargs.get('model_id')
            cpu: bool = bool(kwargs.get('cpu', False))
            temperature: int = float(kwargs.get('temperature', '0.8'))
            top_p: int = float(kwargs.get('top_p', '0.9'))
            sample_len: int = int(kwargs.get('sample_len', '100'))

            # shell_prompt
            shell_prompt: str = shlex.quote(prompt)

            if model_id:
                model_path = try_to_load_from_cache(repo_id=model_id, filename=model)
            else:
                model_path = model

            cmd.extend([
                f'{self.candle_path}/target/release/examples/quantized',
            ])

            if cpu:
                cmd.extend([
                    '--cpu',
                ])

            cmd.extend([
                '--model', model_path,
                '--temperature', temperature,
                '--top-p', top_p,
                '--sample-len', sample_len,
                '--prompt', shell_prompt,
            ])
        else:
            raise ValueError(f'Unsupported kind: {kind}')

        cmd = ' '.join(str(n) for n in cmd)
        return cmd


    def _format_cmd(self, msg: LLMParams):
        engine: str = msg['engine']
        cmd: str

        if engine == 'llama.cpp':
            cmd = self._format_llama_cpp_cmd(**msg)
        elif engine == 'candle':
            cmd = self._format_candle_cmd(**msg)
        else:
            raise ValueError(f'Unknown engine: {engine}')

        return cmd


    async def _run_shell_cmd(self, ws: web.WebSocketResponse | None, msg: LLMParams, cmd: str) -> AsyncIterator[str]:
        prompt: str = msg['prompt']
        stop: str = msg.get('stop', [])
        prompt_enc: bytes = prompt.encode()
        stop_enc = None if stop is None else [n.encode() for n in stop]
        stdout: bytes = b''
        stderr: bytes = b''
        print(f'[DEBUG] _run_shell_cmd {ws} {msg} {cmd}')

        async with self.lock:
            try:
                async with asyncio.timeout(self.timeout):
                    # create new proc for model
                    proc = await asyncio.create_subprocess_shell(
                        cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )

                    # associate ws with proc
                    if ws is not None:
                        self.ws_proc_map[ws] = proc
                    
                    # receive original prompt in stdout
                    # strip original prompt from return
                    prev_buf: bytes
                    buf: bytes

                    while not proc.stdout.at_eof():
                        # stdout
                        buf = await proc.stdout.read(1024)
                        stdout += buf
                    
                        # skip original prompt
                        if len(stdout) > len(prompt_enc):
                            break

                        await asyncio.sleep(0.2)

                    # yield left-overs from stdout as buf
                    stdout = stdout[stdout.index(prompt_enc) + len(prompt_enc):]

                    # read rest of tokens
                    prev_buf = stdout
                    buf = b''
                    text: str = stdout.decode()
                    stopped: bool = False

                    while not proc.stdout.at_eof():
                        buf = await proc.stdout.read(256)
                        prev_buf += buf
                        stdout += buf

                        try:
                            text = prev_buf.decode()
                        except Exception as e:
                            print(f'[ERROR] buf.decode() exception: {e}')
                            continue

                        prev_buf = b''
                        yield text

                        # check for stop words
                        if stop_enc:
                            for n in stop_enc:
                                if n in stdout:
                                    print(f'[INFO] stop word: {stop!r}')
                                    stdout = stdout[:stdout.index(n)]
                                    stopped = True
                                    break

                        if stopped:
                            break

                        await asyncio.sleep(0.2)

                    if stopped:
                        print(f'[INFO] stop word, trying to kill proc: {proc}')

                        try:
                            proc.kill()
                            await proc.wait()
                            print('[INFO] proc kill [stop]')
                        except Exception as e:
                            print(f'[INFO] proc kill [stop]: {e}')
                        finally:
                            proc = None
                    
                    # read stderr at once
                    stderr = await proc.stderr.read()
            except asyncio.TimeoutError as e:
                print(f'[ERROR] timeout, trying to kill proc: {proc}')

                try:
                    proc.kill()
                    await proc.wait()
                    print('[INFO] proc kill [timeout]')
                except Exception as e:
                    print(f'[INFO] proc kill [timeout]: {e}')
                    raise e
                finally:
                    proc = None

            stderr = '...' + stderr.decode()[-1024:]
            print('[DEBUG] stderr:')
            print(stderr)


    def _run_cmd(self, ws: web.WebSocketResponse | None, msg: LLMParams) -> AsyncIterator[str]:
        engine: str = msg['engine']
        kind: str = msg['kind']
        cmd: str = self._format_cmd(msg)
        res: AsyncIterator[str]
        assert engine in ('llama.cpp', 'candle')

        if (engine == 'llama.cpp' and 'model_id' in msg) or (engine == 'candle' and kind == 'quantized' and 'model_id' in msg):
            model_id = msg['model_id']
            model = msg['model']
            
            if model_id:
                # check if model exists
                model_path = try_to_load_from_cache(repo_id=model_id, filename=model)

                if not isinstance(model_path, str):
                    raise ValueError(f'Model missing: {model_path}')
                else:
                    print(f'[INFO] found model: {model_path}')
            else:
                # FIXME: check if model exists
                model_path = model

        res = self._run_shell_cmd(ws, msg, cmd)
        return res


    async def _api_1_0_text_completions(self, ws: web.WebSocketResponse, msg: LLMParams):
        async for chunk in self._run_cmd(ws, msg):
            if DEBUG:
                print(f'chunk: {chunk!r}')

            msg: dict = {'chunk': chunk}
            await ws.send_json(msg)

        await ws.close()


    def _convert_chat_to_text_message(self, msg: LLMParams) -> LLMParams:
        messages: list = msg['messages']
        system_message_text: list[str] = []
        conversation_text: list[str] = []
        prompt: list[str] | str = []

        for m in messages:
            if m['role'] == 'system':
                system_message_text.append(m['content'])
                system_message_text.append('\n')
            elif m['role'] == 'user':
                conversation_text.append('User: ')
                conversation_text.append(m['content'])
                conversation_text.append('\n')
            elif m['role'] == 'assistant':
                conversation_text.append('Assistant: ')
                conversation_text.append(m['content'])
                conversation_text.append('\n')

        prompt.extend(system_message_text)
        prompt.extend(conversation_text)
        prompt = ''.join(prompt)

        chat_msg: dict = {k: v for k, v in msg.items() if k != 'messages'}
        chat_msg['prompt'] = prompt
        return chat_msg


    async def post_api_1_0_text_completions(self, request):
        data: LLMParams = await request.json()
        text: list[str] | str = []

        async for chunk in self._run_cmd(None, data):
            if DEBUG:
                print(f'chunk: {chunk!r}')

            text.append(chunk)

        text = ''.join(text)

        res: dict = {
            'output': text,
        }

        return web.json_response(res)


    async def post_api_1_0_chat_completions(self, request):
        data: LLMParams = await request.json()
        data = self._convert_chat_to_text_message(data)
        text: list[str] | str = []

        async for chunk in self._run_cmd(None, data):
            if DEBUG:
                print(f'chunk: {chunk!r}')

            text.append(chunk)

        text = ''.join(text)

        res: dict = {
            'output': text,
        }

        return web.json_response(res)


    async def get_api_1_0_text_completions(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        print(f'[INFO] websocket openned: {ws}')
        
        try:
            async with asyncio.TaskGroup() as tg:
                async for msg in ws:
                    if msg.type == WSMsgType.PING:
                        await ws.pong(msg.data)
                    elif msg.type == WSMsgType.TEXT:
                        data: LLMParams = json.loads(msg.data)
                        coro = self._api_1_0_text_completions(ws, data)
                        task = tg.create_task(coro)
                    elif msg.type == WSMsgType.ERROR:
                        print(f'[ERROR] websocket closed with exception: {ws.exception()}')
        except ExceptionGroup as e:
            # traceback.print_exc()
            print(f'[ERROR] websocket ExceptionGroup: {e}')
        except Exception as e:
            # traceback.print_exc()
            print(f'[ERROR] TaskGroup Exception: {e}')

        if ws in self.ws_proc_map:
            proc = self.ws_proc_map.pop(ws)
            print(f'[INFO] proc: {proc}')

            try:
                proc.kill()
                await proc.wait()
                print('[INFO] proc kill [TaskGroup]')
            except Exception as e:
                print(f'[WARN] proc kill [TaskGroup]: {e}')
            finally:
                proc = None

        # close ws
        await ws.close()

        print(f'[INFO] websocket closed: {ws}')
        return ws


    async def get_api_1_0_chat_completions(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        print(f'[INFO] websocket openned: {ws}')
        
        try:
            async with asyncio.TaskGroup() as tg:
                async for msg in ws:
                    if msg.type == WSMsgType.PING:
                        await ws.pong(msg.data)
                    elif msg.type == WSMsgType.TEXT:
                        data: LLMParams = json.loads(msg.data)
                        data = self._convert_chat_to_text_message(data)
                        coro = self._api_1_0_text_completions(ws, data)
                        task = tg.create_task(coro)
                    elif msg.type == WSMsgType.ERROR:
                        print(f'[ERROR] websocket closed with exception: {ws.exception()}')
                        break
        except ExceptionGroup as e:
            # traceback.print_exc()
            print(f'[ERROR] websocket ExceptionGroup: {e}')
        except Exception as e:
            # traceback.print_exc()
            print(f'[ERROR] TaskGroup Exception: {e}')

        if ws in self.ws_proc_map:
            proc = self.ws_proc_map.pop(ws)
            print('[INFO] proc: {proc}')

            try:
                proc.kill()
                await proc.wait()
                print('[INFO] proc kill [TaskGroup]')
            except Exception as e:
                print(f'[WARN] proc kill [TaskGroup]: {e}')
            finally:
                proc = None

        # close ws
        await ws.close()

        print(f'[INFO] websocket closed: {ws}')
        return ws


    def get_routes(self):
        return [
            web.post('/api/1.0/text/completions', self.post_api_1_0_text_completions),
            web.post('/api/1.0/chat/completions', self.post_api_1_0_chat_completions),
            web.get('/api/1.0/text/completions', self.get_api_1_0_text_completions),
            web.get('/api/1.0/chat/completions', self.get_api_1_0_chat_completions),
        ]


    def run(self):
        routes = self.get_routes()
        self.app.add_routes(routes)
        web.run_app(self.app, host=self.host, port=self.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='server', description='Python llama.cpp HTTP Server')
    parser.add_argument('--host', help='http server host', default='0.0.0.0')
    parser.add_argument('--port', help='http server port', default=5000, type=float)
    parser.add_argument('--timeout', help='llama.cpp timeout in seconds', default=300.0, type=float)
    parser.add_argument('--candle-path', help='candle directory path', default='~/candle')
    parser.add_argument('--llama-cpp-path', help='llama.cpp directory path', default='~/llama.cpp')
    cli_args = parser.parse_args()

    server = MLIServer(
        host=cli_args.host,
        port=cli_args.port,
        timeout=cli_args.timeout,
        candle_path=os.path.expanduser(cli_args.candle_path),
        llama_cpp_path=os.path.expanduser(cli_args.llama_cpp_path),
    )

    server.run()
