# Part 1 of the CS325 Project

This is the documentation of all my steps taken to get the LLM to run.
I used te Ollama software to run my model since I am already familliar with it.
I also ran the model on my remote PC at home since my laptop does not have the nessesary capacity to even run a small model without heating up too much. I can of course show and explain all the steps I took on the remote server as well. 

## Installation of Ollama
As stated above I ran the Ollama software on a remote PC at home. For that I set up a fresh Ubuntu 24.04 Virtual machine and Installed Docker on it. I used this guide to install docker via the installation script https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script.

After that I used Docker-Compose to run an Instance of Ollama, this is the compose.yaml file:

```yaml
services:
  ollama:
    image: ollama/ollama:latest     # This is the Image, I used the latest version avaible
    container_name: ollama          # The Hostname of the container, not nessesary but helpful
    tty: true                       # nessesary to enable access to the CLI of the container for testing
    ports:                          # the ports that are passed out of the internal docker network
      - 11434:11434                 # in this case I used the standard port of ollama
    networks:                       # The internal Docker Network
      - AI-Network                  # In this case a custom network I created beforehand
    volumes:                        # A permanen storage so the data does not get lost on reboot
      - /docker-data/ollama:/root/.ollama   # Mapped to a folder on the Machine
    restart: unless-stopped         # Tells the container to restat everytine unless I stopped it myself

networks:                           # All the Networks that can be used by the services in this file
  AI-Network:                       # The Network Mentionded above
    external: true                  # signals that the network already exists
```

I then started the container via docker compose and accessed its CLI via `docker exec -it ollama bash`.

There I checked if ollama is running correctly by typing `ollama -v` to view the current verion.
Sice this worked fine I started to download the model I needed. 
Ollama has an extensive list of supported Models including big Names like Llama3.1 or mistral. A full list can be viewed here: https://ollama.com/library

For the usse in this Project I decided on Phi3 with 3.8 Billion Parameters. https://ollama.com/library/phi3:3.8b
This can be simply downloaded by typing `ollama pull phi3:3.8b` into the ollama console.
The Model will then start to download and when it is finished it can be used with `ollama run phi3:3.8b`.
It this was all sucessful we can now swich to python code.


## The Python Code

I decided on using the ollama python library (https://github.com/ollama/ollama-python) to interface with my instance of Ollama.

I then created 2 text files, one for the prompts that were given in the assignent and one for the models replys. 
In the `main.py` file ther is the actual code that interfaces with the model.