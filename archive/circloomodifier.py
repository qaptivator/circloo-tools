
def x(x):
  return x - 820
def y(y):
  return y - 384

template = '''/
/ circloO level
/ Made with circloO Level Editor v1.2.1
/ EDITOR_TOOL 1 
/ EDITOR_VIEW 2300 1899 2.32
/ EDT 19138
levelscriptVersion 4
COLORS 123
grav 1 270
totalCircles 7 0
'''

class Level:
    def __init__(self, level=template):
        self.level = level
    def index_line(self, index=0):
        if index != -1:
            return self.level.splitlines()[index]
        # return self.level[index:]. partition('\n')[0]
    def index_object(self, index=0):
        return self.index_line(self.level.find('< ' + index))  
    def set_line(self, line='', options=[]):
        result = line.split(' ')[0]
        for value in options:
            result += ' ' + value
        return result + '\n'
    def set_level_options(self, options=[]):
        for key, value in options.items():
            found = self.level.find(key)
            if found != -1:
                pass
    def last_index(self):
        found = self.level.rfind('< ')
        if found != -1:
            return int(self.level[found + 2:found + 3])
        else:
            return 0
    def insert(self, type='', options=[]):
        result = ''
        match type:
            case 'circle':
                pass # c
            case 'block':
                pass # b
            case 'triangle':
                pass # t
            case 'line':
                pass # l_at
            case 'growing_circle':
                pass # gc
            case 'movable_circle':
                pass # mc
            case 'movable_block':
                pass # mb
            case 'movable_triangle':
                pass # mt
            case 'player':
                pass # bullet?
            case 'c_main':
                pass # ic 'i'
            case 'c_main_col':
                pass # ic 'io'
            case 'c_gravity':
                pass # ic 'ig'
            case 'c_gravity_col':
                pass # ic 'im'
            case 'c_size':
                pass # ic 'is'
            case 'c_size_col':
                pass # ic 'iso'
            case 'c_disconnect':
                pass # ic 'irb'
            case 'c_disconnect_col':
                pass # ic 'irbo'
            case _:
                return
        self.level += f'\n{result}\n< {self.last_index()}'