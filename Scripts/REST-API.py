# -*- coding: utf-8 -*-

### REST-API : Tools to communicate in REST
import requests
r = requests.get('https://github.com/timeline.json')
print(r.text)