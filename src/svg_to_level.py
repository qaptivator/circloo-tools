from circlib import Level
from svgpathtools import svg2paths2, wsvg, parse_path
import re

def extract_num(v):
    return ''.join(re.findall(r'\d+', v))

def parse_svg(svg_content='', cpos=(1500,1500)):
    paths, attrs, svg_attrs = svg2paths2(svg_content)
    svg_w, svg_h = svg_attrs['width'], svg_attrs['height']
    pos_w, pos_h = cpos
    def offset_x(x):
      return pos_w - float(extract_num(svg_w)) + x
    def offset_y(y):
      return pos_h - float(extract_num(svg_h)) + y
    def offset_pos(pos):
      return [offset_x(pos.real), offset_y(pos.imag)]

    level = Level()

    for path in paths:
      parsed_path = parse_path(path.d())
      for el in parsed_path:
        match el.__class__.__name__:
          case 'Line':
            level.create_object('line',
              offset_pos(el.start) +
              offset_pos(el.end) + [2]
            )
          case 'CubicBezier':
            level.create_object('bezier_curve',
              offset_pos(el.start) +
              offset_pos(el.control1) +
              offset_pos(el.control2) +
              offset_pos(el.end) + [2, 100]
            )
          #case 'QuadraticBezier':
          #  return
          #  curves = cubic_to_quad(*(offset_pos(el.start) + offset_pos(el.control) + offset_pos(el.end)), 0.1)
          #  for i in range(len(curves) // 6):
          #    level.create_object('bezier_curve', [
          #      curves[i],
          #      curves[i + 1],
          #      curves[i + 2],
          #      curves[i + 3],
          #      curves[i + 4],
          #      curves[i + 5],
          #      2,
          #      100
          #    ])

    return level

def main():
    res = parse_svg(input('Path to SVG file: ')) #input('Center position (leave blank for default center): '))
    print(res.stringify())

if __name__ == '__main__':
    main()