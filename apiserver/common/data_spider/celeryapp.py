from celery import Celery

app = Celery('celeryapp')
app.config_from_object('config.celery_config')

@app.task
def test():
    print '123'

#if __name__ == '__main__':
#    test.delay()
