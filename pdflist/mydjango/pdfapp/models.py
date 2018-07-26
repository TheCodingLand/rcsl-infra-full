from django.db import models


class PDF(models.Model):
    hashstr = models.CharField(max_length=250, unique=True)
    size = models.CharField(max_length=150, unique=False, blank=True, null=True)
    name = models.CharField(max_length=2000, null=True)
    lastmod = models.DateTimeField(null=True)
    pages = models.IntegerField(null=True, blank = True)
    lxt = models.CharField(max_length=200, null=True, blank=True)
    archived = models.BooleanField(default=True)
    profil =models.CharField(max_length=200, null = True,unique=False)
    tool =models.CharField(max_length=200, null = True,unique=False)
    producer =models.CharField(max_length=200, null = True,unique=False)
    pdfversion =models.CharField(max_length=200, null = True,unique=False)
    lastDetectedChange = models.DateTimeField(null=True, blank=True)


    def get_last_error(self):
        try:
            #print (self.errors.all().last())
            return self.errors.all().last()
          
        except IndexError:
            pass
    def __str__(self):
        return "%s" % self.name



 

class Error(models.Model):
    profil =models.CharField(max_length=200, null = True,unique=False) 
    text = models.CharField(max_length=2000, unique=True, null = True)
    name = models.CharField(max_length=2000, unique=False, null = True)
    page = models.CharField(max_length=2000, unique=False, null=True, blank=True)
    pdf = models.ManyToManyField(PDF, related_name='errors')
    
    def __str__(self):
        return "%s" % self.text


class Solution(models.Model):

    title = models.CharField(max_length=2000, null = True)  
    text = models.CharField(max_length=2000, null = True)
    error = models.OneToOneField(Error, null=True, blank=True, on_delete=models.CASCADE,  related_name='solution')
    def __str__(self):
        return "%s" % self.title