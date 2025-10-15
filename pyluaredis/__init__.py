from importlib.metadata import metadata, version, PackageNotFoundError
from pyluaredis.client import PyRedis
from pyluaredis.data_type_converter import TypeConverter

package_metadata = metadata('pyluaredis')

__author__ = package_metadata.get('Author', '')
__license__ = package_metadata.get('License', '')
__description__ = package_metadata.get('Summary', '')
__url__ = package_metadata.get('Home-page', '')

try:
    __version__ = version('pyluaredis')
except PackageNotFoundError:
    __version__ = 'No package metadata was found for pyluaredis'
