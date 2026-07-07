"""Exceptions related to user operations."""


class UserNotFound(Exception):
    pass

class UserAlreadyExists(Exception):
    pass