arithm = {'+', '-', '*', '/'}
cond = {'<', '>', '<=', '>=', '==' , '!='}

# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.lst = self.code.split()
        self.length = len(self.lst)

    # move the lexer position and identify next possible tokens.
    def get_token(self):

        if self.lst[self.position] == 'while':
            return "while"
        elif self.lst[self.position] == 'if':
            return "if"
        else:
            return "expression"


        

# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    # function to parse the entire program
    def parse(self):
        retStr = ""
        while self.lexer.position < self.lexer.length - 1:
            str = self.lexer.get_token()
            if str == "expression":
                retStr = retStr + self.assignment()
            elif str == "if":
                retStr = retStr + self.if_statement()
            else:
                retStr = retStr + self.while_loop()
        
        return retStr


    # move to the next token.
    def advance(self):

    # parse the one or multiple statements
    def program(self):
        
    
    # parse if, while, assignment statement.
    def statement(self):


    # parse assignment statements
    def assignment(self):
     

    # parse arithmetic expressions
    def arithmetic_expression(self):
        
   
    def term(self):
    

    def factor(self):


    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):

    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
    

    def condition(self):