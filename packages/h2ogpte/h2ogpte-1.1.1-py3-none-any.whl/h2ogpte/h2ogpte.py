import json
import requests
import time
from typing import Iterable, Any, Union, List, Dict, Tuple, Optional, cast
from h2ogpte.session import Session

from h2ogpte.types import (
    Answer,
    ChatMessage,
    ChatMessageReference,
    ChatSessionCount,
    ChatSessionForCollection,
    ChatSessionInfo,
    ChatMessageMeta,
    Chunk,
    Chunks,
    Collection,
    CollectionCount,
    CollectionInfo,
    Document,
    DocumentCount,
    DocumentInfo,
    ExtractionAnswer,
    Identifier,
    InvalidArgumentError,
    User,
    Permission,
    Job,
    Meta,
    ObjectCount,
    ObjectNotFoundError,
    Result,
    ShareResponseStatus,
    SchedulerStats,
    SearchResult,
    SearchResults,
    SessionError,
)


class H2OGPTE:
    """Connect to and interact with an h2oGPTe server."""

    def __init__(
        self,
        address: str,
        api_key: str,
        verify: Union[bool, str] = True,
        strict_version_check=False,
    ):
        """Create a new H2OGPTE client.

        Args:
            address:
                Full URL of the h2oGPTe server to connect to, e.g. "https://h2ogpte.h2o.ai".
            api_key:
                API key for authentication to the h2oGPTe server. Users can generate
            a key by accessing the UI and navigating to the Settings.
            verify:
                Whether to verify the server's TLS/SSL certificate.
                Can be a boolean or a path to a CA bundle.
                Defaults to True.
            strict_version_check:
                Indicate whether a version check should be enforced.

        Returns:
            A new H2OGPTE client.
        """
        # Remove trailing slash from address, if any
        address = address.rstrip("/ ")

        self._address = address
        self._api_key = api_key
        self._verify = verify
        self._auth_header = f"Bearer {self._api_key}"
        server_version = self.get_meta().version
        if server_version[0] == "v":
            server_version = server_version[1:]

        from h2ogpte import __version__ as client_version

        if server_version != client_version:
            msg = (
                f"Warning: Server version {server_version} doesn't match client "
                f"version {client_version}: unexpected errors may occur.\n"
                f"Please install the correct version of H2OGPTE "
                f"with `pip install h2ogpte=={server_version}`."
            )
            if strict_version_check:
                raise RuntimeError(msg)
            else:
                print(msg)
                print(
                    "You can enable strict version checking by passing strict_version_check=True."
                )

    def _get(self, slug: str):
        res = requests.get(
            f"{self._address}{slug}",
            headers={
                "Content-Type": "application/json",
                "Authorization": self._auth_header,
            },
            verify=self._verify,
        )
        if res.status_code != 200:
            raise Exception(f"HTTP error: {res.status_code} {res.reason}")
        return unmarshal(res.text)

    def _post(self, slug: str, data: Any):
        res = requests.post(
            f"{self._address}{slug}",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self._auth_header,
            },
            verify=self._verify,
        )
        if res.status_code != 200:
            if res.status_code == 404:
                raise ObjectNotFoundError(
                    f"Object not found. {res.content.decode('utf-8')}"
                )
            if res.status_code == 400:
                raise InvalidArgumentError(
                    f"Invalid argument type. {res.content.decode('utf-8')}"
                )
            if res.status_code == 500:
                raise Exception(f"{res.content.decode('utf-8')}")
            else:
                raise Exception(
                    f"HTTP error: {res.status_code} {res.content.decode('utf-8')}"
                )
        return unmarshal(res.text)

    def _db(self, method: str, *args):
        return self._post("/rpc/db", marshal([method, *args]))

    def _job(self, method: str, **kwargs):
        return self._post("/rpc/job", marshal([method, kwargs]))

    def _lang(self, method: str, **kwargs):
        res = self._post("/rpc/lang", marshal(dict(method=method, params=kwargs)))
        err = res.get("error")
        if err:
            raise Exception(err)
        return res["result"]

    def _vex(self, method: str, collection_id: str, **kwargs):
        return self._post(
            "/rpc/vex",
            marshal(dict(method=method, collection_id=collection_id, params=kwargs)),
        )

    def _wait(self, d):
        job_id = _to_id(d)
        while True:
            time.sleep(1)
            job = self.get_job(job_id)
            if job.completed or job.canceled:
                break
        return job

    def answer_question(
        self,
        question: Optional[str] = None,
        system_prompt: str = "",  # '' to disable, 'auto' to use LLMs default, None for h2oGPTe default
        text_context_list: Optional[List[str]] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        chat_conversation: Optional[List[Tuple[str, str]]] = None,
        **kwargs,
    ):
        """Send a message and get a response from an LLM.

        Format of inputs content:

            .. code-block::

                {text_context_list}
                \"\"\"\\n{chat_conversation}{question}

        Args:
            question:
                Text query to send to the LLM.
            text_context_list:
                List of raw text strings to be included.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` for the model default, or None for h2oGPTe default. Defaults
                to '' for no system prompt.
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm.
            chat_conversation:
                List of tuples for (human, bot) conversation that will be pre-appended
                to an (question, None) case for a query.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT.

        Returns:
            Answer: The response text and any errors.
        """
        ret = self._lang(
            "answer_question_using_context",
            prompt=question,
            system_prompt=system_prompt,
            text_context_list=text_context_list,
            llm=llm,
            llm_args=llm_args,
            chat_conversation=chat_conversation,
            **kwargs,
        )
        assert isinstance(ret, dict)
        ret = cast(Dict[str, Any], ret)
        for key in ret:
            assert key in ["content", "error"]
        if ret["error"]:
            raise SessionError(ret["error"])
        return Answer(**ret)

    def summarize_content(
        self,
        text_context_list: Optional[List[str]] = None,
        system_prompt: str = "",  # '' to disable, 'auto' to use LLMs default
        pre_prompt_summary: Optional[str] = None,
        prompt_summary: Optional[str] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Summarize one or more contexts using an LLM.

        Format of summary content:

        .. code-block::

            "{pre_prompt_summary}\"\"\"
            {text_context_list}
            \"\"\"\\n{prompt_summary}"

        Args:
            text_context_list:
                List of raw text strings to be summarized.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` for the model default or None for h2oGPTe defaults. Defaults
                to '' for no system prompt.
            pre_prompt_summary:
                Text that is prepended before the list of texts. The default can be
                customized per environment, but the standard default is :code:`"In order to write a concise single-paragraph
                or bulleted list summary, pay attention to the following text:\\\\n"`
            prompt_summary:
                Text that is appended after the list of texts. The default can be customized
                per environment, but the standard default is :code:`"Using only the text above, write a condensed and concise
                summary of key results (preferably as bullet points):\\\\n"`
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT.

        Returns:
            Answer: The response text and any errors.
        """
        return Answer(
            **self._lang(
                "create_summary_from_context",
                text_context_list=text_context_list,
                system_prompt=system_prompt,
                pre_prompt_summary=pre_prompt_summary,
                prompt_summary=prompt_summary,
                llm=llm,
                llm_args=llm_args,
                **kwargs,
            )
        )

    def extract_data(
        self,
        text_context_list: Optional[List[str]] = None,
        system_prompt: str = "",  # '' to disable, 'auto' to use LLMs default, None for h2oGPTe default
        pre_prompt_extract: Optional[str] = None,
        prompt_extract: Optional[str] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Extract information from one or more contexts using an LLM.

        pre_prompt_extract and prompt_extract variables must be used together. If these
        variables are not set, the inputs texts will be summarized into bullet points.

        Format of extract content:

            .. code-block::

                "{pre_prompt_extract}\"\"\"
                {text_context_list}
                \"\"\"\\n{prompt_extract}"

        Examples:

            .. code-block:: python

                extract = h2ogpte.extract_data(
                    text_context_list=chunks,
                    pre_prompt_extract="Pay attention and look at all people. Your job is to collect their names.\\n",
                    prompt_extract="List all people's names as JSON.",
                )

        Args:
            text_context_list:
                List of raw text strings to extract data from.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` or None for the model default. Defaults
                to '' for no system prompt.
            pre_prompt_extract:
                Text that is prepended before the list of texts. If not set,
                the inputs will be summarized.
            prompt_extract:
                Text that is appended after the list of texts. If not set, the inputs will be summarized.
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT.

        Returns:
            ExtractionAnswer: The list of text responses and any errors.
        """
        return ExtractionAnswer(
            **self._lang(
                "extract_data_from_context",
                text_context_list=text_context_list,
                system_prompt=system_prompt,
                pre_prompt_extract=pre_prompt_extract,
                prompt_extract=prompt_extract,
                llm=llm,
                llm_args=llm_args,
                **kwargs,
            )
        )

    def cancel_job(self, job_id: str) -> Result:
        """Stops a specific job from running on the server.

        Args:
            job_id:
                String id of the job to cancel.

        Returns:
            Result: Status of canceling the job.
        """
        return Result(**self._job(".Cancel", job_id=job_id))

    def count_chat_sessions(self) -> int:
        """Counts number of chat sessions owned by the user.

        Returns:
            int: The count of chat sessions owned by the user.
        """
        return ChatSessionCount(**self._db("count_chat_sessions")).chat_session_count

    def count_chat_sessions_for_collection(self, collection_id: str) -> int:
        """Counts number of chat sessions in a specific collection.

        Args:
            collection_id:
                String id of the collection to count chat sessions for.

        Returns:
            int: The count of chat sessions in that collection.
        """
        return ChatSessionCount(
            **self._db("count_chat_sessions_for_collection", collection_id)
        ).chat_session_count

    def count_collections(self) -> int:
        """Counts number of collections owned by the user.

        Returns:
            int: The count of collections owned by the user.
        """
        return CollectionCount(**self._db("count_collections")).collection_count

    def count_documents(self) -> int:
        """Counts number of documents owned by the user.

        Returns:
            int: The count of documents owned by the user.
        """
        return DocumentCount(**self._db("count_documents")).document_count

    def count_documents_in_collection(self, collection_id: str) -> int:
        """Counts the number of documents in a specific collection.

        Args:
            collection_id:
                String id of the collection to count documents for.

        Returns:
            int: The number of documents in that collection.
        """
        return DocumentCount(
            **self._db("count_documents_in_collection", collection_id)
        ).document_count

    def count_assets(self) -> ObjectCount:
        """Counts number of objects owned by the user.

        Returns:
            ObjectCount: The count of chat sessions, collections, and documents.
        """
        return ObjectCount(**self._db("count_assets"))

    def create_chat_session(self, collection_id: str) -> str:
        """Creates a new chat session for asking questions of documents.

        Args:
            collection_id:
                String id of the collection to chat with.

        Returns:
            str: The ID of the newly created chat session.
        """
        return _to_id(self._db("create_chat_session", collection_id))

    def create_chat_session_on_default_collection(self) -> str:
        """Creates a new chat session for asking questions of documents on the default collection.

        Returns:
            str: The ID of the newly created chat session.
        """
        return _to_id(self._db("create_chat_session_on_default_collection"))

    def create_collection(self, name: str, description: str) -> str:
        """Creates a new collection.

        Args:
            name:
                Name of the collection.
            description:
                Description of the collection

        Returns:
            str: The ID of the newly created collection.
        """
        return _to_id(self._db("create_collection", name, description))

    def delete_chat_sessions(self, chat_session_ids: Iterable[str]) -> Result:
        """Deletes chat sessions and related messages.

        Args:
            chat_session_ids:
                List of string ids of chat sessions to delete from the system.

        Returns:
            Result: Status of the delete job.
        """
        return Result(**self._db("delete_chat_sessions", chat_session_ids))

    def delete_collections(self, collection_ids: Iterable[str]):
        """Deletes collections from the environment.

        Documents in the collection will not be deleted.

        Args:
            collection_ids:
                List of string ids of collections to delete from the system.
        """
        return self._wait(
            self._job("crawl.DeleteCollectionsJob", collection_ids=collection_ids)
        )

    def delete_documents(self, document_ids: Iterable[str]):
        """Deletes documents from the system.

        Args:
            document_ids:
                List of string ids to delete from the system and all collections.
        """
        return self._wait(
            self._job("crawl.DeleteDocumentsJob", document_ids=document_ids)
        )

    def delete_documents_from_collection(
        self, collection_id: str, document_ids: Iterable[str]
    ):
        """Removes documents from a collection.

        See Also: H2OGPTE.delete_documents for completely removing the document from the environment.

        Args:
            collection_id:
                String of the collection to remove documents from.
            document_ids:
                List of string ids to remove from the collection.
        """
        return self._wait(
            self._job(
                "crawl.DeleteDocumentsFromCollectionJob",
                collection_id=collection_id,
                document_ids=document_ids,
            )
        )

    def encode_for_retrieval(self, chunks: List[str]) -> List[List[float]]:
        """Encode texts for semantic searching.

        See Also: H2OGPTE.match for getting a list of chunks that semantically match
        each encoded text.

        Args:
            chunks:
                List of strings of texts to be encoded.

        Returns:
            List of list of floats: Each list in the list is the encoded original text.
        """
        return self._lang("encode_for_retrieval", chunks=chunks)

    def get_chunks(self, collection_id: str, chunk_ids: Iterable[int]) -> List[Chunk]:
        """Get the text of specific chunks in a collection.

        Args:
            collection_id:
                String id of the collection to search in.
            chunk_ids:
                List of ints for the chunks to return. Chunks are indexed starting at 1.

        Returns:
            Chunk: The text of the chunk.

        Raises:
            Exception: One or more chunks could not be found.
        """
        res = self._vex("get_chunks", collection_id, chunk_ids=list(chunk_ids))
        return Chunks(**res).result

    def get_collection(self, collection_id: str) -> Collection:
        """Get metadata about a collection.

        Args:
            collection_id:
                String id of the collection to search for.

        Returns:
            Collection: Metadata about the collection.

        Raises:
            KeyError: The collection was not found.
        """
        res = self._db("get_collection", collection_id)
        if len(res) == 0:
            raise ObjectNotFoundError(f"Collection {collection_id} not found")
        return Collection(**res[0])

    def get_collection_for_chat_session(self, chat_session_id: str) -> Collection:
        """Get metadata about the collection of a chat session.

        Args:
            chat_session_id:
                String id of the chat session to search for.

        Returns:
            Collection: Metadata about the collection.
        """
        res = self._db("get_collection_for_chat_session", chat_session_id)
        if len(res) == 0:
            raise ObjectNotFoundError(f"Collection not found")
        return Collection(**res[0])

    def get_document(self, document_id: str) -> Document:
        """Fetches information about a specific document.

        Args:
            document_id:
                String id of the document.

        Returns:
            Document: Metadata about the Document.

        Raises:
            KeyError: The document was not found.
        """
        res = self._db("get_document", document_id)
        if len(res) == 0:
            raise ObjectNotFoundError(f"Document {document_id} not found")
        return Document(**res[0])

    def get_job(self, job_id: str) -> Job:
        """Fetches information about a specific job.

        Args:
            job_id:
                String id of the job.

        Returns:
            Job: Metadata about the Job.
        """
        res = self._job(".Get", job_id=job_id)
        if len(res) == 0:
            raise ObjectNotFoundError(f"Job {job_id} not found")
        return Job(**(res[0]))

    def get_meta(self) -> Meta:
        """Returns information about the environment and the user.

        Returns:
            Meta: Details about the version and license of the environment and
            the user's name and email.
        """
        return Meta(**(self._get("/rpc/meta")))

    def get_scheduler_stats(self) -> SchedulerStats:
        """Count the number of global, pending jobs on the server.

        Returns:
            SchedulerStats: The queue length for number of jobs.
        """
        return SchedulerStats(**self._job(".Stats"))

    def ingest_from_file_system(self, collection_id: str, root_dir: str, glob: str):
        """Add files from the local system into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            root_dir:
                String path of where to look for files.
            glob:
                String of the glob pattern used to match files in the root directory.
        """
        return self._wait(
            self._job(
                "crawl.IngestFromFileSystemJob",
                collection_id=collection_id,
                root_dir=root_dir,
                glob=glob,
            )
        )

    def ingest_uploads(self, collection_id: str, upload_ids: Iterable[str]):
        """Add uploaded documents into a specific collection.

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            delete_upload: Delete uploaded file

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            upload_ids:
                List of string ids of each uploaded document to add to the collection.
        """
        return self._wait(
            self._job(
                "crawl.IngestUploadsJob",
                collection_id=collection_id,
                upload_ids=upload_ids,
            )
        )

    def ingest_website(self, collection_id: str, url: str):
        """Crawl and ingest a website into a collection.

        All web pages linked from this URL will be imported. External links will be ignored. Links to other
        pages on the same domain will be followed as long as they are at the same level or
        below the URL you specify. Each page will be transformed into a PDF document.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            url:
                String of the url to crawl.
        """
        return self._wait(
            self._job("crawl.IngestWebsiteJob", collection_id=collection_id, url=url)
        )

    def list_chat_messages(
        self, chat_session_id: str, offset: int, limit: int
    ) -> List[ChatMessage]:
        """Fetch chat message and metadata for messages in a chat session.

        Messages without a `reply_to` are from the end user, messages with a `reply_to`
        are from an LLM and a response to a specific user message.

        Args:
            chat_session_id:
                String id of the chat session to filter by.
            offset:
                How many chat messages to skip before returning.
            limit:
                How many chat messages to return.

        Returns:
            list of ChatMessage: Text and metadata for chat messages.
        """
        return [
            ChatMessage(**{k: v for k, v in d.items() if v != [None]})
            for d in self._db("list_chat_messages", chat_session_id, offset, limit)
        ]

    def list_chat_message_references(
        self, message_id: str
    ) -> List[ChatMessageReference]:
        """Fetch metadata for references of a chat message.

        References are only available for messages sent from an LLM, an empty list will be returned
        for messages sent by the user.

        Args:
            message_id:
                String id of the message to get references for.

        Returns:
            list of ChatMessageReference: Metadata including the document name, polygon information,
            and score.
        """
        return [
            ChatMessageReference(**d)
            for d in self._db("list_chat_message_references", message_id)
        ]

    def list_list_chat_message_meta(self, message_id: str) -> List[ChatMessageMeta]:
        """Fetch chat message meta information.

        Args:
            message_id:
                Message id to which the metadata should be pulled.

        Returns:
            list of ChatMessageMeta: Metadata about the chat message.
        """
        return [
            ChatMessageMeta(**d) for d in self._db("list_chat_message_meta", message_id)
        ]

    def list_chat_message_meta_part(
        self, message_id: str, info_type: str
    ) -> ChatMessageMeta:
        """Fetch one chat message meta information.

        Args:
            message_id:
                Message id to which the metadata should be pulled.
            info_type:
                Metadata type to fetch.

        Returns:
            ChatMessageMeta: Metadata information about the chat message.
        """
        res = self._db("list_chat_message_meta_part", message_id, info_type)
        if len(res) == 0:
            raise ObjectNotFoundError(f"Chat meta type not found")
        return ChatMessageMeta(**res[0])

    def list_chat_sessions_for_collection(
        self, collection_id: str, offset: int, limit: int
    ) -> List[ChatSessionForCollection]:
        """Fetch chat session metadata for chat sessions in a collection.

        Args:
            collection_id:
                String id of the collection to filter by.
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.

        Returns:
            list of ChatSessionForCollection: Metadata about each chat session including the
            latest message.
        """
        return [
            ChatSessionForCollection(**d)
            for d in self._db(
                "list_chat_sessions_for_collection", collection_id, offset, limit
            )
        ]

    def list_collections_for_document(
        self, document_id: str, offset: int, limit: int
    ) -> List[CollectionInfo]:
        """Fetch metadata about each collection the document is a part of.

        At this time, each document will only be available in a single collection.

        Args:
            document_id:
                String id of the document to search for.
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """
        return [
            CollectionInfo(**d)
            for d in self._db(
                "list_collections_for_document", document_id, offset, limit
            )
        ]

    def list_documents_in_collection(
        self, collection_id: str, offset: int, limit: int
    ) -> List[DocumentInfo]:
        """Fetch document metadata for documents in a collection.

        Args:
            collection_id:
                String id of the collection to filter by.
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.

        Returns:
            list of DocumentInfo: Metadata about each document.
        """
        return [
            DocumentInfo(**d)
            for d in self._db(
                "list_documents_in_collection", collection_id, offset, limit
            )
        ]

    def list_jobs(self) -> List[Job]:
        """List the user's jobs.

        Returns:
            list of Job:
        """
        return [Job(**d) for d in self._job(".list")]

    def list_recent_chat_sessions(
        self, offset: int, limit: int
    ) -> List[ChatSessionInfo]:
        """Fetch user's chat session metadata sorted by last update time.

        Chats across all collections will be accessed.

        Args:
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.

        Returns:
            list of ChatSessionInfo: Metadata about each chat session including the
            latest message.
        """
        return [
            ChatSessionInfo(**d)
            for d in self._db("list_recent_chat_sessions", offset, limit)
        ]

    def list_recent_collections(self, offset: int, limit: int) -> List[CollectionInfo]:
        """Fetch user's collection metadata sorted by last update time.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """
        return [
            CollectionInfo(**d)
            for d in self._db("list_recent_collections", offset, limit)
        ]

    def list_collection_permissions(self, collection_id: str) -> List[Permission]:
        """Returns a list of access permissions for a given collection.

        The returned list of permissions denotes who has access to
        the collection and their access level.

        Args:
            collection_id:
                ID of the collection to inspect.

        Returns:
            list of Permission: Sharing permissions list for the given collection.
        """
        return [
            Permission(**d)
            for d in self._db("list_collection_permissions", collection_id)
        ]

    def list_users(self, offset: int, limit: int) -> List[User]:
        """List system users.

        Returns a list of all registered users fo the system, a registered user,
        is a users that has logged in at least once.

        Args:
            offset:
                How many users to skip before returning.
            limit:
                How many users to return.

        Returns:
            list of User: Metadata about each user.
        """
        return [User(**d) for d in self._db("list_users", offset, limit)]

    def share_collection(
        self, collection_id: str, permission: Permission
    ) -> ShareResponseStatus:
        """Share a collection to a user.

        The permission attribute defined the level of access,
        and who can access the collection, the collection_id attribute
        denotes the collection to be shared.

        Args:
            collection_id:
                ID of the collection to share.
            permission:
                Defines the rule for sharing, i.e. permission level.

        Returns:
            ShareResponseStatus: Status of share request.
        """
        return ShareResponseStatus(
            **self._db("share_collection", collection_id, permission.username)
        )

    def unshare_collection(
        self, collection_id: str, permission: Permission
    ) -> ShareResponseStatus:
        """Remove sharing of a collection to a user.

        The permission attribute defined the level of access,
        and who can access the collection, the collection_id attribute
        denotes the collection to be shared.
        In case of un-sharing, the Permission's user is sufficient

        Args:
            collection_id:
                ID of the collection to un-share.
            permission:
                Defines the user for which collection access is revoked.

        ShareResponseStatus: Status of share request.
        """
        return ShareResponseStatus(
            **self._db("unshare_collection", collection_id, permission.username)
        )

    def unshare_collection_for_all(self, collection_id: str) -> ShareResponseStatus:
        """Remove sharing of a collection to all other users but the original owner

        Args:
            collection_id:
                ID of the collection to un-share.

        ShareResponseStatus: Status of share request.
        """
        return ShareResponseStatus(
            **self._db("unshare_collection_for_all", collection_id)
        )

    def make_collection_public(self, collection_id: str):
        """Make a collection public

        Once a collection is public, it will be accessible to all
        authenticated users of the system.

        Args:
            collection_id:
                ID of the collection to make public.
        """
        self._db("make_collection_public", collection_id)

    def list_recent_documents(self, offset: int, limit: int) -> List[DocumentInfo]:
        """Fetch user's document metadata sorted by last update time.

        All documents owned by the user, regardless of collection, are accessed.

        Args:
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.

        Returns:
            list of DocumentInfo: Metadata about each document.
        """
        return [
            DocumentInfo(**d) for d in self._db("list_recent_documents", offset, limit)
        ]

    def match_chunks(
        self,
        collection_id: str,
        vectors: List[List[float]],
        topics: List[str],
        offset: int,
        limit: int,
        cut_off: float = 0,
        width: int = 0,
    ) -> List[SearchResult]:
        """Find chunks related to a message using semantic search.

        Chunks are sorted by relevance and similarity score to the message.

        See Also: H2OGPTE.encode_for_retrieval to create vectors from messages.

        Args:
            collection_id:
                ID of the collection to search within.
            vectors:
                A list of vectorized message for running semantic search.
            topics:
                A list of document_ids used to filter which documents in the collection to search.
            offset:
                How many chunks to skip before returning chunks.
            limit:
                How many chunks to return.
            cut_off:
                Exclude matches with distances higher than this cut off.
            width:
                How many chunks before and after a match to return - not implemented.

        Returns:
            list of SearchResult: The document, text, score and related information of the chunk.
        """
        res = self._vex(
            "match_chunks",
            collection_id,
            vectors=vectors,
            topics=topics,
            offset=offset,
            limit=limit,
            cut_off=cut_off,
            width=width,
        )
        return SearchResults(**res).result

    def search_chunks(
        self, collection_id: str, query: str, topics: List[str], offset: int, limit: int
    ) -> List[SearchResult]:
        """Find chunks related to a message using lexical search.

        Chunks are sorted by relevance and similarity score to the message.

        Args:
            collection_id:
                ID of the collection to search within.
            query:
                Question or imperative from the end user to search a collection for.
            topics:
                A list of document_ids used to filter which documents in the collection to search.
            offset:
                How many chunks to skip before returning chunks.
            limit:
                How many chunks to return.

        Returns:
            list of SearchResult: The document, text, score and related information of the chunk.
        """
        res = self._vex(
            "search_chunks",
            collection_id,
            query=query,
            topics=topics,
            offset=offset,
            limit=limit,
        )
        return SearchResults(**res).result

    def set_chat_message_votes(self, chat_message_id: str, votes: int) -> Result:
        """Change the vote value of a chat message.

        Set the exact value of a vote for a chat message. Any message type can
        be updated, but only LLM response votes will be visible in the UI.
        The expectation is 0: unvoted, -1: dislike, 1 like. Values outside of this will
        not be viewable in the UI.

        Args:
            chat_message_id:
                ID of a chat message, any message can be used but only
                LLM responses will be visible in the UI.
            votes:
                Integer value for the message. Only -1 and 1 will be visible in the
                UI as dislike and like respectively.

        Returns:
            Result: The status of the update.

        Raises:
            Exception: The upload request was unsuccessful.
        """
        return Result(**self._db("set_chat_message_votes", chat_message_id, votes))

    def update_collection(self, collection_id: str, name: str, description: str) -> str:
        """Update the metadata for a given collection.

        All variables are required. You can use `h2ogpte.get_collection(<id>).name` or
        description to get the existing values if you only want to change one or the other.

        Args:
            collection_id:
                ID of the collection to update.
            name:
                New name of the collection, this is required.
            description:
                New description of the collection, this is required.

        Returns:
            str: ID of the updated collection.
        """
        return _to_id(self._db("update_collection", collection_id, name, description))

    def update_collection_prompt_settings(
        self,
        collection_id: str,
        system_prompt: str,
        pre_prompt_query: str,
        prompt_query: str,
        rag_type: str,
        hyde_no_rag_llm_prompt_extension: str,
        auto_gen_description_prompt: str,
    ) -> str:
        """Update the prompt settings for a given collection.

        Updates the prompt settings for a given collection.

        Args:
            collection_id:
                ID of the collection to update.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond.
            pre_prompt_query:
                Text that is prepended before the contextual document chunks.
            prompt_query:
                Text that is appended to the beginning of the user's message.
            rag_type:
                RAG type to use.
            hyde_no_rag_llm_prompt_extension:
                LLM prompt extension.
            auto_gen_description_prompt:
                prompt to create a description of the collection.

        Returns:
            str: ID of the updated collection.
        """
        return _to_id(
            self._db(
                "update_collection_prompt_settings",
                collection_id,
                system_prompt,
                pre_prompt_query,
                prompt_query,
                rag_type,
                hyde_no_rag_llm_prompt_extension,
                auto_gen_description_prompt,
            )
        )

    def reset_collection_prompt_settings(
        self,
        collection_id: str,
    ) -> str:
        """Reset the prompt settings for a given collection.

        Args:
            collection_id:
                ID of the collection to update.

        Returns:
            str: ID of the updated collection.
        """
        return _to_id(
            self._db(
                "reset_collection_prompt_settings",
                collection_id,
            )
        )

    def upload(self, file_name: str, file: Any) -> str:
        """Upload a file to the H2OGPTE backend.

        Uploaded files are not yet accessible and need to be ingested into a collection.

        See Also:
            ingest_uploads: Add the uploaded files to a collection.
            delete_upload: Delete uploaded file

        Args:
            file_name:
                What to name the file on the server, must include file extension.
            file:
                File object to upload, often an opened file from `with open(...) as f`.

        Returns:
            str: The upload id to be used in ingest jobs.

        Raises:
            Exception: The upload request was unsuccessful.
        """
        res = requests.put(
            f"{self._address}/rpc/fs",
            headers={
                "Authorization": self._auth_header,
            },
            files=dict(file=(file_name, file)),
            verify=self._verify,
        )
        if res.status_code != 200:
            raise Exception(f"HTTP error: {res.status_code} {res.reason}")
        return _to_id(unmarshal(res.text))

    def delete_upload(self, upload_id: str) -> str:
        """Delete a file previously uploaded with the "upload" method.

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            ingest_uploads: Add the uploaded files to a collection.

        Args:
            upload_id:
                ID of a file to remove

        Returns:
            upload_id: The upload id of the removed.

        Raises:
            Exception: The delete upload request was unsuccessful.
        """
        res = requests.delete(
            f"{self._address}/rpc/fs?id={upload_id}",
            headers={
                "Authorization": self._auth_header,
            },
            verify=self._verify,
        )
        if res.status_code != 200:
            raise Exception(f"HTTP error: {res.status_code} {res.reason}")
        return _to_id(unmarshal(res.text))

    def connect(self, chat_session_id: str) -> Session:
        """Create and participate in a chat session.

        This is a live connection to the H2OGPTE server contained to a specific
        chat session on top of a single collection of documents. Users will find all
        questions and responses in this session in a single chat history in the
        UI.

        Args:
            chat_session_id:
                ID of the chat session to connect to.

        Returns:
            Session: Live chat session connection with an LLM.

        """
        collection = self.get_collection_for_chat_session(chat_session_id)

        return Session(
            self._address,
            api_key=self._api_key,
            chat_session_id=chat_session_id,
            system_prompt=collection.system_prompt,
            pre_prompt_query=collection.pre_prompt_query,
            prompt_query=collection.prompt_query,
            rag_type=collection.rag_type,
            hyde_no_rag_llm_prompt_extension=collection.hyde_no_rag_llm_prompt_extension,
        )

    def get_llms(self) -> List[dict]:
        """Lists metadata information about available LLMs in the environment.

        Returns:
            list of dict (string, ANY): Name and details about each available model.

        """
        return self._lang("get_llms")

    def get_llm_names(self) -> List[str]:
        """Lists names of available LLMs in the environment.

        Returns:
            list of string: Name of each available model.

        """
        return self._lang("get_llm_names")


def _to_id(data: Dict[str, Any]) -> str:
    return Identifier(**data).id


def marshal(d):
    return json.dumps(d, allow_nan=False, separators=(",", ":"))


def unmarshal(s: str):
    return json.loads(s)
