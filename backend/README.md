# Backend

## Back Library Install
Django와 관련된 의존성 설치
```bash
pip install -r requirements.txt
```

*개별로 설치하는 방법*
python 3.10 기준
```bash
pip install django djangorestframework drf_yasg djangorestframework-simplejwt markdown django-filter pykafka apache-flink install django-allauth django-cors-headers
```

## Django Start
```bash
# backend 폴더에서
django-admin startproject config .
```

## Make Apps
```bash
python manage.py startapp accounts
```

## Django Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

## Django Server Start
```bash
python manage.py runserver
```



