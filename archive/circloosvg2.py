import numpy as np
import xml.etree.ElementTree as ET
import math

def x(x):
  return x - 820
def y(y):
  return y - 384 # 554

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

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def quadratic_bezier(t=0, p0=Vector2(), p1=Vector2(), p2=Vector2()):
    return Vector2(
        (1 - t)**2 * p0.x + 2 * (1 - t) * t * p1.x + t**2 * p2.x,
        (1 - t)**2 * p0.y + 2 * (1 - t) * t * p1.y + t**2 * p2.y
    )

def cubic_bezier(t, p0, p1, p2, p3):
    return Vector2(
        (1 - t)**3 * p0.x + 3 * (1 - t)**2 * t * p1.x + 3 * (1 - t) * t**2 * p2.x + t**3 * p3.x,
        (1 - t)**3 * p0.y + 3 * (1 - t)**2 * t * p1.y + 3 * (1 - t) * t**2 * p2.y + t**3 * p3.y
    )

def parsesvg(level=template, xmlpath=''):
    result = level
    root = ET.parse(xmlpath).getroot()
    for child in root:
        match child.tag:
            case 'rect':
                result += f"b {child.get('x', 0)} {child.get('y', 0)} {child.get('width', 10)} {child.get('height', 10)}"
            case 'circle':
                result += f"c {child.get('cx', 0)} {child.get('cy', 0)} {child.get('r', 5)}"
            case 'line':
                result += f"l_at {child.get('x1', 0)} {child.get('y1', 0)} {child.get('x2', 0)} {child.get('y2', 0)} 2"
            case 'path':
                stuff = {child.get('d', '')}
            case _:
                print(f'<{child.tag}> tag is unsupported!')
    return result
