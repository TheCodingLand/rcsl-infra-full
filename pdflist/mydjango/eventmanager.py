import os
import logging
import redis, time, json, datetime
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'

django.setup()
from pdfapp.models import PDF, Error
r = redis.StrictRedis(host='redis-rcsl', port=6379, db=1)

logging.warning("starting Script for redis import")
while True:
    
    keys = r.keys('*')
    if len(keys) == 0:
        time.sleep(1)
    for key in keys:
        try:
            filedict = json.loads(r.get(key).decode('utf-8'))
        except:
            r.delete(key)
        pdf, created = PDF.objects.get_or_create(hashstr=filedict['hash'])
        if created == False:
            logging.warning("creating file in db")

        pdf.name = filedict['name']
        pdf.producer = filedict['producer']
        pdf.tool = filedict['tool']
        pdf.pdfversion = filedict['pdfversion']
        pdf.lxt = filedict['lxt']
        pdf.pages = int(filedict['pages'])
        pdf.lastmod = filedict['lastmod']
        pdf.profil = filedict['profil']
        pdf.size = filedict['size']
        if created:
            pdf.lastDetectedChange = datetime.datetime.now()
        pdf.save()
           
        for error in filedict['errors']:
            e, created = Error.objects.get_or_create(text=error)
            e.profil = filedict['profil']
            if ":" in error and "Page" in error:
                message = error.split(":")
                e.page = int(message[0].replace("Page","").replace(" ", ""))
                e.name = message[1] 
            else:
                e.name = error
            e.pdf.add(pdf)
            e.save()

        r.delete(key)
    