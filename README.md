# DRF User Activity Tracker
## _Log All User Activities_

![version](https://img.shields.io/badge/version-1.0.0-blue.svg)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)
<a href="https://github.com/bigmo94"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>

An API Logger of User Activity for your Django Rest Framework project.

It logs all the API information for content type "application/json".

Note: It logs just API information for registered user. (Anonymous User Activities are ignored.) 

1. User_ID
2. URL_PATH
3. URL_NAME
4. Request Body
5. Request Headers
6. Request Method
7. API Response
8. Status Code
9. API Call Time
10. Server Execution Time
11. Client IP Address

You can log API information into the database or listen to the logger signals for different use-cases, or you can do both.

* The logger usage a separate thread to run, so it won't affect your API response time.

## Requirements
* Django
* Django Rest Framework
* Simple JWT

## Installation

Install or add drf-user-activity-tracker.
```shell script
pip install drf-user-activity-tracker
```

Add in INSTALLED_APPS
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_user_activity_tracker',  #  Add here
]
```

Add in MIDDLEWARE
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'drf_user_activity_tracker.middleware.activity_tracker_middleware.ActivitytrackerMiddleware', # Add here
]
```

#### * Add these lines in Django settings file.

## Store logs into the database
Log every request into the database.
```python
DRF_ACTIVITY_TRACKER_DATABASE = True  # Default to False
```

* Logs will be available in Django Admin Panel.

* The search bar will search in Request Body, Response, Headers and API URL.

* You can also filter the logs based on the "created_time" date, Status Code and Request Methods.

Note: Make sure to migrate. It will create a table for logger if "DRF_ACTIVITY_TRACKER_DATABASE" is True else if already exists, it will delete the table.

## To listen for the logger signals.
Listen to the signal as soon as any API is called. So you can log the API data into a file or for different use-cases.
```python
DRF_ACTIVITY_TRACKER_SIGNAL = True  # Default to False
```
Example code to listen to the API Logger Signal.
```python
"""
Import ACTIVITY_TRACKER_SIGNAL
"""
from drf_user_activity_tracker import ACTIVITY_TRACKER_SIGNAL


"""
Create a function that is going to listen to the API logger signals.
"""
def listener_one(**kwargs):
    print(kwargs)

def listener_two(**kwargs):
    print(kwargs)

"""
It will listen to all the API logs whenever an API is called.
You can also listen signals in multiple functions.
"""
ACTIVITY_TRACKER_SIGNAL.listen += listener_one
ACTIVITY_TRACKER_SIGNAL.listen += listener_two

"""
Unsubscribe to signals.
"""

ACTIVITY_TRACKER_SIGNAL.listen -= listener_one
```

### Queue

DRF ACTIVITY TRACKER usage queue to hold the logs before inserting into the database. Once queue is full, it bulk inserts into the database.

Specify the queue size.
```python
DRF_ACTIVITY_TRACKER_QUEUE_MAX_SIZE = 50  # Default to 50 if not specified.
```

### Interval

DRF ACTIVITY TRACKER also waits for a period of time. If queue is not full and there are some logs to be inserted, it inserts after interval ends.

Specify an interval (In Seconds).
```python
DRF_ACTIVITY_TRACKER_INTERVAL = 10  # In Seconds, Default to 10 seconds if not specified.
```
Note: The API call time (created_time) is a timezone aware datetime object. It is actual time of API call irrespective of interval value or queue size.
### Skip namespace
You can skip the entire app to be logged into the database by specifying namespace of the app as list.
```python
DRF_ACTIVITY_TRACKER_SKIP_NAMESPACE = ['APP_NAMESPACE1', 'APP_NAMESPACE2']
```

### Skip URL Name
You can also skip any API to be logged by using url_name of the API.
```python
DRF_ACTIVITY_TRACKER_SKIP_URL_NAME = ['url_name1', 'url_name2']
```

Note: It does not log Django Admin Panel API calls and history logs list API calls.

### Hide Sensitive Data From Logs
You may wish to hide sensitive information from being exposed in the logs. 
You do this by setting `DRF_ACTIVITY_TRACKER_EXCLUDE_KEYS` in settings.py to a list of your desired sensitive keys. 
The default is
```python
DRF_ACTIVITY_TRACKER_EXCLUDE_KEYS = ['password', 'token', 'access', 'refresh']
# Sensitive data will be replaced with "***FILTERED***".
```

### Change default database to store API logs
```python
DRF_ACTIVITY_TRACKER_DEFAULT_DATABASE = 'default'  # Default to "default" if not specified
"""
Make sure to migrate the database specified in DRF_ACTIVITY_TRACKER_DEFAULT_DATABASE.
"""
```

#### Using Mongodb database
```shell script
pip install pymongo==3.12.1 djongo
```
Add in Databases:
```
DATABASES = {
    'db_name': {    # Default to "default"
        'ENGINE': 'djongo',
        'NAME': 'your-db-name'
    }
}
```

Make migrate on specefic database:
```
python manage.py migrate --database=db_name
```

### Want to identify slow APIs? (Optional)
You can also identify slow APIs by specifying `DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE` in settings.py.

A new filter (By API Performance) will be visible, and you can choose slow or fast API.
```python
DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE = 200  # Default to None
# Specify in milli-seconds.
```

### Want to log only selected request methods? (Optional)
You can log only selected methods by specifying `DRF_ACTIVITY_TRACKER_METHODS` in settings.py.
```python
DRF_ACTIVITY_TRACKER_METHODS = ['GET', 'POST', 'DELETE', 'PUT']  # Default to empty list (Log all the requests).
```

### Want to see the API information in local timezone? (Optional)
You can also change the timezone by specifying `DRF_ACTIVITY_TRACKER_TIMEDELTA` in settings.py.
It won't change the Database timezone. It will still remain UTC or the timezone you have defined.
```python
DRF_ACTIVITY_TRACKER_TIMEDELTA = 330 # UTC + 330 Minutes = IST (5:Hours, 30:Minutes ahead from UTC) 
# Specify in minutes.
```
```python
# Yoc can specify negative values for the countries behind the UTC timezone.
DRF_ACTIVITY_TRACKER_TIMEDELTA = -30  # Example
```

### API with or without Host
You can specify an endpoint of API should have absolute URI or not by setting this variable in DRF settings.py file.
```python
DRF_ACTIVITY_TRACKER_PATH_TYPE = 'ABSOLUTE'  # Default to ABSOLUTE if not specified
# Possible values are ABSOLUTE, FULL_PATH or RAW_URI
```

Considering we are accessing the following URL: http://127.0.0.1:8000/api/v1/?page=123
DRF_ACTIVITY_TRACKER_PATH_TYPE possible values are:
1. ABSOLUTE (Default) :   

    Function used ```request.build_absolute_uri()```
    
    Output: ```http://127.0.0.1:8000/api/v1/?page=123```
    
2. FULL_PATH

    Function used ```request.get_full_path()```
    
    Output: ```/api/v1/?page=123```
    
3. RAW_URI

    Function used ```request.get_raw_uri()```
    
    Output: ```http://127.0.0.1:8000/api/v1/?page=123```
    
    Note: Similar to ABSOLUTE but skip allowed hosts protection, so may return an insecure URI.


### Use DRF ACTIVITY TRACKER Model to query 
You can use the DRF Activity Log Model to query some information.

Note: Make sure to set "DRF_ACTIVITY_TRACKER_DATABASE = True" in settings.py file.
```
from drf_user_activity_tracker.models import ActivityLogModel

"""
Example:
Select records for status_code 200.
"""
result_for_200_status_code = ActivityLogModel.objects.filter(status_code=200)
```

DRF Activity Log Model:
```
class ActivityLogModel(models.Model):
    user_id = models.IntegerField()
    api = models.CharField(max_length=1024, help_text='API URL')
    url_path = models.CharField(max_length=512)
    url_name = models.CharField(max_length=255)
    headers = models.TextField()
    body = models.TextField()
    method = models.CharField(max_length=10, db_index=True)
    client_ip_address = models.CharField(max_length=50)
    response = models.TextField()
    status_code = models.PositiveSmallIntegerField(help_text='Response status code', db_index=True)
    execution_time = models.DecimalField(decimal_places=5, max_digits=8,
                                         help_text='Server execution time (Not complete response time.)')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.api

    @property
    def event_name(self):
        if hasattr(settings, 'EVENT_NAME'):
            if isinstance(settings.EVENT_NAME, dict):
                return settings.EVENT_NAME.get(self.url_name, self.url_name)
        return self.url_name

    class Meta:
        db_table = 'drf_activity_log'
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

```

### API Call For History Of Activities By Users Or Admin 

Add in your_project_root/project_name/urls.py
```
urlpatterns = [
    path('service_admin_zone/', admin.site.urls),
    path('activity-logs/', include('drf_user_activity_tracker.urls')),
]
```
##### Access to this API by following URL:
{{ your_base_url }}/activity-logs/history/

##### The response includes these:

1. id
2. event_name
3. client_ip_address
4. created_time

By default event name is url_name. You can also change the event name by specifying `DRF_ACTIVITY_TRACKER_EVENT_NAME` in settings.py.
```python
DRF_ACTIVITY_TRACKER_EVENT_NAME = {
        'user_register': 'Registeration',
        'orders-redeem': 'Redeem Card',
}
```
### Note:
After sometime, there will be too many data in the database. Searching and filter may get slower.
If you want, you can delete or archive the older data.
To improve the searching or filtering, try to add indexes in the 'drf_activity_log' table.