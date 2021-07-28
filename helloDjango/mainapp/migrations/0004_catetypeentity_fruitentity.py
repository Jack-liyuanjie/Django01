# Generated by Django 2.0.1 on 2021-07-14 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210714_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='CateTypeEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='分类名')),
                ('order_num', models.IntegerField(verbose_name='排序')),
            ],
            options={
                'db_table': 't_category',
                'ordering': ['-order_num'],
            },
        ),
        migrations.CreateModel(
            name='FruitEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='水果名')),
                ('price', models.FileField(upload_to='', verbose_name='价格')),
                ('source', models.CharField(max_length=30, verbose_name='原产地')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.CateTypeEntity')),
            ],
            options={
                'verbose_name': '水果表',
                'verbose_name_plural': '水果表',
                'db_table': 't_fuite',
            },
        ),
    ]
