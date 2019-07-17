# AndelaEatsApi
[![CircleCI](https://circleci.com/gh/andela/AndelaEatsApi.svg?style=svg)](https://circleci.com/gh/andela/AndelaEatsApi)
[![Coverage Status](https://coveralls.io/repos/github/andela/AndelaEatsApi/badge.svg?branch=develop)](https://coveralls.io/github/andela/AndelaEatsApi?branch=develop)

This backend application serves as an API backend to the AndelaEats application, which allows Andelans to pre-order lunch a day ahead



https://andelaeats.herokuapp.com/



## Usage
Using  Python download and install the latest version of Python 3+.

The application is built with Python

To clone the respository execute the following command.
```
git clone https://github.com/andela/andelaeatsapi.git
```
Navigate into the cloned project directory.

Edit the `env-sample` file with your gmail credentials and save it as `.env`

Change the parameters in there to your own settings.

The key ```FLASK_APP``` must be set to ```run```. The value of the`APP_ENV` between 

`development` and `testing` in order to run the application `development` or `testing` 

mode respectively.

On the prompt execute the following 
```
export $(cat .env)
```


Execute the following code to install all the application dependencies.
```
python install -r requirements.txt
```

Execute the following code to migrate all data tables/object
```
python run.py db migrate
```


Execute the following code to seed the database
```
flask seed_database
```

Execute the following command in the terminal to start the redis server
```
bash redis.sh
```

Execute the following at the command line
```
python run.py runserver
```

Browse the application in the url
```
http://localhost:5000
```

### Features of Andela Eats App
- View available meals
- View order history
- Rate a meal



### Testing
Tests can be run using
```
pytest
```