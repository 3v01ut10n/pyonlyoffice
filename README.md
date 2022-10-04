## Beginning of work.

1. Create a script and import the module for the library to work:

```
import pyonlyoffice
```

2. Add authorization data:

```
onlyoffice = pyonlyoffice.PyOnlyOffice(
    username="test@example.com",
    password="qwerty123",
    baseurl="https://mistereko.ru/",
)
```

OnlyOffice API - https://api.onlyoffice.com/