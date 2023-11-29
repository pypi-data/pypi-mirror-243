"""
Main interface for inspector-scan service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_inspector_scan import (
        Client,
        inspectorscanClient,
    )

    session = Session()
    client: inspectorscanClient = session.client("inspector-scan")
    ```
"""

from .client import inspectorscanClient

Client = inspectorscanClient


__all__ = ("Client", "inspectorscanClient")
