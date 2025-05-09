import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import itertools

def plot_region(x_range, y_range, z_range, function, order, steps, interval):
    for widget in plot_frame.winfo_children():
        widget.destroy()

    x, y, z = sp.symbols('x y z')
    f_numeric = sp.lambdify((x, y, z), function, 'numpy')

    fig = plt.Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111, projection='3d')

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()

    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    ax.set_zlim(z_range[0], z_range[1])

    bars = []

    def update(frame):
        for bar in bars:
            bar.remove()
        bars.clear()

        x_step = (x_range[1] - x_range[0]) / steps
        y_step = (y_range[1] - y_range[0]) / steps
        z_step = (z_range[1] - z_range[0]) / steps

        order_map = {
            'dx, dy, dz': ('x', 'y', 'z'),
            'dx, dz, dy': ('x', 'z', 'y'),
            'dy, dx, dz': ('y', 'x', 'z'),
            'dy, dz, dx': ('y', 'z', 'x'),
            'dz, dx, dy': ('z', 'x', 'y'),
            'dz, dy, dx': ('z', 'y', 'x'),
        }

        dim_order = order_map[order]

        idx_ranges = {
            'x': (x_range, x_step),
            'y': (y_range, y_step),
            'z': (z_range, z_step)
        }

        def get_coord(var, i):
            return idx_ranges[var][0][0] + i * idx_ranges[var][1]

        max_frames = steps * 3
        phase = frame // steps
        step = frame % steps + 1

        for i1 in range(step if phase >= 0 else 0):
            for i2 in range(step if phase >= 1 else 1):
                for i3 in range(step if phase >= 2 else 1):
                    idx = {dim_order[0]: i1, dim_order[1]: i2, dim_order[2]: i3}
                    x_val = get_coord('x', idx['x']) if 'x' in idx else x_range[0]
                    y_val = get_coord('y', idx['y']) if 'y' in idx else y_range[0]
                    z_val = get_coord('z', idx['z']) if 'z' in idx else z_range[0]

                    height = f_numeric(x_val, y_val, z_val)
                    bar = ax.bar3d(x_val, y_val, 0, x_step, y_step, height, color='orange', edgecolor='k', alpha=0.6)
                    bars.append(bar)

        ax.set_title(f"Step {frame + 1} - Order: {order}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    anim = FuncAnimation(fig, update, frames=steps * 3, interval=interval, repeat=False)
    canvas.draw()

def calculate_integral(function, bounds, order):
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

# GUI Setup
root = tk.Tk()
root.title("Triple Integral Visualizer")

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

tk.Label(root, text="Order of Integration:").grid(row=7, column=0)
order_combobox = ttk.Combobox(root, values=[
    "dx, dy, dz", "dx, dz, dy", "dy, dx, dz", "dy, dz, dx", "dz, dx, dy", "dz, dy, dx"])
order_combobox.set("dx, dy, dz")
order_combobox.grid(row=7, column=1)

tk.Label(root, text="Steps:").grid(row=8, column=0)
steps_entry = tk.Entry(root)
steps_entry.grid(row=8, column=1)

tk.Label(root, text="Interval (ms):").grid(row=9, column=0)
interval_entry = tk.Entry(root)
interval_entry.grid(row=9, column=1)

calc_button = tk.Button(root, text="Calculate and Plot", command=update_result)
calc_button.grid(row=10, column=0, columnspan=2)

result_label = tk.Label(root, text="Integral Result: ")
result_label.grid(row=11, column=0, columnspan=2)

plot_frame = tk.Frame(root)
plot_frame.grid(row=12, column=0, columnspan=2)

root.mainloop()