__all__ = (
    "ChangeAction",
    "CreateFileService",
    "CreateFileServiceMiddleware",
    "CreateSnapshotService",
    "CreateSnapshotServiceMiddleware",
    "FileService",
    "Hasher",
    "ImageDict",
    "MediaInfo",
    "Node",
    "PrivateDict",
    "ReadableFile",
    "RemoveAction",
    "UpdateAction",
    "VideoDict",
    "WritableFile",
)


from abc import ABCMeta, abstractmethod
from collections.abc import (
    AsyncIterable,
    Callable,
)
from contextlib import AbstractAsyncContextManager
from datetime import datetime
from pathlib import PurePath
from typing import (
    Literal,
    Self,
    TypedDict,
)


class ImageDict(TypedDict):
    width: int
    height: int


class VideoDict(TypedDict):
    width: int
    height: int
    ms_duration: int


type PrivateDict = dict[str, str]


class Node(metaclass=ABCMeta):
    @property
    @abstractmethod
    def id(self) -> str:
        ...

    @property
    @abstractmethod
    def parent_id(self) -> str | None:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def is_folder(self) -> bool:
        ...

    @property
    @abstractmethod
    def trashed(self) -> bool:
        ...

    @property
    @abstractmethod
    def ctime(self) -> datetime:
        ...

    @property
    @abstractmethod
    def mtime(self) -> datetime:
        ...

    @property
    @abstractmethod
    def mime_type(self) -> str | None:
        ...

    @property
    @abstractmethod
    def hash(self) -> str:
        ...

    @property
    @abstractmethod
    def size(self) -> int:
        ...

    @property
    @abstractmethod
    def is_image(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_video(self) -> bool:
        ...

    @property
    @abstractmethod
    def width(self) -> int:
        ...

    @property
    @abstractmethod
    def height(self) -> int:
        ...

    @property
    @abstractmethod
    def ms_duration(self) -> int:
        ...

    @property
    @abstractmethod
    def private(self) -> PrivateDict | None:
        ...


type RemoveAction = tuple[Literal[True], str]
type UpdateAction = tuple[Literal[False], Node]
type ChangeAction = RemoveAction | UpdateAction


class MediaInfo(object):
    @staticmethod
    def image(width: int, height: int) -> "MediaInfo":
        return MediaInfo(is_image=True, width=width, height=height)

    @staticmethod
    def video(width: int, height: int, ms_duration: int) -> "MediaInfo":
        return MediaInfo(
            is_video=True,
            width=width,
            height=height,
            ms_duration=ms_duration,
        )

    def __init__(
        self,
        *,
        is_image: bool = False,
        is_video: bool = False,
        width: int = 0,
        height: int = 0,
        ms_duration: int = 0,
    ) -> None:
        self._is_image = is_image
        self._is_video = is_video
        self._width = width
        self._height = height
        self._ms_duration = ms_duration

    def __str__(self) -> str:
        if self.is_image:
            return f"MediaInfo(is_image=True, width={self.width}, height={self.height})"
        if self.is_video:
            return f"MediaInfo(is_video=True, width={self.width}, height={self.height}, ms_duration={self.ms_duration})"
        return "MediaInfo()"

    @property
    def is_image(self) -> bool:
        return self._is_image

    @property
    def is_video(self) -> bool:
        return self._is_video

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def ms_duration(self) -> int:
        return self._ms_duration


class ReadableFile(AsyncIterable[bytes], metaclass=ABCMeta):
    """
    An async readable file interface.
    """

    @abstractmethod
    async def read(self, length: int) -> bytes:
        """
        Read at most `length` bytes.
        """

    @abstractmethod
    async def seek(self, offset: int) -> int:
        """
        Seek to `offset` position. Always starts from the begining.
        """

    @abstractmethod
    async def node(self) -> Node:
        """
        Get the node being read.
        """


class Hasher(metaclass=ABCMeta):
    """
    Hash calculator.

    MUST be pickleable to work with multi-processes.
    """

    @abstractmethod
    def update(self, data: bytes) -> None:
        """
        Put `data` into the stream.
        """

    @abstractmethod
    def digest(self) -> bytes:
        """
        Get raw digest.
        """

    @abstractmethod
    def hexdigest(self) -> str:
        """
        Get hex digest.
        """

    @abstractmethod
    def copy(self) -> Self:
        """
        Return a copy to self. Does not require clone the state.
        """


class WritableFile(metaclass=ABCMeta):
    """
    An async writable file interface.
    """

    @abstractmethod
    async def tell(self) -> int:
        """
        Get current position.
        """

    @abstractmethod
    async def seek(self, offset: int) -> int:
        """
        Seek to `offset` position. Always starts from the begining.
        """

    @abstractmethod
    async def write(self, chunk: bytes) -> int:
        """
        Writes `chunk` to the stream.
        Returns actual written byte length.
        """

    @abstractmethod
    async def node(self) -> Node | None:
        """
        Get the wrote node. May be `None` if write failed.
        """


class Service(metaclass=ABCMeta):
    @property
    @abstractmethod
    def api_version(self) -> int:
        """
        Get competible API version for this class.
        """


type CreateService[T: Service] = Callable[[], AbstractAsyncContextManager[T]]
type CreateServiceMiddleware[T: Service] = Callable[[T], AbstractAsyncContextManager[T]]


class FileService(Service, metaclass=ABCMeta):
    """
    Provides actions to cloud drives.
    """

    @abstractmethod
    async def get_initial_cursor(self) -> str:
        """
        Get the initial check point.
        """

    @abstractmethod
    async def get_root(self) -> Node:
        """
        Fetch the root node.
        """

    @abstractmethod
    def get_changes(
        self,
        cursor: str,
    ) -> AsyncIterable[tuple[list[ChangeAction], str]]:
        """
        Fetch changes starts from `cursor`.

        Will be used like this:
        ```
        async for changes, next_cursor in self.fetch_changes('...'):
            ...
        ```
        So you should yield a page for every iteration.
        """

    @abstractmethod
    async def move(
        self,
        node: Node,
        *,
        new_parent: Node | None,
        new_name: str | None,
    ) -> Node:
        """
        Rename a node, or move to another folder, or do both.

        `node` is the node to be modified.

        `new_parent` is the new parent folder. `None` means don't move the node.

        `new_name` is the new node name. `None` means don't rename the node.
        """

    @abstractmethod
    async def trash(self, node: Node) -> None:
        """
        Trash the node.

        Should raise exception if failed.
        """

    @abstractmethod
    async def create_folder(
        self,
        folder_name: str,
        parent: Node,
        *,
        exist_ok: bool,
        private: PrivateDict | None,
    ) -> Node:
        """
        Create a folder.

        `parent_node` should be a folder you want to put this folder in.

        `folder_name` will be the name of the folder.

        `private` is an optional metadata, you can decide how to place this for
        each services.

        If `exist_ok` is `False`, you should not create the folder if it is
        already exists, and raise an exception.

        Will return the created node.
        """

    @abstractmethod
    def download_file(self, node: Node) -> AbstractAsyncContextManager[ReadableFile]:
        """
        Download the node.

        Will return a `ReadableFile` which is a file-like object.
        """

    @abstractmethod
    def upload_file(
        self,
        file_name: str,
        parent: Node,
        *,
        file_size: int | None,
        mime_type: str | None,
        media_info: MediaInfo | None,
        private: PrivateDict | None,
    ) -> AbstractAsyncContextManager[WritableFile]:
        """
        Upload a file.

        `parent_node` is the target folder.

        `file_name` is required.

        `file_size` can be `None`, for cases that the file size is unavailable.
        e.g. The uploading file is from a stream.

        `mime_type`, `media_info` and `private` are optional. It is your choice
        to decide how to place these properties.
        """

    @abstractmethod
    async def get_hasher(self) -> Hasher:
        """
        Get a hash calculator.
        """

    @abstractmethod
    async def is_authorized(self) -> bool:
        """
        Is OAuth 2.0 authorized.
        """

    @abstractmethod
    async def get_oauth_url(self) -> str:
        """
        Get OAuth 2.0 URL.
        """

    @abstractmethod
    async def set_oauth_token(self, token: str) -> None:
        """
        Set OAuth 2.0 token.
        """


type CreateFileService = CreateService[FileService]
type CreateFileServiceMiddleware = CreateServiceMiddleware[FileService]


class SnapshotService(Service, metaclass=ABCMeta):
    """
    Provides actions to cache file metadata.
    """

    @abstractmethod
    async def get_root(self) -> Node:
        """
        Get root folder as Node.
        """

    @abstractmethod
    async def set_root(self, node: Node) -> None:
        """
        Set root folder to the snapshot.
        """

    @abstractmethod
    async def get_current_cursor(self) -> str:
        """
        Get the current cursor. If no cursor present (e.g. the first run),
        should return an empty string.
        """

    @abstractmethod
    async def get_node_by_id(self, node_id: str) -> Node:
        """
        Get node by ID.
        """

    @abstractmethod
    async def get_node_by_path(self, path: PurePath) -> Node:
        """
        Resolve node by file path.
        """

    @abstractmethod
    async def resolve_path_by_id(self, node_id: str) -> PurePath:
        """
        Resolve absolute path by ID.
        """

    @abstractmethod
    async def get_child_by_name(self, name: str, parent_id: str) -> Node:
        """
        Get a child under the given parent by name.
        """

    @abstractmethod
    async def get_children_by_id(self, parent_id: str) -> list[Node]:
        """
        Get first-level children under a node.
        """

    @abstractmethod
    async def get_trashed_nodes(self) -> list[Node]:
        """
        Get trashed nodes.
        """

    @abstractmethod
    async def apply_changes(
        self,
        changes: list[ChangeAction],
        cursor: str,
    ) -> None:
        """
        Apply the given changes to the snapshot.
        """

    @abstractmethod
    async def find_nodes_by_regex(self, pattern: str) -> list[Node]:
        """
        Find node by regex.
        """


type CreateSnapshotService = CreateService[SnapshotService]
type CreateSnapshotServiceMiddleware = CreateServiceMiddleware[SnapshotService]


class Drive(metaclass=ABCMeta):
    """
    Interact with the drive.
    """

    @abstractmethod
    async def get_root(self) -> Node:
        """Get the root node."""

    @abstractmethod
    async def get_node_by_id(self, node_id: str) -> Node:
        """Get node by node id."""

    @abstractmethod
    async def get_node_by_path(self, path: PurePath) -> Node:
        """Get node by absolute path."""

    @abstractmethod
    async def resolve_path(self, node: Node) -> PurePath:
        """Resolve absolute path of the node."""

    @abstractmethod
    async def get_child_by_name(
        self,
        name: str,
        parent: Node,
    ) -> Node:
        """Get node by given name and parent."""

    @abstractmethod
    async def get_children(self, parent: Node) -> list[Node]:
        """Get the child node list of given node."""

    @abstractmethod
    async def get_trashed_nodes(self, flatten: bool = False) -> list[Node]:
        """Get trashed node list."""

    @abstractmethod
    async def find_nodes_by_regex(self, pattern: str) -> list[Node]:
        """Find nodes by name."""

    @abstractmethod
    def walk(
        self,
        node: Node,
        *,
        include_trashed: bool = False,
    ) -> AsyncIterable[tuple[Node, list[Node], list[Node]]]:
        """Traverse nodes from given node."""

    @abstractmethod
    async def create_folder(
        self,
        folder_name: str,
        parent: Node,
        *,
        exist_ok: bool = False,
    ) -> Node:
        """Create a folder."""

    @abstractmethod
    def download_file(self, node: Node) -> AbstractAsyncContextManager[ReadableFile]:
        """Download file."""

    @abstractmethod
    def upload_file(
        self,
        file_name: str,
        parent: Node,
        *,
        file_size: int | None = None,
        mime_type: str | None = None,
        media_info: MediaInfo | None = None,
    ) -> AbstractAsyncContextManager[WritableFile]:
        """Upload file."""

    @abstractmethod
    async def trash(self, node: Node) -> None:
        """Move the node to trash."""

    @abstractmethod
    async def move(
        self,
        node: Node,
        *,
        new_parent: Node | None = None,
        new_name: str | None = None,
    ) -> Node:
        """Move or rename the node."""

    @abstractmethod
    def sync(self) -> AsyncIterable[ChangeAction]:
        """Synchronize the snapshot.

        This is the ONLY function which will modify the snapshot.
        """

    @abstractmethod
    async def get_hasher(self) -> Hasher:
        """Get a Hasher instance for checksum calculation."""

    @abstractmethod
    async def is_authorized(self) -> bool:
        """Is the drive authorized."""

    @abstractmethod
    async def get_oauth_url(self) -> str:
        """Get OAuth 2.0 URL"""

    @abstractmethod
    async def set_oauth_token(self, token: str) -> None:
        """Set OAuth 2.0 token"""
