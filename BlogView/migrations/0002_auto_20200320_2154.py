# Generated by Django 2.2.11 on 2020-03-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogView', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletterregistration',
            name='cognome',
            field=models.CharField(blank=True, help_text='se vuoi inserisci il tuo cognome', max_length=50),
        ),
        migrations.AddField(
            model_name='newsletterregistration',
            name='consenso_privacy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newsletterregistration',
            name='localita',
            field=models.CharField(blank=True, help_text='se vuoi inserisci la località', max_length=50),
        ),
        migrations.AlterField(
            model_name='newsletterregistration',
            name='nome',
            field=models.CharField(blank=True, help_text='se vuoi inserisci il tuo nome o un identificativo', max_length=50),
        ),
    ]