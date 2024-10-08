# Generated by Django 5.0.3 on 2024-09-07 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0009_remove_documentsubmission_document_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentsubmission',
            name='document_type',
            field=models.CharField(blank=True, choices=[('medical_report', '의무기록지/진료비 내역서'), ('wage_statement', '근 3개월 간의 임금내역(통장사본)'), ('witness_statement', '목격자 진술서'), ('accident_confirmation', '사고 사실확인서'), ('alien_registration', '외국인 등록증')], max_length=50, null=True),
        ),
    ]
