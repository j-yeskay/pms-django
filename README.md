# *PMS*
---
---
**PMS** is a simple product management system build with django.
___
This project is built for a qualifying task for an internship.  

## How to setup?

Navigate to the directory where you want to store the project and open command line there.

Now from the command line,

#### STEP 0 (clone the repo)
```
git clone https://github.com/j-yeskay/pms-django.git
cd pms-django
```

##### NOTE : USE *PYTHON 3.x.x*, I USED *PYTHON 3.9.6*  


#### STEP 1 (create a venv virtual environment)
``python -m venv virt``

Activate the virtual environment by

**For Windows on cmd**  

``virt\Scripts\activate``

**For Mac**  

``source virt/bin/activate``

#### STEP 2 (install the dependencies)
``pip install -r requirements.txt``  

#### STEP 3 (create SECRET_KEY and set DEBUG = True in settings . py )

Now in the command line
Type **python** and hit enter.
```
>>>import secrets
>>>secrets.token_hex(24)
<a secret key will be generated>
```
Copy the generated secret key and in the **settings . py** file  
Change the code

**FROM THIS**
```
SECRET_KEY = config('SECRET_KEY')
```

**TO THIS**
```
SECRET_KEY = < paste the generated secret key here>
```

**AND FROM THIS**
```
DEBUG = config('DEBUG', cast=bool, default = True)
```  


**TO THIS**
```
DEBUG = True
```  

#### STEP 4 (run the migrations)
```
python manage.py makemigrations
python manage.py migrate
```

#### STEP 5 (run the app)
```
python manage.py runserver
```


