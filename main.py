import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Function to animate the integration approximation
def plot_region(x_range, y_range, z_range, function, order, steps, interval):
    for widget in plot_frame.winfo_children():
        widget.destroy()

    x, y, z = sp.symbols('x y z')
    f_numeric = sp.lambdify((x, y, z), function, 'numpy')

    fig = plt.Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111, projection='3d')

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()

    x_vals = np.linspace(x_range[0], x_range[1], 50)
    y_vals = np.linspace(y_range[0], y_range[1], 50)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = f_numeric(X, Y, 0)

    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    ax.set_zlim(0, np.max(Z) * 1.2)

    # Plot bars (initially empty)
    bars = []

    def update(frame):
        x_step = (x_range[1] - x_range[0]) / steps
        y_step = (y_range[1] - y_range[0]) / steps
        z_step = (z_range[1] - z_range[0]) / steps

        # Clear previous bars (for smoother animation)
        for bar in bars:
            bar.remove()

        bars.clear()

        # Dynamically select the order of integration
        if order == 'dx, dy, dz':
            # Iterate in x, y, z order
            if frame <= steps:
                for i in range(frame):
                    xi = x_range[0] + i * x_step
                    bar = ax.bar3d(xi, y_range[0], 0, x_step, y_range[1] - y_range[0], 0, color='orange', edgecolor='k', alpha=0.6)
                    bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing X Dimension")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

            elif frame <= 2 * steps:
                for i in range(steps):
                    for j in range(min(frame - steps, steps)):
                        xi = x_range[0] + i * x_step
                        yi = y_range[0] + j * y_step
                        bar = ax.bar3d(xi, yi, 0, x_step, y_step, 0, color='orange', edgecolor='k', alpha=0.6)
                        bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing X and Y Dimensions")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

            else:
                for i in range(steps):
                    for j in range(steps):
                        for k in range(min(frame - 2 * steps, steps)):
                            xi = x_range[0] + i * x_step
                            yi = y_range[0] + j * y_step
                            zi = z_range[0] + k * z_step
                            bar = ax.bar3d(xi, yi, 0, x_step, y_step, f_numeric(xi, yi, zi), color='orange', edgecolor='k', alpha=0.6)
                            bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing X, Y, and Z Dimensions")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

        elif order == 'dy, dx, dz':
            # Iterate in y, x, z order
            if frame <= steps:
                for j in range(frame):
                    yi = y_range[0] + j * y_step
                    bar = ax.bar3d(x_range[0], yi, 0, x_range[1] - x_range[0], y_step, 0, color='orange', edgecolor='k', alpha=0.6)
                    bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing Y Dimension")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

            elif frame <= 2 * steps:
                for j in range(steps):
                    for i in range(min(frame - steps, steps)):
                        yi = y_range[0] + j * y_step
                        xi = x_range[0] + i * x_step
                        bar = ax.bar3d(xi, yi, 0, x_step, y_step, 0, color='orange', edgecolor='k', alpha=0.6)
                        bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing X and Y Dimensions")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

            else:
                for j in range(steps):
                    for i in range(steps):
                        for k in range(min(frame - 2 * steps, steps)):
                            yi = y_range[0] + j * y_step
                            xi = x_range[0] + i * x_step
                            zi = z_range[0] + k * z_step
                            bar = ax.bar3d(xi, yi, 0, x_step, y_step, f_numeric(xi, yi, zi), color='orange', edgecolor='k', alpha=0.6)
                            bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing X, Y, and Z Dimensions")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

        elif order == 'dz, dx, dy':
            # Iterate in z, x, y order
            if frame <= steps:
                for k in range(frame):
                    zi = z_range[0] + k * z_step
                    bar = ax.bar3d(x_range[0], y_range[0], 0, x_range[1] - x_range[0], y_range[1] - y_range[0], 0, color='orange', edgecolor='k', alpha=0.6)
                    bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing Z Dimension")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

            elif frame <= 2 * steps:
                for k in range(steps):
                    for i in range(min(frame - steps, steps)):
                        zi = z_range[0] + k * z_step
                        xi = x_range[0] + i * x_step
                        bar = ax.bar3d(xi, y_range[0], 0, x_step, y_range[1] - y_range[0], 0, color='orange', edgecolor='k', alpha=0.6)
                        bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing X and Z Dimensions")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

            else:
                for k in range(steps):
                    for i in range(steps):
                        for j in range(min(frame - 2 * steps, steps)):
                            zi = z_range[0] + k * z_step
                            xi = x_range[0] + i * x_step
                            yi = y_range[0] + j * y_step
                            bar = ax.bar3d(xi, yi, 0, x_step, y_step, f_numeric(xi, yi, zi), color='orange', edgecolor='k', alpha=0.6)
                            bars.append(bar)
                ax.set_title(f"Step {frame+1} - Showing X, Y, and Z Dimensions")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

        ax.set_xlim(x_range[0], x_range[1])
        ax.set_ylim(y_range[0], y_range[1])
        ax.set_zlim(0, np.max(Z) * 1.2)

    anim = FuncAnimation(fig, update, frames=3 * steps, interval=interval, repeat=False)
    canvas.draw()

# Function to calculate the triple integral
def calculate_integral(function, bounds, order):
    x, y, z = sp.symbols('x y z')
    x_lower, x_upper = bounds['x']
    y_lower, y_upper = bounds['y']
    z_lower, z_upper = bounds['z']

    if order == 'dx, dy, dz':
        integral = sp.integrate(function, (x, x_lower, x_upper), (y, y_lower, y_upper), (z, z_lower, z_upper))
    elif order == 'dy, dx, dz':
        integral = sp.integrate(function, (y, y_lower, y_upper), (x, x_lower, x_upper), (z, z_lower, z_upper))
    elif order == 'dz, dx, dy':
        integral = sp.integrate(function, (z, z_lower, z_upper), (x, x_lower, x_upper), (y, y_lower, y_upper))
    else:
        integral = "Invalid order"

    return integral

# Function to update the integral and plot
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
        steps = int(steps_entry.get())
        interval = int(interval_entry.get())

        bounds = {
            'x': (x_lower, x_upper),
            'y': (y_lower, y_upper),
            'z': (z_lower, z_upper)
        }

        x, y, z = sp.symbols('x y z')
        function_expr = sp.sympify(function)

        result = calculate_integral(function_expr, bounds, order)
        result_label.config(text=f"Integral Result: {result}")

        plot_region((x_lower, x_upper), (y_lower, y_upper), (z_lower, z_upper),
                    function_expr, order, steps, interval)

    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Main window
root = tk.Tk()
root.title("Triple Integral Visualizer")

# Function input
tk.Label(root, text="Function:").grid(row=0, column=0)
func_entry = tk.Entry(root)
func_entry.grid(row=0, column=1)

# Bounds input
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

# Order of integration
tk.Label(root, text="Order of Integration:").grid(row=7, column=0)
order_combobox = ttk.Combobox(root, values=["dx, dy, dz", "dy, dx, dz", "dz, dx, dy"])
order_combobox.set("dx, dy, dz")
order_combobox.grid(row=7, column=1)

# Steps and interval input
tk.Label(root, text="Steps:").grid(row=8, column=0)
steps_entry = tk.Entry(root)
steps_entry.grid(row=8, column=1)

tk.Label(root, text="Interval (ms):").grid(row=9, column=0)
interval_entry = tk.Entry(root)
interval_entry.grid(row=9, column=1)

# Calculate and plot button
calc_button = tk.Button(root, text="Calculate and Plot", command=update_result)
calc_button.grid(row=10, column=0, columnspan=2)

# Result display
result_label = tk.Label(root, text="Integral Result: ")
result_label.grid(row=11, column=0, columnspan=2)

# Plot display frame
plot_frame = tk.Frame(root)
plot_frame.grid(row=12, column=0, columnspan=2)

root.mainloop()