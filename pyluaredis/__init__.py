from importlib.metadata import metadata, version, PackageNotFoundError
from pyluaredis.client import PyRedis
from pyluaredis.data_type_converter import TypeConverter


try:
    package_metadata = metadata('pyluaredis')

    __author__ = package_metadata.get('Author', '')
    __license__ = package_metadata.get('License', '')
    __description__ = package_metadata.get('Summary', '')
    __url__ = package_metadata.get('Home-page', '')
    __version__ = version('pyluaredis')
except PackageNotFoundError:
    __version__ = 'No package metadata was found for pyluaredis'
    __license__ = 'No package metadata was found for pyluaredis'
    __description__ = 'No package metadata was found for pyluaredis'
    __url__ = 'No package metadata was found for pyluaredis'
