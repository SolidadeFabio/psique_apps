from django.shortcuts import get_object_or_404
from .utils import download_certificado
from .models import CaEPI
from datetime import date, datetime
from django.http import HttpResponse
from django.core.files.base import ContentFile


def caepi(request, ca):
    try:
        caepi = CaEPI.objects.get(ca_number=ca)
        print('achou')
        
        if caepi.validade < date.today():
            raise CaEPI.DoesNotExist
        
        response = HttpResponse(caepi.pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{caepi.pdf.name}"'
        return response
    
    except CaEPI.DoesNotExist:
        file_content, data = download_certificado(ca=ca)
        
        c_a = data['CA']
        validade = datetime.strptime(data['Validade'], '%d/%m/%Y').strftime('%Y-%m-%d')

        
        if file_content:
            file_content_file = ContentFile(file_content)
            caepi = CaEPI(
                ca_number=c_a,
                validade=validade,
            )
            caepi.pdf.save(f'CA{ca}.pdf', file_content_file)
            caepi.save()
            
            response = HttpResponse(caepi.pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{caepi.pdf.name}"'
            return response
        
        else:
            return HttpResponse("Não foi possível baixar o arquivo", status=500)
        