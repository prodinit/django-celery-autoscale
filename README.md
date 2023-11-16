# Heading


## Intro
As your web application scales, you will often encounter different reasons to keep track of IP Addresses. Perhaps, you just rolled out an Advert application and need to track visits and interactions in the back-end; perhaps, an 'evil' IP address continously pesters your endpoints without provocation and you'd like to implement a blacklist; better still, you need to track visitors across web pages on a 'IP' basis rather than just sessions.

Or perhaps, you have this biting need to have fun and fill production DBs with IP adresses whether you need it or not.

This application is a quite simple and effective solution to that.

### How to do?
It's quite simple to use. Install with:
```pip install git+https://github.com/prodinit/django-celery-autoscale.git@main```

Next step is to  add `celery_autoscale` to your INSTALLED_APPS like so:

```
INSTALLED_APPS = [
    #... apps I don't care about here
    'celery_autoscale',
]
```