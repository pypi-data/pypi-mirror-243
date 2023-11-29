import chromadb
import numpy as np
import pandas as pd
import openai
import re
import os

from datetime import datetime

from tqdm import tqdm
from typing import List

# Langchain dependencies
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

# Base model structure
from cortex_cli.core.models.cortex_model import CortexModel
# Base inference structure
from general_knowledge_agent.inference import Conversation

# Threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class GeneralKnowledgeAgent(CortexModel):

    ##################
    ### Properties ###
    ##################

    @property
    def debug(self):
        """
        Enables debug mode for the model.
        """
        return False
    

    @property
    def loaded_docs(self):
        """
        Returns True if documents have been loaded into the model.
        """
        return 'preprocessed_docs' in dir(self) and len(self.preprocessed_docs) > 0


    @property
    def has_chromadb(self):
        """
        Returns True if a ChromaDB has been created.
        """
        return os.path.isdir(self.params['chroma_directory'])

    ################################
    ### Initialization Functions ###
    ################################

    def initialize(self):
        """
        Sets input and output examples for the Cortex model.
        """
        input_example = pd.DataFrame({'Role': ['system'], 'Message': ['This is a test input']})

        self._set_input_output_examples(
            input_example, 
            np.array(['This is a test output'])
        )

        self.prompt = PromptTemplate(
            template=self.params['prompt_template'],
            input_variables=self.params['prompt_variables']
        )
        self.inquiry = PromptTemplate(
            template=self.params['inquiry_template'],
            input_variables=self.params['inquiry_variables']
        )

        self.embeddings = OpenAIEmbeddings(
            deployment='ada',
            chunk_size=16
        )

        self.is_deployment = False

        return 'Nearly Human General Knowledge Agent initialized successfully.'
    

    def setup_azure_openai_access(self):
        """
        Setup Azure OpenAI access via API keys.
        """
        if not openai.api_key:
            openai.api_type = 'azure'
            openai.api_base = 'https://nh-test.openai.azure.com'
            openai.api_version = '2023-03-15-preview'
            openai.api_key = self.secrets_manager.get_secret('AOAI_TOKEN')

            os.environ['OPENAI_API_TYPE'] = openai.api_type
            os.environ['OPENAI_API_BASE'] = openai.api_base
            os.environ['OPENAI_API_VERSION'] = openai.api_version
            os.environ['OPENAI_API_KEY'] = openai.api_key


    ##########################
    ### ChromaDB Functions ###
    ##########################


    def read_docs(self):
        """
        Loads documents from Cortex data into memory.
        """
        self.documents = []
        self.metadatas = []
        for file in self.cortex_data.files:
            if file.type in ['doc', 'docx', 'txt', 'pdf', 'rtf', 'md']:
                self.documents.append(file.load().strip())
                self.metadatas.append({
                    'file_name': file.name.rsplit('.', 1)[0]
                })
    

    def preprocess_docs(self):
        if self.has_chromadb:
            return 'Skipping document preprocessing, ChromaDB already exists.'
        
        # Split documents by NH delimiter
        recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4096,
            chunk_overlap=0,
            length_function=len,
            separators=['\n\n', '\n']
        )

        new_texts = []
        new_metadatas = []

        pattern = r'\s+({.*?})'

        for i, doc in enumerate(self.documents):
            split = doc.split('--- NH SECTION DELIMITER ---')
            for j, section in enumerate(split):
                new_metadata = self.metadatas[i]
                
                # Select dict from first line of each section if it exists
                match = re.search(pattern, section.split('\n')[0])
                if match:
                    try:
                        metadata = eval(match.group(0))
                        # Handle exceptions
                        if type(metadata) != dict:
                            raise Exception('Invalid dictionary format')
                        
                        if len(metadata.keys()) == 0:
                            raise Exception('Empty dictionary')
                        
                        if 'section_images' in metadata.keys():
                            metadata['section_images'] = ','.join(metadata['section_images'])
                                            
                        metadata.update(new_metadata)

                        # Add expanded metadata if additional found
                        new_metadatas.append(metadata)

                        # Remove original metadata text from section
                        split[j] = '\n'.join(section.split('\n')[1:])

                        continue
                    except Exception as e:
                        # Invalid dictionary format
                        print(f'Invalid dictionary input for context section:\n{section}\n{e}')

                # Add default document metadata if none found
                new_metadatas.append(new_metadata)
            # Add documents in bulk
            new_texts.extend(split)
        recurse_documents = recursive_splitter.create_documents(new_texts, new_metadatas)

        ### Handle associated prompts ###
        original_texts = []
        embedding_texts = []
        metadatas = []

        for doc in recurse_documents:
            original_texts.append(doc.page_content)
            embedding_texts.append(self.strip_text(doc.page_content))
            metadatas.append(doc.metadata)
            if 'associated_prompts' in doc.metadata.keys():
                for associated_prompt in doc.metadata['associated_prompts']:
                    original_texts.append(doc.page_content)
                    embedding_texts.append(associated_prompt)
                    metadatas.append(doc.metadata)
                
                # Remove list metadata
                del doc.metadata['associated_prompts']
        #################################


        ### Embed documents ###
        embeddings, error_count = self.safe_embed(embedding_texts)
        #######################

        self.preprocessed_docs = (original_texts, metadatas, embeddings)

        if self.debug:
            with open('chunks.txt', 'w') as f:
                f.write('\n\n-------------------------------------------------------\n\n\n\n'.join([doc.page_content for doc in recurse_documents]))

            with open('embeddings.txt', 'w') as f:
                f.write('\n\n-------------------------------------------------------\n\n\n\n'.join([str(x) for x in embeddings]))
            
            with open('final_chunks.txt', 'w') as f:
                f.write('\n\n-------------------------------------------------------\n\n\n\n'.join(original_texts))

        self._add_cleanup_var(['documents', 'metadatas'])

        print(f'Encountered {error_count} embedding errors.')

        return f'Encountered {error_count} embedding errors.'


    def strip_text(self, text: str) -> str:
        """
        Strips text of all non-alphanumeric characters.
        """
        # Matches any number of '#' characters at the beginning of the string
        hash_pattern = re.compile(r'^#+\s*')
        result1 = re.sub(hash_pattern, '', text)
        # Matches any number of '/*' characters
        star_pattern = re.compile(r'\*')
        result2 = re.sub(star_pattern, '', result1)
        # Matches '-' characters on their own line
        dash_pattern = re.compile(r'^\s*-\s*', re.MULTILINE)
        result3 = re.sub(dash_pattern, '', result2)

        return result3

    
    def safe_embed(self, documents: List[str], max_workers: int=9, progress_bar: bool=True) -> (List[np.ndarray], int):
        final_embeddings = []
        embeddings = []

        total_embeddings = 9

        batch_results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(total_embeddings):
                batch_results.append(executor.submit(self.embeddings.embed_documents, documents))
            for result in tqdm(as_completed(batch_results), desc='Running embedding batches', disable=not progress_bar):
                embeddings.append(np.array(result.result()))

        error_count = 0
        
        for i in range(len(embeddings[0])):
            emb_dict = {}
            for j in range(len(embeddings)):
                sum = embeddings[j][i].sum()

                if sum in emb_dict:
                    emb_dict[sum].append(embeddings[j][i])
                else:
                    emb_dict[sum] = [embeddings[j][i]]
            
            best_key = None
            max_count = 0

            if len(emb_dict.keys()) > 1:
                error_count += 1
            for k, v in emb_dict.items():
                count = len(v)

                if best_key is None or count > max_count:
                    best_key = k
                    max_count = count
            
            final_embeddings.append(emb_dict[best_key][0].tolist())
        
        return (final_embeddings, error_count)


    def fine_tune(self):
        """
        Creates a ChromaDB from the documents in Cortex data.
        """
        print('Fine tuning model...')

        save_chroma_db = not self.has_chromadb

        if self.has_chromadb:
            client_local = chromadb.PersistentClient(self.params['chroma_directory'])
            collection_local = client_local.get_collection('nearlyhuman')

            local_data = collection_local.get(include=['embeddings', 'documents', 'metadatas'])

            self.preprocessed_docs = (local_data['documents'], local_data['metadatas'], local_data['embeddings'])

        if not self.loaded_docs:
            return 'No Cortex documents found to fine tune on.'
        
        self._add_cleanup_var(['db'])

        documents, metadatas, embeddings = self.preprocessed_docs

        client = chromadb.PersistentClient(path=self.params['chroma_directory'])
        if save_chroma_db:
            collection = client.create_collection(name="nearlyhuman", metadata={"hnsw:space": "cosine"})

            collection.add(
                ids=[str(i) for i in range(len(documents))],
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
        
        self.db = Chroma(
            collection_name='nearlyhuman',
            client=client,
            embedding_function=self.embeddings,
            collection_metadata={"hnsw:space": "cosine"}
        )

        # Only save chroma_db if we generated a new chroma_db and we're not in deployment mode
        if save_chroma_db and not self.is_deployment:
            file_paths = []

            # Get files from pipeline run
            for root, dirs, files in os.walk(self.params['chroma_directory']):
                for file in files:
                    file_paths.append(os.path.join(root, file))

            # Upload files to Cortex
            self.cortex_data.upload_to_cortex(file_paths)

        return 'ChromaDB created successfully.'


    def fine_tune_messages(self, conversation: Conversation, inquiry: str) -> Conversation:
        """
        Formats messages for model ingestion.
        """

        last_idx = len(conversation.interactions) - 1
        last_interaction = conversation.interactions[last_idx]
        if last_interaction.role == 'user':
            docs = self.get_context(inquiry if inquiry else last_interaction.message)
            if len(docs) == 0:
                fallback_context = 'NO relevent documents found within knowledgebase.'
                last_interaction.message = self.prompt_engineer(last_interaction.message, fallback_context)
            else:
                # Format document contents with section names for LLM interpretation
                if 'expose_section_headers' in self.params and self.params['expose_section_headers']:
                    contents = [f'Document Section: {doc.metadata["section_name"]}\n{doc.page_content}' if (doc.metadata and 'section_name' in doc.metadata) else doc.page_content for doc in docs]
                else:
                    contents = [doc.page_content for doc in docs]
                context = '\n\n\n'.join([content for content in contents])
                last_interaction.message = self.prompt_engineer(last_interaction.message, context)

            # Update conversation
            conversation.interactions[last_idx] = last_interaction
            conversation.set_documents(docs)

        return conversation


    def get_context(self, message: str, k: int=10):
        """
        Grabs context from the ChromaDB based on a user's latest message.
        """
        # Get safe embedding for query message
        embeddings = self.safe_embed([message], progress_bar=False)[0]

        confident_docs = self.db.similarity_search_by_vector_with_relevance_scores(embeddings, k=k)
        docs = []

        # Set relevance scores within document metadata
        for doc, conf in confident_docs:
            doc.metadata['relevance'] = int((1 - round(conf, 2)) * 100)
            if doc.metadata['relevance'] > self.params['context_dropout_threshold'] * 100:
                docs.append(doc)

        # Return empty list of no relavent documents found
        if len(docs) == 0:
            return docs
        
        removed_duplicates = self.remove_duplicate_doc_texts(docs)

        # Fit documents to size
        fitted_docs = self.fit_to_size([doc.page_content for doc in removed_duplicates])

        # Return documents in reversed order (Helps LLM attention span)
        return docs[:len(fitted_docs)][::-1]


    @staticmethod
    def remove_duplicate_doc_texts(lst: List[Document]) -> List[Document]:
        """
        Removes duplicate documents from a list based on their page content.
        """

        new_lst = []

        for i, doc in enumerate(lst):
            for compare in lst:
                # If duplicate page contents are found and documents are fundimentally different
                if doc.page_content == compare.page_content and doc != compare:
                    continue
            new_lst.append(doc)
        return new_lst

    @staticmethod
    def fit_to_size(lst: List[str], limit=8192) -> List[str]:
        """
        Takes in lst of strings and returns join of strings
        up to `limit` number of chars (no substrings)

        :param lst: (list)
            list of strings to join
        :param limit: (int)
            optional limit on number of chars, default 50
        :return: (list)
            string elements joined up until length of 50 chars.
            No partial-strings of elements allowed.
        """
        for i in range(len(lst)):
            new_join = lst[:i+1]
            if len('\n\n\n'.join(new_join)) > limit:
                return lst[:i]
        return lst


    def prompt_engineer(self, message: str, context: str=None) -> str:
        """
        Formats the last user message for model ingestion.
        """
        if self.loaded_docs:
            return self.prompt.format(
                instruction=message,
                context=context
            )

        return self.prompt.format(
            instruction=message,
            context=''
        )


    ############################
    ### Prediction Functions ###
    ############################


    def predict(self, model_inputs: pd.DataFrame) -> pd.DataFrame:
        """
        Runs inference on a dataframe of messages.
        """
        response = 'Unable to complete the request to Nearly Human General Knowledge Agent.'

        roles = []
        messages = []
        if self.params and self.params['system_prompt']:
            roles.append('system')
            messages.append(self.params['system_prompt'])
                
        roles.extend(model_inputs['Role'].to_list())
        messages.extend(model_inputs['Message'].to_list())

        ### Inquiry ###

        inquery = None

        inquiry_message = self.inquiry.format(
            user_prompt=messages[-1],
            conversation_history='\n'.join([f'{role}: {message}' for role, message in zip(roles[1:-1], messages[1:-1]) if role == 'user'])
        )

        for i in range(self.params['max_retries']):
            try:
                inquiry_response = openai.ChatCompletion.create(
                    engine   = self.params['deployment_name'],
                    model    = self.params['model'],
                    messages = [{'role': 'system', 'content': self.params['inquiry_system_prompt']}, {'role': 'user', 'content': inquiry_message}],
                    temperature=self.params['inquiry_temperature'],
                    timeout=self.params['timeout']
                )

                inquiry = inquiry_response['choices'][0]['message']['content'].strip()
                break
            except Exception as e:
                raise e

        ################

        conversation = Conversation(roles, messages)
        conversation = self.fine_tune_messages(conversation, inquiry)

        documents, metadatas = [], []
        for doc in conversation.documents:
            documents.append(doc.page_content)
            metadatas.append(doc.metadata)

        for i in range(self.params['max_retries']):
            try:
                response = openai.ChatCompletion.create(
                    engine   = self.params['deployment_name'],
                    model    = self.params['model'],
                    messages = conversation.to_openai(), # Convert conversation to OpenAI format
                    temperature=self.params['temperature'],
                    timeout=self.params['timeout']
                )

                response = self.replace_image_url_format(f'{response["choices"][0]["message"]["content"].strip()}')
                break
            except Exception as e:
                raise e

        result = pd.DataFrame({
            'Message': [response],
            'Role': ['assistant'],
            'Documents': [documents],
            'Metadatas': [metadatas]
        })
        return result
    

    def replace_image_url_format(self, message: str) -> str:
        """
        Matches URLs in the format [alt text](url) and replaces them with ![alt text](url)
        when http, https, and www are not found in the URL. Allows for proper image rendering
        """
        regex = r'(!?\[)([^]]+)(\]\([^)]+\))'

        matches = re.finditer(regex, message)

        for match in matches:
            full_match = match.group(0)
            
            # Check if the URL part does not contain '!, 'http', 'https', or 'www'
            if not re.search(r'!|http[s]?://|www\.', full_match):
                message = message.replace(full_match, f'!{full_match}')
        
        return message


    def evaluate(self) -> str:
        """
        Single evaluation point for the model. Useful for testing.
        """
        evaluation = Conversation(
            roles=['user'], 
            messages=['What can you assist me with?']
        )

        llm_response = self.predict(evaluation.to_pandas())['Message'].iloc[0]

        evaluation.add_interaction('assistant', llm_response)
       
        evaluation_str = evaluation.to_str()

        print(evaluation_str)

        return evaluation_str


    ##################################
    ### Batch Evaluation Functions ###
    ##################################

    
    def batch_prediction(self, df: pd.DataFrame, batch_size: int, batch_idx: int):
        """
        Takes list of questions, processes them, runs inference on each question, then returns batch.
        Param: List of Questions
        """

        # For each question in the current batch
        for i in range(df.shape[0]):
            global_idx = batch_idx * batch_size + i
            response = self.predict(df.loc[i:i, :])
            self.df.loc[global_idx:global_idx, 'Answer'] = response['Message'].values[0]


    def thread_batch_eval(self, batch_size: int=1):
        """
        Threads batch inferences using predict function. 
        Param: List of Questions, Batch Size. (Set to 1 by default)
        """
        batch_results = []

        with ThreadPoolExecutor(max_workers=None) as executor:
            
            for i in range(0, self.df.shape[0], batch_size):
                batch_input = self.df.iloc[i : i + batch_size].reset_index(drop=True)
                batch_results.append(executor.submit(self.batch_prediction, batch_input, batch_size, i))
            for result in as_completed(batch_results):
                result.result()


    def thread_batch_eval_pipe(self, excel_file: str='data/eval/evaluation.csv'):
        """
        Kicks off batch evaluation pipeline.
        """
        try:
            self.df = pd.read_csv(excel_file)
            self.df = self.df.astype({'Answer': 'str'})
            self.thread_batch_eval()
            file_name = f'data/eval/v{self.params["model_version"]}_{datetime.now().strftime("%m-%d-%Y_%H:%M:%S")}.csv'
            self.df.to_csv(file_name, index=False)
            self._add_cleanup_var('df')

            self.cortex_data.upload_to_cortex(file_name)
        except FileNotFoundError:
            return 'Skipping Batch Evaluation, CSV File not found.'
    
        except KeyError:
            return 'Couldn\'t deconstruct CSV, please check formatting.'


    #########################
    ### Cleanup Functions ###
    #########################


    def setup_deployment_variables(self):
        self.is_deployment = True
