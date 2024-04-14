"""
Black Hole Visualization using Matplotlib.

This script generates a visualization of a black hole with its accretion disk,
event horizon, singularity, and Hawking radiation. It utilizes theoretical physics
equations to calculate and display the Schwarzschild radius and simulate the accretion
disk around a black hole.

Author: Ricard Santiago Raigada García
Date: 14/04/2024
"""
import numpy as np
from matplotlib import patches
import matplotlib.pyplot as plt


def schwarzschild_radius(M):
    """
    Calculate the Schwarzschild radius for a given mass.

    Parameters:
    - M: float, Mass of the black hole in solar masses.

    Returns:
    - float, Schwarzschild radius in meters.
    """
    G = 6.67430e-11  # gravitational constant in m^3 kg^-1 s^-2
    c = 299792458  # speed of light in m/s
    M = M * 1.98847e30  # convert mass from solar masses to kg
    return 2 * G * M / c**2


def accretion_disk(x, y, Rs):
    """
    Simulate the brightness and color of the accretion disk around a black hole.

    Parameters:
    - x, y: arrays, Coordinate grids for the disk.
    - Rs: float, Schwarzschild radius of the black hole.

    Returns:
    - array, Calculated brightness multiplied by color adjustment.
    """
    r = np.sqrt(x**2 + y**2)
    # Exponential brightness decay
    brightness = np.exp(-((r - Rs * 3) / Rs))
    # Color fades from white at center to black at edge
    color = np.clip(1 - r / (5 * Rs), 0, 1)
    return brightness * color


# Parameters for the black hole and visualization
M = 10  # mass of the black hole in solar masses
Rs = schwarzschild_radius(M)  # Schwarzschild radius

# Coordinate grid for the simulation
x = np.linspace(-5 * Rs, 5 * Rs, 400)
y = np.linspace(-5 * Rs, 5 * Rs, 400)
X, Y = np.meshgrid(x, y)
Z = accretion_disk(X, Y, Rs)

# Visualization setup
fig, ax = plt.subplots(figsize=(10, 10), dpi=600)
image = ax.imshow(
    Z,
    extent=(
        x.min(),
        x.max(),
        y.min(),
        y.max()),
    origin='lower',
    cmap='inferno',
    interpolation='bilinear')
ax.set_aspect('equal')
ax.axis('off')  # Turn off the axis for visual clarity

# Event Horizon
event_horizon = patches.Circle(
    (0, 0), Rs, linewidth=2, edgecolor='cyan', facecolor='none')
ax.add_patch(event_horizon)
ax.text(
    0,
    Rs + 1.4 * Rs,
    "Event Horizon",
    color='cyan',
    ha='center',
    va='bottom',
    fontsize=10)
ax.text(
    0,
    Rs + 0.9 * Rs,
    "$R_s = \\frac{2GM}{c^2}$",
    color='cyan',
    ha='center',
    va='bottom',
    fontsize=15)

# Singularity
singularity = patches.Circle((0, 0), Rs * 0.1, color='white')
ax.add_patch(singularity)
ax.text(
    0,
    0,
    "Singularity",
    color='black',
    ha='center',
    va='center',
    fontsize=10)

# Interior Space
ax.annotate(
    'Interior Space',
    xy=(0, -0.5 * Rs),
    xytext=(3 * Rs, -2 * Rs),
    arrowprops=dict(
        facecolor='white',
        shrink=0.05),
    color='white',
    ha='center',
    fontsize=10)
ax.text(0, -Rs - 1.2 * Rs, "Space and time are distorted",
        color='white', ha='center', va='top', fontsize=10)

# Hawking Radiation
for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
    ax.annotate('',
                xy=(2 *
                    Rs *
                    np.cos(angle), 2 *
                    Rs *
                    np.sin(angle)
                    ),
                xytext=(Rs *
                        np.cos(angle), Rs *
                        np.sin(angle)),
                arrowprops=dict(
                    arrowstyle="->",
                    color='red')
                )
ax.text(
    3 * Rs,
    1.3 * Rs,
    "Hawking Radiation",
    color='red',
    ha='center',
    va='center',
    fontsize=10)
ax.text(
    3 * Rs,
    0.9 * Rs,
    "$\\frac{\\hbar c^3}{8\\pi k_BGM}$",
    color='red',
    ha='center',
    va='center',
    fontsize=15)

# Save and show the figure
FIG_PATH = "./Black_hole_visualization_HR.png"
fig.savefig(FIG_PATH, dpi=600, bbox_inches='tight', pad_inches=0)
