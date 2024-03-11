import math
# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.lst = self.code.split()
        self.length = len(self.lst)

    #helper function that splits parenthesis from variable or values
    def splitLst(self):
        lst = self.lst
        for i in range(len(lst) -1):
            last = len(lst[i])-1
            if lst[i][0] == '(':
                lst[i] = lst[i][1:]
                lst = lst[:i] + ['('] + lst[i:]
        
            elif lst[i][last] == ')':
                lst[i] = lst[i][:last]
                lst = lst[:i+1] + [')'] + lst[i+1:]

        self.lst = [i for i in lst if i != '']
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


arithm = {'+', '-', '*', '/', '='}
cond = {'<', '>', '<=', '>=', '==' , '!='}

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
   # def advance(self):

    # parse the one or multiple statements
   # def program(self):
        
    
    # parse if, while, assignment statement.
   # def statement(self):


    # parse assignment statements
    def assignment(self):
        iter = self.lexer.position + 1
        
        # checks until end of the statement
        while iter < self.lexer.length - 1:
            curr = self.lexer.lst[iter]
            if curr not in arithm:
                break
            iter += 2

        lst = self.lexer.lst[self.lexer.position + 2:iter]
        print("full: ", self.lexer.lst[self.lexer.position:iter])
        print("input: ", lst)

        retStr = "('=', '" + self.lexer.lst[self.lexer.position] + "', " + self.arithmetic_expression(lst) + ')'
        print("return: ", retStr)
        self.lexer.position = iter
        
    
    # parse arithmetic expressions
    def arithmetic_expression(self, lst):
        
        if len(lst) == 1:
            if lst[0].isdigit(): return lst[0]
            else: return "'" + lst[0] + "'"

        str = ""
        for i in range(len(lst)-2):
            
            # using recursion in case of parenthesis within arithmetic expressions
            if lst[i] == '(':
                str = "'" + lst[i+1] + "', " + self.arithmetic_expression(lst[i+1:]) 
                # figuring out how far the parenthesis went
                count = 1
                numPar = 1
                for x in range(len(lst[i+1:])):
                    if x == '(': 
                        numPar += 1
                    elif numPar == 1 and x == ')':
                        break
                    elif x == ')':
                        numPar -= 1
                    count += 1
                i += count
                        
            elif lst[i] == ')':
                return str
            else:
                if lst[i].isdigit():
                    str = "'" + lst[i+1] + "', " + lst[i] + ", "
                else:
                    str = "'" + lst[i+1] + "', '" + lst[i] + ", "
                i += 2

        return "(" + str + ")"
