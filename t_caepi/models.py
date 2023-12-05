from django.db import models

class CaEPI(models.Model):
    ca_number = models.CharField(max_length=10, unique=True)
    validade = models.DateField()
    pdf = models.FileField(upload_to='caepi_pdfs/')
