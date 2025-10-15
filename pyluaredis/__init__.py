from importlib.metadata import version, PackageNotFoundError
from pyluaredis.client import PyRedis
from pyluaredis.data_type_converter import TypeConverter


try:
    __version__ = version('pyluaredis')
except PackageNotFoundError:
    __version__ = 'No package metadata was found for pyluaredis'
