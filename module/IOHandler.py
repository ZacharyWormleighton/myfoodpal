class IOHandler:
    """
    A class to handle input and output with the console, sepcifically input validation.

    ...

    Methods
    -------
    input_():
        Returns a valid input, or False for an invalid input.
    validate_input(_input):
        Returns True if an input is valid or False if an input is invalid.
    """
    lastInput = ""

    def __init__(self):
        self.lastInput = ""
    
    def input_(self):
        '''
        Returns a valid input, or False for an invalid input.
        '''
        _input = input()
        if self.validate_input(_input):
            return _input
        else:
            return False
    
    def validate_input(self, _input):
        '''
        Returns True if an input is valid or False if an input is invalid.

                Parameters:
                        _input (string): An input string

                Returns:
                        is_valid (boolean): Boolean of the validation
        '''
        is_valid = False
        # Perform input validation
        if _input != "":
            is_valid = True
        return is_valid