import re
from typing import List, Optional

from pydantic import BaseModel, Field, conint, field_validator


class Options(BaseModel):
    temperature: float = Field(..., description="Temperature for the model", ge=0.0, le=1.0)


class Ollama(BaseModel):
    hosts: List[str] = Field(..., description="List of hosts URLs")
    llm_name: str = Field(..., description="Model name")
    embedding_model_name: str = Field(..., description="Embedding Model name")
    options: Options = Field(..., description="Options for the model")


class ScanLocations(BaseModel):
    # include_paths: List[str] = Field(..., description="Paths to include in the scan")
    # exclude_paths: List[str] = Field(..., description="Paths to exclude from the scan")
    # include_patterns: List[str] = Field(..., description="Patterns to include in the scan")
    # exclude_patterns: List[str] = Field(..., description="Patterns to exclude from the scan")

    location: str = Field(..., description="Paths to include in the scan")
    pattern: str = Field(..., description="Paths to include in the scan")


class Params(BaseModel):
    recursion_depth: Optional[conint(ge=0)] = Field(...,
                                                    description="Recursion depth for scanning")
    file_size_limit: str = Field(...,
                                 description="File size limit with unit (e.g., 100MB, 1GB)")

    @field_validator('file_size_limit')
    def validate_file_size_limit(cls, v):
        if not re.match(r'^\d+(?:MB|GB|KB)$', v):
            raise ValueError('file_size_limit must be in the format <number><unit>, e.g., 100MB, 1GB')
        return v

    scan_locations: List[ScanLocations] = Field(..., description="Scan locations configuration")


class DataSource(BaseModel):
    type: str = Field(..., description="Type of data source")
    ds_params: Params = Field(..., description="Parameters for the data source")


class Gemini(BaseModel):
    api_key: str = Field(..., description="Gemini API Key")
    llm_name: str = Field(..., description="Gemini Model Name. Ex: gemini-1.5-flash, gemini-1.5-pro")


class OpenAI(BaseModel):
    api_key: str = Field(..., description="OpenAI API Key")
    org_id: str = Field(..., description="Organization ID for OpenAI")
    llm_name: str = Field(..., description="OpenAI Model Name. Ex: gpt-3.5-turbo-instruct")


class Anthropic(BaseModel):
    api_key: str = Field(..., description="Anthropic API Key")
    llm_name: str = Field(..., description="Anthropic Model Name. Ex: claude-3-opus-20240229")


class Config(BaseModel):
    service: str = Field(..., description="LLM service type. Ex: ollama, gemini")
    ollama: Optional[Ollama] = Field(..., description="Ollama configuration")
    gemini: Optional[Gemini] = Field(..., description="Gemini configuration")
    openai: Optional[OpenAI] = Field(..., description="OpenAI configuration")
    anthropic: Optional[Anthropic] = Field(..., description="Anthropic configuration")
    data_sources: List[DataSource] = Field(..., description="List of data sources")
    num_chunks_to_return: int = Field(..., description="Number of chunks to return")
