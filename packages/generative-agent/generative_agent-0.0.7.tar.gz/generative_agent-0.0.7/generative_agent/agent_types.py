import os
import json
from .database_connector import Redis_Connector

class Agent_Type():
    def __init__(self, kind, lang, info, conversation, guard):
        self.kind = kind
        if lang in ["TH", "EN"]:
            self.lang = lang
        else:
            raise ValueError(
                    "lang should be in ['TH', 'EN'] for current."
                )
        for key in ["traits","common_behavior","inappropiates","summary"]:
            try:
                info[key]
            except:
                raise ValueError(f"{key} is not found in info. Please provide it.")
        self.info = info
        self.conversation = conversation
        self.guard = guard

class Agent_Types:
    def __init__(
        self, 
        redis_config={
            "host":"apn1-clear-vervet-33851.upstash.io", 
            "port":33851, 
            "password":"e248949a8af44f07aee8e6e23681862b"
        },
        characters_path=None
        ):
        if redis_config:
            r = Redis_Connector(host=redis_config["host"], port=redis_config["port"], password=redis_config["password"])
            self.__client = r.get_client()
        if characters_path:
            characters = os.listdir(characters_path)
            self.__characters_infomation = dict()
            if len(characters)>0:
                for name in characters:
                    lang, kind = name.split("_")
                    if "template" not in name:
                        self.__characters_infomation.update({
                            name.upper():{
                                "kind": kind.upper(),
                                "lang": lang.upper()
                            }
                        })
                        files = os.listdir(os.path.join(characters_path, name))
                        if ("info.json" in files) and ("conversation.txt" in files) and ("guard.txt" in files):
                            for file in os.listdir(os.path.join(characters_path, name)):
                                with open(os.path.join(characters_path, name, file), 'r') as f:
                                    if file.endswith('.json'):
                                        _ = json.load(f)
                                    else:
                                        _ = f.read()
                                self.__characters_infomation[name.upper()].update({file.split('.')[0]: _})
                        else:
                            raise ValueError(f"There is not complete 3 files in character: {name} (info.json, conversation.txt, guard.txt)")
            else:
                raise ValueError(f"There is no characters in {character_path} folder.")
        else:
            self.__characters_infomation = json.loads(self.__client.get('agent_type'))
    
    def get_all_agent_type(self):
        print(list(self.__characters_infomation.keys()))

    def append_agent_type(self, agent_type:Agent_Type):
        info = agent_type.__dict__
        self.__characters_infomation.update({
            f"{info['lang']}_{info['kind']}":info
        })
        
    def set_agent_type(self, character_type:str):
        for item, value in self.__characters_infomation[character_type].items():
            setattr(self, item, value)

    def save_agent_types(self):
        agent_type_data = json.dumps(self.__characters_infomation)
        self.__client.set('agent_type', value=agent_type_data)

