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
flask seed-database
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


### Quick Start
Running the backend application in docker.

Starts all services including Postgres, Redis and the api at http://localhost:4070.

```
make up
```

Rebuild and launch all containers including api at http://localhost:4070.
```
make buildup
```

Clean code and stop any docker container.
```
make stop
```

Clean code and destroy docker processes, images and volumes.
```
make destroy
```

Destroy docker processes, images and volumes.
```
make destroy-all
```

Clean code and destroy docker processes.
```
make down
```

Download docker images in parallel.
```
make pull
```

Connect to the shell inside the api container.
```
make shell
```

Connect to the shell inside the Postgres container.
```
make shell-db
```

Connect to the shell inside the Redis container.
```
make shell-redis
```

Remove all compiled files, coverage. 'sudo' maybe needed.
```
make clean
```

Seed database from seed data files.
```
make seed-database
```

Compile requirements.txt from requirements.in and build the images for the api service.
```
make pip-compile
```

Compile requirements.txt from requirements.in upgrading the packages and build the images for the api service.
```
make pip-compile-upgrade
```


Run all tests.
```
make test
```

Run all pytests.
```
make pytest
```

Show pytest help
```
make pytest-h
```

Run pytests (takes args additional via ARGS="..." eg. ``make pytest ARGS="tests/unit/ --reuse-db"`` or ``make pytest ARGS="-m \'mark1 and not mark2\'"``).
```
make pytest
```

Run pytests by keyword eg. ``make pytest-k test_my_serializer (takes additional args via ARGS="..." as above).
```
make pytest-k
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


pip-compile --output-file requirements.txt requirements.in