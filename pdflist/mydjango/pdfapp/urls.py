from django.conf.urls import url
from django.urls import path
from pdfapp.views import pdfs, errors


urlpatterns = [
    path('', pdfs, name='pdfs'),
    path('errors/<int:pdf_id>/', errors, name='errors'),
   
    
]


