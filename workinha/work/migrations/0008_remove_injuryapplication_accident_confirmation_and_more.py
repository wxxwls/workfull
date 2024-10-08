# Generated by Django 5.0.3 on 2024-09-07 11:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0007_injuryapplication_accident_confirmation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='injuryapplication',
            name='accident_confirmation',
        ),
        migrations.RemoveField(
            model_name='injuryapplication',
            name='alien_registration',
        ),
        migrations.RemoveField(
            model_name='injuryapplication',
            name='medical_report',
        ),
        migrations.RemoveField(
            model_name='injuryapplication',
            name='wage_statement',
        ),
        migrations.RemoveField(
            model_name='injuryapplication',
            name='witness_statement',
        ),
        migrations.CreateModel(
            name='DocumentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('medical_report', '의무기록지/진료비 내역서'), ('wage_statement', '근 3개월 간의 임금내역(통장사본)'), ('witness_statement', '목격자 진술서'), ('accident_confirmation', '사고 사실확인서'), ('alien_registration', '외국인 등록증')], max_length=50)),
                ('uploaded_file', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
