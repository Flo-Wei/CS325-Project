# CS325 Project - Part 3
# by Florian Weigelt
#
#   utils code file
#
# This is a file with additional code that can be imported and used in other parts of the project later

import matplotlib.pyplot as plt
import numpy as np
import json
import os
import logging

def plot_response_durations(responses:list):
    """
    This function is only for debug purposes.
    It plots the durations of different process durations during llm chat completions
    """

    # Extract data for the plot
    total_duration = [item["total_duration"] / 1e9 for item in responses]
    load_duration = [item["load_duration"] / 1e9 for item in responses]
    prompt_eval_duration = [item["prompt_eval_duration"] / 1e9 for item in responses]
    eval_duration = [item["eval_duration"] / 1e9 for item in responses]

    # Create x-axis based on the index of each response
    indices = list(range(len(responses)))

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(indices, total_duration, label='Total Duration (s)')
    plt.plot(indices, load_duration, label='Load Duration (s)')
    plt.plot(indices, prompt_eval_duration, label='Prompt Eval Duration (s)')
    plt.plot(indices, eval_duration, label='Eval Duration (s)')

    # Labeling and title
    plt.xlabel('Review Index')
    plt.ylabel('Duration (seconds)')
    plt.title('Durations of API Responses by Type')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_sentiment_counter(data):
    """
    This function plots the number of positive, neutral and negative reviews for each product as a bar chart

    data format: {"item_name": Counter()}
    """
    # Extract data for each sentiment type
    positive_counts = [count['positive'] for count in data.values()]
    negative_counts = [count['negative'] for count in data.values()]
    neutral_counts = [count['neutral'] for count in data.values()]

    # Set bar width
    bar_width = 0.25

    # Set positions for each bar group
    index = np.arange(len(data))

    # Create the plot
    fig, ax = plt.subplots()

    # Plot each sentiment type
    bars_positive = ax.bar(index - bar_width, positive_counts, bar_width, label='Positive', color='blue')
    bars_neutral = ax.bar(index, neutral_counts, bar_width, label='Neutral', color='orange')
    bars_negative = ax.bar(index + bar_width, negative_counts, bar_width, label='Negative', color='red')

    # Add text labels above the bars to display the counts
    for bars in [bars_negative, bars_positive, bars_neutral]:
        ax.bar_label(bars, padding=3)

    # Add labels, legend, and title
    ax.set_ylabel('Counts')
    ax.set_title('Sentiment Analysis by Device')
    ax.set_xticks(index)
    ax.set_xticklabels(data.keys(), rotation=15, ha='right')
    ax.grid(True, linestyle="--", axis='y')
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


def load_input_file(file_path:str):
    """
    This function loads an input file with item names, urls and a prompt template for sentiment analysis. 
    """
    with open(os.path.abspath(file_path), 'r') as file:
        data = json.load(file)
        logging.debug(f"loaded {len(data['items'])} items from input file")
        return data["items"], data["prompt_template"]
    

def save_data(data, file_path:str):
    """
    Saves data to a file in json format. 
    """
    file_path = os.path.abspath(file_path)
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        logging.error(f"An error occurred while writing to the file: {e}")