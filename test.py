import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_trajectory_with_velocity_color(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract relevant columns
    vx = data.iloc[:, -4]  # Forward velocity (vx)
    yaw_rate = data.iloc[:, -1]  # Yaw rate (cmd_omega)
    time = data.iloc[:, 0]  # Time

    # Initialize position arrays
    x_pos = np.zeros(len(vx))
    y_pos = np.zeros(len(vx))
    yaw = np.zeros(len(vx))

    # Calculate positions based on forward velocity and yaw rate
    for i in range(1, len(vx)):
        dt = time[i] - time[i - 1]
        yaw[i] = yaw[i - 1] + yaw_rate[i] * dt
        x_pos[i] = x_pos[i - 1] + vx[i] * np.cos(yaw[i]) * dt
        y_pos[i] = y_pos[i - 1] + vx[i] * np.sin(yaw[i]) * dt

    # Chop the second half of the trajectory
    x_pos = x_pos[:len(x_pos)//2 + 5]
    y_pos = y_pos[:len(y_pos)//2 + 5]
    vx = vx[:len(vx)//2 + 5]

    # Plot the trajectory with color proportional to the velocity
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(x_pos, y_pos, c=vx, cmap='Greens', s=10)
    plt.colorbar(scatter, label='Velocity (vx)')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    # plt.title('2D Trajectory of the Agent')
    plt.grid(True)
    plt.axis('equal')
    # make colorbar limits 0 to 0.15
    plt.clim(0, 0.15)

    # scatter some points to show the targets
    red1 = [3,1]
    blu1 = [-1,7]
    red2 = [3.5,7.7]
    blu2 = [1.5,12]
    red3 = [6.25,11]

    plt.scatter(*red1, color='red', s=100, marker='o', label='Red Target 1')
    plt.scatter(*blu1, color='blue', s=100, marker='o', label='Blue Target 2')
    plt.scatter(*red2, color='red', s=100, marker='o', label='Red Target 3')
    plt.scatter(*blu2, color='blue', s=100, marker='o', label='Blue Target 4')
    plt.scatter(*red3, color='red', s=100, marker='o', label='Red Target 5')

    # set xlim and ylim
    # plt.xlim(-6, 8)
    # plt.axis('off')
    # tight layout
    plt.tight_layout()
    plt.show()

# Example usage
plot_trajectory_with_velocity_color('/media/makramchahine/dji_loggers/1702219309.68_ctrnn_wiredcfccellgs_110hz.csv')
