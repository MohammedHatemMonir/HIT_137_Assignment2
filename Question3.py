import turtle
"""
Group Name: Sydney 11
Course Code: HIT137
Group Members:
Mohamed Hatem Moneir Mansour Elshekh - 393891
Roshan Pandey - 395865
Kamana  - 392322
Sejal Pradhan - 396928

"""
def draw_fractal_edge(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        draw_fractal_edge(t, length, depth - 1)
        t.left(60)
        draw_fractal_edge(t, length, depth - 1)
        t.right(120)
        draw_fractal_edge(t, length, depth - 1)
        t.left(60)
        draw_fractal_edge(t, length, depth - 1)

def draw_fractal_polygon(sides, side_length, depth):
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)
    
    for _ in range(sides):
        draw_fractal_edge(t, side_length, depth)
        t.right(360 / sides)
    
    turtle.done()



sides = int(input("Enter the number of sides: "))
side_length = int(input("Enter the side length (pixels): "))
depth = int(input("Enter the recursion depth: "))
    
draw_fractal_polygon(sides, side_length, depth) #Recursively draw polygons
