# Triple Integral Visualizer

A Python GUI application that symbolically calculates and **visually animates** triple integrals over rectangular regions in 3D space. Built with **Tkinter**, **SymPy**, **NumPy**, and **Matplotlib**, this tool is ideal for learning, teaching, or demonstrating how triple integrals accumulate volume step-by-step.

---

## Features

-  Enter any valid 3-variable function (e.g. `x*y*z`, `sin(x*y) + z`)
-  Set upper and lower bounds for `x`, `y`, and `z`
-  Choose the **order of integration** (e.g. `dx dy dz`)
-  Visually watch the region of integration fill up as it calculates
-  Adjust **step resolution** and **animation speed** via sliders
-  Symbolically calculates and displays the exact value of the integral

---

##  Function Input Format

The function you enter should follow **Python-style mathematical syntax** and use the variables:

- `x`, `y`, and `z` (case-sensitive)
- Example functions:
  - `x*y*z`
  - `sin(x*y) + z`
  - `exp(-x**2 - y**2 - z**2)`
  - `(x**2 + y**2 + z**2)**0.5`

### Supported operations and functions:

| Operation        | Example         | Notes                        |
|------------------|------------------|-------------------------------|
| Addition         | `x + y + z`      |                              |
| Multiplication   | `x*y*z`          | Use `*` between terms        |
| Exponentiation   | `x**2`, `z**0.5` | Use `**`, not `^`            |
| Trig functions   | `sin(x)`, `cos(y*z)` | From SymPy (`sympy.sin`, etc.) |
| Log/Exp          | `log(x)`, `exp(y)`  | Natural log and exponential |
| No conditionals  | ❌ No `if`, `abs`, or `max` |

If unsure, write your function as you would in Python and avoid functions like `abs()` unless you verify SymPy can parse it.

---

## 🧪 Requirements

- Python 3.7+
- `sympy`
- `numpy`
- `matplotlib`

You can install all dependencies using pip:

```bash
pip install sympy numpy matplotlib
