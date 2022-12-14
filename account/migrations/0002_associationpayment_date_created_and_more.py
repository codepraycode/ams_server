# Generated by Django 4.1.1 on 2022-09-21 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0004_alter_associationgroups_name_associationmemeber'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='associationpayment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default="2022-9-9"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='associationpayment',
            name='date_paid',
            field=models.DateTimeField(),
        ),
        migrations.AlterUniqueTogether(
            name='associationlevy',
            unique_together={('association', 'label')},
        ),
    ]
