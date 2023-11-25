import io

class StreamPeek():
    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.buffer = io.StringIO()
        self.pending_buffer = False

    def peek(self, lines=1):
        line = self.file_obj.readline()
        self.buffer.write(line)
        self.pending_buffer = True
        return line

    def read(self, *args, **kwargs):
        if self.pending_buffer:
            self.buffer.seek(0)
            self.pending_buffer = False
            return self.buffer.read(*args, **kwargs)
        return self.file_obj.read(*args, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        if self.pending_buffer:
            self.buffer.seek(0)
            self.pending_buffer = False
            result = self.buffer.read()
            if result == '':
                raise StopIteration
            return result

        result = self.file_obj.readline()
        if result == '':
            raise StopIteration
        return result

class DotWrapper(object):
    """Used for wrapping a delegate object for dot access"""
    def __init__(self, target):
        self.__target__ = target

    def get_target(self):
        return self.__dict__['__target__']

    def __getattr__(self, attr):
        if attr == ('__target__', 'get_target'):
            return self.__dict__.get('__target__', None)
        if hasattr(self.__target__, 'get'):
            return self.__target__.get(attr)
        else:
            return getattr(self.__target__, attr)

    def __getitem__(self, attr):
        return self.__target__.__getitem__(attr)

    def __setattr__(self, key, value):
        if key == '__target__':
            self.__dict__['__target__'] = value
        else:
            self.__target__.__setitem__(key, value)

    def __setitem__(self, key, value):
        self.__target__.__setitem__(key, value)

    def __delattr__(self, item):
        self.__target__.__delitem__(item)

    def __delitem__(self, key):
        del self.__target__[key]

class PowerSelector():
    EMPTY = type('Empty', (), {})

    def __init__(self, selector):
        self.selector = selector
        self.segments = selector.split('.')

    def get(self, obj, default=None):
        ref = obj
        for segment in self.segments:
            if type(ref) == dict:
                result = ref.get(segment, self.EMPTY)
            else:
                result = getattr(ref, segment, self.EMPTY)
            if result is self.EMPTY:
                return default
            ref = result
        return ref

    def set(self, obj, value):
        # Clone for special handling
        segments = list(self.segments)
        attribute = segments.pop()

        root = obj
        if root is None:
            root = {}
        ref = root
        for segment in segments:
            if type(ref) == dict:
                if not segment in ref:
                    new_ref = {}
                    ref[segment] = new_ref
                    ref = new_ref
                else:
                    ref = ref.get(segment)
            else:
                return root
        if type(ref) == dict:
            if value == self.EMPTY:
                ref.pop(attribute) 
            else:
                ref[attribute] = value

        return root

    def append(self, obj, value):
        current_value = self.get(obj)
        if current_value is None:
            new_value = [value]
        elif type(current_value) == list:
            current_value.append(value)
        else: 
            new_value = [current_value, value]
        new_root = self.set(obj, new_value)
        return new_root

def py_executor(code, statement=False):
    expression = not statement
    runner = exec if statement else eval
    bytecode = compile(code, '<string::transform>', runner.__name__)

    def exec_with_context(context):
        scope = {**globals(), **context}
        try:
            result = runner(bytecode, scope, scope)
        except Exception as e:
            result = None
        return scope, result
    return exec_with_context
