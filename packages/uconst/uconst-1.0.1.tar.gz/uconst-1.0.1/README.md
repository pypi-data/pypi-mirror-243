# uconst
Simple url constructor library.

```python
import uconst

c = uconst.Constructor("api.example.org")

print(c) # == str(c)

c = c / "api" / ["v2", "get_smth"]

print(c.as_str())
```
