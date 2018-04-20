# Cathink_ImageX



Deployment Requirement

0. Please make sure you have installed the following library packages in your project interpreter, Python 3.6
   [Django 2.0.X, Pillow, django-widget-tweaks, django-tagging, djangorestframework]
1. In images/model.py, you should comment out line 34, 70 which have TagField and uncomment line 33, 69 to use CharField for tag.*
2. Run 'makemigrations' then 'migrate' in manage.py
3. Reverse the changes of step 1, comment out line 33, 69 and uncomment line 34, 70 to use TagField for tag in images/model.py.*
4. Repeat step 2, run 'makemigrations' then 'migrate' in manage.py
5. Run the command 'createsuperuser' in manage.py as administrator account of imageX.
6. Ready for use now.

*
The imageX implements the "tagging" functionality using the library 'Django-Tagging'.
The library 'Django-Tagging' must be included in INSTALLED_APPS[] of setting.py.
Then, run the 'migrate' command in manage.py to creates the necessary database tables.
We cannot directly use its functionalities, e.g. TagField along with the above process in one 'migration'
Therefore, you should use CharField for 'tag' and migrate first.
Then, modify the images/model.py to reverse the changes to use TagField and migrate.


