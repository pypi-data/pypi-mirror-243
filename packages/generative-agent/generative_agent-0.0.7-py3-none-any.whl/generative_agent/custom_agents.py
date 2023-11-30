import math
import json
import time
import threading
import importlib
import concurrent.futures
from datetime import timedelta
import pinecone
import chromadb
from chromadb.config import Settings
from collections import defaultdict

from .tools import (
    datetime,
    text_from_inapp_list,
    get_thai_datetime,
    text_chat_hist,
    get_text_from_docs,
    Mem_Type,
    Vector_Database_Type,
    RateLimiter,
    generate_unique_id
)

from .agent_types import Agent_Types, Agent_Type
from .time_weighted_retriever import TimeWeightedVectorStoreRetrieverModified

from langchain.llms import VertexAI, OpenAI
from langchain.chains import LLMChain
from langchain.schema import Document
from langchain.vectorstores import Pinecone, Chroma
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


def relevance_score_fn(score: float) -> float:
    """Return a similarity score on a scale [0, 1]."""
    # This will differ depending on a few things:
    # - the distance / similarity metric used by the VectorStore
    # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
    # This function converts the euclidean norm of normalized embeddings
    # (0 is most similar, sqrt(2) most dissimilar)
    # to a similarity function (0 to 1)
    return 1.0 - score / math.sqrt(2)


def use_textllm_with_prompt(textllm, prompt_template, inps, verbose):
    prompt = PromptTemplate(
        input_variables=prompt_template["input_variables"],
        template=prompt_template["prompt_template"],
    )
    chain = LLMChain(llm=textllm, prompt=prompt, verbose=verbose)
    return chain(inputs=inps)["text"]


def use_chatllm_with_prompt(chatllm, prompt_template, inps, verbose):
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                template=prompt_template["system"]["prompt_template"],
                input_variables=prompt_template["system"]["input_variables"],
            ),
            HumanMessagePromptTemplate.from_template(
                template=prompt_template["user"]["prompt_template"],
                input_variables=prompt_template["user"]["input_variables"],
            ),
        ]
    )
    chain = LLMChain(llm=chatllm, prompt=chat_prompt, verbose=verbose)
    return chain(inputs=inps)["text"]


class custom_agent:
    def __init__(
        self,
        textllm,
        chatllm,
        embeddings_model,
        name: str = None,
        age=None,
        agent_type: Agent_Types = None,
        traits: str = None,
        summary: str = None,
        inappropiates=None,
        chat_memlen: int = 100,
        load_memory=False,
        agent_id=None,
        vector_database_type=Vector_Database_Type.CHROMA,
        routine_process_time=300,
        verbose=False,
    ):
        self.textllm = textllm
        self.chatllm = chatllm
        self.embeddings_model = embeddings_model
        self.dimension = 768 if isinstance(textllm, VertexAI) else 1536

        self.name = name if name else ""
        self.age = age if age else 0
        self.agent_type = agent_type
        self.traits = traits if traits else ""
        self.summary = summary if summary else ""
        self.inappropiates = (
            text_from_inapp_list(inappropiates) if inappropiates else []
        )

        self.status = ""
        self.feelings = ""
        self.place = ""
        self.plan = []
        self.chat = defaultdict(dict)

        self.chat_memlen = chat_memlen
        self.verbose = verbose
        self.start_interview = False
        self.load_memory = load_memory
        self.agent_id = agent_id
        self.vector_database_type = vector_database_type
        self.routine_process_time = routine_process_time
        if self.load_memory:
            if self.agent_id == None:
                raise ValueError(
                    "If you set load_memory=True, you need to include agent_id too!"
                )

        # limiter for GCP VertexAI Quota limit -> It is around 60 Requests per minute:RPM
        self.rate_limiter = RateLimiter(rate_limit=30, time_window=timedelta(minutes=1))

        if agent_type:
            # Check what type of agent, so we can import prompt and chat examples.
            self._check_agent_type()
            if load_memory == False:
                if self.verbose:
                    print("Create new memory")
                if self.vector_database_type == Vector_Database_Type.PINECONE:
                    self._create_retriever_and_vectordb(
                        environment="gcp-starter",
                        api_key="95a72afb-25c7-4aaf-867c-5a5680303df7",
                        dimensions=self.dimension,
                        exist_delete=True,
                    )
                else:  # CHROMA
                    self._create_retriever_and_vectordb(
                        host="localhost", port="8000", exist_delete=True
                    )
                self.add_character(self.summary.split("\n"))

            # Multithread process agent self summarization
            # set routine function
            self.__start_routine_func(self._update_summary, self.routine_process_time)
            self.__start_routine_func(self._update_status, self.routine_process_time)
            self.__start_routine_func(self._update_place, self.routine_process_time)

        if self.verbose:
            print("Finish create Generative Agent: {}".format(self.name))

    def __str__(self):
        return f"""name: {self.name}
age: {self.age}
traits: {self.traits}
summary: {self.summary}
status: {self.status}
feeling: {self.feelings}
at place: {self.place}
plan: {self.plan}
inapp_topics: {self.inappropiates}
chat: {self.chat}"""

    def __get_chat_info(self, user_id):
        chat = self.chat[user_id]
        try:
            chat_history = chat['chat_history']
        except:
            chat['chat_history'] = []
            chat_history = chat['chat_history']
        
        try:
            chat_summary = chat['chat_summary']
        except:
            chat['chat_summary'] = ''
            chat_summary = chat['chat_summary']
        
        return chat_history, chat_summary


    def _create_retriever_and_vectordb(
        self,
        exist_delete: bool = False,
        score_weight: dict = dict({"time": 0.3, "importance": 0.1}),
        **kwargs,
    ):
        """
        A function use for create vectorstore for generative agents to store behavior & knowledge memory

        Keyword Arguments:
        vector_type (vector_database): Type of vector database (vector_database.PINECONE, vector_database.CHROMA).
        name (str): Name of agent
        embeddings_model
        exist_delete (boolean): True = delete existing, False = not delete
        if vector_database.PINECONE:
            embedding_size (int)
            environment (str)
            api_key (str)
        """
        agent_name = generate_unique_id(self.name.lower())
        index_collection_name = f"{agent_name}-vector-db"
        if self.vector_database_type == Vector_Database_Type.PINECONE:
            # Initialize the vectorstore as empty
            try:
                embedding_size = kwargs["dimensions"]  # 768 # 1536
                env = kwargs["environment"]  # "gcp-starter"
                api = kwargs["api_key"]  # "95a72afb-25c7-4aaf-867c-5a5680303df7"
            except KeyError as e:
                raise KeyError(
                    f"Needed Parameter not found: {e} is not available in the function parameter."
                )
                # print("Invalid input. Cannot convert to an integer.")
            pinecone.init(
                api_key=api,  # find at app.pinecone.io
                environment=env,  # next to api key in console
            )
            existing_indexs = pinecone.list_indexes()
            if len(existing_indexs) == 1:
                existing_index = existing_indexs[0]
                index_agent_name = existing_index.split("-")
                if exist_delete:
                    pinecone.delete_index(name=existing_index)
                    pinecone.create_index(
                        name=index_collection_name,
                        metric="cosine",
                        dimension=embedding_size,
                    )
                    index = pinecone.Index(index_name=index_collection_name)
                else:
                    if index_agent_name[0] == agent_name:
                        index = pinecone.Index(index_name=index_collection_name)
                    else:
                        pinecone.delete_index(name=existing_index)
                        pinecone.create_index(
                            name=index_collection_name,
                            metric="cosine",
                            dimension=embedding_size,
                        )
                        index = pinecone.Index(index_name=index_collection_name)
            else:
                pinecone.create_index(
                    name=index_collection_name,
                    metric="cosine",
                    dimension=embedding_size,
                )
                index = pinecone.Index(index_name=index_collection_name)
            self.vectorstore = Pinecone(
                embedding=self.embeddings_model, index=index, text_key="text"
            )

        elif self.vector_database_type == Vector_Database_Type.CHROMA:
            try:
                host = kwargs["host"]
                port = kwargs["port"]
            except KeyError as e:
                raise KeyError(
                    f"Needed Parameter not found: {e} is not available in the function parameter."
                )
            client = chromadb.HttpClient(
                host=host, port=port, settings=Settings(allow_reset=True)
            )
            # client.reset()  # resets the database
            if index_collection_name in [col.name for col in client.list_collections()]:
                if exist_delete:
                    client.delete_collection(index_collection_name)
            elif index_collection_name not in [
                col.name for col in client.list_collections()
            ]:
                _ = client.create_collection(index_collection_name)

            self.vectorstore = Chroma(
                client=client,
                collection_name=index_collection_name,
                embedding_function=self.embeddings_model,
            )

        self.retriever = TimeWeightedVectorStoreRetrieverModified(
            vectorstore=self.vectorstore,
            score_weight=score_weight,
            vector_database_type=self.vector_database_type,
            other_score_keys=["importance"],
            k=5,
        )

    def _check_agent_type(self):
        self.lang = self.agent_type.lang
        self.kind = self.agent_type.kind
        module_name = f"generative_agent.conversation_examples"
        try:
            self.chat_examples = self.agent_type.conversation
            self.guard_examples = self.agent_type.guard
            # imported_module = importlib.import_module(module_name)
            # print(imported_module)
            # self.chat_examples = getattr(
            #     imported_module, f"{self.lang}_{self.kind}_CONV_EX"
            # )
            # self.guard_examples = getattr(
            #     imported_module, f"{self.lang}_{self.kind}_GUARD_EX"
            # )
        except ModuleNotFoundError:
            print(
                f"{self.lang}_{self.kind}_CONV_EX or {self.lang}_{self.kind}_GUARD_EX is not implemented."
            )

        module_name = f"generative_agent.prompt.{self.lang.lower()}_prompt"
        try:
            self.prompt = importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(f"{self.lang.lower()}_prompt is not implemented.")

    def __start_routine_func(self, func, timesleep):
        t = threading.Thread(
            target=self.__call_loop, kwargs={"func": func, "timesleep": timesleep}
        )
        t.start()

    def __call_loop(self, func, timesleep):
        while True:
            func()
            time.sleep(timesleep)

    def add_character(self, list_of_character):
        threads = []
        if isinstance(list_of_character, str):
            list_of_character = [list_of_character]
        for character in list_of_character:
            t = threading.Thread(
                target=self.__add_memory_with_rate_limiting,
                args=(character, Mem_Type.BEHAVIOR.value),
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def add_knowledge(self, list_of_knowledge):
        threads = []
        if isinstance(list_of_knowledge, str):
            list_of_knowledge = [list_of_knowledge]
        for knowledge in list_of_knowledge:
            t = threading.Thread(
                target=self.__add_memory_with_rate_limiting,
                args=(knowledge, Mem_Type.KNOWLEDGE.value),
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    # Modify the add_memory function to include rate limiting
    def __add_memory_with_rate_limiting(self, mem_info, mem_type):
        if self.verbose:
            print("adding memory...")

        mem_time = datetime.now().isoformat()
        inps = {"mem": mem_info}
        rate = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_ADDMEM,
            inps=inps,
            verbose=self.verbose,
        )
        if len(rate) > 2:
            rate = 1
        rate_score = int(rate) / 10
        request = {
            "function": self.retriever.add_documents,
            "kwargs": {
                "documents": [
                    Document(
                        page_content=mem_info,
                        metadata={
                            "importance": rate_score,
                            "memory_type": mem_type,
                            "created_at": mem_time,
                        },
                    )
                ],
                "current_time": mem_time,
            },
        }  # Modified argument passing using kwargs

        self.rate_limiter.add_to_queue(request)

    def _update_summary(self):
        if self.verbose:
            print("update summary...")
        core_character = ""
        feeling = ""
        if len(self.retriever.memory_stream) != 0:
            core_character = self.__get_core_character()
            feeling = self.__get_feeling()
        description = core_character + " " + feeling
        if self.lang == "TH":
            self.summary = (
                f"ชื่อ: {self.name} (อายุ: {self.age})"
                + f"\nอุปนิสัย: {self.traits}"
                + f"\nสรุปลักษณะของ{self.name}: {description}"
            )
        else:
            self.summary = (
                f"Name: {self.name} (Age: {self.age})"
                + f"\Traits: {self.traits}"
                + f"\n{self.name}'s characteristics summary: {description}"
            )

    def _update_status(self):
        if self.verbose:
            print("update status...")
        now = datetime.now().isoformat()
        for each_plan in self.plan:
            if now >= each_plan["from"] and now <= each_plan["to"]:
                self.status = each_plan["task"]
                return
        self.__get_plan()
        recently_task = self.plan[0]
        self.status = recently_task["task"]

    def _update_place(self, timesleep=None):
        if self.verbose:
            print("update place...")
        inps = {"name": self.name, "place": self.status}
        self.place = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_PLACE,
            inps=inps,
            verbose=self.verbose,
        )

    def _update_chat_hist(self):
        if self.verbose:
            print("Chat summarizing...")
        
        for item in self.chat:
            chat=self.chat[item]
            chat_history = chat['chat_history']
            chat_summary = chat['chat_summary']
        
            if (chat_summary == "" and len(chat_history) > 0) or len(
                chat_history
            ) >= self.chat_memlen:
                inps = {"chat_history": text_chat_hist(chat_history)}
                incoming_chatsum = use_textllm_with_prompt(
                    textllm=self.textllm,
                    prompt_template=self.prompt.PROMPT_CHATSUM,
                    inps=inps,
                    verbose=self.verbose,
                )
                inps = {"chatsum": chat_summary + incoming_chatsum}
                chat_summary = use_textllm_with_prompt(
                    textllm=self.textllm,
                    prompt_template=self.prompt.PROMPT_SUMHIST,
                    inps=inps,
                    verbose=self.verbose,
                )
                chat_history = []
                if self.verbose:
                    print("Chat summarized")
            if (
                self.verbose
                and chat_summary == ""
                and len(chat_history) == 0
            ):
                print("sleep first because no chat history")

    def __get_core_character(self):
        # CORE Character
        if self.verbose:
            print("get core characteristic...")
        query = (
            "ลักษณะสำคัญของ" + self.name + "คืออะไร"
            if self.lang == "TH"
            else "What is a core characteristic of " + self.name
        )
        print(query)
        docs = self.retriever.get_relevant_documents(
            query,
            current_time=datetime.now().isoformat(),
            mem_type=Mem_Type.BEHAVIOR.value,
        )
        result = get_text_from_docs(docs)
        inps = {"name": self.name, "statements": result}
        core_charac = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_CORE,
            inps=inps,
            verbose=self.verbose,
        )
        return core_charac

    def __get_feeling(self):
        if self.verbose:
            print("get feeling...")
        query = (
            "ความรู้สึกเกี่ยวกับความก้าวหน้าในชีวิตล่าสุดของ" + self.name
            if self.lang == "TH"
            else "Feelings about recent progress in life of" + self.name
        )
        docs = self.retriever.get_relevant_documents(
            query,
            current_time=datetime.now(),
            mem_type=Mem_Type.BEHAVIOR.value,
        )
        statement = get_text_from_docs(docs)
        inps = {"name": self.name, "statements": statement}
        feel = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_FEELING,
            inps=inps,
            verbose=self.verbose,
        )
        return feel

    def __get_plan(self):
        inps = {
            "name": self.name,
            "datetime": get_thai_datetime(),
            "current_time": datetime.now().strftime("%H:%M"),
            "place": self.place,
            "summary": self.summary,
        }
        plan = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_PLAN,
            inps=inps,
            verbose=self.verbose,
        )
        plan = plan.split("\n")
        # clean
        plan = [p.lstrip().rstrip().replace("24", "00") for p in plan]
        for p in plan:
            if (
                not ("ตั้งแต่" in p or "From" in p)
                or not ("ถึง" in p or "to" in p)
                or not (":" in p)
                or (len(p.split(" ")) < 5)
            ):
                plan.remove(p)
        if self.verbose:
            print(plan)
        plan_list = []
        for task in plan:
            tmp = {}
            split_temp = task.split(" ")
            split_temp[0] = split_temp[0][1:]
            split_temp[3] = split_temp[3][:-2]

            today_date = datetime.today().date()

            from_time = datetime.strptime(split_temp[1], "%H:%M").time()
            from_datetime = datetime.combine(today_date, from_time)

            to_time = datetime.strptime(split_temp[3], "%H:%M").time()
            to_datetime = datetime.combine(today_date, to_time)

            tmp["from"] = from_datetime.isoformat()
            tmp["to"] = to_datetime.isoformat()
            tmp["task"] = split_temp[-1]
            plan_list.append(tmp)
        self.plan = plan_list

    def interview(self, user, query):
        docs = self.retriever.get_relevant_documents(
            query=query,
            current_time=datetime.now().isoformat(),
            mem_type=Mem_Type.KNOWLEDGE.value,
        )
        context = get_text_from_docs(docs)
        if not (self.start_interview):
            # start thread for updating chat summary every 5 minutes
            self.__start_routine_func(self._update_chat_hist, self.routine_process_time)
            self.start_interview = True

        chat_history, chat_summary = self.__get_chat_info(user_id=generate_unique_id(original_string=user))
        
        inps = {
            "current_time": get_thai_datetime(),
            "name": self.name,
            "status": self.status,
            "place": self.place,
            "summary": self.summary,
            "context": context,
            "exam_conversation": self.chat_examples.format(
                Player=user, Character=self.name
            ),
            "chatsum": chat_summary,
            "chat_history": chat_history,
            "user": user,
            "question": query,
        }
        
        chat_history.append("{}: {}".format(user, query))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the functions with input parameters for concurrent execution
            guard = executor.submit(self.__guarding, question=query, chat_summary=chat_summary)
            interview = executor.submit(
                use_chatllm_with_prompt,
                chatllm=self.chatllm,
                prompt_template=self.prompt.PROMPT_INTERVIEW,
                inps=inps,
                verbose=self.verbose,
            )

            # Retrieve the return values from the futures
        guard_resp = guard.result()
        int_resp = interview.result()
        if self.verbose:
            print("Guard response: {}".format(guard_resp))
            print("Interview response: {}".format(int_resp))
        if guard_resp["related"]:
            guard_resp["emotion"] = "Neutral"
            chat_history.append("{}: {}".format(self.name, guard_resp["response"]))
            return guard_resp
        chat_history.append("{}: {}".format(self.name, int_resp))
        return json.loads(int_resp, strict=False)

    def __guarding(self, question, chat_summary):
        inps = {
            "name": self.name,
            "inappropiate_topic": self.inappropiates,
            "guard_exam": self.guard_examples.format(name=self.name),
            "chatsum": chat_summary,
            "question": question,
        }
        response = use_chatllm_with_prompt(
            chatllm=self.chatllm,
            prompt_template=self.prompt.PROMPT_GUARD,
            inps=inps,
            verbose=self.verbose,
        )
        if (
            response.lstrip()
            == "I'm not able to help with that, as I'm only a language model. If you believe this is an error, please send us your feedback."
        ):
            if self.lang == "TH":
                response = (
                    f"{self.name}ไม่สามารถสนทนาเกี่ยวกับเรื่องที่คุณพูดถึงได้จริงๆ"
                )
            else:
                response = f"{self.name} can't really have a conversation about the topic you're talking about."
            return {
                "related": True,
                "type": "unknown",
                "response": response,
            }
        print(response)
        response = json.loads(response.lstrip(), strict=False)
        return response
