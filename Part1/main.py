# CS325 Project - Part 1
# by Florian Weigelt
#
#   main code file
#
# This is the main python file that takes the prompts from te promps.txt file line by line
# and sends them to the Ollama instance of the remote PC mentioned in the REAMDE.md.
# The responses are then written into the replys.txt file.


from ollama import Client               # The Ollama module
import os                               # for interacting with the operating system
from tqdm import tqdm                   # for adding a progress bar
from utils import LLM_Message           # importing the Message Class from the utils file



if __name__ == "__main__":

    ollama_host_ip = "http://192.168.100.8:11434"                       # this is the ip of the remote pc and the port of ollama
    client = Client(host=ollama_host_ip)                                # connecting to the Ollama instance on the remote PC

    working_dir=os.path.dirname(os.path.abspath(__file__))              # detecting the path of the current file
    messages = LLM_Message()                                            # initializing the Message object

    with open(os.path.join(working_dir,"prompts.txt"), "r") as f:       # open the prompts file in read only mode
        prompts = f.readlines()                                         # read all lines and save them in a list

    for line in tqdm(prompts, desc="Progress"):                         # go through each line/prompt and add a progress bar 
        messages.add_user_message(line)                                 # add the first user prompt to the chat history
        
        response = client.chat(                                         # open a chat with Ollama
            model='phi3:3.8b',                                          # use the Model phi3 with 3.8 billion parameters
            messages=messages.get_message())                            # send a list with the complete chat history to the model

        messages.add_response(response)                                 # add the response from the model to the chat history

    with open(os.path.join(working_dir, "replys.txt"), "w") as f:       # open the replys file in write mode
        f.write(messages.get_history())                                 # write the whole chat history into the file 