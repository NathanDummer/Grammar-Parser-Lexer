import math
# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.lst = self.code.split()
        self.length = len(self.lst)


    #goes through and puts multiplication and division statements in parenthesis
    def precedence(self):
        i = 0
        while i < self.length-1:
            if self.lst[i] == "*" or self.lst[i] == "/":
                #case there is a statement in parenthesis that is operated on in front
                if self.lst[i-1] == ")":
                    x = i-2
                    count = 1
                    while count != 0:
                        
                        if self.lst[x] == "(":
                            count -= 1
                        if self.lst[x] == ")":
                            count += 1
                            i+=1
                        x -= 1
                    x += 1
                    
                    self.lst = self.lst[:x] + ["("] + self.lst[x:]
                else:
        
                    self.lst = self.lst[:i-1] + ["("] + self.lst[i-1:]    
                i+=1
            
                #case there is statement in parenthesis that is operated on behind
                if self.lst[i+1] == "(":
                    x = i+2
                    
                    count = 1
                    while count != 0:
                        
                        if self.lst[x] == "(":
                            count += 1
                        if self.lst[x] == ")":
                            count -= 1
                        x += 1

                    self.lst = self.lst[:x] + [")"] + self.lst[x:] 
                else:
                    self.lst = self.lst[:i+2] + [")"] + self.lst[i+2:]
                i+=1
                self.length += 2   
            i+=1

    #helper function that splits parenthesis from variable or values
    def splitLst(self):
        lst = self.lst

        i = 0
        length = len(lst)
        while i < length:
            
            last = len(lst[i]) - 1
            
            if lst[i][0] == '(':
                lst[i] = lst[i][1:]
                lst = lst[:i] + ['('] + lst[i:]
                length += 1
        
            elif lst[i][last] == ')' and len(lst[i]) > 1:
                
                lst[i] = lst[i][:last]
                lst = lst[:i+1] + [')'] + lst[i+1:]
                length += 1
                i-=1
            
            i += 1
        
        
        self.lst = [i for i in lst if i != '']
        self.length = len(self.lst)
        

    # move the lexer position and identify next possible tokens.
    def get_token(self):
        #print("string: ", self.lst[self.position])
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
        
        self.lexer.splitLst()
        
        self.lexer.precedence()
        
        retStr = ""
        while self.lexer.position < self.lexer.length - 1:
            retStr = retStr + self.statement()
        
        return retStr


    # move to the next token.
   # def advance(self):

    # parse the one or multiple statements
   # def program(self):
        
    
    # parse if, while, assignment statement.
    def statement(self):
        str = self.lexer.get_token()
            
        if str == "expression":
            retStr = self.assignment()
        elif str == "if":
            retStr = self.if_statement()
        else:
            retStr = self.while_loop()

        return retStr

    # parse assignment statements
    def assignment(self):
        iter = self.lexer.position + 1
        
        # checks until end of the statement
        while iter < self.lexer.length:
            curr = self.lexer.lst[iter]
            #this checks for parenthesis and ignores them if so
            
            while self.lexer.lst[iter - 1] == '(' or self.lexer.lst[iter] == ')':
                iter += 1
                if iter < self.lexer.length - 1:
                    curr = self.lexer.lst[iter]
                else: break
            
            if curr not in arithm:
                break
            iter += 2
        
        lst = self.lexer.lst[self.lexer.position + 2:iter]
        

        retStr = "('=', '" + self.lexer.lst[self.lexer.position] + "', " + self.arithmetic_expression(lst) + ')'
        self.lexer.position = iter
        return retStr
        
    # parse arithmetic expressions
    def arithmetic_expression(self, lst):
        if len(lst) == 1:
            if lst[0].isdigit(): return lst[0]
            else: return "'" + lst[0] + "'"

        str = ""
        while len(lst) > 1:
            # using recursion in case of parenthesis within arithmetic expressions
            if lst[0] == '(':
                lst[0] = self.arithmetic_expression(lst[1:]) 
                # figuring out how far the parenthesis went
                count = 1
                numPar = 1
                for i in range(1, len(lst[1:])):
                    if lst[i] == '(': 
                        numPar += 1
                    elif numPar == 1 and lst[i] == ')':
                        break
                    elif lst[i] == ')':
                        numPar -= 1
                    count += 1
                lst = lst[:1] + lst[count+1:]
            
            elif lst[1] == ')':
                return lst[0] 
            
            elif len(lst) > 3 and lst[2] == '(':
                lst[2] = self.arithmetic_expression(lst[3:])
                count = 1
                numPar = 1
                for i in range(3, len(lst[3:]) + 2):
                    if lst[i] == '(': 
                        numPar += 1
                    elif numPar == 1 and lst[i] == ')':
                        break
                    elif lst[i] == ')':
                        numPar -= 1
                    count += 1
                
                #only case where lst[2] will be operation in parenthesis so separate print statements
                if lst[0].isdigit():
                    lst[0] = "'" + lst[1] + "', " + lst[0] + ", " + lst[2]
                elif lst[0][0] == '(':
                    lst[0] = "'" + lst[1] + "', " + lst[0] + ", " + lst[2]
                else:
                    lst[0] = "'" + lst[1] + "', '" + lst[0] + "', " + lst[2]
                lst[0] = "(" + lst[0] + ")"
                lst = lst[:1] + lst[count+3:]

            else:
                #This part is used for a normal statement without parenthesis within

                #this is the first statement if it is a digit
                if lst[0].isdigit(): 
                    if lst[2].isdigit():
                        lst[0] = "'" + lst[1] + "', " + lst[0] + ", " + lst[2]
                    else:
                        lst[0] = "'" + lst[1] + "', " + lst[0] + ", '" + lst[2] + "'"
                    lst[0] = "(" + lst[0] + ")"
                
                #this is if there is more than one terms so lst[0] will be another formatted operation
                elif lst[0][0] == '(':
                    if lst[2].isdigit():
                        lst[0] = "'" + lst[1] + "', " + lst[0] + ", " + lst[2]
                    else:
                        lst[0] = "'" + lst[1] + "', " + lst[0] + ", '" + lst[2] + "'"
                    lst[0] = "(" + lst[0] + ")"
                        
                #this is the first statement if it is a variable and not a constant
                else:
                    if lst[2].isdigit():
                        lst[0] = "'" + lst[1] + "', '" + lst[0] + "', " + lst[2] 
                    else:
                        lst[0] = "'" + lst[1] + "', '" + lst[0] + "', '" + lst[2] + "'"
                    lst[0] = "(" + lst[0] + ")"
                lst = lst[:1] + lst[3:]


        return lst[0] 

   
   # def term(self):
    

   # def factor(self):


    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        #find where if statement ends and if there is else statement
        iter = self.lexer.position + 1
        while iter < self.lexer.length:
            curr = self.lexer.lst[iter]
            if curr == "then":
                break
            iter += 1

        #condition inside of if statement
        cond = self.lexer.lst[self.lexer.position + 1:iter]
        self.lexer.position = iter + 1
        retStr = "('if', " + self.condition(cond) + ", " + self.statement()

        #checks if theres an else statement and iterates if so
        if self.lexer.length - 1 > self.lexer.position:
            if self.lexer.lst[self.lexer.position] == "else":
                self.lexer.position += 1
                retStr += ", " + self.statement() + ")"
        else:
            retStr += ")"
        return retStr
        
    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        #find where while loop ends and if there is nested if or while statement
        iter = self.lexer.position + 1
        while iter < self.lexer.length:
            curr = self.lexer.lst[iter]
            if curr == "do":
                break
            iter += 1

        #condition inside of while loop
        cond = self.lexer.lst[self.lexer.position + 1:iter]
        self.lexer.position = iter + 1

        retStr = "('while', " + self.condition(cond) + ", [" + self.statement() + "])"
        return retStr

    #used to format a conditional statement
    def condition(self, lst):
        retStr = ""
        if len(lst) == 3:
            if lst[0].isdigit():
                retStr += "('" + lst[1] + "', " + lst[0] + ", " 
            else:
                retStr += "('" + lst[1] + "', '" + lst[0] + "', "
            if lst[2].isdigit():
                retStr += lst[2] + ")"
            else:
                retStr += "'" + lst[2] + "')"
        else:
            return "-1"
        return retStr
  
def selfTesting():
    code = '''
    x = (5 + 8 * 10)
    '''

    lex = Lexer(code)
    pars = Parser(lex)
    
    ast = pars.parse()
    ast_str = ''.join(map(str, ast))
    print("output: ", ast_str)

#selfTesting()
