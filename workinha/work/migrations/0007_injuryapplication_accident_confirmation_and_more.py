# Generated by Django 5.0.3 on 2024-09-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0006_remove_injuryapplication_accident_report_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='injuryapplication',
            name='accident_confirmation',
            field=models.FileField(blank=True, null=True, upload_to='accident_confirmations/'),
        ),
        migrations.AddField(
            model_name='injuryapplication',
            name='alien_registration',
            field=models.FileField(blank=True, null=True, upload_to='alien_registrations/'),
        ),
        migrations.AddField(
            model_name='injuryapplication',
            name='medical_report',
            field=models.FileField(blank=True, null=True, upload_to='medical_reports/'),
        ),
        migrations.AddField(
            model_name='injuryapplication',
            name='wage_statement',
            field=models.FileField(blank=True, null=True, upload_to='wage_statements/'),
        ),
        migrations.AddField(
            model_name='injuryapplication',
            name='witness_statement',
            field=models.FileField(blank=True, null=True, upload_to='witness_statements/'),
        ),
    ]
