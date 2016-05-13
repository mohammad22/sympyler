
A very basic usage example:

```python
import sympyler as spy

params_text = ' x : [1, 2]\ny\nz : range(10, 20)\n'
env = spy.environHandler(params_text)
value = spy.env.evaluator('x**2 + y')
```
The value will be `y + 1` or ` y + 4.`

Various, interesting use cases, are visible in the test file. 




