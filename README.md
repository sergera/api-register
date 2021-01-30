## A simple API that registers a user with a valid e-mail address on MongoDB

#### Dependencies OS:

docker
docker-compose

#### Install dependencies:

    make build

#### Run:

    make run

#### Insert user

    curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "sergio joselli", "email": "sergio.joselli@gmail.com"}' \
    http://localhost:8080/user

#### Get users

    curl -X GET http://localhost:8080/users

#### Run in dev mode:

    make run-dev

    Make sure MongoDB is running locally at 27017

#### Insert user

    curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "sergio joselli", "email": "sergio.joselli@gmail.com"}' \
    http://localhost:5000/user

#### Get users

    curl -X GET http://localhost:5000/users

#### For other commands

    make help
