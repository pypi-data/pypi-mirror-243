import pathlib
from typing import Any
from termcolor import colored
import datetime

from .qwen import VllmBase
from langchain.llms.base import LLM
from hashlib import md5
from aiowebsocket.converses import AioWebSocket
from websocket import create_connection
import websockets
from websockets.server import serve
import time
import asyncio
import json
import numpy as np

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.generation.utils import GenerationConfig
except Exception as e:
    pass



def load_model_on_gpus_old(checkpoint_path, num_gpus: int = 2,device_map = "auto"):
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_path, use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(checkpoint_path, device_map=device_map, num_gpus=num_gpus, torch_dtype=torch.bfloat16, trust_remote_code=True)
    model.generation_config = GenerationConfig.from_pretrained(checkpoint_path)


    return model,tokenizer

class Baichuan2LLM(LLM):
    max_token: int = 4096
    temperature: float = 0.01
    top_p = 0.9
    history = []
    history_id = "default"
    tokenizer: Any = None
    model: Any = None
    history_len: int = 10
    model: Any = None
    tokenizer: Any = None
    cpu: bool = False
    streaming: bool = False
    verbose: bool = False
    callbacks :Any  = []
    # callback_manager:  Any = BaseCallbackManager
    remote_host: Any = None
    tokenizer: Any = None
    model: Any = None
    history_len: int = 10
    model: Any = None
    tokenizer: Any = None
    model_path: str = pathlib.Path.home() / ".cache" / "baichuan2"
    streaming: bool = False
    remote_host: str = None
    
    @classmethod
    def load(cls, *args,model_path=None, **kargs):
        mo = cls(*args, **kargs)
        if model_path is not None:
            mo.model_path = pathlib.Path(model_path)
        
        if mo.model_path.exists() and mo.remote_host is None:
            if torch.cuda.device_count() > 0:
                print(colored("[GPU]","green"),":",torch.cuda.device_count(), "GPUs" )
                # use baichuan2
                try:
                    mo.model, mo.tokenizer = load_model_on_gpus_old(mo.model_path, num_gpus=torch.cuda.device_count())

                except Exception as e:
                    print(colored("[GPU]","yellow"),": failed !! but try load use new way " + str(e),torch.cuda.device_count(), "GPUs" )
        else:
            pass
        return mo        

    def make_args(self, parameter):
        # parameter["stop"] = ['<|im_end|>','<|endoftext|>']
        # parameter["stop"] = '<|im_end>'
        return parameter

    def make_context(self, prompt, history=[],system="You are a assistant."):
        def _token(role, content):
            return f"{role}:\n{content}"

        raw_text = _token("system", system) + "\n"
        for q, h in history:
            raw_text += _token("user", q)
            raw_text += "\n"+_token("assistant", h) +"\n"
        return raw_text + _token("user", prompt) + "\n" + self.start_token + "assistant\n"

    def parse_output(self, output):
        return output
    
    async def asend_to_remote(self, data, ws):
        """
        every chunk of data is 2M
        """
        for i in range(0, len(data), 1024*1024*2):
            await ws.send(data[i:i+1024*1024*2])
        await ws.send("[STOP]")
    
    async def aclient_send(self, prompt):
        
        uri = f"ws://{self.remote_host}:15000"
        result = ''
        TODAY = datetime.datetime.now()
        PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
        # self.callback_manager =  BaseCallbackManager(self.callbacks)
        # self.callback_manager.set_handlers(self.callbacks)
        async with AioWebSocket(uri) as aws:
            converse = aws.manipulator
            
            user_id = md5(time.asctime().encode()).hexdigest()
            await converse.send(json.dumps({"user_id":user_id, "password":PASSWORD}).encode())
            res = await converse.receive()
            res = res.decode()
            if res != "ok":
                raise Exception("password error:"+res)
            data = json.dumps({"prompt":prompt, "history":self.history,"model":"chatglm","temperature":self.temperature}).encode()
            await self.asend_to_remote(data, converse)

            # for call in self.callbacks:
            #     if is_async_method(call.on_llm_start):
            #         await call.on_llm_start(prompt, None, verbose=self.verbose)
            while 1:
                res = await converse.receive()
                msg = json.loads(res.decode())
                # { "new":delta,"response": response, "history": history,"query": prompt}
                if "stop" in msg:
                    break
                new_token = msg["new"]
                response = msg["response"]
                msg["verbose"] = self.verbose
                # for call in self.callbacks:
                #     if is_async_method(call.on_llm_start):
                #         await call.on_llm_new_token(new_token, **msg)
                yield msg
                result = response
        self.history = self.history+[[prompt, result]]
        # for call in self.callbacks:
        #     if is_async_method(call.on_llm_start):
        #         await call.on_llm_end(result, verbose=self.verbose)
        # return result

            

    
    def client_send(self, prompt):
        TODAY = datetime.datetime.now()
        PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
        assert self.remote_host is not None
        uri = f"ws://{self.remote_host}:15000"
        result = ''
        # self.callback_manager =  BaseCallbackManager(self.callbacks)
        # self.callback_manager.set_handlers(self.callbacks)
        
        ws = create_connection(f"ws://{self.remote_host}:15000")
        user_id = md5(time.asctime().encode()).hexdigest()
        # self.callback_manager =  langchain.callbacks.base.BaseCallbackManager(self.callbacks)
        
        # self.callback_manager =  BaseCallbackManager(self.callbacks)
        # self.callback_manager.set_handlers(self.callbacks)
        ws.send(json.dumps({"user_id":user_id, "password":PASSWORD}))
        # time.sleep(0.5)
        res = ws.recv()
        if res != "ok":
            print(colored("[info]:","yellow") ,res)
            raise Exception("password error")
        result = ''
            
            
        data = json.dumps({"prompt":prompt, "history":self.history,"model":"baichuan2-7b", "temperature": self.temperature})
        self.send_to_remote(data, ws)
        while 1:
            res = ws.recv()
            try:
                msg = json.loads(res)
            except Exception as e:
                print(colored("[info]:","yellow") ,res)
                continue
            # { "new":delta,"response": response, "history": history,"query": prompt}
            if "stop" in msg:
                break
            # new_token = msg["new"]
            # response = msg["response"]
            # history = msg["history"]
            msg["verbose"] = self.verbose
            result = msg
            yield msg
            
            # for call in self.callbacks:
            #     if is_async_method(call.on_llm_start):
                    # await call.on_llm_end(result, verbose=self.verbose)
        self.history = self.history+[[prompt, result]]
        # yield result
    

    def send_to_remote(self,data,ws):
        """
        every chunk of data is 2M
        """
        for i in range(0, len(data), 1024*1024*2):
            ws.send(data[i:i+1024*1024*2])
        ws.send("[STOP]")

    @property
    def _llm_type(self) -> str:
        return "baichuan2-7b"

    def _call(self, prompt):
        for data in self.stream(prompt):
            delta = data["new"]
            self.callback_manager.on_llm_new_token(
                    delta, verbose=self.verbose, **data
                )
        return data["response"]
    
    async def _acall(self, prompt):
        async for data in self.aclient_send(prompt):
            delta = data["new"]
            self.callback_manager.on_llm_new_token(
                delta, verbose=self.verbose, **data
            )
        return data["response"]
    
    def stream(self, prompt):
        if self.remote_host is not None:
            for result in self.client_send(prompt):
                yield result
            
        else:
            position = 0
            messages = []
            for u,h in self.history:
                messages.append({"role":"user", "content":u})
                messages.append({"role":"assistant", "content":h})
            messages.append({"role":"user", "content":prompt})
                
            for response in self.model.chat(self.tokenizer, messages, stream=True):
                delta = response[position:]
                position = len(response)
                data = {"new": delta, "response": response, "history": self.history, "query": prompt}
                if torch.backends.mps.is_available():
                    torch.mps.empty_cache()
                yield data
            self.history.append((prompt, response))