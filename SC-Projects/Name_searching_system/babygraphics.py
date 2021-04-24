"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    x_coordinate = GRAPH_MARGIN_SIZE + year_index*(width-2*GRAPH_MARGIN_SIZE)/len(YEARS)
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    # chart frame(top)
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    # chart frame(bottom)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    # chart frame(left)
    canvas.create_line(GRAPH_MARGIN_SIZE, 0, GRAPH_MARGIN_SIZE, CANVAS_HEIGHT)

    # year-lines & year-labels
    for i in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), 0, get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i) + TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE,
                           text=str(YEARS[i]), anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    # Draw as many lines as the values loaded in lookup_names
    for j in range(len(lookup_names)):
        # Draw and connect the lines between years for a name
        for i in range(len(YEARS)-1):
            x1 = get_x_coordinate(CANVAS_WIDTH, i)
            x2 = get_x_coordinate(CANVAS_WIDTH, i + 1)
            # Avoid from OBOB set rank_iplus1 as a integer variable
            rank_i_plus1 = 0
            # Check if the name is ranked within 1000
            if str(YEARS[i]) in name_data[lookup_names[j]]:
                rank_i = int(name_data[lookup_names[j]][str(YEARS[i])])
                y1 = GRAPH_MARGIN_SIZE + (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) * rank_i / 1000
                canvas.create_text(x1 + TEXT_DX, y1, text=lookup_names[j] + " " + str(rank_i), anchor=tkinter.SW,
                                   fill=COLORS[j % len(COLORS)])
            else:
                y1 = GRAPH_MARGIN_SIZE + (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE)
                canvas.create_text(x1 + TEXT_DX, y1, text=lookup_names[j] + ' *', anchor=tkinter.SW,
                                   fill=COLORS[j % len(COLORS)])

            if str(YEARS[i+1]) in name_data[lookup_names[j]]:
                rank_i_plus1 = int(name_data[lookup_names[j]][str(YEARS[i + 1])])
                y2 = GRAPH_MARGIN_SIZE + (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) * rank_i_plus1 / 1000
            else:
                y2 = GRAPH_MARGIN_SIZE + (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE)
            # Draw the line on the canvas
            canvas.create_line(x1, y1, x2, y2, fill=COLORS[j % len(COLORS)], width=LINE_WIDTH)

            # Avoid from OBOB, label the last year of a name
            if i == len(YEARS) - 2:
                if rank_i_plus1 != 0:
                    canvas.create_text(x2 + TEXT_DX, y2, text=lookup_names[j] + " " + str(rank_i_plus1),
                                       anchor=tkinter.SW, fill=COLORS[j % len(COLORS)])
                else:
                    canvas.create_text(x2 + TEXT_DX, y2, text=lookup_names[j] + ' *', anchor=tkinter.SW,
                                       fill=COLORS[j % len(COLORS)])


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
