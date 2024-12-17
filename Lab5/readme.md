# Line Clipping Algorithms

This project is a graphical application for demonstrating line clipping algorithms using Python's Tkinter library. It allows users to visualize the results of the Liang-Barsky and polygon clipping algorithms by loading line segments and a clipping window from a file.

## Features

- **Choose an Algorithm**: Select between the Liang-Barsky algorithm and polygon clipping.
- **Load Data**: Load line segments and clipping window parameters from a text file.
- **Visualize Results**: Visualize the clipping results on a grid canvas.
- **Adjust Grid Scale**: Dynamically adjust the grid scale to enhance visualization.
- **Execution Time Display**: Shows the time taken to execute the selected algorithm.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Installation

1. Clone this repository or download the code.
2. Ensure you have Python installed on your computer.
3. Run the application using the command:

   ```bash
   python line_clipping_app.py
   ```

## File Format for Input Data

The input data file should be structured as follows:

```
N
x1 y1 x2 y2
x1 y1 x2 y2
...
x_min y_min x_max y_max
```

- `N` is the number of line segments.
- Each subsequent line contains the coordinates of the endpoints of each line segment.
- The last line specifies the clipping window coordinates in the format `(x_min, y_min, x_max, y_max)`.

### Example Input File

```
3
-10 -10 10 10
-15 5 5 -15
-20 -20 20 20
-5 -5 5 5
```

## Usage

1. Launch the application.
2. Select the desired algorithm from the dropdown menu.
3. Click on "Load Data" to select your input file.
4. Click "Run" to execute the clipping algorithm. The results will be displayed in green on the canvas.
