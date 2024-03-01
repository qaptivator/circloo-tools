import math

# Aproximates cubic bezier curves with quadratic ones.
# Converted from Javascript to Python.
# Source: https://github.com/fontello/cubic2quad/tree/master
# Was another candidate: https://github.com/googlefonts/cu2qu/tree/main

# Precision used to check determinant in quad and cubic solvers,
# any number lower than this is considered to be zero.
# `8.67e-19` is an example of real error occurring in tests.
epsilon = 1e-16

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def sub(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def mul(self, value):
        return Point(self.x * value, self.y * value)

    def div(self, value):
        return Point(self.x / value, self.y / value)

    def sqr(self):
        return self.x * self.x + self.y * self.y

    def dot(self, point):
        return self.x * point.x + self.y * point.y

def calc_power_coefficients(p1, c1, c2, p2):
    # point(t) = p1*(1-t)^3 + c1*t*(1-t)^2 + c2*t^2*(1-t) + p2*t^3 = a*t^3 + b*t^2 + c*t + d
    # for each t value, so
    # a = (p2 - p1) + 3 * (c1 - c2)
    # b = 3 * (p1 + c2) - 6 * c1
    # c = 3 * (c1 - p1)
    # d = p1
    a = p2.sub(p1).add(c1.sub(c2).mul(3))
    b = p1.add(c2).mul(3).sub(c1.mul(6))
    c = c1.sub(p1).mul(3)
    d = p1
    return [a, b, c, d]

def calc_power_coefficients_quad(p1, c1, p2):
    # point(t) = p1*(1-t)^2 + c1*t*(1-t) + p2*t^2 = a*t^2 + b*t + c
    # for each t value, so
    # a = p1 + p2 - 2 * c1
    # b = 2 * (c1 - p1)
    # c = p1
    a = c1.mul(-2).add(p1).add(p2)
    b = c1.sub(p1).mul(2)
    c = p1
    return [a, b, c]

def calc_point(a, b, c, d, t):
    # a*t^3 + b*t^2 + c*t + d = ((a*t + b)*t + c)*t + d
    return a.mul(t).add(b).mul(t).add(c).mul(t).add(d)

def calc_point_quad(a, b, c, t):
    # a*t^2 + b*t + c = (a*t + b)*t + c
    return a.mul(t).add(b).mul(t).add(c)

def calc_point_derivative(a, b, c, d, t):
    # d/dt[a*t^3 + b*t^2 + c*t + d] = 3*a*t^2 + 2*b*t + c = (3*a*t + 2*b)*t + c
    return a.mul(3 * t).add(b.mul(2)).mul(t).add(c)

def quad_solve(a, b, c):
    # a*x^2 + b*x + c = 0
    if a == 0:
        return [] if b == 0 else [-c / b]
    D = b * b - 4 * a * c
    if abs(D) < epsilon:
        return [-b / (2 * a)]
    elif D < 0:
        return []
    DSqrt = math.sqrt(D)
    return [(-b - DSqrt) / (2 * a), (-b + DSqrt) / (2 * a)]





def min_distance_to_line_sq(point, p1, p2):
    p1p2 = p2.sub(p1)
    dot = point.sub(p1).dot(p1p2)
    len_sq = p1p2.sqr()
    param = 0
    diff = Point(0, 0)
    if len_sq != 0:
        param = dot / len_sq
    if param <= 0:
        diff = point.sub(p1)
    elif param >= 1:
        diff = point.sub(p2)
    else:
        diff = point.sub(p1.add(p1p2.mul(param)))
    return diff.sqr()

def process_segment(a, b, c, d, t1, t2):
    # Rename the method `calcPoint` to `calc_point`
    f1 = calc_point(a, b, c, d, t1)
    f2 = calc_point(a, b, c, d, t2)
    f1_ = calc_point_derivative(a, b, c, d, t1)
    f2_ = calc_point_derivative(a, b, c, d, t2)

    D = -f1_.x * f2_.y + f2_.x * f1_.y
    if abs(D) < 1e-8:
        return [f1, f1.add(f2).div(2), f2]  # straight line segment
    cx = (f1_.x * (f2.y * f2_.x - f2.x * f2_.y) + f2_.x * (f1.x * f1_.y - f1.y * f1_.x)) / D
    cy = (f1_.y * (f2.y * f2_.x - f2.x * f2_.y) + f2_.y * (f1.x * f1_.y - f1.y * f1_.x)) / D
    return [f1, Point(cx, cy), f2]

def is_segment_approximation_close(a, b, c, d, tmin, tmax, p1, c1, p2, error_bound):
    # Rename the method `calcPowerCoefficientsQuad` to `calc_power_coefficients_quad`
    n = 10  # number of points
    t, dt = 0, 0
    p = calc_power_coefficients_quad(p1, c1, p2)
    qa, qb, qc = p[0], p[1], p[2]
    i, j, dist_sq = 0, 0, 0
    error_bound_sq = error_bound * error_bound
    cubic_points = []
    quad_points = []
    min_dist_sq = 0

    dt = (tmax - tmin) / n
    for i in range(n + 1):
        cubic_points.append(calc_point(a, b, c, d, t))
        t += dt

    dt = 1 / n
    t = 0
    for i in range(n + 1):
        quad_points.append(calc_point_quad(qa, qb, qc, t))
        t += dt

    for i in range(1, len(cubic_points) - 1):
        min_dist_sq = float('inf')
        for j in range(len(quad_points) - 1):
            dist_sq = min_distance_to_line_sq(cubic_points[i], quad_points[j], quad_points[j + 1])
            min_dist_sq = min(min_dist_sq, dist_sq)
        if min_dist_sq > error_bound_sq:
            return False

    for i in range(1, len(quad_points) - 1):
        min_dist_sq = float('inf')
        for j in range(len(cubic_points) - 1):
            dist_sq = min_distance_to_line_sq(quad_points[i], cubic_points[j], cubic_points[j + 1])
            min_dist_sq = min(min_dist_sq, dist_sq)
        if min_dist_sq > error_bound_sq:
            return False

    return True

def _is_approximation_close(a, b, c, d, quad_curves, error_bound):
    dt = 1 / len(quad_curves)
    for i in range(len(quad_curves)):
        p1 = quad_curves[i][0]
        c1 = quad_curves[i][1]
        p2 = quad_curves[i][2]
        if not is_segment_approximation_close(a, b, c, d, i * dt, (i + 1) * dt, p1, c1, p2, error_bound):
            return False
    return True

def from_flat_array(points):
    result = []
    segments_number = (len(points) - 2) / 4
    for i in range(int(segments_number)):
        result.append([
            Point(points[4 * i], points[4 * i + 1]),
            Point(points[4 * i + 2], points[4 * i + 3]),
            Point(points[4 * i + 4], points[4 * i + 5])
        ])
    return result

def to_flat_array(quads_list):
    result = []
    result.append(quads_list[0][0].x)
    result.append(quads_list[0][0].y)
    for i in range(len(quads_list)):
        result.append(quads_list[i][1].x)
        result.append(quads_list[i][1].y)
        result.append(quads_list[i][2].x)
        result.append(quads_list[i][2].y)
    return result

def is_approximation_close(p1x, p1y, c1x, c1y, c2x, c2y, p2x, p2y, quads, error_bound):
    pc = calc_power_coefficients(
        Point(p1x, p1y),
        Point(c1x, c1y),
        Point(c2x, c2y),
        Point(p2x, p2y)
    )
    return _is_approximation_close(pc[0], pc[1], pc[2], pc[3], from_flat_array(quads), error_bound)

def subdivide_cubic(x1, y1, x2, y2, x3, y3, x4, y4, t):
    u = 1 - t
    v = t

    bx = x1 * u + x2 * v
    sx = x2 * u + x3 * v
    fx = x3 * u + x4 * v
    cx = bx * u + sx * v
    ex = sx * u + fx * v
    dx = cx * u + ex * v

    by = y1 * u + y2 * v
    sy = y2 * u + y3 * v
    fy = y3 * u + y4 * v
    cy = by * u + sy * v
    ey = sy * u + fy * v
    dy = cy * u + ey * v

    return [
        [x1, y1, bx, by, cx, cy, dx, dy],
        [dx, dy, ex, ey, fx, fy, x4, y4]
    ]

def by_number(x, y):
    return x - y

def solve_inflections(x1, y1, x2, y2, x3, y3, x4, y4):
    p = -(x4 * (y1 - 2 * y2 + y3)) + x3 * (2 * y1 - 3 * y2 + y4) + \
        x1 * (y2 - 2 * y3 + y4) - x2 * (y1 - 3 * y3 + 2 * y4)
    q = x4 * (y1 - y2) + 3 * x3 * (-y1 + y2) + \
        x2 * (2 * y1 - 3 * y3 + y4) - x1 * (2 * y2 - 3 * y3 + y4)
    r = x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3)

    return [t for t in quad_solve(p, q, r) if 0 < t < 1]

def _cubic_to_quad(p1x, p1y, c1x, c1y, c2x, c2y, p2x, p2y, error_bound):
    p1 = Point(p1x, p1y)
    c1 = Point(c1x, c1y)
    c2 = Point(c2x, c2y)
    p2 = Point(p2x, p2y)
    pc = calc_power_coefficients(p1, c1, c2, p2)
    a, b, c, d = pc

    for segments_count in range(1, 9):
        approximation = []
        for t in range(0, 1, 1 / segments_count):
            approximation.append(process_segment(a, b, c, d, t, t + (1 / segments_count)))
        
        if segments_count == 1 and \
                (approximation[0][1].sub(p1).dot(c1.sub(p1)) < 0 or
                 approximation[0][1].sub(p2).dot(c2.sub(p2)) < 0):
            continue
        
        if _is_approximation_close(a, b, c, d, approximation, error_bound):
            break
    
    return to_flat_array(approximation)


def cubic_to_quad(p1x, p1y, c1x, c1y, c2x, c2y, p2x, p2y, error_bound):
    inflections = solve_inflections(p1x, p1y, c1x, c1y, c2x, c2y, p2x, p2y)

    if not inflections:
        return _cubic_to_quad(p1x, p1y, c1x, c1y, c2x, c2y, p2x, p2y, error_bound)

    result = []
    curve = [p1x, p1y, c1x, c1y, c2x, c2y, p2x, p2y]
    prev_point = 0

    for inflection in inflections:
        split = subdivide_cubic(
            *curve, 
            1 - (1 - inflection) / (1 - prev_point)
        )

        quad = _cubic_to_quad(
            *split[0][:8], 
            error_bound
        )

        result.extend(quad[:-2])
        curve = split[1]
        prev_point = inflection

    quad = _cubic_to_quad(
        *curve, 
        error_bound
    )

    return result + quad
