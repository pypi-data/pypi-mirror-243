# rich is an optional dependency, users install it if they want to
try:
    from rich import print
except ImportError:
    ...

print("Hello: 1, 2, 3")
print({"a": 1, "b": 2})
