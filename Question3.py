import turtle  # Import turtle module for simple graphics/drawing
"""
Group Name: Sydney 11
Course Code: HIT137

Group Members:
Mohamed Hatem Moneir Mansour Elshekh - 393891
Roshan Pandey - 395865
Kamana  - 392322
Sejal Pradhan - 396928


This program uses Python's turtle graphics to draw a fractal polygon where each side
The user provides:
- Number of sides for the polygon
- Side length in pixels (validated, 10–500)
- Recursion depth for the fractal (0 draws straight sides; higher values add detail)

Program behavior:
- Recursively subdivides each side into segments and turns to create the fractal edge.
- Draws the full polygon by repeating the edge and rotating by 360/sides each time.
- Handles early window close gracefully with a friendly message.

Main functions implemented:
1) draw_fractal_edge(t, length, depth): recursively draws one fractal edge.
2) draw_fractal_polygon(sides, side_length, depth): sets up turtle and draws the polygon.
3) get_int_from_user(name, min_val, max_val): robust integer input with optional bounds.
4) main(): collects input and starts drawing.



References

ChatGPT-5. (2025). AI assistant for code layout and documentation grammar. OpenAI. https://openai.com/chatgpt
 - Used for: comment style/wording; high-level structure (no algorithmic code copied).

GeeksforGeeks. (2025). Python Turtle Tutorial. https://www.geeksforgeeks.org/python/python-turtle-tutorial/
 - Used for: turtle basics (screen/turtle setup, speed, turning).

Real Python. (n.d.). Working with None in Python. https://realpython.com/null-in-python/
 - Used for: defensive checks and understanding of None handling.

Python Software Foundation. (2024). The __main__ module. https://docs.python.org/3/library/__main__.html
 - Used for: main entry-point guard usage.

Khan Academy. (n.d.). Recursion and fractals. Retrieved from https://www.khanacademy.org/computing/computer-science/algorithms/recursive-algorithms
 - Used for: recursion concepts applied in draw_fractal_edge.

W3Schools. (n.d.). Python Function Arguments — Default parameter value. Retrieved September 5, 2025, from https://www.w3schools.com/python/python_functions_arguments.asp
 - Used for: function parameter defaults and prompts.

Python Software Foundation. (2025). Errors and Exceptions. https://docs.python.org/3/tutorial/errors.html
 - Used for: checked error types and how to catch them in except blocks.
"""
def draw_fractal_edge(t, length, depth):
    """Draw a single fractal edge using recursion.

    - Base case (depth == 0): move forward by the current length.
    - Recursive case: split the segment into thirds and turn to form the pattern.
    """

    if depth == 0:  # Base case: no more recursion, just draw a straight segment
        t.forward(length)  # Move the turtle forward by the current segment length
    else:
        length /= 3.0  # Split this edge into 3 equal parts for the Koch-style pattern
        draw_fractal_edge(t, length, depth - 1)  # Draw the first third recursively
        t.left(60)  # Turn left to create the "bump" of the fractal
        draw_fractal_edge(t, length, depth - 1)  # Draw the second third recursively
        t.right(120)  # Turn right to point downwards for the middle segment
        draw_fractal_edge(t, length, depth - 1)  # Draw the third third recursively
        t.left(60)  # Turn back to original heading direction
        draw_fractal_edge(t, length, depth - 1)  # Draw the final third recursively


def draw_fractal_polygon(sides, side_length, depth):
    """Create a turtle screen and draw a fractal polygon with the given parameters."""
    screen = turtle.Screen()  # Create a new drawing window (screen)
    screen.bgcolor("white")  # Set the background color to white for clarity
    t = turtle.Turtle()  # Create a new turtle (the pen that draws)
    t.home()  # Reset turtle position and heading to the center facing east
    t.speed(0)  # Increase drawing speed so fractals render faster (0=fastest, 10=fast) as per reference
    try:
        for _ in range(sides):  # Repeat for each side of the polygon
            draw_fractal_edge(t, side_length, depth)  # Draw one full fractal edge
            t.right(360 / sides)  # Rotate to align with the next side of the polygon
    except Exception as e:
        print("Unexpected drawing error:", e)
        return  # Stop if the window is closed mid-draw to avoid crashes
    
    turtle.done()  # Keep the window open until the user closes it

def get_int_from_user(name, min_val = None, max_val = None): 
    """
    Take input from user and check wether if it's a string, float, or INT

    in case it's a string, ask the user to re-enter the value
    in case it's a float, round the value to the nearest int
    in case it's an int, proceed normally.
    """

    is_number = False  # Variable to keep track whether we have a valid integer yet
    while is_number is False:  # Keep asking until the user enters a valid number
        user_input = input(str(name))  # Show the custom prompt to the user and read input
        try:
            # Accept floats by rounding to nearest int
            val = round(float(user_input))
            if min_val is not None and val < min_val:  # Enforce minimum bound if provided
                print(f"Value must be at least {min_val}. Please try again.")
                continue
            if max_val is not None and val > max_val:  # Enforce maximum bound if provided
                print(f"Value must be at most {max_val}. Please try again.")  # Explain the constraint
                continue  # Ask again while staying in the loop

            isNumber = True  # Mark that we finally got a valid number
            return val  # Return the integer value and exit the loop
        except (ValueError, TypeError):
            print("That's not a number! Please enter a valid, correct number.")  # Guide the user to try again
            # The while loop continues, so we ask again


def main():
    """
    Main function to run the fractal polygon drawing program.
    Gets user input for polygon parameters and draws the fractal.
    """
    print("Fractal Polygon Generator")  # Title of the program for the user
    print("=" * 25)  # Simple underline for readability
    
    sides = get_int_from_user("Enter the number of sides (3-12): ", 3, 12)  # Validate reasonable polygon sides
    side_length = get_int_from_user("Enter the side length in pixels (10-500): ", 10, 500)  # Ask for side length with bounds
    depth = get_int_from_user("Enter the recursion depth (1-6): ", 1, 6)  # Bound recursion depth to avoid very long runs
    
    print(f"\nDrawing a fractal polygon with:")  # Provide a quick summary before drawing
    print(f"- Sides: {sides}")  # Echo the number of sides back to the user
    print(f"- Side length: {side_length} pixels")  # Echo the side length
    print(f"- Recursion depth: {depth}")  # Echo the recursion depth
    print("\nDrawing... Close the turtle window when done.")  # Instruction for finishing
    
    draw_fractal_polygon(sides, side_length, depth)  # Recursively draw the fractal polygon

if __name__ == "__main__":
    main()
