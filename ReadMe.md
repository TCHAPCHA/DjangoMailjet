# Django Register/Login Website with DB and email verification using **_Mailjet_**

## SuperUser is not created!
## You must have a registered domain to use Mailjet!

## Using:
### Libs:
* Django 5.*
* Requests
### Running:
* Create file config.py near the manage.py
* Insert into them:
    * MAILJET_AUTH (See how to find it below)
    * sender_email (e.g. no-reply@website.org)
    * sender_name (e.g. WebSite NO-REPLY)
    * django_secret_key (from settings.py)
* Run these commands:
   * pip install -r requirements.txt
   * python manage.py makemigrations
   * python manage.py migrate
   * python manage.py runserver ip:port (e.g. localhost:8000)
* Enter into the browser ip and port that you wrote in runserver
---
* To register Mailjet account you must add a DNS records in cloudflare/domain control panel
* You can also watch Mailjet documentation using this link: https://dev.mailjet.com/email/reference/
# How to find MAILJET_AUTH:
* You need to have an API key and Secret key from your`s Mailjet cabinet.
* You`re going to https://www.base64encode.org/ and writing: API key:Secret key, click encode and copy the result
* Now you have to write into the config.py MAILJET_AUTH = 'Basic (Copied result)', e.g. MAILJET_AUTH = 'dXNlcm5hbWU6cGFzc3dvcmQ='