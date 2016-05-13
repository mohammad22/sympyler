import sympyler as sp
import unittest


class Testsympler(unittest.TestCase):
    def setUp(self):
        self.handler = sp.environHandler('x: [1, 2]\n y\nz: range(10, 20)\nt: [10]\n', code = 'a = 1\ndef f():\n    return a\n\n')

    def test_variables(self):
        self.assertEqual(set(self.handler.variables), set(['x', 'y', 'z', 't']))

    def test_variablesets(self):
        self.assertEqual(set(self.handler.variables_set), set(['x_set', 'z_set', 't_set']))
    
    def test_parameterizedvariable(self):
        self.assertEqual(eval('x_set', self.handler.glob_env), [1, 2])
        self.assertEqual(eval('z_set', self.handler.glob_env),\
                range(10, 20))
        self.assertEqual(eval('t_set', self.handler.glob_env), [10])

    def test_codeExecutor(self):
        self.assertEqual(eval('a', self.handler.glob_env), 1)
       
    def test_funcExecutor(self):   
        self.assertEqual(eval('f()', self.handler.glob_env), 1)
        
    def test_evalparameterized(self):
        self.assertEqual(self.handler.evaluator('t'), 10)
    
    def test_evalopenvariable(self):
        from sympy import symbols
        y = symbols('y')
        self.assertEqual(self.handler.evaluator('  y'), y)

    def test_complextevaluator(self):
        from sympy import symbols
        y = symbols('y')
        self.assertIn(self.handler.evaluator('x + y'), { y + 1, y + 2})
        self.assertIn(self.handler.evaluator('    x + y'), { y + 1, y + 2})
   
    def test_emptyparameter(self):
        
        self.handler2 = sp.environHandler('')
        self.assertEqual(self.handler2.variables, [])
        self.assertEqual(self.handler2.message, [])

    def test_textrender(self):
        self.assertIn(self.handler.renderText('hi |$ y + 1 $|.'), {'hi $y + 1$.', 'hi $ 1 + y$.'})
        self.assertIn(self.handler.renderText('hi |$ x + y $|.'), \
        {'hi $1 + y$.', 'hi $2 + y$.', 'hi $y + 1$.', 'hi $y + 2$.'})
       
    def text_latexMixExpr(self):
        self.assertIn(self.handler.renderText('$ x = $ |$ x $|.'), \
        {'$ x = $ $1$.', '$ x = $ $2$.'})

if __name__ == '__main__':
    unittest.main()



