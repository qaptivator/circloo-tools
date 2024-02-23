# circloo-editor
# Python package for editing circloo levels

def x(x):
  return x - 820
def y(y):
  return y - 384

template = '''/
/ circloO level
/ Made with circloO Level Editor v1.3
totalCircles 7 0
/ EDITOR_TOOL 1 
/ EDITOR_VIEW 2252 1870.50 1.68
/ EDT 9523
/ _SAVE_TIME_1708537654000_END
levelscriptVersion 6
COLORS 29
grav 1 270
'''

class Level:
    level = []
    def __init__(self, level):
        if type(level) == str:
           pass
        else:
            self.level = level
