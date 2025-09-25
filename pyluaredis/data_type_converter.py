class TypeConverter:
	"""
	Class providing methods for converting data
	"""
	__slots__ = ('data_type_names', 'true_equals', 'false_equals', 'boolean_equals')

	def __init__(self):
		self.data_type_names: dict[str, type] = {
			'int': int,
			'integer': int,
			'float': float,
			'double': float,
			'numeric': float,
			'bool': bool,
			'boolean': bool,
			'bytes': bytes
		}

		self.true_equals = ('1', 'True', 'true')
		self.false_equals = ('0', 'False', 'false', '')
		self.boolean_equals = (*self.true_equals, *self.false_equals)

	def converter(self, value: str | list[str] | set[str], _type: str):
		type_check: tuple = tuple(_type.split('_', 1))

		type_len = len(type_check)
		extended = True if type_len == 2 and type_check[1] == 'any' and type_check[0] != 'bytes' else False
		encoding = type_check[1] if type_len == 2 and type_check[0] == 'bytes' and type_check[1] != 'any' else 'utf-8'
		_type = self.data_type_names.get(type_check[0]) if type_len in (1, 2) else None
		if _type is None:
			return value

		# If try to convert an array of type ['True', 'False'] to type bool,
		# then need to iterate over each element
		# Which makes the conversion for such an array the most expensive function
		if _type is bool and extended is False and isinstance(value, (list, set)):
			if set(value).intersection(set(self.boolean_equals)):
				extended = True

		return self.convert_to_type(value, _type) if not extended and _type is not bytes \
			else self.convert_to_type_extended(value, _type, encoding)

	def convert_to_type(self, value: str | list[str] | set[str], _type: type):
		"""
		Conversion on the principle of "all or nothing"
		"""
		if isinstance(value, (list, set)):
			try:
				return list(map(_type, value)) if isinstance(value, list) else set(map(_type, value))
			except (ValueError, TypeError):
				return value

		return self.__helper_convert_to_type(value, _type)

	def convert_to_type_extended(self, value: str | list[str] | set[str], _type: type, encoding: str):
		"""
		Array conversion is performed for each element separately
		"""
		if isinstance(value, (list, set)):
			return [self.__helper_convert_to_type(i, _type, encoding) for i in value] \
				if isinstance(value, list) \
				else {self.__helper_convert_to_type(i, _type, encoding) for i in value}

		return self.__helper_convert_to_type(value, _type, encoding)

	def __helper_convert_to_type(self, value: str, _type, encoding: str = 'utf-8'):
		try:
			if _type is int:
				if '.' in value:
					# if it`s float, then before converting it`s necessary to slice the fractional part from the string
					idx: int = value.find('.')
					value: str = value[:idx]
				value: int = int(value)
			elif _type is float:
				value: float = float(value)
			elif _type is bool:
				value: bool | str = (value in self.true_equals) if value in self.boolean_equals else value
			elif _type is bytes:
				value: bytes = value.encode(encoding)
		except (ValueError, TypeError):
			pass
		return value
