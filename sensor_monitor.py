import random
import csv
import numpy as np
import matplotlib.pyplot as plt

SENSOR_TYPES = ["1: Temperature", "2: Light", "3: Humidity", "4: Pressure", "5: Sound"]

questions = ("Select a sensor from the following sensors: " + "\n" + str(SENSOR_TYPES),
             "Choose the amount of readings you want to take",
             "What is the maximum limit for the data range",
             "What is the minimum limit for the data range",
             "Choose a threshold value within your range",)


def get_user_input():
    answers = []  # created fresh each time so old answers never carry over
    for index, question in enumerate(questions):
        while True:
            print("--------------------------------------------------------")
            print(question + " (Enter q to quit)")
            answer = input("Answer: ").strip()

            if answer.lower() == "q":
                print("Quitting")
                exit()

            try:
                answer = float(answer)
            except ValueError:
                print("Please enter a number")
                continue

            # Conditions for each question
            if index == 0 and answer not in (1, 2, 3, 4, 5):
                print("Choose a number from 1 to 5")
            elif index == 1 and (answer <= 0 or answer % 1 != 0):
                print("Readings must be a whole number greater than 0")
            elif index == 3 and answer >= answers[2]:
                print("Minimum must be less than the maximum")
            elif index == 4 and not (answers[3] < answer < answers[2]):
                print("Threshold must be between the minimum and maximum")
            else:
                break

        answers.append(answer)
    return answers


def generate_readings(count, maximum, minimum):
    readings = []
    for _ in range(int(count)):
        value = round(random.uniform(minimum, maximum), 2)
        readings.append(value)
    print("Readings generated:")
    print(readings)
    return readings


def calculate_statistics(readings):
    if len(readings) == 0:
        print("No readings available. Generate or load some first.")
        return
    data = np.array(readings)
    print("--------------------------------------------------------")
    print("Statistics")
    print("Count:             ", len(data))
    print("Mean:              ", round(float(np.mean(data)), 2))
    print("Median:            ", round(float(np.median(data)), 2))
    print("Standard deviation:", round(float(np.std(data)), 2))
    print("Lowest reading:    ", float(np.min(data)))
    print("Highest reading:   ", float(np.max(data)))


def find_outliers(readings, threshold):
    if len(readings) == 0:
        print("No readings available. Generate or load some first.")
        return
    if threshold is None:
        print("No threshold set. Generate new readings or enter a threshold after loading.")
        return
    data = np.array(readings)
    above = data[data > threshold]
    below = data[data < threshold]
    print("--------------------------------------------------------")
    print("Threshold:", threshold)
    print("Readings above the threshold:", len(above), list(above))
    print("Readings below the threshold:", len(below), list(below))


def save_readings(readings):
    if len(readings) == 0:
        print("No readings to save. Generate or load some first.")
        return
    filename = input("File name to save to (e.g. readings.csv): ").strip()
    if filename == "":
        filename = "readings.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"

    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Reading number", "Value"])
            for number, value in enumerate(readings, 1):
                writer.writerow([number, value])
        print("Saved", len(readings), "readings to", filename)
    except OSError:
        print("Could not save the file. Check the name and try again.")


def load_readings():
    filename = input("File name to load (e.g. readings.csv): ").strip()
    if not filename.endswith(".csv"):
        filename += ".csv"

    loaded = []
    try:
        with open(filename, newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row in reader:
                loaded.append(float(row[1]))
    except FileNotFoundError:
        print("File not found.")
        return []
    except (ValueError, IndexError):
        print("That file isn't in the right format.")
        return []

    print("Loaded", len(loaded), "readings from", filename)
    print(loaded)
    return loaded


def plot_readings(readings, threshold, sensor_name):
    if len(readings) == 0:
        print("No readings to plot. Generate or load some first.")
        return
    plt.figure()
    plt.plot(range(1, len(readings) + 1), readings, marker="o", label="Readings")
    if threshold is not None:
        plt.axhline(threshold, color="red", linestyle="--", label="Threshold")
    plt.title(sensor_name + " readings")
    plt.xlabel("Reading number")
    plt.ylabel("Value")
    plt.legend()
    plt.show()


def plot_histogram(readings, threshold, sensor_name):
    if len(readings) == 0:
        print("No readings to plot. Generate or load some first.")
        return
    plt.figure()
    plt.hist(readings, bins=10, edgecolor="black")
    if threshold is not None:
        plt.axvline(threshold, color="red", linestyle="--", label="Threshold")
        plt.legend()
    plt.title(sensor_name + " histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()


def visualise_data(readings, threshold, sensor_name):
    if len(readings) == 0:
        print("No readings to visualise. Generate or load some first.")
        return
    print("--------------------------------------------------------")
    print("1: Plot readings")
    print("2: Plot histogram")
    print("3: Back")
    choice = input("Choice: ").strip()
    if choice == "1":
        plot_readings(readings, threshold, sensor_name)
    elif choice == "2":
        plot_histogram(readings, threshold, sensor_name)
    elif choice != "3":
        print("Please choose 1, 2 or 3")


def ask_threshold():
    # used after loading a file, since the file doesn't store the threshold
    while True:
        answer = input("Enter a threshold value (or press Enter to skip): ").strip()
        if answer == "":
            return None
        try:
            return float(answer)
        except ValueError:
            print("Please enter a number")


def main():
    readings = []
    threshold = None
    sensor_name = "Sensor"

    while True:
        print("--------------------------------------------------------")
        print("1: Generate readings")
        print("2: Load existing readings")
        print("3: Save readings")
        print("4: Visualise data")
        print("5: Statistics and threshold check")
        print("q: Quit")
        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            answers = get_user_input()
            sensor, count, maximum, minimum, threshold = answers
            sensor_name = SENSOR_TYPES[int(sensor) - 1].split(": ")[1]
            readings = generate_readings(count, maximum, minimum)
        elif choice == "2":
            loaded = load_readings()
            if len(loaded) > 0:
                readings = loaded
                sensor_name = "Loaded"
                threshold = ask_threshold()
        elif choice == "3":
            save_readings(readings)
        elif choice == "4":
            visualise_data(readings, threshold, sensor_name)
        elif choice == "5":
            calculate_statistics(readings)
            find_outliers(readings, threshold)
        elif choice == "q":
            print("Quitting")
            break
        else:
            print("Please choose 1-5 or q")


if __name__ == "__main__":
    main()