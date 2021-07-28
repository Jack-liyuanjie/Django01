# Generated by Django 2.0.1 on 2021-07-20 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='单价')),
                ('pay_status', models.IntegerField(choices=[(0, '待支付'), (1, '已支付')], verbose_name='支付状态')),
            ],
            options={
                'db_table': 't_order',
            },
        ),
    ]