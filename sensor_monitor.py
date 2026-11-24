import random
import csv
import numpy as np
import matplotlib.pyplot as plt

SENSOR_TYPES = ["1: Temperature", "2: Light", "3: Humidity", "4: Pressure", "5: Sound"]
add_to_list = [] #for inputs from user

questions = ("Select a sensor from the following sensors: " + "\n" + str(SENSOR_TYPES),
             "Choose the amount of readings you want to take",
             "What is the maximum limit for the data range",
             "What is the minimum limit for the data range",
             "Choose a threshold value within your range",)

def get_user_input():
    question_counter = 0 #keeps track of which question is asked

    for question in questions:
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

            #Conditions for each question
            if question_counter == 0 and answer not in (1, 2, 3, 4, 5):
                print("Choose a number from 1 to 5")
            elif question_counter == 1 and (answer <= 0 or answer % 1 != 0):
                print("Readings must be a whole number greater than 0")
            elif question_counter == 3 and answer >= add_to_list[2]:
                print("Minimum must be less than the maximum")
            elif question_counter == 4 and not (add_to_list[3] < answer < add_to_list[2]):
                print("Threshold must be between the minimum and maximum")
            else:
                break

        add_to_list.append(answer)
        question_counter += 1
    print(add_to_list)
    generate_readings(add_to_list[1],add_to_list[2],add_to_list[3])


def generate_readings(count, max, min):
    print("Readings generated: ")

    readings = []

    for _ in range(int(count)):
        value = round(random.uniform(min, max))
        readings.append(value)

    print(readings)


def calculate_statistics():
    pass

def find_outliers():
    pass

def save_readings():
    pass

def plot_readings():
    pass

def plot_histogram():
    pass

def main():
    get_user_input() 

if __name__ == "__main__":
    main()

