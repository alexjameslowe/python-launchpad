
def validateArgs(args):
  if(args.show_this == "99"):
    return 'No you cant pass in 99 here.'
  
  return None


info = {

   #This is the argument which will select this task.
  'taskArg':'example_task',

   #This is the name of the task to run. Note that there must be a Task.py and 
   #a Monitor.py file in the task folder.
  'taskName':'ExampleTask',
  
   #Here are the other arguments that will be present in the command-line.
  'args': [
      
    #This is a flag-only arg "-test-arg". It just comes through as "1" if present in the 
    #command arguments.
    {
      'name':'test_arg',
      'help':'This is a test flag-only argument',
      'flag':True
    },

    # Here's another one and this one takes the same parameters as the add_argument function.
    # e.g. help='Get version info', default="0", const="1", nargs='?'
    # Two things to note:
    #
    # 1. the 'required' option is not present. Required is always going to be false. If we have 
    # a CLI with mutliple different modes and schemas for the arguments, then they really all have
    # to be optional and we have to enforce requiredness through other means.
    #  
    # 2. We have the name field, which is the dash_delimited version of the argument, 
    # i.e., show_this -> -show-this on the command line.
    
    { 
      'name':'show_this',
      'help':'Get the information', 
      'default':None 
    }

  ],

  # The validator. An argument that takes the parsed args object as the single
  # argument and does validation. All of the arguments have to be optional for reasons
  # stated above, and because of that, we have to do validation manually. If there's
  # something wrong with the arguments, then the validator's job is to return
  # an error message. A return value of None will indicate that nothing is wrong.
  'validator': validateArgs

}