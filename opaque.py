import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


M_VALUES = [-1, 1]

###
# ENTER VALUES
###


# The area you want to test

# UNIT SQUARE
good_area = [((0.5, 0.5), (-0.5, 0.5)), ((-0.5, 0.5), (-0.5, -0.5)), ((-0.5, -0.5), (0.5, -0.5)), ((0.5, -0.5), (0.5, 0.5))]
# RIGHT TRIANGLE
#good_area = [((0.5, 0.5), (-0.5, 0.5)), ((-0.5, 0.5), (-0.5, -0.5)), ((-0.5, -0.5), (0.5, 0.5))]


# The set of segments you want to try on the area

# STEINER TREES 
# format: [((x1, y1),(x2, y2),(x3, y3)), etc]
steiner_sets = [((-0.5, -0.5),(-0.5, 0.5),(0.5, 0.5))]

# PERPENDICULAR LINES
# format: [((x1,y1),(x2,y2),(xp,yp)), etc] *draws from the point (xp,yp) to the point on the given line that creates a right angle
perp_sets = [((-0.5, -0.5),(0.5, 0.5),(0.2, -0.2))]

# OTHER LINES
# format: [((x1,y1),(x2,y2)), etc]
other_sets = []


###
# END ENTER VALUES
###




# Thanks to abybaddi009 on stackexchange from 2016 lol (https://codegolf.stackexchange.com/questions/79691/calculate-the-fermat-point-of-a-triangle)
def fermat_point(vertices):
    x, y, z = vertices
    d = lambda x,y: ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5
    s = lambda A,B,C : (d(B,C), d(C,A), d(A,B))
    j = lambda a,b,c : math.acos((b*b+c*c-a*a)/(2*b*c))
    t = lambda a,b,c: 1/math.cos(j(a,b,c)-math.pi/6)
    b = lambda A,B,C,p,q,r: [(p*A[i]+q*B[i]+r*C[i])/(p+q+r) for i in [0,1]]
    f = lambda A,B,C: A if j(*s(A,B,C)) >= 2*math.pi/3 else B if j(*s(B,C,A)) >= 2*math.pi/3 else C if j(*s(C,A,B)) >= 2*math.pi/3 else b(A,B,C,d(B,C)*t(*s(A,B,C)),d(C,A)*t(*s(B,C,A)),d(A,B)*t(*s(C,A,B)))
    return (f(x, y, z))

# Takes a point, draws a line perpendicular starting from that point and ending on the other line
def find_perpendicular(perp_set):
    x1, y1 = perp_set[0]
    x2, y2 = perp_set[1]
    x3, y3 = perp_set[2]
    # Check if the line segment is vertical
    if x1 == x2:
        x4 = x1
        y4 = y3
    else:
        # Calculate slopes and intercepts
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        perpendicular_m = -1 / m
        perpendicular_b = y3 - perpendicular_m * x3

        # Solve for the intersection point
        x4 = (perpendicular_b - b) / (m - perpendicular_m)
        y4 = perpendicular_m * x4 + perpendicular_b

    return ((x3, y3), (x4, y4))

# Get the segments of a steiner tree with the given points
def get_steiner_segments(vertices):
    segments = []
    ferm_point = tuple(fermat_point(vertices))

    for vertex in vertices:
        if ferm_point != vertex:
            segments.append((ferm_point, vertex))

    return segments

# Get all segments of the starting lines
def get_starting_lines(steiner_sets, perp_sets, other_sets):
    segments = []
    # add lines of steiner trees
    for steiner in steiner_sets:
        steins = get_steiner_segments(steiner)
        for stein in steins:
            segments.append(stein)

    # add perpendicular lines
    for perp in perp_sets:
        new_line = find_perpendicular(perp)
        segments.append(new_line)

    # add other lines
    for other in other_sets:
        segments.append(other)

    return segments

# list of all segments
segments = get_starting_lines(steiner_sets, perp_sets, other_sets)



###
# AREA FUNCTIONS
###



# Once all ducks are in order, do the deed
def total_area(halfcepts, widths, heights_good_area, heights_segments):
    total = 0
    for i in range(len(halfcepts)):
        verticals = subtract_verticals(heights_good_area[i], heights_segments[i])
        for vertical in verticals:
            total += (vertical[1] - vertical[0]) * widths[i]
    return total

# Get the lengths of verticals at each halfcept
def get_type_lengths(lines, halfcepts):
    heights = []
    for x in halfcepts:
        current = []
        for line in lines:
            (x1, y1), (x2, y2) = line
            y = y1 + ((y2 - y1) / (x2 - x1)) * (x - x1)
            current.append(y)
        heights.append(current)

    new_heights = []
    for val in heights:
        new_heights.append(pair_elements(val))
    return new_heights

# Find all intersects of the various lines
def find_intersections(line_segments):
    x_values = [-1.0]
    line_segments = list(set(line_segments))
    for i, (start1, end1) in enumerate(line_segments):
        for start2, end2 in line_segments[i+1:]:
            a, b = start1[1] - start2[1], end1[1] - end2[1]
            if a == b or a == 0 or b == 0 or math.copysign(1, a) == math.copysign(1, b): continue
            if start1[1] == end1[1]: # If first line section is horizontal
                x_intersection = (a * (end2[0] - start2[0]) / (end2[1] - start2[1]) + start2[0])
            elif start2[1] == end2[1]: # If second line section is horizontal
                x_intersection = ((start2[1] - start1[1]) * (end1[0] - start1[0]) / (end1[1] - start1[1]) + start1[0])
            else:
                x_intersection = (
                    (start1[0] * (end1[1] - start1[1]) - start1[1] * (end1[0] - start1[0])) *
                    (start2[0] - end2[0]) - (start1[0] - end1[0]) *
                    (start2[0] * (end2[1] - start2[1]) - start2[1] * (end2[0] - start2[0]))
                ) / ((end1[0] - start1[0]) * (end2[1] - start2[1]) - (end1[1] - start1[1]) * (end2[0] - start2[0]))
            x_values.append(x_intersection)
    x_values.append(1.0)
    x_values = sorted(list(set(x_values)))
    return x_values

# The vertical lines between the intercepts
def get_halfcepts(list):
    halfcepts = []
    for i in range(len(list) - 1):
        halfway = (list[i] + list[i + 1]) / 2
        halfcepts.append(halfway)
    return halfcepts

# The distance between each vertical intercept line
def get_widths(list):
    widths = []
    for i in range(len(list) - 1):
        widths.append(list[i + 1] - list[i])
    return widths

# Find the area to draw each color
def get_area_bounds(point1, point2):
    lower_b_values = []
    upper_b_values = []
    # Calculate the b values for each m
    for m in M_VALUES:
        # Calculate the slope and intercept for the line y = mx + b
        lower_b_values.append(point1[1] - m * point1[0])
        upper_b_values.append(point2[1] - m * point2[0])
    return lower_b_values, upper_b_values

# Formatting, sorting, simplifying
def pair_elements(input_list):
    # Formatting, sorting the pairs
    paired_tuples = []
    for i in range(0, len(input_list), 2):
        pair = (input_list[i], input_list[i + 1])
        pair = tuple(sorted(pair))
        paired_tuples.append(pair)
    segments = sorted(paired_tuples)

    # If empty, return the empty set
    if not(segments): return segments

    # Combine verticals that overlap
    combined_segments = [segments[0]]
    for i in range(1, len(segments)):
        current_segment = segments[i]
        previous_segment = combined_segments[-1]
        if current_segment[0] <= previous_segment[1]: combined_segments[-1] = (previous_segment[0], max(current_segment[1], previous_segment[1]))
        else: combined_segments.append(current_segment)

    return combined_segments

# Get that sweet sweet gray length
def subtract_verticals(set1, set2):
    result_segments = []
    i, j = 0, 0

    while i < len(set1) and j < len(set2):
        segment1 = set1[i]
        segment2 = set2[j]

        if segment1[1] <= segment2[0]:
            # No overlap, add segment1 to the result and move to the next segment in set1
            result_segments.append(segment1)
            i += 1
        elif segment1[0] >= segment2[1]:
            # No overlap, move to the next segment in set2
            j += 1
        else:
            # There is an overlap, split segment1 into non-overlapping parts
            if segment1[0] < segment2[0]: result_segments.append((segment1[0], segment2[0]))
            if segment1[1] > segment2[1]:
                set1[i] = (segment2[1], segment1[1])
                j += 1
            else: i += 1

    # Add any remaining segments from set1 to the result
    while i < len(set1):
        result_segments.append(set1[i])
        i += 1

    # Add 0 set of nothing is left
    if not(result_segments): result_segments = [(0, 0)]
    return result_segments

# Swap x and y
def flip(segments):
    flipped_segments = []
    for segment in segments:
        flipped_segment = tuple([(point[1], point[0]) for point in segment])
        flipped_segments.append(flipped_segment)
    return flipped_segments

# Plot
def plot(set, ax, color, alpha, hatch):
    lower_uppers = []

    for line in set:
        lower_b_values, upper_b_values = get_area_bounds(line[0], line[1])
        lower_uppers.append([lower_b_values, upper_b_values])
        ax.fill_between(M_VALUES, lower_b_values, upper_b_values, hatch=hatch, color=color, alpha=alpha)

    formatted_set = get_formatted_set(lower_uppers)

    return formatted_set

# Get formatted set
def get_formatted_set(ugly_sets):
    formatted_set = []
    for ugly_set in ugly_sets:
        for vals in ugly_set:
            formatted_set.append(((M_VALUES[0], vals[0]), (M_VALUES[1], vals[1])))
    return formatted_set

# Putting it all together
def calculate_valid_area(good_area, segments, ax, color1, color2, alpha1, alpha2):
    # Plot the segments
    good_area_lines = plot(good_area, ax, color1, alpha1, None)
    segments_lines = plot(segments, ax, color2, alpha2, None)

    # Find important values
    intercepts = find_intersections(good_area_lines + segments_lines)
    halfcepts = get_halfcepts(intercepts)
    widths = get_widths(intercepts)

    # Get the important verticals
    heights_good_area = get_type_lengths(good_area_lines, halfcepts)
    heights_segments = get_type_lengths(segments_lines, halfcepts)

    # Calculate the area
    area = total_area(halfcepts, widths, heights_good_area, heights_segments)
    return area

# Calculate total length of line segments
def calculate_combined_length(line_segments):
    combined_length = 0.0
    for segment in line_segments:
        point1, point2 = segment
        x1, y1 = point1
        x2, y2 = point2
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        combined_length += length
    return combined_length

# Reset to starting lines
def button_1(steiner_sets, perp_sets, other_sets, good_area, fig, ax1, ax2, ax3, text_a, text_b):
    global clicked_points
    clicked_points = []
    ax3.cla()
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)
    ax3.set_aspect('equal')
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.plot([-1, 1], [1, 1], linestyle=("--"), color='grey')
    ax3.plot([1, 1], [1, -1], linestyle=("--"), color='grey')
    ax3.plot([1, -1], [-1, -1], linestyle=("--"), color='grey')
    ax3.plot([-1, -1], [-1, 1], linestyle=("--"), color='grey')
    text1 = ax3.text(ax3.get_position().x0 - 1.2, ax3.get_position().y0 + 1.0, 'Click to Draw Lines')
    segments = get_starting_lines(steiner_sets, perp_sets, other_sets)
    
    # Calculate the original area
    area_original = calculate_valid_area(good_area, segments, ax1, 'gray', 'blue', 1, 0.5)

    # Calculate the flipped area
    area_flipped = calculate_valid_area(flip(good_area), flip(segments), ax2, 'gray', 'red', 1, 0.5)

    # Calculate the total area
    area_total = area_original + area_flipped

    # Iterate through the line segments and plot each one
    for segment in good_area:
        x_values = [segment[0][0], segment[1][0]]
        y_values = [segment[0][1], segment[1][1]]
        ax3.plot(x_values, y_values, linestyle='-', color='gray')
    for segment in segments:
        x_values = [segment[0][0], segment[1][0]]
        y_values = [segment[0][1], segment[1][1]]
        ax3.plot(x_values, y_values, linestyle='-', color='black')

    length = calculate_combined_length(segments)
    print('---')
    print('Total Remaining Grey:')
    print(area_total)
    print('Total Length:')
    print(length)
    text_a.set_text(f'{area_total}')
    text_b.set_text(f'{length}')

    for segment in segments:
        clicked_points.append(segment[0])
        clicked_points.append(segment[1])

    fig.canvas.draw()

    #return clicked_points

# Erase all lines
def button_2(fig, ax1, ax2, ax3, text_a, text_b):
    global clicked_points
    clicked_points = []
    segments = []
    ax3.cla()
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)
    ax3.set_aspect('equal')
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.plot([-1, 1], [1, 1], linestyle=("--"), color='grey')
    ax3.plot([1, 1], [1, -1], linestyle=("--"), color='grey')
    ax3.plot([1, -1], [-1, -1], linestyle=("--"), color='grey')
    ax3.plot([-1, -1], [-1, 1], linestyle=("--"), color='grey')
    text1 = ax3.text(ax3.get_position().x0 - 1.2, ax3.get_position().y0 + 1.0, 'Click to Draw Lines')

    # Calculate the original area
    area_original = calculate_valid_area(good_area, segments, ax1, 'gray', 'blue', 1, 0.5)

    # Calculate the flipped area
    area_flipped = calculate_valid_area(flip(good_area), flip(segments), ax2, 'gray', 'red', 1, 0.5)

    # Calculate the total area
    area_total = area_original + area_flipped

    for segment in good_area:
        x_values = [segment[0][0], segment[1][0]]
        y_values = [segment[0][1], segment[1][1]]
        ax3.plot(x_values, y_values, linestyle='-', color='gray')
    
    length = calculate_combined_length(segments)
    print('---')
    print('Total Remaining Grey:')
    print(area_total)
    print('Total Length:')
    print(length)
    text_a.set_text(f'{area_total}')
    text_b.set_text(f'{length}')

    fig.canvas.draw()

# Redraw function for drawing lines
def redraw(good_area, clicked_points, ax1, ax2, ax3, text_a, text_b):
    segments = []
    for i in range(0, len(clicked_points), 2):
        segments.append((clicked_points[i], clicked_points[i + 1]))
    
    # Calculate the original area
    area_original = calculate_valid_area(good_area, segments, ax1, 'gray', 'blue', 1, 0.5)

    # Calculate the flipped area
    area_flipped = calculate_valid_area(flip(good_area), flip(segments), ax2, 'gray', 'red', 1, 0.5)

    # Calculate the total area
    area_total = area_original + area_flipped

    # Iterate through the line segments and plot each one
    for segment in good_area:
        x_values = [segment[0][0], segment[1][0]]
        y_values = [segment[0][1], segment[1][1]]
        ax3.plot(x_values, y_values, linestyle='-', color='gray')
    for segment in segments:
        x_values = [segment[0][0], segment[1][0]]
        y_values = [segment[0][1], segment[1][1]]
        ax3.plot(x_values, y_values, linestyle='-', color='black')

    length = calculate_combined_length(segments)
    print('---')
    print('Total Remaining Grey:')
    print(area_total)
    print('Total Length:')
    print(length)
    text_a.set_text(f'{area_total}')
    text_b.set_text(f'{length}')

# When clicking the draw graph
def on_click(event, fig, ax1, ax2, ax3, clicked_points, good_area, segments, text_a, text_b):
    if event.inaxes == ax3:
        # Check if the click occurred within the axes of the plot
        x_coord = event.xdata  # Get the x-coordinate of the click
        y_coord = event.ydata  # Get the y-coordinate of the click

        # Store the clicked point
        clicked_points.append((x_coord, y_coord))

        if len(clicked_points) % 2 == 0:
            redraw(good_area, clicked_points, ax1, ax2, ax3, text_a, text_b)

        # Plot the clicked point on the graph
        ax3.plot(x_coord, y_coord, 'k.', markersize=3)

        # Redraw the canvas to update the plot
        fig.canvas.draw()

# The main thang
def plot_that_shit(good_area, segments):
    # Create two separate plots using subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# You can access each subplot using the 'axes' array
    ax1 = axes[0, 0]
    ax2 = axes[0, 1]
    ax3 = axes[1, 0]
    ax4 = axes[1, 1]

    # Calculate the original area
    area_original = calculate_valid_area(good_area, segments, ax1, 'gray', 'blue', 1, 0.5)

    # Calculate the flipped area
    area_flipped = calculate_valid_area(flip(good_area), flip(segments), ax2, 'gray', 'red', 1, 0.5)

    # Calculate the total area
    area_total = area_original + area_flipped

    print("Total Remaining Grey:")
    print(area_total)


    # Iterate through the line segments and plot each one
    for segment in good_area:
        x_values = [segment[0][0], segment[1][0]]
        y_values = [segment[0][1], segment[1][1]]
        ax3.plot(x_values, y_values, linestyle='-', color='gray')
    for segment in segments:
        x_values = [segment[0][0], segment[1][0]]
        y_values = [segment[0][1], segment[1][1]]
        ax3.plot(x_values, y_values, linestyle='-', color='black')

    # Set axis limits if needed
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)
    ax3.set_aspect('equal')
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.plot([-1, 1], [1, 1], linestyle=("--"), color='grey')
    ax3.plot([1, 1], [1, -1], linestyle=("--"), color='grey')
    ax3.plot([1, -1], [-1, -1], linestyle=("--"), color='grey')
    ax3.plot([-1, -1], [-1, 1], linestyle=("--"), color='grey')

    # Format first plot
    ax1.set_xlabel('m')
    ax1.set_ylabel('b')
    ax1.set_title('Original Segments')
    ax1.grid(color='black', alpha=0.1)
    ax1.set_aspect('equal')

    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)

    # Format second plot
    ax2.set_xlabel('m')
    ax2.set_ylabel('b')
    ax2.set_title('Flipped Segments')
    ax2.grid(color='black', alpha=0.1)

    ax2.set_xlim(-1, 1)
    ax2.set_ylim(-1, 1)
    ax2.set_aspect('equal')

    global clicked_points
    clicked_points = []
    for segment in segments:
        clicked_points.append(segment[0])
        clicked_points.append(segment[1])
    length = calculate_combined_length(segments)
    print("Total Length:")
    print(length)
    cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, fig, ax1, ax2, ax3, clicked_points, good_area, segments, text3, text5))

    plt.tight_layout()
    plt.gca().set_aspect('equal', adjustable='box')
    ax3.set_position([ax3.get_position().x0 + 0.15, ax3.get_position().y0, ax3.get_position().width/1.1, ax3.get_position().height/1.1])
    ax4.set_aspect('auto')
    ax4.set_position([ax2.get_position().x0 + 0.03, ax2.get_position().y0 - 0.26, 0.15, 0.03])
    ax5 = plt.axes([ax2.get_position().x0 + 0.03, ax2.get_position().y0 - 0.3, 0.1, 0.03])
    button1 = Button(ax4, 'Reset to Starting Lines')
    button2 = Button(ax5, 'Erase All Lines')

    text1 = ax3.text(ax3.get_position().x0 - 1.2, ax3.get_position().y0 + 1.0, 'Click to Draw Lines')
    text2 = ax4.text(ax4.get_position().x0 - 0.6, ax4.get_position().y0 + 4.2, f'Total Remaining Grey:')
    text3 = ax4.text(ax4.get_position().x0 - 0.6, ax4.get_position().y0 + 3.5, f'{area_total}')
    text4 = ax4.text(ax4.get_position().x0 - 0.6, ax4.get_position().y0 + 2.5, f'Length:')
    text5 = ax4.text(ax4.get_position().x0 - 0.6, ax4.get_position().y0 + 1.8, f'{length}')

    button1.on_clicked(lambda event: button_1(steiner_sets, perp_sets, other_sets, good_area, fig, ax1, ax2, ax3, text3, text5))
    button2.on_clicked(lambda event: button_2(fig, ax1, ax2, ax3, text3, text5))
    
    plt.show()



plot_that_shit(good_area, segments)

