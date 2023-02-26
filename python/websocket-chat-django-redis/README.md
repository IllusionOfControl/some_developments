## Chat-Django 

_proof of concept_

---

Chat on Django web-framework that works via websocket
Requirements:
    
+ Python >3.7
+ Redis

**Run localy**:
```shell
python -m pip install -r requirements.txt
python ./manage.py migrate

# users are created through the creation of superusers
python ./manage.py createsuperuser

python ./manage.py runserver
```

Point your browser to http://localhost:8000
