from .types import Node


class DriveError(Exception):
    pass


class InvalidServiceError(DriveError):
    pass


class InvalidArgumentError(DriveError):
    pass


class NodeConflictedError(DriveError):
    def __init__(self, node: Node) -> None:
        super().__init__(f"node already exists: {node.name}")
        self.node = node


class NodeNotFoundError(DriveError):
    def __init__(self, id: str) -> None:
        super().__init__(f"node not found: {id}")
        self.id = id


class UnauthorizedError(DriveError):
    pass


class DownloadError(DriveError):
    pass


class UploadError(DriveError):
    pass
