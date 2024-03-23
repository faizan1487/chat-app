import matplotlib.pyplot as plt

# Sample data points
x = [1, 2, 3, 4, 5]
y = [3, 5, 7, 6, 9]

# Calculate the mean of x and y
mean_x = sum(x) / len(x)
mean_y = sum(y) / len(y)

# Calculate the slope (m) and intercept (b) of the best fit line
m = (sum([(xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)]) /
     sum([(xi - mean_x)**2 for xi in x]))
b = mean_y - m * mean_x

# Calculate the predicted y values for each x
predicted_y = [m * xi + b for xi in x]

# Plot the data points and the best fit line
plt.plot(x, y, 'o', label='Data points')
plt.plot(x, predicted_y, label='Best fit line')

# Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Linear Regression with Best Fit Line")

# Add legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
