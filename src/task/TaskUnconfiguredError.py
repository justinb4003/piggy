class TaskUnconfiguredError(Exception):
    """Thrown when a task is asked to run before import_as_dict() has run"""
    pass
