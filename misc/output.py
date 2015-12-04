#!/usr/bin/env python

import os
from blessings import Terminal
import __main__ as main
import functools

term = Terminal()

def START():
    print term.bold('\nSTARTING TASK: [' + os.path.splitext(main.__file__)[0].upper() + ']\n')

def WARNING(message):
    print term.red + term.bold('WARNING: ' + message)

def SUCCESS(message):
    print term.green + term.bold('SUCCESS: ' + message)

def EXIT():
    print term.bold('\nFINISHED TASK: [' + os.path.splitext(main.__file__)[0].upper() + ']\n')

#Exception handler wrapper from http://code.activestate.com/recipes/408937-basic-exception-handling-idiom-using-decorators/
#plus a few changes
def ExpHandler(*pargs):
    def wrapper(f):
        #TODO: remove the need for passing a tuple
        if pargs:
            (handler,li) = pargs
            t = [(ex, handler)
                 for ex in li ]
            t.reverse()
        else:
            t = [(Exception,None)]

        def newfunc(t,*args, **kwargs):
            ex, handler = t[0]
            print('\nStarting [' + f.__name__ + ']\n')
            try:
                if len(t) == 1:
                    f(*args, **kwargs)
                else:
                    newfunc(t[1:],*args,**kwargs)
            except ex,e:
                if handler:
                    handler(e)
                else:
                    print e.__class__.__name__, ':', e

        return functools.partial(newfunc,t)
    return wrapper

#Pick which handler you want to use for the exception
#For example, 
#@ExpHandler(handler,(Exception,))
#or
#@ExpHandler(boto,(Exception,))

def handler(e):
    print 'Caught exception!', e

def boto(e):
    print WARNING('(AWS) ' + str(e.message))

def HTTP(e):
    response = e.response
    if response.status_code != 200:
      error = response.json()['error']
      WARNING('(HTTP Response) ' + str(error['message']).lower())
    else:
      print('it worked')

#Always run when this is imported
START()
#TODO: Wait for process to finish then run EXIT()
