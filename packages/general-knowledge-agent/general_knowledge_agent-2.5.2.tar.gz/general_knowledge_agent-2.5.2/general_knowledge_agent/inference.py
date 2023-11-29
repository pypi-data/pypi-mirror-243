import pandas as pd

from langchain.schema.document import Document
from typing import List


class Interaction:
    def __init__(self, role: str, message: str):
        self.role = role
        self.message = message


class Conversation:
    @property
    def roles(self):
        return [interaction.role for interaction in self.interactions]

    @property
    def messages(self):
        return [interaction.message for interaction in self.interactions]


    def __init__(self, roles: List[str], messages: List[str]):
        self.interactions = [Interaction(role, message) for role, message in zip(roles, messages)]
    

    def to_pandas(self):
        return pd.DataFrame(
            {
                'Role': self.roles, 
                'Message': self.messages
            }
        )
    

    def to_str(self):
        return '\n'.join([f'{interaction.role}: {interaction.message}' for interaction in self.interactions])

    
    def to_openai(self):
        return [{'role': interaction.role, 'content': interaction.message} for interaction in self.interactions]


    def set_documents(self, documents: List[Document]):
        self.documents = documents


    def add_interaction(self, role: str, message: str):
        self.interactions.append(Interaction(role, message))
