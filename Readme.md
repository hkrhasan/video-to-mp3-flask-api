# Video to mp3 converter


## Prerequesites

- install `python3`, `docker`, `kubectl` and `minikube` 
- install `mongodb` and `mysql`

### Step 1 clone this repositery

```
git clone https://github.com/hkrhasan/video-to-audio-flask-api.git
cd video-to-audio-flask-api
```

### Step 2 migrate or create database in mysql

```
cd auth
mysql -u <dbuser> -p < init.sql
```

### Step 3 start auth service

- update `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_DB` and `MYSQL_PORT` in `manifests/configmap.yaml` file
- update `MYSQL_PASSWORD` and `JWT_SECRET` in `manifests/secret.yaml` file

```
kubectl apply -f ./manifests
```


### Step 4 start rabbitmq service
### Step 5 start converter service
### Step 6 start gateway service
### Step 6 start notification service
