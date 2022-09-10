import ctypes, sys


def represent_type(target):
	name = target.__class__.__qualname__
	if isinstance(target, ctypes.Structure):
		values = ', '.join(f'{name}={getattr(target, name)!r}'  for (name, type) in target._fields_)
		return f'{name}({values})'
	else:
		return f'{target.value!r}'

common_scope = dict(
	__repr__ = represent_type,
)

def create_c_type(name, ctypes_name):
	return type(name, (getattr(ctypes, ctypes_name),), common_scope)

def create_c_typedef(name, source):
	return type(name, (source,), common_scope)

def create_c_struct(name, **members):
	return type(name, (ctypes.Structure,), dict(
		_fields_ = tuple(members.items()),
		**common_scope
	))

def create_c_function(library, name, return_type, **parameters):
	#TODO - possibly create a function definition that contains more information about arguments etc
	library_function = getattr(library, name)
	library_function.argtypes = tuple(parameters.values())
	library_function.restype = return_type

	return library_function

def c_type(name, ctypes_name):
	sys._getframe(1).f_locals[name] = create_c_type(name, ctypes_name)

def c_typedef(name, source):
	sys._getframe(1).f_locals[name] = create_c_typedef(name, source)

def c_struct(name, **members):
	sys._getframe(1).f_locals[name] = create_c_struct(name, **members)

def c_function(library, name, return_type, **parameters):
	sys._getframe(1).f_locals[name] = create_c_function(library, name, return_type, **parameters)



c_lib = ctypes.CDLL
c_pointer = ctypes.POINTER