import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D plots


# Function to plot the region of integration
def plot_region(x_range, y_range, z_range, function, order):
    # Clear the previous plot if any
    for widget in plot_frame.winfo_children():
        widget.destroy()

    x, y, z = sp.symbols('x y z')
    f_numeric = sp.lambdify((x, y, z), function, 'numpy')

    # Create meshgrid for x and y
    x_vals = np.linspace(x_range[0], x_range[1], 50)
    y_vals = np.linspace(y_range[0], y_range[1], 50)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = f_numeric(X, Y, 0)  # Fixed z=0 for visualization

    # Create a figure for Tkinter
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Function Value')

    # Embed the figure in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Function to calculate the double/triple integral
def calculate_integral(function, bounds, order):
    x, y, z = sp.symbols('x y z')

    x_lower, x_upper = bounds['x']
    y_lower, y_upper = bounds['y']
    z_lower, z_upper = bounds['z']

    if order == 'dx, dy, dz':
        integral = sp.integrate(function, (x, x_lower, x_upper), (y, y_lower, y_upper), (z, z_lower, z_upper))
    elif order == 'dx, dz, dy':
        integral = sp.integrate(function, (x, x_lower, x_upper), (z, z_lower, z_upper), (y, y_lower, y_upper))
    elif order == 'dy, dx, dz':
        integral = sp.integrate(function, (y, y_lower, y_upper), (x, x_lower, x_upper), (z, z_lower, z_upper))
    elif order == 'dy, dz, dx':
        integral = sp.integrate(function, (y, y_lower, y_upper), (z, z_lower, z_upper), (x, x_lower, x_upper))
    elif order == 'dz, dx, dy':
        integral = sp.integrate(function, (z, z_lower, z_upper), (x, x_lower, x_upper), (y, y_lower, y_upper))
    elif order == 'dz, dy, dx':
        integral = sp.integrate(function, (z, z_lower, z_upper), (y, y_lower, y_upper), (x, x_lower, x_upper))

    return integral


# Function to update the result and plot
def update_result():
    try:
        function = func_entry.get()
        x_lower = float(x_lower_entry.get())
        x_upper = float(x_upper_entry.get())
        y_lower = float(y_lower_entry.get())
        y_upper = float(y_upper_entry.get())
        z_lower = float(z_lower_entry.get())
        z_upper = float(z_upper_entry.get())
        order = order_combobox.get()

        bounds = {
            'x': (x_lower, x_upper),
            'y': (y_lower, y_upper),
            'z': (z_lower, z_upper)
        }

        # Define the function using sympy
        x, y, z = sp.symbols('x y z')
        function_expr = sp.sympify(function)

        # Calculate the integral
        result = calculate_integral(function_expr, bounds, order)
        result_label.config(text=f"Integral Result: {result}")

        # Plot the region
        plot_region((x_lower, x_upper), (y_lower, y_upper), (z_lower, z_upper), function_expr, order)
    except Exception as e:
        result_label.config(text=f"Error: {e}")


# Create the main Tkinter window
root = tk.Tk()
root.title("Double/Triple Integral Visualizer")

# Input fields
tk.Label(root, text="Function (in terms of x, y, z):").grid(row=0, column=0)
func_entry = tk.Entry(root, width=30)
func_entry.grid(row=0, column=1)

tk.Label(root, text="x lower bound:").grid(row=1, column=0)
x_lower_entry = tk.Entry(root, width=10)
x_lower_entry.grid(row=1, column=1)

tk.Label(root, text="x upper bound:").grid(row=2, column=0)
x_upper_entry = tk.Entry(root, width=10)
x_upper_entry.grid(row=2, column=1)

tk.Label(root, text="y lower bound:").grid(row=3, column=0)
y_lower_entry = tk.Entry(root, width=10)
y_lower_entry.grid(row=3, column=1)

tk.Label(root, text="y upper bound:").grid(row=4, column=0)
y_upper_entry = tk.Entry(root, width=10)
y_upper_entry.grid(row=4, column=1)

tk.Label(root, text="z lower bound:").grid(row=5, column=0)
z_lower_entry = tk.Entry(root, width=10)
z_lower_entry.grid(row=5, column=1)

tk.Label(root, text="z upper bound:").grid(row=6, column=0)
z_upper_entry = tk.Entry(root, width=10)
z_upper_entry.grid(row=6, column=1)

tk.Label(root, text="Order of Integration:").grid(row=7, column=0)
order_combobox = ttk.Combobox(root, values=[
    "dx, dy, dz", "dx, dz, dy", "dy, dx, dz",
    "dy, dz, dx", "dz, dx, dy", "dz, dy, dx"
])
order_combobox.grid(row=7, column=1)
order_combobox.set("dx, dy, dz")  # Default

# Button to calculate and plot
calculate_button = tk.Button(root, text="Calculate and Plot", command=update_result)
calculate_button.grid(row=8, column=0, columnspan=2)

# Result display
result_label = tk.Label(root, text="Integral Result: ")
result_label.grid(row=9, column=0, columnspan=2)

# Frame for matplotlib plot
plot_frame = tk.Frame(root)
plot_frame.grid(row=10, column=0, columnspan=2)

# Start the GUI loop
root.mainloop()
