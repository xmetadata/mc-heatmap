from celery import Celery

app = Celery('celeryapp')
app.config_from_object('config.celery_config')

#if __name__ == '__main__':
#    test.delay()
