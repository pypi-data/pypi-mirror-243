__all__ = (
    "download_file_to_local",
    "upload_file_from_local",
    "find_duplicate_nodes",
    "create_drive",
)


from contextlib import AsyncExitStack, asynccontextmanager
from collections.abc import AsyncIterable, Sequence, AsyncIterator
from logging import getLogger
from pathlib import Path, PurePath
from typing import BinaryIO
import asyncio
import os

from .exceptions import (
    InvalidDataError,
    InvalidArgumentError,
    InvalidServiceError,
    NodeExistsError,
    NodeNotFoundError,
    IsADirectoryError,
    TimeoutError,
    UnauthorizedError,
)
from .util import (
    else_none,
    is_valid_name,
    normalize_path,
    resolve_path,
)
from .types import (
    ChangeAction,
    CreateFileService,
    CreateFileServiceMiddleware,
    CreateService,
    CreateServiceMiddleware,
    CreateSnapshotService,
    CreateSnapshotServiceMiddleware,
    Drive,
    FileService,
    Hasher,
    MediaInfo,
    Node,
    ReadableFile,
    Service,
    SnapshotService,
    WritableFile,
)


API_VERSION = 4
DEFAULT_FILE_MIME_TYPE = "application/octet-stream"
_CHUNK_SIZE = 64 * 1024


@asynccontextmanager
async def create_drive(
    *,
    file: CreateFileService,
    snapshot: CreateSnapshotService,
    file_middleware: Sequence[CreateFileServiceMiddleware] | None = None,
    snapshot_middleware: Sequence[CreateSnapshotServiceMiddleware] | None = None,
) -> AsyncIterator[Drive]:
    async with _create_service(
        create_service=snapshot,
        middleware_list=snapshot_middleware,
    ) as snapshot_service, _create_service(
        create_service=file, middleware_list=file_middleware
    ) as file_service:
        yield _DefaultDrive(
            file_service=file_service, snapshot_service=snapshot_service
        )


@asynccontextmanager
async def _create_service[
    T: Service
](
    create_service: CreateService[T],
    middleware_list: Sequence[CreateServiceMiddleware[T]] | None,
):
    async with AsyncExitStack() as stack:
        service = await stack.enter_async_context(create_service())
        if service.api_version != API_VERSION:
            raise InvalidServiceError(
                f"invalid version: required {API_VERSION}, got {service.api_version}"
            )

        if not middleware_list:
            middleware_list = []

        for create_middleware in middleware_list:
            service = await stack.enter_async_context(create_middleware(service))
            if service.api_version != API_VERSION:
                raise InvalidServiceError(
                    f"invalid version: required {API_VERSION}, got {service.api_version}"
                )

        yield service


class _DefaultDrive(Drive):
    def __init__(
        self,
        *,
        file_service: FileService,
        snapshot_service: SnapshotService,
    ) -> None:
        self._sync_lock = asyncio.Lock()
        self._fs = file_service
        self._ss = snapshot_service

    async def get_root(self) -> Node:
        return await self._ss.get_root()

    async def get_node_by_id(self, node_id: str) -> Node:
        return await self._ss.get_node_by_id(node_id)

    async def get_node_by_path(self, path: PurePath) -> Node:
        path = normalize_path(path)
        return await self._ss.get_node_by_path(path)

    async def resolve_path(self, node: Node) -> PurePath:
        return await self._ss.resolve_path_by_id(node.id)

    async def get_child_by_name(
        self,
        name: str,
        parent: Node,
    ) -> Node:
        return await self._ss.get_child_by_name(name, parent.id)

    async def get_children(self, parent: Node) -> list[Node]:
        return await self._ss.get_children_by_id(parent.id)

    async def get_trashed_nodes(self, flatten: bool | None = False) -> list[Node]:
        rv = await self._ss.get_trashed_nodes()
        if flatten:
            return rv

        ancestor_set = set(_.id for _ in rv if _.is_directory)
        if not ancestor_set:
            return rv

        tmp: list[Node] = []
        for node in rv:
            if not await _in_ancestor_set(self, node, ancestor_set):
                tmp.append(node)
        return tmp

    async def find_nodes_by_regex(self, pattern: str) -> list[Node]:
        return await self._ss.find_nodes_by_regex(pattern)

    async def walk(
        self,
        node: Node,
        *,
        include_trashed: bool = False,
    ) -> AsyncIterable[tuple[Node, list[Node], list[Node]]]:
        if not node.is_directory:
            return
        q = [node]
        while q:
            node = q[0]
            del q[0]
            if not include_trashed and node.is_trashed:
                continue

            children = await self.get_children(node)
            directorys: list[Node] = []
            files: list[Node] = []
            for child in children:
                if not include_trashed and child.is_trashed:
                    continue
                if child.is_directory:
                    directorys.append(child)
                else:
                    files.append(child)
            yield node, directorys, files

            q.extend(directorys)

    async def create_directory(
        self,
        name: str,
        parent: Node,
        *,
        exist_ok: bool = False,
    ) -> Node:
        # sanity check
        if not parent.is_directory:
            raise InvalidArgumentError("parent is not a directory")
        if not name:
            raise InvalidArgumentError("directory name is empty")
        if not is_valid_name(name):
            raise InvalidArgumentError("no `/` or `\\` allowed in directory name")
        if not await self.is_authorized():
            raise UnauthorizedError()

        if not exist_ok:
            node = await else_none(
                self.get_child_by_name(
                    name,
                    parent,
                )
            )
            if node:
                raise NodeExistsError(node)

        return await self._fs.create_directory(
            name,
            parent,
            exist_ok=exist_ok,
            private=None,
        )

    @asynccontextmanager
    async def download_file(
        self, node: Node, *, timeout: float | None = None
    ) -> AsyncIterator[ReadableFile]:
        # sanity check
        if node.is_directory:
            raise InvalidArgumentError("node should be a file")
        if not await self.is_authorized():
            raise UnauthorizedError()

        async with self._fs.download_file(node, timeout=timeout) as file:
            yield file

    @asynccontextmanager
    async def upload_file(
        self,
        name: str,
        parent: Node,
        *,
        size: int | None = None,
        mime_type: str | None = None,
        media_info: MediaInfo | None = None,
        timeout: float | None = None,
    ) -> AsyncIterator[WritableFile]:
        # sanity check
        if not parent.is_directory:
            raise InvalidArgumentError("parent is not a directory")
        if not name:
            raise InvalidArgumentError("directory name is empty")
        if not is_valid_name(name):
            raise InvalidArgumentError("no `/` or `\\` allowed in directory name")
        if not await self.is_authorized():
            raise UnauthorizedError()

        node = await else_none(self.get_child_by_name(name, parent))
        if node:
            raise NodeExistsError(node)

        async with self._fs.upload_file(
            name,
            parent,
            size=size,
            mime_type=mime_type,
            media_info=media_info,
            private=None,
            timeout=timeout,
        ) as file:
            yield file

    async def trash(self, node: Node) -> None:
        # sanity check
        if not await self.is_authorized():
            raise UnauthorizedError()

        root_node = await self.get_root()
        if root_node.id == node.id:
            raise InvalidArgumentError("cannot discard root node")

        await self._fs.trash(node)

    async def move(
        self,
        node: Node,
        *,
        new_parent: Node | None = None,
        new_name: str | None = None,
    ) -> Node:
        # sanity check
        if node.is_trashed:
            raise InvalidArgumentError("source node is in trash")
        root_node = await self.get_root()
        if node.id == root_node.id:
            raise InvalidArgumentError("source node is the root node")
        if not await self.is_authorized():
            raise UnauthorizedError()

        if not new_parent and not new_name:
            raise InvalidArgumentError("need new_parent or new_name")

        if new_name and not is_valid_name(new_name):
            raise InvalidArgumentError("no `/` or `\\` allowed in file name")

        if new_parent:
            if new_parent.is_trashed:
                raise InvalidArgumentError("new_parent is in trash")
            if not new_parent.is_directory:
                raise InvalidArgumentError("new_parent is not a directory")
            if await _contains(self, node, new_parent):
                raise InvalidArgumentError(
                    "new_parent is a descendant of the source node"
                )

        return await self._fs.move(
            node,
            new_parent=new_parent,
            new_name=new_name,
        )

    async def sync(self) -> AsyncIterable[ChangeAction]:
        if not await self.is_authorized():
            raise UnauthorizedError()

        async with self._sync_lock:
            initial_cursor = await self._fs.get_initial_cursor()

            cursor = await self._ss.get_current_cursor()
            if not cursor:
                cursor = initial_cursor

            # no data before, get the root node and cache it
            if cursor == initial_cursor:
                node = await self._fs.get_root()
                await self._ss.set_root(node)

            async for changes, next_ in self._fs.get_changes(cursor):
                await self._ss.apply_changes(changes, next_)

                for change in changes:
                    yield change

    async def get_hasher(self) -> Hasher:
        return await self._fs.get_hasher()

    async def is_authorized(self) -> bool:
        return await self._fs.is_authorized()

    async def get_oauth_url(self) -> str:
        return await self._fs.get_oauth_url()

    async def set_oauth_token(self, token: str):
        return await self._fs.set_oauth_token(token)


async def download_file_to_local(
    drive: Drive,
    node: Node,
    path: Path,
    *,
    timeout: float | None = None,
) -> Path:
    if node.is_directory:
        raise InvalidArgumentError(f"cannot download a directory")

    if not path.is_dir():
        raise InvalidArgumentError(f"{path} is not a directory")

    # check if exists
    complete_path = path.joinpath(node.name)
    if complete_path.is_file():
        return complete_path

    # exists but not a file
    if complete_path.exists():
        raise IsADirectoryError(complete_path)

    # if the file is empty, no need to download
    if node.size <= 0:
        open(complete_path, "w").close()
        return complete_path

    # resume download
    tmp_path = complete_path.parent.joinpath(f"{complete_path.name}.__tmp__")
    if tmp_path.is_file():
        offset = tmp_path.stat().st_size
        if offset > node.size:
            raise InvalidDataError(
                f"local file size of `{complete_path}` is greater then remote"
                f" ({offset} > {node.size})"
            )
    elif tmp_path.exists():
        raise IsADirectoryError(complete_path)
    else:
        offset = 0

    if offset < node.size:
        async with drive.download_file(node, timeout=timeout) as fin:
            await fin.seek(offset)
            with open(tmp_path, "ab") as fout:
                await _download_retry(fin, fout)

    # rename it back if completed
    tmp_path.rename(complete_path)

    return complete_path


async def _download_retry(fin: ReadableFile, fout: BinaryIO) -> None:
    while True:
        try:
            async for chunk in fin:
                fout.write(chunk)
            break
        except TimeoutError:
            getLogger(__name__).exception("download timeout")

        offset = fout.tell()
        await fin.seek(offset)


async def upload_file_from_local(
    drive: Drive,
    path: Path,
    parent: Node,
    *,
    mime_type: str | None = None,
    media_info: MediaInfo | None = None,
    timeout: float | None = None,
) -> Node | None:
    # sanity check
    path = path.resolve()
    if not path.is_file():
        raise InvalidArgumentError("invalid file")

    file_name = path.name
    total_file_size = path.stat().st_size
    if not mime_type:
        mime_type = DEFAULT_FILE_MIME_TYPE

    async with drive.upload_file(
        name=file_name,
        parent=parent,
        size=total_file_size,
        mime_type=mime_type,
        media_info=media_info,
        timeout=timeout,
    ) as fout:
        with open(path, "rb") as fin:
            await _upload_retry(fin, fout)

    node = await fout.node()
    return node


async def _upload_retry(fin: BinaryIO, fout: WritableFile) -> None:
    while True:
        try:
            await _upload_feed(fin, fout)
            break
        except TimeoutError:
            getLogger(__name__).exception("upload timeout")

        await _upload_continue(fin, fout)


async def _upload_feed(fin: BinaryIO, fout: WritableFile) -> None:
    while True:
        chunk = fin.read(_CHUNK_SIZE)
        if not chunk:
            break
        await fout.write(chunk)


async def _upload_continue(fin: BinaryIO, fout: WritableFile) -> None:
    offset = await fout.tell()
    await fout.seek(offset)
    fin.seek(offset, os.SEEK_SET)


async def find_duplicate_nodes(
    drive: Drive,
    root_node: Node | None = None,
) -> list[list[Node]]:
    if not root_node:
        root_node = await drive.get_root()

    rv: list[list[Node]] = []
    async for _root, directorys, files in drive.walk(root_node):
        nodes = directorys + files
        seen: dict[str, list[Node]] = {}
        for node in nodes:
            if node.name not in seen:
                seen[node.name] = [node]
            else:
                seen[node.name].append(node)
        for nodes in seen.values():
            if len(nodes) > 1:
                rv.append(nodes)

    return rv


async def _in_ancestor_set(drive: Drive, node: Node, ancestor_set: set[str]) -> bool:
    if node.parent_id is None:
        return False
    parent = await drive.get_node_by_id(node.parent_id)
    if not parent:
        return False
    if parent.id in ancestor_set:
        return True
    included = await _in_ancestor_set(drive, parent, ancestor_set)
    if included:
        ancestor_set.add(parent.id)
    return included


async def _contains(drive: Drive, ancestor: Node, node: Node) -> bool:
    visited: set[str] = set()
    while True:
        if ancestor.id == node.id:
            # meet the ancestor
            return True
        if not node.parent_id:
            # reached the root but never meet the ancestor
            return False

        visited.add(node.id)
        node = await drive.get_node_by_id(node.parent_id)
        if node.id in visited:
            raise RuntimeError("detected node cycle")


async def move_node(
    drive: Drive,
    src_path: PurePath,
    dst_path: PurePath,
) -> Node:
    src_node = await drive.get_node_by_path(src_path)

    # case 1 - move to a relative path
    if not dst_path.is_absolute():
        # case 1.1 - a name, not path
        if dst_path.name == dst_path:
            # case 1.1.1 - move to the same directory, do nothing
            if dst_path.name == ".":
                return src_node
            # case 1.1.2 - rename only
            if dst_path.name != "..":
                return await drive.move(
                    src_node,
                    new_parent=None,
                    new_name=dst_path.name,
                )
            # case 1.1.3 - move to parent directory, the same as case 1.2

        # case 1.2 - a relative path, resolve to absolute path
        # NOTE PurePath does not implement normalizing algorithm
        dst_path = resolve_path(src_path.parent, dst_path)

    # case 2 - move to an absolute path
    dst_node = await else_none(drive.get_node_by_path(dst_path))
    # case 2.1 - the destination is empty
    if not dst_node:
        # move to the parent directory of the destination
        try:
            new_parent = await drive.get_node_by_path(dst_path.parent)
        except NodeNotFoundError as e:
            raise InvalidArgumentError(f"no direct path to {dst_path}") from e
        return await drive.move(src_node, new_parent=new_parent, new_name=dst_path.name)
    # case 2.2 - the destination is a file
    if not dst_node.is_directory:
        # do not overwrite existing file
        raise NodeExistsError(dst_node)
    # case 2.3 - the distination is a directory
    return await drive.move(src_node, new_parent=dst_node, new_name=None)
