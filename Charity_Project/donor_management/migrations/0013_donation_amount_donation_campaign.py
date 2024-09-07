# Generated by Django 5.1 on 2024-08-31 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor_management', '0012_alter_campaign_end_date_alter_campaign_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='amount',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='campaign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donor_management.campaign'),
        ),
    ]