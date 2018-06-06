import math
def make_cylinder_volume_func(r):
    def volume(h):
        return math.pi * r * r * h
    return volume