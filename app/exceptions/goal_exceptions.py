"""Exceptions related to goal operations."""


class GoalNotFound(Exception):
    pass

class GoalAlreadyExists(Exception):
    pass

class GoalTargetAmountExceeded(Exception):
    pass