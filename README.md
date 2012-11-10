ed
==

Generacja sieci na podstawie tekstu




Instalacja
==========

Najlepiej utworzyć osobne virtualenv:

```bash
$ virtualenv app
. app/bin/activate
```

Zainstalować Pyramid:
```bash
$(app) easy_install pyramid
```

Jeśli brakuje w systemie to doinstalować: networkx, ntlk

W katalogu ED/:
```bash
$(app) python setup.py install
```



Teraz już z katalogu ED/
```bash
$(app) pserve --reload development.ini
```
