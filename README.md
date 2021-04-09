# Python-Flask-REST-Redis

### Used Technologies

* Python
* Redis
* Docker

### Project Dependencies

* Flask
* redis
* pytest
* gunicorn
* Swagger-UI


### Run the app

Everything is containerized from the client, backend to the database. So all you need is Docker installed, and then you can run :

```
docker-compose up --build
```

And your app will be up on the *port 8000* !

## Sample CURL Commands


Visit [Swagger](http://localhost:8000/swagger) for all endpoints

#### /api/keys/ (PUT HTTP)
>The following `curl` command set a new key value pair
    
    
    $ curl -X PUT http://127.0.0.1:8000/api/keys/ -H 'content-type: application/json' -d '{"key":"test_key","value":"test_value"}'
 
    {
      "key": "test_key",
      "value": "test_value"
    }

#### /api/keys (GET HTTP)
>The following `curl` command show value of given key
    
    
    $ curl -X GET http://127.0.0.1:8000/api/keys?key=test_key -H 'content-type: application/json'
 
    {
      "key": "test_key",
      "value": "test_value"
    }


## Run the test

There are 8 test cases, however it is possible to increase the number of test cases.
You can run the following command to test endpoints for written test cases

```
docker-compose run web python -m pytest
```

## API Documentation

[Swagger](http://localhost:8000/swagger)

