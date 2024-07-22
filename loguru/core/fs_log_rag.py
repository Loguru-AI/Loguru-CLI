import os
import random
import re
import shutil
import time

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

from loguru import LOGURU_DATA_DIR, HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE
from loguru.core.models.config import Config, DataSource, Params


class LoguruRAG:
    def __init__(self, config: Config):
        self._config = config
        self._vector_store_directory = None
        self._ollama_api_base_url = random.choice(config.ollama.hosts)
        self._model_name = config.ollama.llm_name
        self._embedding_model_name = config.ollama.embedding_model_name
        self._vector_store_directory = os.path.join(LOGURU_DATA_DIR, 'cache')

    def scan(self, clean_and_rebuild: bool = False):
        if clean_and_rebuild or not os.path.exists(self._vector_store_directory):
            print("Scanning log locations to rebuild index. Please be patient. This may take a while.")
            shutil.rmtree(self._vector_store_directory, ignore_errors=True)
            for ds in self._config.data_sources:
                ds: DataSource
                for sl in ds.ds_params.scan_locations:
                    print(f"Scanning directory: {sl.location}...")
                    for fl in os.listdir(sl.location):
                        if '.DS_Store' in fl:
                            continue
                        self._load_log_file(
                            log_file_path=os.path.join(sl.location, fl),
                            pattern_to_split_log_lines=sl.pattern
                        )
            print("Scanning complete.")
        # else use existing vectorstore/cache
        # print("Skipping log location scanning and loading the previous index...")

    def _load_log_file(self, log_file_path, pattern_to_split_log_lines):
        if log_file_path is None:
            raise ValueError("Log file path not provided.")
        # print(f"Using vector store: {self._vector_store_directory}")
        # Load the Embedding Model
        embedding_model = self._load_embedding_model(model_name=self._embedding_model_name)
        # load and split the documents
        documents = self._parse_log_file(
            log_file_path=log_file_path,
            pattern_to_split_log_lines=pattern_to_split_log_lines
        )
        print(f"Processing {log_file_path}...")

        if not os.path.exists(self._vector_store_directory):
            print(f"Creating new vector store with logs of {log_file_path}...")
            os.makedirs(self._vector_store_directory, exist_ok=True)
            vectorstore = FAISS.from_documents(documents, embedding_model)
            vectorstore.save_local(self._vector_store_directory)
        else:
            print(f"Updating vector store with logs of {log_file_path}...")
            vectorstore = FAISS.load_local(self._vector_store_directory, embedding_model,
                                           allow_dangerous_deserialization=True)
            vectorstore.add_documents(documents)
            vectorstore.save_local(self._vector_store_directory)

    def _parse_log_file(self, log_file_path: str, pattern_to_split_log_lines: str) -> [Document]:
        """
        Reads a log file and split the log file into an array of log entries by specified pattern.

        For example: if the log file contents looks like this:

            2024-06-14T11:05:48.406+05:30 DEBUG [app-service,,] 73331 --- [main] c.i.o.MyApplication        : Running with Spring Boot v3.1.5, Spring v6.1.5
            2024-06-14T11:05:48.408+05:30  INFO [app-service,,] 73331 --- [main] c.i.o.MyApplication        : No active profile set, falling back to 1 default profile: "default"
            2024-06-14T11:05:49.102+05:30  WARN [app-service,,] 73331 --- [main] c.i.o.MyApplication        : Config file not specified.
            We will try to use the default config file: /app/data/cfg.ini
            2024-06-14T11:05:49.233+05:30  WARN [app-service,,] 73331 --- [main] c.i.o.MyApplication        : Starting application...

        You would want to split the logs by the date pattern to identify each log entry.
        So you would provide a pattern: '(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2})'

        :param log_file_path:
        :param pattern_to_split_log_lines: r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2})'
        :return: []
        """
        with open(log_file_path, 'r') as file:
            log_content = file.read()
        raw_entries = re.split(pattern_to_split_log_lines, log_content)
        _log_entries = []
        for i in range(1, len(raw_entries), 2):
            log_entry = raw_entries[i] + raw_entries[i + 1]
            _log_entries.append(
                Document(
                    page_content=log_entry.strip(),
                    metadata={
                        'log_dir': os.path.dirname(log_file_path),
                        'file_name': os.path.basename(log_file_path)
                    }
                )
            )
        return _log_entries

    def _load_embedding_model(self, model_name, normalize_embedding=True):
        # print("Loading embedding model...")
        start_time = time.time()
        hugging_face_embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE},  # here we will run the model with CPU only
            encode_kwargs={
                'normalize_embeddings': normalize_embedding  # keep True to compute cosine similarity
            }
        )
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        return hugging_face_embeddings

    def _load_qa_chain(self, retriever, llm, prompt):
        start_time = time.time()
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=True,
            chain_type_kwargs={'prompt': prompt}
        )
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        # print(f"QA chain load time: {time_taken} seconds.\n")
        return qa_chain

    def _get_response(self, query, chain, stream: bool = False) -> tuple[str, list[Document]]:
        if stream:
            # TODO: fix the streaming code and return the response and source docs to the caller function
            for chunks in chain.stream({"query": query}):
                print('', end='', flush=True)
            print('')
            return '', []
        else:
            response = chain.invoke({"query": query})
            res = response['result']
            src_docs = response['source_documents']
            response = res.strip()
            print(response, flush=True)
            print('\n')
            return res, src_docs

    def ask(self, question: str, stream: bool = False) -> tuple[str, list[Document]]:
        embedding_model = self._load_embedding_model(model_name=self._embedding_model_name)
        vectorstore = FAISS.load_local(
            self._vector_store_directory,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": self._config.num_chunks_to_return, 'fetch_k': self._config.num_chunks_to_return})

        template = """
        ### System:
        You are an honest assistant.
        You will accept contents of a log file and you will answer the question asked by the user appropriately.
        If you don't know the answer, just say you don't know. Don't try to make up an answer.
        If you find time, date or timestamps in the logs, make sure to convert the timestamp to more human-readable format in your response as DD/MM/YYYY HH:SS

        ### Context:
        {context}

        ### User:
        {question}

        ### Response:
        """

        prompt = PromptTemplate.from_template(template)
        llm = ChatOllama(
            temperature=0,
            base_url=self._ollama_api_base_url,
            model=self._model_name,
            streaming=True,
            # seed=2,
            top_k=10,
            # A higher value (100) will give more diverse answers, while a lower value (10) will be more conservative.
            top_p=0.3,
            # Higher value (0.95) will lead to more diverse text, while a lower value (0.5) will generate more
            # focused text.
            num_ctx=3072,  # Sets the size of the context window used to generate the next token.
            verbose=False
        )

        if stream:
            llm.callbacks = [StreamingStdOutCallbackHandler()]

        chain = self._load_qa_chain(retriever, llm, prompt)
        start_time = time.time()
        response, source_docs = self._get_response(question, chain, stream=stream)
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        # print(f"Response time: {time_taken} seconds.\n")
        # print(response)
        # print("-------------------------------------------")
        # print("--------------   Source Docs   ------------")
        # print("-------------------------------------------")
        # for d in source_docs:
        #     print(d.page_content)
        #     print("-------------------------------------------")
        return response, source_docs
