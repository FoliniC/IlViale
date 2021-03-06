# Generated by Django 2.2.11 on 2020-03-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogView', '0002_auto_20200320_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletterregistration',
            name='cognome',
            field=models.CharField(blank=True, help_text='se vuoi inserisci il tuo cognome', max_length=50, verbose_name='Inserisci il tuo cognome (facoltativo)'),
        ),
        migrations.AlterField(
            model_name='newsletterregistration',
            name='consenso_privacy',
            field=models.BooleanField(default=False, help_text='conferma di permetterci di registrare i dati inseriti'),
        ),
        migrations.AlterField(
            model_name='newsletterregistration',
            name='indirizzo_mail',
            field=models.EmailField(help_text='Inserisci lemail dove vuoi ricevere la newsletter', max_length=254, verbose_name='Inserisci il tuo indirizzo di email'),
        ),
        migrations.AlterField(
            model_name='newsletterregistration',
            name='localita',
            field=models.CharField(blank=True, help_text='se vuoi inserisci la località', max_length=50, verbose_name='Inserisci il tuo comune (facoltativo)'),
        ),
        migrations.AlterField(
            model_name='newsletterregistration',
            name='nome',
            field=models.CharField(blank=True, help_text='se vuoi inserisci il tuo nome o un identificativo', max_length=50, verbose_name='Inserisci il tuo nome (facoltativo)'),
        ),
    ]
