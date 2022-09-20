# Generated by Django 4.1.1 on 2022-09-20 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('association', '0004_alter_associationgroups_name_associationmemeber'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationLevy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='Levy label')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levies', to='association.association')),
            ],
            options={
                'verbose_name': 'Association levy',
                'verbose_name_plural': 'Association levies',
                'db_table': 'association_levies_tb',
            },
        ),
        migrations.CreateModel(
            name='AssociationLevyCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=1000000, max_length=100, verbose_name='Levy charge')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('levy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='account.associationlevy')),
            ],
            options={
                'verbose_name': 'Association charge',
                'verbose_name_plural': 'Association charges',
                'db_table': 'association_charges_tb',
            },
        ),
        migrations.CreateModel(
            name='AssociationPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=1000000, verbose_name='Amount Paid')),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='account.associationlevycharge')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='association.associationmemeber')),
            ],
            options={
                'verbose_name': 'Association payment',
                'verbose_name_plural': 'Association payments',
                'db_table': 'association_payments_tb',
            },
        ),
    ]
