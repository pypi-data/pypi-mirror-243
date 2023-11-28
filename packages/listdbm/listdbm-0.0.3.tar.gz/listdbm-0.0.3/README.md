# Explaining The Library:
---
#### This Library is Useful, Why?

#### Because This Library can be used for `.JSON` Format Databases
# Examples: 
---
Creating a User:
```
from listdbm import SetUser
user = SetUser('rose', 'rosesecretpass1234', 'rosemail@gmail.com')
```
SetUser Args: `name`, `password` and `email`

Result:
```
list: [202, True, {'uuid': '1d0552db-4280-4d7b-83e5-a97a825ba3f5', ...}]
```

# Changelog 0.0.3
---
- Added own file Name Support
- In the User() functions like `name`, `password` and `email` have changed to variables


# Understand More by Exploring...