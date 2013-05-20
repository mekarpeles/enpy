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
    prespacing = leading_spaces(line)
    line = line.strip() if not ':' in line else line.strip().split(':')[0]
    for token in line.split(" "):

        if '**' == token[0] + token[-1]:
            funcname = token[1:-1]
            largs = args.lower()
            if any(largs.index(x) == 0 for x in 
                   ["given", "having", "which takes", "provided"]
                   if x in largs):
                args = args.split(':')[0] if ':' in args else args
                return FUNC % (prespacing * " ", funcname,
                               ', '.join([arg.split(' ')[-1] 
                                          for arg in args.split(',')])
                               )
            return FUNC % (funcname, '')
    raise Exception("Failed to process function header:\n%s" % line)

def main(src, pyfilename, code):
    code.write(HEADER % (pyfilename, '~' * len(pyfilename)))
    index = 0
    lines = src.readlines()
    while index < len(lines):
        line = lines[index]
        line = prune(line)
        sline = line.lower().strip()
        if not sline:
            index += 1
            continue
        if any([sline.index(x) == 0 for x in 
                ["compose", "def", "define", "declare"] if x in sline]):
            index += 1
            args = lines[index].strip()
            while not args:
                index += 1
                args = lines[index].strip()
            code.write(create_function_header(line, args))
        elif "test:" in sline and sline.index('test:') == 0:
            start = line.index(':') + 1
            code.write("\nif __name__ == '__main__':\n")
            line = "    " + line[start:]
            code.write(parse_line(line))
        else:
            code.write(parse_line(line))
        index += 1

if __name__ == "__main__":
    """Parses a .en enpy file into python"""
    en = sys.argv[1]
    py = "%s.py" % os.path.splitext(en)[0]
    with open(en, 'r') as src:
        with open(py, 'wb') as code:
            code.write(HEADER % (py, '~' * len(py)))
            main(src, py, code)
