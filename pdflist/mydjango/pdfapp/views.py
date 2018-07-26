from django.shortcuts import render
from pdfapp.models import PDF, Error
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

def pdfs(request):
    print ("RENDERING PDFS")
    
    filterdate = datetime.now() - timedelta(days=6)
    
    data = PDF.objects.filter(lastDetectedChange__gte=filterdate).order_by('-lastDetectedChange')
    return render(request, 'pdfapp/pdf.html', {'DATA': data})


def errors(request, pdf_id):
    print ("RENDERING ERRORS")
    pdf = get_object_or_404(PDF, pk=pdf_id)
    errorset = pdf.errors.all().order_by('page')

    return render(request, 'pdfapp/errors.html', {'DATA': errorset, 'PDF':pdf})
    