# Generated by Django 5.1.5 on 2025-02-01 23:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField()),
                ('price', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default='1', max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Box_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default='1', max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.CharField(max_length=250)),
                ('customer', models.CharField(max_length=250)),
                ('total', models.FloatField(default=0)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('type', models.CharField(choices=[('1', 'Stock-in'), ('2', 'Stock-Out')], default='1', max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.box')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('quantity', models.FloatField(default=0)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.box')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.invoice')),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.stock')),
            ],
        ),
    ]
