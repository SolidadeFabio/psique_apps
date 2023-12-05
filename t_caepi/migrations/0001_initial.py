# Generated by Django 5.0 on 2023-12-05 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaEPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ca_number', models.CharField(max_length=10, unique=True)),
                ('validade', models.DateField()),
                ('pdf', models.FileField(upload_to='caepi_pdfs/')),
            ],
        ),
    ]
