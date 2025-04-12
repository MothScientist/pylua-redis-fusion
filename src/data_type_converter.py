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
		}

		self.true_equals = ('1', 'True', 'true')
		self.false_equals = ('0', 'False', 'false', '')
		self.boolean_equals = (*self.true_equals, *self.false_equals)

	def converter(self, value: str | list[str] | set[str], _type: str):
		type_check: tuple = tuple(_type.split('_', 1))

		extended = True if len(type_check) == 2 and type_check[1] == 'any' else False
		_type = self.data_type_names.get(type_check[0]) if len(type_check) in (1, 2) else None
		if _type is None:
			return value

		# If try to convert an array of type ['True', 'False'] to type bool,
		# then need to iterate over each element
		# Which makes the conversion for such an array the most expensive function
		if _type is bool and extended is False and isinstance(value, (list, set)):
			if set(value).intersection(set(self.boolean_equals)):
				extended = True

		return self.convert_to_type(value, _type) if not extended \
			else self.convert_to_type_extended(value, _type)

	def convert_to_type(self, value: str | list[str] | set[str], _type):
		"""
		Conversion on the principle of "all or nothing"
		"""
		if isinstance(value, (list, set)):
			try:
				return list(map(_type, value)) if isinstance(value, list) else set(map(_type, value))
			except (ValueError, TypeError):
				return value

		return self.__helper_convert_to_type(value, _type)

	def convert_to_type_extended(self, value: str | list[str] | set[str], _type):
		"""
		Array conversion is performed for each element separately
		"""
		if isinstance(value, (list, set)):
			return [self.__helper_convert_to_type(i, _type) for i in value] \
				if isinstance(value, list) \
				else {self.__helper_convert_to_type(i, _type) for i in value}

		return self.__helper_convert_to_type(value, _type)

	def __helper_convert_to_type(self, value: str | list[str] | set[str], _type):
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
		except (ValueError, TypeError):
			pass
		return value
