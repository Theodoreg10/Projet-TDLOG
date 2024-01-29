# Projet-TDLOG
Site web De gestion de stock

[![Dev](https://img.shields.io/badge/docs-dev-blue.svg)](https://theodoreg10.github.io/Projet-TDLOG/)
[![Code Style: Blue](https://img.shields.io/badge/code%20style-blue-4495d1.svg)](https://github.com/Theodoreg10/Projet-TDLOG)

This repository contains a django app for inventory management.


## Installation and Run

Before running the code tou need to go to stockmng/stockmng/settings.py and change 

ALLOWED_HOSTS = ['theodoreg10.pythonanywhere.com'] to 

ALLOWED_HOSTS = [*]

then run the following command in powershell or cmd
```powershell
Projet-TDLOG> pip install -r requirements.txt

Projet-TDLOG> cd stockmng

Projet-TDLOG/stockmng> python manage.py runserver
```

## Contents

[structure](structure.md)

[templates](templates.md)

[forms](forms.md)

[Models](models.md)

[urls](urls.md)

[views](views.md)


---
layout: default
---
