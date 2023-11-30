import json
import pickle

from .tools import generate_unique_id
from .database_connector import Redis_Connector
from .tools import Vector_Database_Type

class Agent_Memory_Manager:
    def __init__(self, 
                 redis_config={
                    "host":"apn1-clear-vervet-33851.upstash.io", 
                    "port":33851, 
                    "password":"e248949a8af44f07aee8e6e23681862b"}
                ):
        r = Redis_Connector(host=redis_config["host"], port=redis_config["port"], password=redis_config["password"])
        self.client = r.get_client()
        self.__info_format = "generative_agent:{agent_id}:info"
        self.__memory_stream_format = "generative_agent:{agent_id}:memory_stream"
        self.__chat_format = (
            "generative_agent:{agent_id}:chat"
        )

    def load_agent_state_memory(self, agent):
        agent_id = agent.agent_id
        info_key = self.__info_format.format(agent_id=agent_id)
        memory_stream_key = self.__memory_stream_format.format(agent_id=agent_id)
        chat_key = self.__chat_format.format(agent_id=agent_id)

        stored_agent_data = self.client.get(info_key)
        if stored_agent_data:
            agent_data = json.loads(stored_agent_data)

            # Retrieving the memory_stream from Redis
            retrieved_memory_stram = self.client.lrange(memory_stream_key, 0, -1)
            # Deserialize the retrieved list
            memory_stream = [pickle.loads(obj) for obj in retrieved_memory_stram]

            chat_data = pickle.loads(self.client.get(chat_key))

            self.__load_agent_info(
                agent=agent,
                info=agent_data,
                memory_stream=memory_stream,
                chat=chat_data
            )
            agent._check_agent_type()

    def save_agent_state_memory(self, agent):
        # Save custom agent attributes to Datastore
        agent_data = self.__get_agent_info(agent)  # Convert the object to a JSON string
        # agent_data.update(file_urls)
        agent_data = json.dumps(agent_data)
        agent_id = generate_unique_id(original_string=f"{agent.name}")

        info_key = self.__info_format.format(agent_id=agent_id)
        memory_stream_key = self.__memory_stream_format.format(agent_id=agent_id)
        chat_key =self.__chat_format.format(agent_id=agent_id)

        user_id_list= list(agent.chat.keys())
        chat_info = pickle.dumps(agent.chat)
        self.client.set(chat_key, chat_info)

        # Store the JSON string in Redis with key
        self.client.set(info_key, agent_data)
        # Store the List of documents in Redis with key
        self.client.delete(memory_stream_key)
        for memo in [pickle.dumps(item) for item in agent.retriever.memory_stream]:
            self.client.rpush(memory_stream_key, memo)
        

        return {"agent_id": agent_id, "user_id": user_id_list}

    def __get_agent_info(self, agent):
        info = {
            "name": agent.name,
            "age": agent.age,
            "agent_type": pickle.dumps(agent.agent_type).decode("latin-1"),
            "vector_database_type": pickle.dumps(agent.vector_database_type).decode(
                "latin-1"
            ),
            "traits": agent.traits,
            "summary": agent.summary,
            "status": agent.status,
            "feelings": agent.feelings,
            "place": agent.place,
            "plan": json.dumps(
                [
                    {
                        "from": item["from"],
                        "to": item["to"],
                        "task": item["task"],
                    }
                    for item in agent.plan
                ]
            ),
            "inappropiates": agent.inappropiates,
            "chat_memlen": agent.chat_memlen,
            "verbose": agent.verbose,
        }
        return info

    def __load_agent_info(
        self, agent, info, memory_stream, chat
    ):
        agent.name = info["name"]
        agent.age = info["age"]
        agent.agent_type = pickle.loads(info["agent_type"].encode("latin-1"))
        agent.vector_database_type = pickle.loads(
            info["vector_database_type"].encode("latin-1")
        )
        agent.traits = info["traits"]
        agent.summary = info["summary"]
        agent.status = info["status"]
        agent.feelings = info["feelings"]
        agent.place = info["place"]
        agent.plan = [
            {
                "from": item["from"],
                "to": item["to"],
                "task": item["task"],
            }
            for item in json.loads(info["plan"])
        ]
        agent.chat = chat
        agent.inappropiates = info["inappropiates"]
        agent.chat_memlen = info["chat_memlen"]
        agent.verbose = info["verbose"]
        if agent.vector_database_type == Vector_Database_Type.PINECONE:
            agent._create_retriever_and_vectordb(
                environment="gcp-starter",
                api_key="95a72afb-25c7-4aaf-867c-5a5680303df7",
                dimensions=768,
                exist_delete=False,
            )
        else:  # CHROMA
            agent._create_retriever_and_vectordb(
                host="localhost", port="8000", exist_delete=False
            )

        agent.retriever.memory_stream = memory_stream