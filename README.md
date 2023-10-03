# Image Uploader
<div id="top"></div>


This relies on the Django Rest Framework application, which incorporates the essential functionalities for interacting with Redis, Celery, and PostgreSQL.
It exclusively offers the Django Rest Framework UI, so please consult the documentation to access the available URLs. 

## Table of contents
* [Technologies Used](#technologies-used)
* [Features implemented](#features-implemented)
* [Available Urls](#available-urls)
* [How To Set Up Locally](#how-to-set-up-locally)

## Technologies Used
* Python 3.10
* Django 4.2.5
* Redis 5.0.1
* Celery 5.3.4
* Django REST 3.14
* PostgreSQL 2.9.8
* Docker-compose

## Features Implemented
- users are able to upload images via HTTP request
- users are able to list their images
- three builtin `account tiers Basic, Premium and Enterprise`
  - users that have a `"Basic"` plan after uploading an image get: 
    - a link to a thumbnail that's 200px in height
  - users that have a `"Premium"` plan get:
    - a link to a thumbnail that's 200px in height
  - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
  - users that have a `"Enterprise"` plan get
    - a link to a thumbnail that's 200px in height
    - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
    - ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))
- apart from the builtin tiers, admins can create arbitrary tiers with the following things configurable:
  - `arbitrary thumbnail sizes`
  - `presence of the link to the originally uploaded file`
  - `ability to generate expiring links`
- admin UI has been done via django-admin
- tests of the image and account tiers
- validations

<p align="right">(<a href="#top">back to top</a>)</p>

## Available Urls
ADMIN URLS
- http://127.0.0.1:8000/admin

ACCOUNT URLS
- http://127.0.0.1:8000/accounts/login
- http://127.0.0.1:8000/accounts/logout

AUTHENTICATED USERS
- http://127.0.0.1:8000/images
- http://127.0.0.1:8000/images/expiring-links/ (Available only for ENTERPRISE Tier)



## How To Set Up Locally
The simplest method involves using docker-compose.

Here are the steps:
- clone the repo 
- navigate to the project folder
- run `sudo docker-compose build`
- run `sudo docker-compose up`
- admin with superuser privileges will be created
- Visit either of these URLs: `localhost:8000/admin/` or `127.0.0.1:8000/admin/`, and input following credentials:
  - `login: hexadmin`
  - `password: hexadmin`
- create new user via Django admin site
- login using `http://127.0.0.1:8000/accounts/login` url.
- use urls for AUTHENTICATED USERS to upload images and generate expiring links.