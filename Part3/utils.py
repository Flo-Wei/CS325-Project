# CS325 Project - Part 1
# by Florian Weigelt
#
#   utils file
#
# This is a file with additional code that can be imported and used in other parts of the project later

def plot_response_durations(responses:list):
    import matplotlib.pyplot as plt

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
    


