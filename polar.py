import math

def to_polar(x, y, center):
    r = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
    phi = math.atan2(math.radians((y - center[1]) / (x - center[0])))
    return r, phi

def from_polar(r, phi, center):
    x = r * math.cos(phi) + center[0]
    y = r * math.sin(phi) + center[1]
    return x, y