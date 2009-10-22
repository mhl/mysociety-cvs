"""Exceptions in a separate module to avoid circular imports.
"""
class StorageError(Exception):
    """An error occurred when accessing storage."""

class AlreadyQueuedError(Exception):
    """The details asked for are already in the queue."""
