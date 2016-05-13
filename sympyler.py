import re
import os


detector =  re.compile(r'^\s*([^\:\s]*)\s*(?:\:\s*([^\n]*))?\s*(.*)$', re.DOTALL)
symp_lexer = re.compile(r'^(.*?)\|\$(.+?)\$\|(.*)$', re.DOTALL)

class environHandler(object):
    """
    Handles a python  environment with the varibales defined in params_text 
    For initialization of objects of this class, params_text (a text base 
    parameter set) should be given (it ca be empty string), and a global environment.
    There are three main variables:
      -- glob_env: should be passed during parameter initilization, this is
       the global environment of the handler instance;
       if nothing passes, the global environment will be populated just
       by all sympy module objects.
       These are internal properties:
      -- variables: which is a python list containg the string names of all
      the parameters available in environ
      -- variables_set: a python list containing the string 'variable_set' which corresponds to 'variable' from variables list, whihc is the name of a variable_set available in the environ.
      
      This one will contai a list of error messages, that can be used
      to inform the environment user (creator of the instance). The idea
      is to to populate exceptions that may occur in the runtime, instead
      populates these messages that should be used appropritaley, this 
      way end-user will not recieve any internal errors:
      
      -- message: a list of error messages. If every thing goes wrong (in the
      run-time of execution of evaluator method or for example during 
      nitialization of the environment handler) no error or exception will
      be returned, but the corresponding messages will be passed into this list. in this way we can safely for example, pass the result of evaluation of 
      statements to the user, and will be assured that they will not recieve
      any internal errors. On the other hand it is the duty of the creator
      of the handler to deal with these error messages.

      the principal public method:
      
      -- evaluator(self, expr): will return the result of evaluation of expr
      against the environment, if during evaluation
      and exception would rises, None will be returned and a message will be 
      passed into message property of the instance. The expr string should 
      be a meaningful symmpy string against the variables which are defined
      in params_text, also a set of random values are assigned into the 
      parameters which are declared bounded into some range of values.
      For any variable x if a set of constraints is 
      defined after ':' then it will be incorporated in 'x_set' of the environment.
    Example: 
        params_text = ' x : [1, 2]
                        y 
                        z : range(10, 20)
                    '
        then in the environment, you will have three symbolic objects
            x, y, z
        and two objects sets:
            x_set = {1, 2}, z_set = range(10, 20)      
        
        and so, you have access to these objects in
          variables = ['x', 'y', 'z']
          variables_set = ['x_set', 'z_set']
    As soon as, one instance of this class is instatiated, 
    the environment variables, and a random choice for the value of parameters according to params_text is fixed and the environment is ready to evaluate
    symbloic expressions expr according to the setup of this environment.
    Using the pubic method evaluator:
    Example:
        env = environHandler(params_text)
        env.evaluator(expr)
    the expr should be a symbolic expression with variables within the set of 
    variables defined in 'params_text'.
    """

    def __init__(self, params_text, code = None, glob_env = None, detector = detector):
        self.params_text = params_text
        self.code = code
        self.detector = detector
        self.variables = []
        self.variables_set = []
        self.message = []
        self.substitutor = []
        self.glob_env = glob_env
        if self.glob_env is None:
            self.glob_env = {}
            exec("from sympy import *", self.glob_env)
        self.__environment()
        self.__randomizer()
        self.__codeExecutor(self.code)


    def __codeExecutor(self, code = None):
        if code is None:
            code = self.code
        try:
            if not code is None:
                exec(code, self.glob_env)
        except:
            print("Error in code execution\n")
            self.message.append("Code exectuion error")

    def __environment(self):
        params_text = self.params_text
        if not params_text == '':
            try:
                while True:
                    p, l, left = detector.findall(params_text)[0]
                    text = p + " = symbols('" + p + "')"
                    self.variables.append(p)
                    exec(text, self.glob_env)
                    if not l == '':
                        self.variables_set.append(p + '_set') 
                        text = p + "_set = " + l
                        exec(text, self.glob_env)
                    if left == '':
                        break
                    else:
                        params_text = left
            except:
                self.variables = []
                self.variables_set = []
                self.message.append('Environemt initialization Error')


    def __randomizer(self):
       
        import random
        self.substitutor = []
        for var in self.variables:
            var_set = var + '_set'
            if var_set in self.variables_set:
                l = eval("len(" + var_set + ")" , self.glob_env)
                r = random.randint(0, l - 1)
                var_0 = eval(var_set + "[" + repr(r) + "]", self.glob_env)
                self.substitutor.append( "(" + var + ", " + repr(var_0) + ")" )


    def _contextWrapper(self, expr):
        """ 
        returns a new string, ready to evaluate, with the context of the
        current environment, and substitutions made accordingly.
        """
        subs = '[' + ", ".join(self.substitutor) + ']'
        expr = "(" + expr + ")" + ".subs(" + subs + ")"
        return expr


    def evaluator(self, expr):
        try:
            return eval(self._contextWrapper(expr), self.glob_env)
        except:
            
            self.message.append('Expression evaluation error')
            return None


    def inlineLatexer(self, expr):
        """
         First evaluates the expr according to the context, and then 
         returns the string of Latex representation of it, in inline mode.
        """
        lat = "latex(" + self._contextWrapper(expr) + ", mode='inline')"
        try:
            return eval(lat, self.glob_env)
        except:
            self.message.append('Error latex printing')
            return None


    def renderText(self, text):
        """
        Returns a text in which every subtext of the form |$ expr $| is 
        replaced with an evaluated version of expr, represented in latex
        expression format, agianst glob_env of the current 
        environmentHandler instance
        """
        new_text = []
        try:
            while True:
                t = symp_lexer.findall(text)
                if len(t) == 0:
                    new_text.append(text)
                    break
                else:
                    new_text.append(t[0][0])
                    new_text.append(self.inlineLatexer((t[0][1])))
                    text = t[0][2] 
            return ''.join(new_text)        
        except:
            self.message.append('Error in rendering Text.')
            return None





            
