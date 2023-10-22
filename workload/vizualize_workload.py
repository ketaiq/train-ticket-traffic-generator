import pandas as pd
import matplotlib.pyplot as plt


def visualize_integer_array(csv_file_path):
    try:
        # Read the CSV file using pandas skipping header
        data = pd.read_csv(csv_file_path)

        # Convert the DataFrame to a list
        integer_array = data.values.tolist()

        if len(integer_array) > 1:
            integer_array = [int(item[0]) for item in integer_array]
        print(integer_array)

        # integer_array = integer_array[:96]
        # print(len(integer_array))

        # Plot the integer array
        plt.plot(integer_array)
        plt.xlabel("Hour")
        plt.ylabel("Value")
        plt.xticks(range(0, 60 // 15 * 24, 4), range(24))
        plt.title("Visualization of the Integer Array")
        plt.grid(True)
        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Provide the path to your CSV file here
csv_file_path = "workload/by_overlapped_hours/workload_12hours_1.csv"
visualize_integer_array(csv_file_path)
