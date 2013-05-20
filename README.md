# enpy

English syntax for Python

## Programming enpy

is the same as writing in english. The following English (examples/input2.en):

    Compose a function named *firstprime* whose definition is as follows:
    Provided a starting number: *firstprime* will

        Compose a closure named *inner*:
        Which takes a number, and some potential divisor:

            when the number % the divisor is 0, return the divisor;
            otherwise, return the inner of the (number, and the divisor+1)

        return the result of inner of the (number, and 2)

    Test: print the firstprime of (43);assert that the firstprime of (43) is 43;assert the firstprime of (93) is 3
    
generates the following Python:

    #!/usr/bin/env python
    #-*- coding: utf-8 -*-

    """
        input2.py
        ~~~~~~~~~
    """

    def firstprime(number):
       def inner(number, divisor):
           if number % divisor == 0:
               return divisor;
           return inner(number, divisor+1)
       return inner(number, 2)

    if __name__ == '__main__':
         print firstprime(43);assert firstprime(43) == 43;assert firstprime(93) == 3
         
and (in the next version) will run the generated code.
