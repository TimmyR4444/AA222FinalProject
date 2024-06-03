import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.ticker import MultipleLocator

# Coordinates
coordinates = {
    0: (873,495),
    1: (935,145),
    2: (120,300),
    3: (812,524),
    4: (857,176),
    5: (616,152),
    6: (330,240),
    7: (440,192),
    8: (256,562),
    9: (743,254),
    10: (257,517),
    11: (694,240),
    12: (523,267),
    13: (738,493),
    14: (463,232),
    15: (142,558),
    16: (648,204),
    17: (965,438),
    18: (818,367),
    19: (863,521),
    20: (722,110),
    21: (849,566),
    22: (414,347),
    23: (338,520),
    24: (144,349),
    25: (80,359)
}

path = [(559,791)]
#itinerary = [25, 20, 4, 15, 12, 22, 26, 1, 18, 28, 13, 2, 23, 10, 8, 6, 27, 21, 3, 19, 9, 7]
itinerary = [6, 7, 22, 13, 14, 9, 12, 2, 23, 26, 25, 21, 3, 28, 27, 1, 20, 4, 11, 19, 29]
last_coor = (0,0)
for ride in itinerary:
    if (ride in [26,27,28,29]):
        curr_coor = last_coor
    else:
        curr_coor = coordinates[ride]
    path.append(curr_coor)
    last_coor = curr_coor

# Load the map image
map_image = Image.open('map.png')

'''
# Extract x and y coordinates from the path
x_coords, y_coords = zip(*path)

# Plot the map image
fig, ax = plt.subplots()
ax.imshow(map_image)

# Plot the path on the map
ax.plot(x_coords, y_coords, marker='o', color='red', linestyle='-', linewidth=2, markersize=5)


# Show the plot
plt.show()
'''
# Extract x and y coordinates from the path
x_coords, y_coords = zip(*path)

# Create a colormap
cmap = plt.cm.plasma  # You can choose any colormap you like
norm = plt.Normalize(vmin=0, vmax=len(path)-1)

# Plot the map image
fig, ax = plt.subplots()
ax.imshow(map_image)

# Plot each segment of the path with a different color
for i in range(len(path) - 1):
    x_values = [x_coords[i], x_coords[i + 1]]
    y_values = [y_coords[i], y_coords[i + 1]]
    ax.plot(x_values, y_values, color=cmap(norm(i)), linewidth=2)

# Plot the points and label the start point
for i, (x, y) in enumerate(path):
    ax.plot(x, y, 'o', color=cmap(norm(i)))  # Plot the point
    if i == 0:
        ax.annotate('Start', (x, y), textcoords="offset points", xytext=(20,-2.5), 
                    ha='center', color='black', fontsize=8, fontweight='bold',
                    bbox=dict(facecolor='white', edgecolor='none', pad=0))

# Remove the grid, axis labels, and ticks
ax.grid(False)  # Disable grid
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks
ax.set_xticklabels([])  # Remove x-axis labels
ax.set_yticklabels([])  # Remove y-axis labels

# Show the plot
plt.show()
