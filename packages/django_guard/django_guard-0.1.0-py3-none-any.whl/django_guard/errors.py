class BaseException(Exception):
    """all expceptions should inherit from this class"""
    pass


class SettingsException(BaseException):
    """raised when settings are not set"""
    pass