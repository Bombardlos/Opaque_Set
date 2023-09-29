import math


M_VALUES = [-1, 1]
# The area you want to test
# UNIT SQUARE
GOOD_AREA = [((0.5, 0.5), (-0.5, 0.5)), ((-0.5, 0.5), (-0.5, -0.5)), ((-0.5, -0.5), (0.5, -0.5)), ((0.5, -0.5), (0.5, 0.5))]
# RIGHT TRIANGLE
#GOOD_AREA = [((0.5, 0.5), (-0.5, 0.5)), ((-0.5, 0.5), (-0.5, -0.5)), ((-0.5, -0.5), (0.5, 0.5))]

# The set of segments you want to try on the area
segments = [((-0.5, 0.5), (-0.15, -0.25))]



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

# Calculate distance between 2 points
def distance(all_points):
    length = 0
    for points in all_points:
        math.sqrt((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2)
    return length

# Swap x and y
def flip(segments):
    flipped_segments = []
    for segment in segments:
        flipped_segment = tuple([(point[1], point[0]) for point in segment])
        flipped_segments.append(flipped_segment)
    return flipped_segments

FLIP_GOOD_AREA = flip(GOOD_AREA)

# Plot
def get_formatted_set(set):
    formatted_set = []
    for line in set:
        lower_b_values, upper_b_values = get_area_bounds(line[0], line[1])
        for vals in lower_b_values, upper_b_values:
            formatted_set.append(((M_VALUES[0], vals[0]), (M_VALUES[1], vals[1])))
    return formatted_set

# Putting it all together
def calculate_valid_area(good_area, segments):
    # Plot the segments
    good_area_lines = get_formatted_set(good_area)
    segments_lines = get_formatted_set(segments)

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



###
# START HERE
###



# Calculate the remaining areas
area_original = calculate_valid_area(GOOD_AREA, segments)
area_flipped = calculate_valid_area(FLIP_GOOD_AREA, flip(segments))
area_total = area_original + area_flipped
length = distance(segments)

print("Total Remaining Grey:")
print(area_total)

print("Total Length:")
print(length)
