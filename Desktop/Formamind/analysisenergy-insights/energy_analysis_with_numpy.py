import numpy as np

# Sample energy levels of users over 7 days
# Each row represents one user
data = np.array([
    [60, 65, 70, 68, 72, 75, 73],
    [50, 52, 55, 54, 58, 57, 60],
    [80, 82, 85, 87, 83, 88, 87],
])

# Task 1: Mean and standard deviation for each user
mean_per_user = np.mean(data, axis=1)
std_per_user = np.std(data, axis=1)

print("Average energy per user:", mean_per_user)
print("Standard deviation per user:", std_per_user)

# Task 2: Daily energy change rate (%) for user 1
rate_of_change_user1 = np.diff(data[0]) / data[0][:-1] * 100
print("Daily energy change rate for user 1 (%):", rate_of_change_user1)

# Task 3: Normalize data with Min-Max Scaling
normalized_data = (data - np.min(data, axis=1, keepdims=True)) / \
                  (np.max(data, axis=1, keepdims=True) - np.min(data, axis=1, keepdims=True))
print("Normalized energy data:", normalized_data)

# Task 4: Compare user energy levels on the last day
last_day = data[:, -1]
best_user_index = np.argmax(last_day)
worst_user_index = np.argmin(last_day)
print(f"Highest energy on last day: User {best_user_index + 1}")
print(f"Lowest energy on last day: User {worst_user_index + 1}")

# Task 5: Detect outliers using Z-Score
z_scores = (data - np.mean(data)) / np.std(data)
outliers = np.where(np.abs(z_scores) > 2)

if outliers[0].size > 0:
    print("Outliers detected at indices:", list(zip(outliers[0], outliers[1])))
else:
    print("No outliers found.")
