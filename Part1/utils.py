# CS325 Project - Part 1
# by Florian Weigelt
#
#   utils file
#
# This is a file with additional code that can be imported and used in other parts of the project later


class LLM_Message():
    """
    This class is for storing a Chat history of a conversation with a LLM in the right format 
    and make it easy to add to the chat history if the conversation continues
    """

    def __init__(self) -> None:
        self.message = []                                           # initialise the list that stores the chat history

    def add_user_message(self, content:str):
        """
        This method can add a user Prompt to the chat history.
        Arguments:
        """
        if not isinstance(content, str):                            # check if the input is really a string
            raise ValueError("Message content must be a String")    # raise error if not

        new_message = {                                             # create a dict that contains:
            "role": "user",                                         # role: user means that it is a prompt from the user
            "content": content                                      # content is the actual text of the promt
        }
        self.message.append(new_message)                            # append the new message to the chat history
    
    def add_response(self, model_response: dict):
        """
        This method adds a response from the model. 
        It takes in the whole response dict as an input
        and only appends the actual message.
        """
        if not isinstance(model_response, dict):                    # check if input is really a dict
            raise ValueError("Model Response must be a Dict")       # raise error if not
        self.message.append(model_response["message"])              # append only the actual response to the history 

    def get_history(self):
        """
        returns the whole conversation as a formated string
        """
        history = ""                                                # initialize the string
        for elem in self.message:                                   # go through every element in the chat history 
            content = elem['content'].replace('\n', '')             # remove all line breaks
            history += f"{elem['role']}: {content} \n"              # format the text into a readable format and add it to the string
        return history
    
    def get_message(self):
        """
        returns the whole conversation as a list of dicts
        this list can be directly used as input in a LLM
        """
        return self.message
    


