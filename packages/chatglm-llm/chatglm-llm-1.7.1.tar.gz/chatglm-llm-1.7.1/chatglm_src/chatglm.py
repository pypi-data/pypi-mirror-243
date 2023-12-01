from langchain.llms.base import LLM
from typing import Iterable, List
import re
from typing import List, Dict, Any, Optional, Union
import pathlib
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from .callbacks import AsyncWebsocketHandler, AsyncWebSocksetCallbackManager
import langchain
try:
    from langchain.cache import GPTCache
except:
    pass
import gptcache
from gptcache.processor.pre import get_prompt
from gptcache.manager.factory import get_data_manager
from aiowebsocket.converses import AioWebSocket
from websocket import create_connection
import websockets
from websockets.server import serve
from langchain.embeddings import HuggingFaceEmbeddings
from termcolor import colored
import datetime
from hashlib import md5
import time
import json
import inspect

try:
    
    from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
    from fastchat.serve.inference import load_model
    from fastchat.conversation import get_default_conv_template
    from accelerate import load_checkpoint_and_dispatch
    
    from fastchat.serve.inference import generate_stream
    import torch, gc
    from .hf_server.cli_utils import create_chat_completion, ChatMessage, acreate_chat_completion
    DEFAULT_CACHE_MAP_PATH = str(pathlib.Path.home() / ".cache" / "local_qa_cache_map")
    i = 0

    def init_gptcache_map(cache_obj: gptcache.Cache):
        global i
        cache_path = f'{DEFAULT_CACHE_MAP_PATH}_{i}.txt'
        cache_obj.init(
            pre_embedding_func=get_prompt,
            data_manager=get_data_manager(data_path=cache_path),
        )
        i += 1
    
    langchain.llm_cache = GPTCache(init_gptcache_map)
    # print(colored("init gptcache", "green"))
except Exception as e:
    # raise e
    print("use remote ignore this / load transformers failed, please install transformers and accelerate first and torch.")

def is_async_method(method):
    return inspect.iscoroutinefunction(method)

def load_model_on_gpus_old(checkpoint_path, num_gpus: int = 2,device_map = None, **kwargs):
    if num_gpus < 2 and device_map is None:
        model = AutoModel.from_pretrained(checkpoint_path, trust_remote_code=True, **kwargs).half().cuda()
    else:
        from accelerate import dispatch_model
        model = AutoModel.from_pretrained(checkpoint_path, trust_remote_code=True, **kwargs).half()
        if device_map is None:
            device_map = auto_configure_device_map(num_gpus)
        model = dispatch_model(model, device_map=device_map)

    return model
def auto_configure_device_map(num_gpus: int) -> Dict[str, int]:
    # transformer.word_embeddings 占用1层
    # transformer.final_layernorm 和 lm_head 占用1层
    # transformer.layers 占用 28 层
    # 总共30层分配到num_gpus张卡上
    num_trans_layers = 28
    per_gpu_layers = 30 / num_gpus

    # bugfix: 在linux中调用torch.embedding传入的weight,input不在同一device上,导致RuntimeError
    # windows下 model.device 会被设置成 transformer.word_embeddings.device
    # linux下 model.device 会被设置成 lm_head.device
    # 在调用chat或者stream_chat时,input_ids会被放到model.device上
    # 如果transformer.word_embeddings.device和model.device不同,则会导致RuntimeError
    # 因此这里将transformer.word_embeddings,transformer.final_layernorm,lm_head都放到第一张卡上
    device_map = {'transformer.word_embeddings': 0,
                  'transformer.final_layernorm': 0, 'lm_head': 0}

    used = 2
    gpu_target = 0
    for i in range(num_trans_layers):
        if used >= per_gpu_layers:
            gpu_target += 1
            used = 0
        assert gpu_target < num_gpus
        device_map[f'transformer.layers.{i}'] = gpu_target
        used += 1

    return device_map

def enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


def auto_gc():
    if torch.cuda.is_available():
        # for all cuda device:
        for i in range(0,torch.cuda.device_count()):
            CUDA_DEVICE = f"cuda:{i}"
            with torch.cuda.device(CUDA_DEVICE):
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
    else:
        gc.collect()

class ChatGLMLLM(LLM):
    """
            Load a model from local or remote
        if want to use stream mode:
            'streaming=True'
        if want to use langchain's Callback:
            examples: 'callbacks=[StreamingStdOutCallbackHandler(), AsyncWebsocketHandler()]'

        if want use cpu: # default will try to use gpu
            'cpu=True'
        
        if want to use remote's model:
            'remote_host="xx.xxx.xx.xx"'  , if set this , will auto call by ws://xx.xxx.xxx.xx:15000"
            optional:
                remote_callback: a callback function, will call when receive a new token like  'callback(new_token, history, response)'
                if not set, will print to stdout

    """
    max_tokens: int = 10000
    temperature: float = 0.01
    top_p = 0.9
    history = []
    history_id = "default"
    tokenizer: Any = None
    model: Any = None
    history_len: int = 10
    model: Any = None
    tokenizer: Any = None
    model_path: str = pathlib.Path.home() / ".cache" / "chatglm"
    cpu: bool = False
    streaming: bool = False
    verbose: bool = False
    callbacks :Any  = [StreamingStdOutCallbackHandler(), AsyncWebsocketHandler()]
    # callback_manager:  Any = BaseCallbackManager
    remote_host: Any = None

    def set_history(self, hist:List[str]):
        self.history = hist
    
    
    @property
    def _llm_type(self) -> str:
        return "ChatGLM"

    async def _acall(self, prompt: str, stop: List[str] = None):
        
        if self.remote_host is not None :
            uri = f"http://{self.remote_host}:15001/v1/chat/completions"
            result = ''
            msgs = [
                ChatMessage(role="system", content="You are ChatGLM3, a helpful assistant. Follow the user's instructions carefully. Respond using markdown.")
            ]
            for h in self.history:
                p,r = h
                msgs.append(ChatMessage(role="user", content=p.strip()))
                msgs.append(ChatMessage(role="assistant", content=r.strip()))
            msgs.append(ChatMessage(role="user", content=prompt))
            for call in self.callbacks:
                if is_async_method(call.on_llm_start):
                    await call.on_llm_start(prompt, None, verbose=self.verbose)
            result = ""
            ss = ""
            async for r in acreate_chat_completion(uri, msgs, temperature=self.temperature, max_tokens=self.max_tokens, top_p=self.top_p):
                for choice in r.choices:
                    if choice.delta.content is not None:
                        msg = {}
                        # yield choice.delta
                        msg["new"] = choice.delta.content
                        ss += choice.delta.content
                        msg["response"] = ss
                        msg["verbose"] = self.verbose
                        result = ss
                        for call in self.callbacks:
                            if is_async_method(call.on_llm_new_token):
                                data = {"response": ss, "history": self.history,"query": prompt}
                                await call.on_llm_new_token(data, verbose=self.verbose, **data)

            self.history = self.history+[[prompt, result]]
            for call in self.callbacks:
                if is_async_method(call.on_llm_start):
                    await call.on_llm_end(result, verbose=self.verbose)
            return result


    def stream(self,prompt: str, stop: List[str] = None):
        uri = f"http://{self.remote_host}:15001/v1/chat/completions"
        result = ''
        msgs = [
            ChatMessage(role="system", content="You are ChatGLM3, a helpful assistant. Follow the user's instructions carefully. Respond using markdown.")
        ]
        for h in self.history:
            p,r = h
            msgs.append(ChatMessage(role="user", content=p.strip()))
            msgs.append(ChatMessage(role="assistant", content=r.strip()))
        msgs.append(ChatMessage(role="user", content=prompt))

        gen = create_chat_completion(uri, msgs, temperature=self.temperature, max_tokens=self.max_tokens, top_p=self.top_p)
        ss = ""
        for r in gen:
            
            for choice in r.choices:
                if choice.delta.content is not None:
                    msg = {}
                    # yield choice.delta
                    msg["new"] = choice.delta.content
                    ss += choice.delta.content
                    msg["response"] = ss
                    msg["verbose"] = self.verbose
                    result = ss
                    yield msg

        self.history = self.history+[[prompt, result]]


    
    def _call(self, prompt: str, stop: List[str]  = None,run_manager: Any = None) -> str:
        
        if self.remote_host is not None :
            uri = f"http://{self.remote_host}:15001/v1/chat/completions"
            result = ''
            msgs = [
                ChatMessage(role="system", content="You are ChatGLM3, a helpful assistant. Follow the user's instructions carefully. Respond using markdown.")
            ]
            for h in self.history:
                p,r = h
                msgs.append(ChatMessage(role="user", content=p.strip()))
                msgs.append(ChatMessage(role="assistant", content=r.strip()))
            msgs.append(ChatMessage(role="user", content=prompt))

            gen = create_chat_completion(uri, msgs, temperature=self.temperature, max_tokens=self.max_tokens, top_p=self.top_p)
            ss = ""
            for callback in self.callbacks:
                if is_async_method(callback.on_llm_start):continue
                callback.on_llm_start(
                    None,
                    prompt,
                    run_id=0,
                    verbose=self.verbose
                )

            for r in gen:
                
                for choice in r.choices:
                    if choice.delta.content is not None:
                        msg = {}
                        # yield choice.delta
                        msg["new"] = choice.delta.content
                        new_token = choice.delta.content
                        ss += choice.delta.content
                        msg["response"] = ss
                        msg["verbose"] = self.verbose
                        result = ss
                        for callback in self.callbacks:
                            if is_async_method(callback.on_llm_start):continue
                            callback.on_llm_new_token(
                                new_token,
                                **msg
                            )
                        result = ss
            
            
            
            for callback in self.callbacks:
                if is_async_method(callback.on_llm_start):continue
                callback.on_llm_end(result, verbose=self.verbose)
            self.history = self.history+[[prompt, result]]
            return result
