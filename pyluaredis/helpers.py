""" Helper methods for the PyRedis object """
from os import path as os_path

from pyluaredis.data_type_converter import TypeConverter


def _load_lua_script_from_file(filename: str) -> str:
	""" Load Lua script from a file """
	with open(
			os_path.join(os_path.dirname(__file__), f'lua_scripts/{filename}.lua'),
			'r', encoding='utf-8'
	) as lua_file:
		return lua_file.read()


def _convert_to_type(value: str | list[str] | set[str], _type: str) -> str | bool | int | float | list | set:
	return TypeConverter().converter(value, _type)


def _compare_and_select_sec_ms(time_s: int | None, time_ms: int | None) -> int | None:
	"""
	If both seconds and milliseconds are specified,
	the time is converted to milliseconds and the smallest one is selected
	"""
	if not (time_s or time_ms):
		return None

	if not time_s or not time_ms:
		return time_s * 1_000 if time_s else time_ms

	return min(time_s * 1_000, time_ms)


def _remove_duplicates(iterable_var: list | tuple | set | frozenset) -> tuple:
	if isinstance(iterable_var, (set, frozenset)):
		return tuple(iterable_var)
	return tuple(set(iterable_var))
