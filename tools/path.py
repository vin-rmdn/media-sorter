import platform

SEPARATOR = '\\' if platform.system() == 'Windows' else '/'

def Path(string):
    return string if string[-1] == SEPARATOR else string+SEPARATOR