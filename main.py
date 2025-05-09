import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

def plot_region(x_range, y_range, z_range, function, order, steps, interval):
    """
    Visualizes the integration region and process in 3D using matplotlib's animation.

    Parameters:
        x_range, y_range, z_range: Tuples of (min, max) bounds for each variable
        function: sympy symbolic function to evaluate
        order: String representing the order of integration (e.g., "dx, dy, dz")
        steps: Number of subdivisions in each axis
        interval: Delay between animation frames in milliseconds
    """
    # Clear previous plot widgets
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Define symbolic variables and numeric function
    x, y, z = sp.symbols('x y z')
    f_numeric = sp.lambdify((x, y, z), function, 'numpy')

    # Set up 3D plot
    fig = plt.Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()

    # Set plot limits
    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    ax.set_zlim(z_range[0], z_range[1])

    # Compute step sizes
    x_step = (x_range[1] - x_range[0]) / steps
    y_step = (y_range[1] - y_range[0]) / steps
    z_step = (z_range[1] - z_range[0]) / steps

    # Mapping of order string to dimension sequence
    order_map = {
        'dx, dy, dz': ('x', 'y', 'z'),
        'dx, dz, dy': ('x', 'z', 'y'),
        'dy, dx, dz': ('y', 'x', 'z'),
        'dy, dz, dx': ('y', 'z', 'x'),
        'dz, dx, dy': ('z', 'x', 'y'),
        'dz, dy, dx': ('z', 'y', 'x'),
    }

    dim_order = order_map[order]

    # Bounds and step sizes for each dimension
    idx_ranges = {
        'x': (x_range, x_step),
        'y': (y_range, y_step),
        'z': (z_range, z_step)
    }

    def get_coord(var, i):
        """Calculate the coordinate of a variable given its index."""
        return idx_ranges[var][0][0] + i * idx_ranges[var][1]

    def generate_traversal(order, steps):
        """
        Generate the traversal order of subvolumes for animation.

        Parameters:
            order: Tuple of dimension names in integration order
            steps: Number of steps in each dimension

        Returns:
            List of dictionaries indicating the index along each axis
        """
        ranges = [range(steps) for _ in range(3)]
        loops = dict(zip(order, ranges))
        traversal = []

        for i in loops[order[2]]:
            for j in loops[order[1]]:
                for k in loops[order[0]]:
                    index = {order[0]: k, order[1]: j, order[2]: i}
                    traversal.append(index)

        return traversal

    traversal = generate_traversal(dim_order, steps)
    bars_drawn = {}

    def update(frame):
        """Update function for each animation frame."""
        if frame >= len(traversal):
            return

        index = traversal[frame]
        i, j, k = index.get('x', 0), index.get('y', 0), index.get('z', 0)

        x_val = get_coord('x', i)
        y_val = get_coord('y', j)
        z_val = get_coord('z', k)

        height = f_numeric(x_val, y_val, z_val)
        key = (i, j, k)

        if key not in bars_drawn:
            # Draw a 3D bar representing a volume element
            bar = ax.bar3d(x_val, y_val, 0, x_step, y_step, height,
                           color='orange', edgecolor='k', alpha=0.6)
            bars_drawn[key] = bar

        ax.set_title(f"Frame {frame + 1} / {len(traversal)} - Order: {order}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    # Animate the traversal of volume elements
    anim = FuncAnimation(fig, update, frames=len(traversal), interval=interval, repeat=False)
    canvas.draw()

def calculate_integral(function, bounds, order):
    """
    Symbolically calculates the triple integral of a function.

    Parameters:
        function: sympy expression of the integrand
        bounds: Dictionary of bounds for x, y, z
        order: String of integration order (e.g. "dx, dy, dz")

    Returns:
        The evaluated sympy integral or an error string
    """
    x, y, z = sp.symbols('x y z')
    x_lower, x_upper = bounds['x']
    y_lower, y_upper = bounds['y']
    z_lower, z_upper = bounds['z']

    order_map = {
        'dx, dy, dz': [(x, x_lower, x_upper), (y, y_lower, y_upper), (z, z_lower, z_upper)],
        'dx, dz, dy': [(x, x_lower, x_upper), (z, z_lower, z_upper), (y, y_lower, y_upper)],
        'dy, dx, dz': [(y, y_lower, y_upper), (x, x_lower, x_upper), (z, z_lower, z_upper)],
        'dy, dz, dx': [(y, y_lower, y_upper), (z, z_lower, z_upper), (x, x_lower, x_upper)],
        'dz, dx, dy': [(z, z_lower, z_upper), (x, x_lower, x_upper), (y, y_lower, y_upper)],
        'dz, dy, dx': [(z, z_lower, z_upper), (y, y_lower, y_upper), (x, x_lower, x_upper)]
    }

    if order not in order_map:
        return "Invalid order"

    return sp.integrate(function, *order_map[order])

def update_result():
    """
    Parses user input, evaluates the integral, and initiates the plot and animation.
    """
    try:
        # Get user input from the GUI
        function = func_entry.get()
        x_lower = float(x_lower_entry.get())
        x_upper = float(x_upper_entry.get())
        y_lower = float(y_lower_entry.get())
        y_upper = float(y_upper_entry.get())
        z_lower = float(z_lower_entry.get())
        z_upper = float(z_upper_entry.get())
        order = order_combobox.get()
        steps = int(steps_slider.get())
        interval = int(interval_slider.get())

        bounds = {
            'x': (x_lower, x_upper),
            'y': (y_lower, y_upper),
            'z': (z_lower, z_upper)
        }

        # Convert the input function to a sympy expression
        x, y, z = sp.symbols('x y z')
        function_expr = sp.sympify(function)

        # Calculate the integral and update the GUI
        result = calculate_integral(function_expr, bounds, order)
        result_label.config(text=f"Integral Result: {result}")

        # Plot the volume animation
        plot_region((x_lower, x_upper), (y_lower, y_upper), (z_lower, z_upper),
                    function_expr, order, steps, interval)

    except Exception as e:
        result_label.config(text=f"Error: {e}")

# -------------------- GUI Setup --------------------

# Main window
root = tk.Tk()
root.title("Triple Integral Visualizer")

# Input fields for function and bounds
tk.Label(root, text="Function:").grid(row=0, column=0)
func_entry = tk.Entry(root)
func_entry.grid(row=0, column=1)

tk.Label(root, text="X Lower Bound:").grid(row=1, column=0)
x_lower_entry = tk.Entry(root)
x_lower_entry.grid(row=1, column=1)

tk.Label(root, text="X Upper Bound:").grid(row=2, column=0)
x_upper_entry = tk.Entry(root)
x_upper_entry.grid(row=2, column=1)

tk.Label(root, text="Y Lower Bound:").grid(row=3, column=0)
y_lower_entry = tk.Entry(root)
y_lower_entry.grid(row=3, column=1)

tk.Label(root, text="Y Upper Bound:").grid(row=4, column=0)
y_upper_entry = tk.Entry(root)
y_upper_entry.grid(row=4, column=1)

tk.Label(root, text="Z Lower Bound:").grid(row=5, column=0)
z_lower_entry = tk.Entry(root)
z_lower_entry.grid(row=5, column=1)

tk.Label(root, text="Z Upper Bound:").grid(row=6, column=0)
z_upper_entry = tk.Entry(root)
z_upper_entry.grid(row=6, column=1)

# Dropdown for order of integration
tk.Label(root, text="Order of Integration:").grid(row=7, column=0)
order_combobox = ttk.Combobox(root, values=[
    "dx, dy, dz", "dx, dz, dy", "dy, dx, dz", "dy, dz, dx", "dz, dx, dy", "dz, dy, dx"])
order_combobox.set("dx, dy, dz")
order_combobox.grid(row=7, column=1)

# Sliders for animation resolution and speed
tk.Label(root, text="Steps:").grid(row=8, column=0)
steps_slider = tk.Scale(root, from_=2, to=30, orient='horizontal')
steps_slider.set(5)
steps_slider.grid(row=8, column=1)

tk.Label(root, text="Animation Speed (ms):").grid(row=9, column=0)
interval_slider = tk.Scale(root, from_=10, to=1000, resolution=10, orient='horizontal')
interval_slider.set(500)
interval_slider.grid(row=9, column=1)

# Button to trigger computation and plotting
calc_button = tk.Button(root, text="Calculate and Plot", command=update_result)
calc_button.grid(row=10, column=0, columnspan=2)

# Label to display the integral result
result_label = tk.Label(root, text="Integral Result: ")
result_label.grid(row=11, column=0, columnspan=2)

# Frame for plotting the animation
plot_frame = tk.Frame(root)
plot_frame.grid(row=12, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()