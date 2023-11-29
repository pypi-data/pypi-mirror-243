"""
Chroma DB required connection information
"""

from dataclasses import dataclass
from typing import Literal, TypedDict, Union


class HuggingFaceEFInputs(TypedDict):
    ef_type: Literal["hf"]
    api_key: str
    model_name: str


class OpenAIEFInputs(TypedDict):
    ef_type: Literal["openai"]
    api_key: str
    model_name: str


class OpenAIAzureEFInputs(TypedDict):
    ef_type: Literal["openai_azure"]
    api_key: str
    model_name: str
    api_base: str
    api_version: str


class SentenceTransformerEFInputs(TypedDict):
    ef_type: Literal["sentence_transformer"]
    model_name: str


@dataclass
class ChromaDB:
    """Class for storing chroma connection details"""

    def __post_init__(self):
        self.db_type = "chroma_db"

    host: str
    port: int
    collection: str
    ef_inputs: Union[
        HuggingFaceEFInputs, OpenAIEFInputs, OpenAIAzureEFInputs, SentenceTransformerEFInputs
    ]
