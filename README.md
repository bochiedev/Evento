# Evento
Evento is an events web app that allows users to view events and admins to perform CRUD operations on events.

#### Installation

To get the app running just simply do:

* Git clone the repo to your machine;
  >  * git clone https://github.com/bochiedev/Evento.git
  >  * cd Evento

* Install virtualenv globally but if you got it you can skip this step;
  > * pip install virtualenv

* Create a virtualenv ;
  > * virtualenv -p python3 venv    
  
* Activate virtualenv ;
  > * source venv/bin/activate  

* Install the requirements;
   > * pip install -r requirements.txt


#### Configurations!

* Add secret key and Mail credentials to .bashrc;
  * Use nano or your favourite editor to edit;
     > * nano ~/.bashrc

  * Add the following to the .bashrc file replacing the value in {} with the correct string;
     > * export SECRET_KEY={your_secret_key}
     > * export EMAIL_HOST_USER={your_email_user}
     > * export EMAIL_HOST_PASSWORD={your_email_password}

* Make/Run Migrations;
  > * python manage.py makemigrations
  > * python manage.py migrate



#### Hurray!! Now Run It!

To start the server just do;
  > python manage.py runserver

The server will be running on    `http://127.0.0.1:8000/`   
