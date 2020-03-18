# esports
Sports

### Requirement:
* Flask
* MySQL
* Rabbit MQ
* ElasticSearch
* Swagger

####Step-1
1. git clone https://github.com/sbsanjaybharti/esports.git
2. docker-compose build
3. docker-compose up

####Step-2
1. open the link http://localhost:8080/dashboard/ here you will get the link url all the container application
2. Open the MySQL phpmyadmin url by IP username: root, password:example
3. Create database "bayes_management"

####Step-3
1. Open the terminal on application
2. Follow the python command:
    3. python run.py db init
    4. python run.py db migrate
    5. python run.py db upgrade
 
####Step-4
1. Open the link http://localhost:8080/dashboard/
2. Run the first API to create the Queue
3. Open the rabbitMQ username: rabbitmq password: rabbitmq
4. Create exchange 'eSports-exchange' and rounding key 'eSports-routing-key' and bind it to queue 'eSports-queue'
5. Now publish json in payload it will be consumed by first API and stored in database

Now you can check the application.

#####Note Links are as follows:
1. Flask API: http://bmapi.docker.localhost/
2. ElasticSearch:http://elasticsearch.docker.localhost
3. RabbitMQ: http://rabbit.docker.localhost
4. phpmyadmin: http://phpmyadmin.docker.localhost (if not working the use IP)