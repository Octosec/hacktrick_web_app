# Hacktrick Conf Web Application Project

### Run with Docker

Run int the following command on the computer where the docker is installed.

```
docker-compose up
```

The project should have worked. You can access on the browser in the following address

```
localhost:8000
```

### Docker commands

Follow in the following method If you want to run command on docker container

```
docker-compose run [container_host_name] [command]
```

For example;
```
docker-compose run web python web/manage.py makemigrations
```
