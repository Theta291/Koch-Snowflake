#Helper Functions for koch curve notebook
from turtle import *
from functools import partial
DEFAULT_FONT = ("Arial", 16, "normal")

# The main koch curve function. Uses recursion to draw curve.
def koch(detail=1, size=300):
    if detail == 0:
        fd(size)
    else:
        def mini_koch():
            koch(detail-1, size/3)
        mini_koch()
        lt(60)
        mini_koch()
        rt(120)
        mini_koch()
        lt(60)
        mini_koch()

def koch0(size=300): koch(0, size)

def koch1(size=300): koch(1, size)

def koch2(size=300): koch(2, size)

# The main minkowski sausage function.
def minkowski(detail=1, size=400):
    if detail == 0:
        fd(size)
    else:
        def mini():
            minkowski(detail-1, size/4)
        mini()
        lt(90)
        mini()
        rt(90)
        mini()
        rt(90)
        mini()
        mini()
        lt(90)
        mini()
        lt(90)
        mini()
        rt(90)
        mini()

# The koch snowflake function. Draws three koch curves in a triangle to make the snowflake.
def koch_snowflake(detail=1, size=300):
    koch(detail, size)
    rt(120)
    koch(detail, size)
    rt(120)
    koch(detail, size)

#The minkowski island function. draws four minkowski sausages in a square.
def minkowski_island(detail=1, size=400):
    minkowski(detail, size)
    right(90)
    minkowski(detail, size)
    right(90)
    minkowski(detail, size)
    right(90)
    minkowski(detail, size)
    right(90)

# A function that can turn a line drawing polygon into a turtle shape without filling.
# Maybe there's a better way to do this?
def get_curve_as_shape(name, curve):
    #Makes a list which contains the curve points, then the curve points backwards.
    *curve_double, = *curve, *reversed(curve)
    register_shape(name, tuple(curve_double))

def frange(*posargs):
    if len(posargs) == 1:
        stop = posargs[0]
        start = 0
        step = 1
    elif len(posargs) == 2:
        start, stop = posargs
        step = 1
    elif len(posargs) == 3:
        start, stop, step = posargs

    if start < stop:
        while start < stop:
            yield start
            start += step
    else:
        while start > stop:
            yield start
            start += step

# Animates changing the size of the turtle shape. End size must be a tuple of two integers.
def change_size_anim(end_size, num_frames):
    *curr_size, outline = *shapesize(),
    ranges = (frange(a, b, (b - a) / num_frames) for a, b in zip(curr_size, end_size))
    for size in zip(*ranges):
        shapesize(*size)
    shapesize(*end_size)

def tiltangle_anim(tilt_angle, num_frames):
    curr_angle = tiltangle()
    increment = (tilt_angle - curr_angle) / num_frames
    for frame in range(num_frames):
        tilt(increment)
    tiltangle(tilt_angle)

def tilt_anim(tilt_angle, num_frames):
    curr_angle = tiltangle()
    end_angle = curr_angle + tilt_angle
    tiltangle_anim(end_angle, num_frames)

def create_koch_shape(detail, size=300):
    koch_name = f"koch{detail}_{size}"
    if koch_name not in getshapes():
        reset()
        speed(0)
        ht()
        pu()
        begin_poly()
        koch(detail, size)
        end_poly()
        temp = get_poly()
        get_curve_as_shape(koch_name, temp)
        reset()

def create_minkowski_shape(detail, size=400):
    minkowski_name = f"minkowski{detail}_{size}"
    if minkowski_name not in getshapes():
        reset()
        speed(0)
        ht()
        pu()
        begin_poly()
        minkowski(detail, size)
        end_poly()
        temp = get_poly()
        get_curve_as_shape(minkowski_name, temp)
        reset()

def grab_and_place(start_pos, prep_pos, shapestr, size_factor, place_pos, angle):
    shape("classic")
    shapesize(1, 1)
    goto(start_pos)
    tiltangle(90)
    shape(shapestr)
    color("red")
    goto(prep_pos)
    change_size_anim((size_factor, size_factor), 100)
    goto(place_pos)
    if angle != 0:
        tilt_anim(angle, 75)
    color("black")
    stamp()
    
#Functions that animates how a koch curve is recursively created.
def koch_recursion_animation(start_step=0, end_step=2, size=300):
    num_steps = end_step - start_step
    for i in range(start_step, end_step+1):
        create_koch_shape(i, size)

    # Defining some important position on the canvas
    start_pos = [(-300, 300 - step * size * 2/3) for step in range(num_steps+1)]
    under_start = [(a, b-size/3) for a, b in start_pos]
    seg2 = [(a + size/3, b) for a, b in start_pos]
    seg3 = [(a + size/2, b + (size / 6) * (3 ** (1/2))) for a, b in start_pos]
    seg4 = [(a + size * 2/3, b) for a, b in start_pos]
    shape_strs = [f"koch{step}_{size}" for step in range(start_step, end_step)]

    # Koch0
    reset()
    shape("classic")
    speed("slowest")
    pu()
    goto(start_pos[0])
    pd()
    koch(start_step, size)
    pu()

    arg_zip = zip(start_pos, under_start, shape_strs)
    for i in range(1, num_steps+1):
        curr_grab = partial(grab_and_place, *(*next(arg_zip), 1/3))
        curr_grab(start_pos[i], 0)
        curr_grab(seg2[i], 60)
        curr_grab(seg3[i], -60)
        curr_grab(seg4[i], 0)
        
    shape("classic")
    shapesize(1, 1)

def minkowski_recursion_animation(start_step=0, end_step=2, size=200):
    num_steps = end_step - start_step
    for i in range(start_step, end_step+1):
        create_minkowski_shape(i, size)

    # Defining some important position on the canvas
    start_pos = [(-300, 300 - step * size * 2/3) for step in range(num_steps+1)]
    under_start = [(a, b-size/3) for a, b in start_pos]
    seg_len = size/4
    seg2 = [(a + seg_len, b) for a, b in start_pos]
    seg3 = [(a, b + seg_len) for a, b in seg2]
    seg4 = [(a + seg_len, b) for a, b in seg3]
    seg5 = [(a, b - seg_len) for a, b in seg4]
    seg6 = [(a, b - seg_len) for a, b in seg5]
    seg7 = [(a + seg_len, b) for a, b in seg6]
    seg8 = [(a, b + seg_len) for a, b in seg7]
    seg_pos = [start_pos, seg2, seg3, seg4, seg5, seg6, seg7, seg8]
    angles = [0, 90, 0, -90, -90, 0, 90, 0]
    shape_strs = [f"minkowski{step}_{size}" for step in range(start_step, end_step)]

    # Minkowski0
    reset()
    shape("classic")
    speed("slowest")
    pu()
    goto(start_pos[0])
    pd()
    minkowski(start_step, size)
    pu()

    arg_zip = zip(start_pos, under_start, shape_strs)
    for i in range(num_steps):
        curr_grab = partial(grab_and_place, *(*next(arg_zip), 1/4))
        for j in range(8):
            curr_grab(seg_pos[j][i+1], angles[j])
        
    shape("classic")
    shapesize(1, 1)
