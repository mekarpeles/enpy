#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    enpy
    ~~~~

    Pronounced 'NP'
"""

import sys
import os

HEADER = """#!/usr/bin/env python
#-*- coding: utf-8 -*-

\"\"\"
    %s
    %s
\"\"\"

"""
FUNC = "%sdef %s(%s):\n"

def innermost_formp(tokens):
    for token in tokens:        
        if ')' in token or '(' in token:
            if '(' in token:
                if token.index('(') < token.index(')'):
                    return False
                return True
    raise IndexError("No closing paren found")
    
def leading_spaces(line):
    """Counts the number of spaces a the beginning of the string"""
    return len(line) - len(line.lstrip())

def prune(expr):
    expr = expr.replace(", and ", ", ")
    expr = expr.replace(" the result of ", " ")
    expr = expr.replace(" the ", " ")
    expr = expr.replace(" that ", " ")
    expr = expr.replace(" of ", "")
    expr = expr.replace(" on ", "")
    expr = expr.replace(" times ", " * ")
    return expr

def parse_expr(expr):    
    expr = prune(expr)
    expr = expr.replace(" is ", " == ")
    code = ""
    tokens = expr.split(' ')
    while tokens:
        token = tokens.pop(0)

        if '(' in token and token.index('(') == 0:
            if '(*' in token:
                pass
            if token == "(product":
                pass
        else:
            code += token + " "

    if '(' in expr:
        if 'product' in expr and expr.index('product') == \
                expr.index('(') + 1:
            pass    
    return expr

def parse_line(line):
    code = ''
    prespacing = leading_spaces(line)
    sline = line.strip().lower()
    if 'when' in sline and sline.index('when') == 0:
        code += "%sif %s == %s:\n%s%s\n" % (
            prespacing * " ",
            sline[sline.index('when ') + 5:sline.index(' is')],
            sline[sline.index('is ') + 3:sline.index(',')],
            (prespacing + 4) * " ",
            sline[sline.index(', ')+ 2:]
            )
    else:
        if 'otherwise' in sline and sline.index("otherwise") == 0:
            sline = sline.replace('otherwise, ', '')
        code += "%s%s\n" % (
            prespacing * " ",
            parse_expr(sline)
            )
    return code

def create_function_header(line, args):
    def funcnamep(token):
        """Determine if this token is the name of a function"""
        return '**' == token[0] + token[-1]

    def cleanline():
        return line.strip() if not ':' in line else line.strip().split(':')[0]

    line = cleanline()
    for token in line.split(" "):
        if funcnamep(token):
            funcname = token[1:-1]
            largs = args.lower()
            if any(largs.index(x) == 0 for x in 
                   ["given", "having", "which takes", "provided", "requiring"]
                   if x in largs):                
                args = args.split(':')[0] if ':' in args else args
                padding = leading_spaces(line) * " "
                variables = ''
                if args.split(' ')[-1].lower() != 'nothing':
                    variables = ', '.join([arg.split(' ')[-1] 
                                          for arg in args.split(',')])
                    return FUNC % (padding, funcname, variables)
            return FUNC % (padding, funcname, variables)
    raise Exception("Failed to process function header:\n%s" % line)

def main(src, filenamepy, code):
    filenamepy = filenamepy.split('/')[-1]
    code.write(HEADER % (filenamepy, '~' * len(py)))

    def funcp(sline):
        return any([sline.index(x) == 0 for x in 
                    ["compose", "def", "define", "declare"] if x in sline])

    def testcasep(sline):
        return "test:" in sline and sline.index('test:') == 0

    lines = src.readlines()
    linenum = 0

    while linenum < len(lines):
        line = prune(lines[linenum])
        sline = line.lower().strip()

        # Skip blank/empty lines
        if not sline:
            linenum +=1
            continue

        # If it's a function
        if funcp(sline):
            linenum += 1

            # Skip until we find the function's params
            args = lines[linenum].strip()
            while not args:
                linenum += 1
                args = lines[linenum].strip()
            code.write(create_function_header(line, args))

        # If testcase
        elif testcasep(sline):
            start = line.index(':') + 1
            code.write("\nif __name__ == '__main__':\n")
            line = "    " + line[start:]
            code.write(parse_line(line))

        # Write code as-is
        else:
            code.write(parse_line(line))

        linenum += 1

if __name__ == "__main__":
    """Parses a .en enpy file into python"""
    en = sys.argv[1]
    filename = os.path.splitext(en)[0]
    py = "%s.py" % filename
    with open(en, 'r') as src:
        with open(py, 'wb') as code:
            main(src, py, code)
