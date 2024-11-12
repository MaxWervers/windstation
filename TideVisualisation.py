import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Load the data
file_path = 'Waterhoogte Astronomisch t.o.v. NAP Brouwershavensche Gat 08.csv'
data = pd.read_csv(file_path, delimiter=';', parse_dates=[['Datum', 'Tijd (NL tijd)']], dayfirst=True)

# Rename columns for easier access
data.columns = ['Datetime', 'Locatie', 'Waterhoogte', 'Extremen']
data['Waterhoogte'] = pd.to_numeric(data['Waterhoogte'], errors='coerce')
data.set_index('Datetime', inplace=True)

# Filter data for a specific day
specific_day = '2024-11-16'
day_data = data.loc[specific_day]

# Find the min and max water levels for color scaling
min_water_level = day_data['Waterhoogte'].min()
max_water_level = day_data['Waterhoogte'].max()

# Normalize water levels to the range [0, 1]
normalized_water_levels = (day_data['Waterhoogte'] - min_water_level) / (max_water_level - min_water_level)

# Create a color gradient from green to orange to red
colors = [mcolors.to_rgb("green"), mcolors.to_rgb("orange"), mcolors.to_rgb("red")]
cmap = mcolors.LinearSegmentedColormap.from_list("green-orange-red", colors)

# Map normalized values to colors
day_data['Color'] = normalized_water_levels.apply(lambda x: cmap(x))

# Plotting the water levels with the color gradient
plt.figure(figsize=(12, 6))
for i in range(len(day_data) - 1):
    plt.plot(day_data.index[i:i+2], day_data['Waterhoogte'].iloc[i:i+2], color=day_data['Color'].iloc[i], linewidth=3)

plt.xlabel('Time')
plt.ylabel('Waterhoogte (cm)')
plt.title(f'Water Level Gradient for {specific_day} (Green=Low, Red=High)')
plt.grid()
plt.show()
