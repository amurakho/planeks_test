# Generated by Django 3.0.5 on 2020-04-30 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200430_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='pub',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Pub'),
            preserve_default=False,
        ),
    ]