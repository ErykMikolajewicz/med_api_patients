class InvalidVisitDate(Exception):
    """Raised when appointment start or end date is beyond specialist working time"""
    pass


class TooShortTimeToCancel(Exception):
    """Raised when appointment is to close (business requirements) to cancel."""
    pass


class NotFound(Exception):
    """Raised when appointment is not found in database."""
    pass


class InsufficientPrivileges(Exception):
    """Raised when privileges to execute action on appointment are invalid."""
    pass
