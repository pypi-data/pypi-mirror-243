"""
Main interface for backupstorage service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_backupstorage import (
        BackupStorageClient,
        Client,
    )

    session = Session()
    client: BackupStorageClient = session.client("backupstorage")
    ```
"""

from .client import BackupStorageClient

Client = BackupStorageClient


__all__ = ("BackupStorageClient", "Client")
