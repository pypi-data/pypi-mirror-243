
import json
import time
import datetime
import re

import tqdm
import pandas as pd

from hashlib import md5
from typing import Iterable
from functools import reduce
from typing import Any
from typing import List

from websocket import create_connection
from termcolor import colored
from .hf_server.cli_utils import R, ModelCard, ModelList, ModelCallResponse,ModelCallRequest,ClearRequest
from .hf_server.cli_utils import MachineInfo


import requests
class SmallModel:
    remote_host_ :str = None
    def __init__(self,name, remote=None):
        if remote is None:
            remote = self.__class__.remote_host_
        assert remote is not None
        self.remote_host  = remote
        self.name = name
        self._ok = False
        self.purpose = "unKnow"
    
    
    def status(self):
        name = self.name
        if "/" in name:
            name = name.rsplit("/",1)[-1]
        for i in self.__class__.show_all_loaded_models():
            if i.id == name:
                return True
        return False
    
    @classmethod
    def from_remote(cls, name,remote=None):
        if remote is None:
            remote = cls.remote_host_
        else:
            cls.remote_host_ = remote
        assert remote is not None
        model = cls(name, remote)
        model.try_load_in_remote()
        return model
    
    @classmethod
    def gpu_info_remote(cls, remote=None) ->MachineInfo:
        if remote is None:
            remote = cls.remote_host_
        else:
            cls.remote_host_ = remote
        assert remote is not None
        url = f"http://{remote}:15001/v1/device/info"
        return MachineInfo.parse_obj(next(R(url, method="get")))
    
    @classmethod
    def clean_all(cls, remote=None):
        if remote is None:
            remote = cls.remote_host_
        else:
            cls.remote_host_ = remote
        assert remote is not None
        all_models = cls.show_all_loaded_models(remote)
        url = f"http://{remote}:15001/v1/models/clear"
        o = ClearRequest(ids=[i.id for i in all_models])
        return next(R(url, object=o))
        
    
    @classmethod
    def show_all_loaded_models(cls, remote=None)->List[ModelCard]:
        if remote is None:
            remote = cls.remote_host_
        else:
            cls.remote_host_ = remote
        assert remote is not None
        url = f"http://{remote}:15001/v1/device/info"
        return MachineInfo.parse_obj(next(R(url, method="get"))).loaded_models.data
        

    @classmethod
    def show_all_models(cls, remote=None) -> List[ModelCard]:
        if remote is None:
            remote = cls.remote_host_
        else:
            cls.remote_host_ = remote
        assert remote is not None
        url = f"http://{remote}:15001/v1/models"
        return ModelList.parse_obj(next(R(url, method="get"))).data
        
    def clean(self):
        try:
            # ws = create_connection(f"ws://{self.remote_host}:15000")
            # user_id = md5(time.asctime().encode()).hexdigest()
            # TODAY = datetime.datetime.now()
            # PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
            # ws.send(json.dumps({"user_id":user_id, "password":PASSWORD}))
            # res = ws.recv()
            # if res != "ok":
            #     print(colored("[info]:","yellow") ,res)
            #     raise Exception("password error")
            # res = self.send_and_recv(json.dumps({"embed_documents":[self.name], "method":"clean"}),ws)
            # return res["embed"]
        
            name = self.name
            if "/" in name:
                name = name.rsplit("/",1)[-1]
            url = f"http://{self.remote_host}:15001//v1/models/clear"
            o = ClearRequest(ids=[name])
            m = MachineInfo.parse_obj(next(R(url, object=o)))
            self._ok = False
            for i in  m.loaded_models.data:
                if i.id == name:
                    self._ok = True
        except Exception as e:
            raise e
        finally:
            pass

    
    # def down_remote(self, try_time=3):
    #     try:
    #         ws = create_connection(f"ws://{self.remote_host}:15000")
    #         user_id = md5(time.asctime().encode()).hexdigest()
    #         TODAY = datetime.datetime.now()
    #         PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
    #         ws.send(json.dumps({"user_id":user_id, "password":PASSWORD}))
    #         res = ws.recv()
    #         if res != "ok":
    #             print(colored("[info]:","yellow") ,res)
    #             raise Exception("password error")
    #         res = self.send_and_recv(json.dumps({"embed_documents":[self.name], "method":"clone"}),ws)
    #         time.sleep(2)
    #         res = self.msg()
    #         if "git clone failed: exit status 128" in res:
    #             print(colored("[Err : ]:","yellow") , colored(res,"red"))
    #             if try_time > 0:
    #                 return self.down_remote(try_time-1)
    #         return res["embed"]
            
    #     except Exception as e:
    #         raise e
    #     finally:
    #         ws.close()

    # @classmethod
    # def send_and_recv(cls, data, ws):
    #     try:
    #         T = len(data)// (1024*102)
    #         bart = tqdm.tqdm(total=T,desc=colored(" + sending data","cyan"))
    #         bart.leave = False
    #         for i in range(0, len(data), 1024*102):
    #             bart.update(1)
    #             ws.send(data[i:i+1024*102])
    #         bart.clear()
    #         bart.close()

    #         ws.send("[STOP]")
    #         message = ""
    #         total = int(ws.recv())
    #         bar = tqdm.tqdm(desc=colored(" + receiving data","cyan", attrs=["bold"]), total=total)
    #         bar.leave = False
    #         while 1:
    #             res = ws.recv()
    #             message += res
    #             bar.update(len(res))
    #             if message.endswith("[STOP]"):
    #                 message = message[:-6]
    #                 break
    #         bar.clear()
    #         bar.close()
    #         msg = json.loads(message)
    #         return msg
    #     except Exception as e:
    #         raise e
    
    # def msg(self):
    #     try:
    #         ws = create_connection(f"ws://{self.remote_host}:15000")
    #         user_id = md5(time.asctime().encode()).hexdigest()
    #         TODAY = datetime.datetime.now()
    #         PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
    #         ws.send(json.dumps({"user_id":user_id, "password":PASSWORD}))
    #         res = ws.recv()
    #         if res != "ok":
    #             print(colored("[info]:","yellow") ,res)
    #             raise Exception("password error")
    #         res = self.send_and_recv(json.dumps({"embed_documents":[self.name], "method":"msg"}),ws)
    #         return res.get("embed","")
    #     except Exception as e:
    #         raise e
    #     finally:
    #         ws.close()
    
    # def change_remote_name(self, new_name):
    #     assert "/" not in new_name
    #     assert " " not in new_name
    #     ss = re.findall(r"[\w\-\_]+",new_name)
    #     assert len(ss) == 1 and ss[0] == new_name
    #     if self.name in self.show_all_models():
    #         try:
    #             ws = create_connection(f"ws://{self.remote_host}:15000")
    #             user_id = md5(time.asctime().encode()).hexdigest()
    #             TODAY = datetime.datetime.now()
    #             PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
    #             ws.send(json.dumps({"user_id":user_id, "password":PASSWORD}))
    #             res = ws.recv()
    #             if res != "ok":
    #                 print(colored("[info]:","yellow") ,res)
    #                 raise Exception("password error")
    #             res = self.send_and_recv(json.dumps({"embed_documents":[self.name, new_name], "method":"change_name"}),ws)
    #             return res["embed"]
    #         except Exception as e:
    #             raise e
    #         finally:
    #             ws.close()
    #     else:
    #         raise Exception("model not exists")

    def check(self):
        self._ok = False
        name = self.name
        if "/" in name:
            name = name.rsplit("/",1)[-1]
        self.try_load_in_remote()
        return self._ok
    
    def try_load_in_remote(self):
        try:
            self._ok = False
            name = self.name
            if "/" in name:
                name = name.rsplit("/",1)[-1]
            url = f"http://{self.remote_host}:15001/v1/models/load"
            
            for i in ModelList.parse_obj(next(R(url, object=ModelCard(id=name)))).data:
                if i.id == name:
                    self._ok = True
                    return True
                
            return False
        except Exception as e:
            raise e
            return False

    # def show_remote_models(self):
    #     try:
    #         name = self.name
    #         if "/" in name:
    #             name = name.rsplit("/",1)[-1]
                
    #         ws = create_connection(f"ws://{self.remote_host}:15000")
    #         user_id = md5(time.asctime().encode()).hexdigest()
    #         TODAY = datetime.datetime.now()
    #         PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
    #         ws.send(json.dumps({"user_id":user_id, "password":PASSWORD}))
    #         res = ws.recv()
    #         if res != "ok":
    #             print(colored("[info]:","yellow") ,res)
    #             raise Exception("password error")
    #         return self.send_and_recv(json.dumps({"embed_documents":[name], "method":"show"}), ws)["embed"]
    #     except Exception as e:
    #         raise e
    #     finally:
    #         ws.close()

    def __call__(self, args: List[str], pandas=False) -> Any:
        if isinstance(args, str):
            args = [args]
        assert isinstance(args, (list, tuple,Iterable,))
        if not self._ok:
            self.check()

        if not self._ok :
            raise Exception("remote's service no such model deployed"+self.name)
        name = self.name
        if "/" in name:
            name = name.rsplit("/",1)[-1]
        url = f"http://{self.remote_host}:15001/v1/models/call"
            
        try:
            o = ModelCallRequest(id=name, messages=args)

            no = 0
            oss = []
            for res in R(url, object=o, use_stream=True):
                ri = ModelCallResponse.parse_obj(res)
                if isinstance(ri.data, List):
                    if  len(ri.data) > 0 and isinstance(ri.data[0], str):
                        oss += ri.data
                    elif isinstance(ri.data[0], dict):
                        for ii in ri.data:
                            ar = args[no]
                            ii["input"] = ar
                            no += 1
                            oss.append(ii)
                    else:
                        oss += ri.data
                    
            if len(oss) > 0 and isinstance(oss[0], dict) and pandas:
                return pd.DataFrame(oss)
            return oss
            
        except Exception as e:
            raise e
            # import ipdb;ipdb.set_trace()
    
    def _merged(self, res_list):
        res = []
        for one_obj in res_list:
            if isinstance(one_obj, list) :
                if len(one_obj) > 1:
                    if isinstance(one_obj[0], dict):
                        res.append({k:reduce(lambda x,y: x+y , map(lambda x: x[k] ,one_obj)) for k in one_obj[0]})
                    else:
                        res.append(one_obj)
                else:
                    res.append(one_obj[0])
            else:
                res.append(one_obj)
        return res




# class SmallModel_v2(SmallModel):

#     def status(self):
#         return super().status()

#     def try_load_in_remote(self):
#         def try_load_in_remote(self):
#         try:
#             self._ok = False
#             name = self.name
#             if "/" in name:
#                 name = name.rsplit("/",1)[-1]
            
            