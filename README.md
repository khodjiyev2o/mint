# Django Boiler-Plate
Back-End for {company_name}.

Visit the [Demo]() url.com 
## Super user credentials for testing:
````
email: admin@gmail.com
passwordl: admin
````

## Getting Started

1. Clone the project from the Github repo :

````
git clone https://github.com/khodjiyev2o/django-boilerplate
````

2. Go to the project directory -> ./ax

3. Create virtual environment :

````
python3 -m venv venv
````

4. Activate virtual environment  : 

````
source\venv\bin\activate
````

if you are using Windows ,then :

````
venv\Scripts\activate
````
if UNIX/LINUX, then :
````
source venv\bin\activate
````
4. Create the .env file and fill out the missing values. You can look at all missing values in sample.env file:

For example: 
````
SECRET_KEY='django-insecure-$i^+*htoqjh4@g%vtw&k2u1ow7jq-84-6fg)u2pt3(l&h1su^9'
````
5. Run the project locally in virtual environment

````

pip3 install -r requirements/dev.txt

````
6. Run the project locally without docker

````

$  python3 manage.py runserver

````

    
7. To run the tests of the project:
````

$  python3 manage.py test

````

8. To run the project in Dockerfile in dev mode, create .env.dev  and .env.dev.db files 
    looking at the sample sample.env and sample.db.env:
````

$ docker-compose -f docker-compose.yml up -d --build

````
9. To run the project in Dockerfile in production mode, create .env.prod  and .env.prod.db files 
    looking at the sample sample.env and sample.db.env:
````

$ docker-compose -f docker-compose.prod.yml up -d --build

````

10. Difference between production mode and development is that there is no 
    nginx and gunicorn installed in development mode