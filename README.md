# Ethereum tracker

_Tracks given Ethereum addresses and detects any changes to their balances_


👨‍💻 J. Pedro Oliveira ([j.pedrodiasoliveira@gmail.com](mailto:j.pedrodiasoliveira@gmail.com))

### TL;DR

Run server:
`docker-compose -f docker-compose.yml up`

Run tests:
`docker-compose -f docker-compose.test.yml up`

----

### Features

This web app allows to track ethereum addresses simply by submitting it to the 
web ui.
Once the user inserts the address, the webapp validates it (40 hexa digits), and
registers on the database. 

In background, every 60 seconds, the server fetches data for each registered 
ethereum address from the [etherscan.io api](https://etherscan.io) 

The app accepts an `HTTP POST` to `/track` to start tracking an address; 
and an `HTTP GET` to `/status/{address}/` to get details about a given address. 
On the details page, a list of transactions for that address is provided.

### Stack

This project was implemented
using [Django (Python web framework)](https://www.djangoproject.com).

Although it was suggested to go for Rails, Elixir, NodeJS or Rust, I decided to
go with Django. It was mainly a personal choice since it's the framework I'm
most comfortable with. This way I was able to implement all the details that
I consider important, such as _address_ validators, or background tasks.
The app was designed following django pattern Model-View-Template, this the web
ui is managed by the framework. A REST-API can easly be achieved due to the 
class based view approach.

Background jobs are taken care by [Celery](https://docs.celeryproject.org/en/stable/),
that allows to manage periodic and assyncronous taks, and [RabbitMQ](
https://www.rabbitmq.com/) as messages broker.

The database engine is [Sqlite](https://www.sqlite.org/) choosen by it's simlicity
and lightweight. For a production environment, a Mysql or 
PostgreSQL would be a better fit.


---

### Improvement opportunities

1. Correct parsing of confirmed balance an number of blocks
2. Support for contract addresses
3. Login to allow personalization 
4. Notification by email when a change occures
5. REST Api for frontend framework or third-party apps
6. Nginx webserver + gunicorn for deploy/staging (docker) environment
