# Generated by Django 4.2.11 on 2024-05-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMarketing', '0008_remove_pago_metodo_pago_pago_fecha_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
