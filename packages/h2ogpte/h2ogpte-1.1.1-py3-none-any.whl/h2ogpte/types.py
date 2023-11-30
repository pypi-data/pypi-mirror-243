from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Union, Optional, List


class JobKind(str, Enum):
    NoOpJob = "NoOpJob"
    IngestFromFileSystemJob = "IngestFromFileSystemJob"
    IngestUploadsJob = "IngestUploadsJob"
    IngestWebsiteJob = "IngestWebsiteJob"
    IndexFilesJob = "IndexFilesJob"
    UpdateCollectionStatsJob = "UpdateCollectionStatsJob"
    DeleteCollectionsJob = "DeleteCollectionsJob"
    DeleteDocumentsJob = "DeleteDocumentsJob"
    DeleteDocumentsFromCollectionJob = "DeleteDocumentsFromCollectionJob"


class Status(str, Enum):
    Unknown = "unknown"
    Scheduled = "scheduled"
    Queued = "queued"
    Running = "running"
    Completed = "completed"
    Failed = "failed"
    Canceled = "canceled"


class Answer(BaseModel):
    content: str
    error: str


class ExtractionAnswer(BaseModel):
    content: List[str]
    error: str


class ChatMessage(BaseModel):
    id: str
    content: str
    reply_to: Optional[str]
    votes: int
    created_at: datetime
    type_list: Optional[List[str]]


class PartialChatMessage(BaseModel):
    id: str
    content: str
    reply_to: Optional[str]


class ChatMessageReference(BaseModel):
    document_id: str
    document_name: str
    chunk_id: int
    pages: str
    score: float


class ChatMessageMeta(BaseModel):
    message_type: str
    content: str


class ChatSessionCount(BaseModel):
    chat_session_count: int


class ChatSessionForCollection(BaseModel):
    id: str
    latest_message_content: Optional[str]
    updated_at: datetime


class ChatSessionInfo(BaseModel):
    id: str
    latest_message_content: Optional[str]
    collection_id: str
    collection_name: str
    updated_at: datetime


class Chunk(BaseModel):
    text: str


class Chunks(BaseModel):
    result: List[Chunk]


class Collection(BaseModel):
    id: str
    name: str
    description: str
    document_count: int
    document_size: int
    created_at: datetime
    updated_at: datetime
    username: str
    system_prompt: Optional[str]
    pre_prompt_query: Optional[str]
    prompt_query: Optional[str]
    rag_type: Optional[str]
    hyde_no_rag_llm_prompt_extension: Optional[str]
    auto_gen_description_prompt: Optional[str]


class CollectionCount(BaseModel):
    collection_count: int


class CollectionInfo(BaseModel):
    id: str
    name: str
    description: str
    document_count: int
    document_size: int
    updated_at: datetime
    user_count: int
    is_public: bool
    username: str


class Document(BaseModel):
    id: str
    name: str
    type: str
    size: int
    page_count: int
    status: Status
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = True


class DocumentCount(BaseModel):
    document_count: int


class DocumentInfo(BaseModel):
    id: str
    name: str
    type: str
    size: int
    page_count: int
    status: Status
    updated_at: datetime

    class Config:
        use_enum_values = True


class ShareResponseStatus(BaseModel):
    status: str


class Permission(BaseModel):
    username: str


class User(BaseModel):
    username: str


class Identifier(BaseModel):
    id: str


class JobStatus(BaseModel):
    id: str
    status: str


class Job(BaseModel):
    id: str
    passed: float
    failed: float
    progress: float
    completed: bool
    canceled: bool
    date: datetime
    kind: JobKind
    statuses: List[JobStatus]
    errors: List[str]


class ConfigItem(BaseModel):
    key_name: str
    string_value: str
    value_type: str
    can_overwrite: bool


class Meta(BaseModel):
    version: str
    build: str
    username: str
    email: str
    license_expired: bool
    license_expiry_date: str
    global_configs: List[ConfigItem]


class ObjectCount(BaseModel):
    chat_session_count: int
    collection_count: int
    document_count: int


class Result(BaseModel):
    status: Status

    class Config:
        use_enum_values = True


class SchedulerStats(BaseModel):
    queue_length: int


class SearchResult(BaseModel):
    id: str
    topic: str
    name: str
    text: str
    size: int
    pages: str
    score: float


class SearchResults(BaseModel):
    result: List[SearchResult]


class SessionError(Exception):
    pass


@dataclass
class ChatRequest:
    t: str  # cq
    mode: str  # l=lexical, s=semantic, h=hybrid
    session_id: str
    correlation_id: str
    body: str
    system_prompt: Optional[str]
    pre_prompt_query: Optional[str]
    prompt_query: Optional[str]
    pre_prompt_summary: Optional[str]
    prompt_summary: Optional[str]
    llm: Union[str, int, None]
    llm_args: Optional[str]
    self_reflection_config: Optional[str]
    rag_config: Optional[str]


@dataclass
class ChatAcknowledgement:
    t: str  # cx
    session_id: str
    correlation_id: str
    message_id: str


@dataclass
class ChatResponse:
    t: str  # ca | cp
    session_id: str
    message_id: str
    reply_to_id: str
    body: str


@dataclass
class ChatError:
    t: str  # ce
    session_id: str
    reply_to_id: str
    body: str


class ObjectNotFoundError(Exception):
    pass


class InvalidArgumentError(Exception):
    pass
