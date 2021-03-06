# Generated by Django 2.0.1 on 2021-07-18 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20210717_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='userentity',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='口令'),
        ),
        migrations.AlterField(
            model_name='fruitentity',
            name='tags',
            field=models.ManyToManyField(blank=True, db_table='t_fruit_tags', null=True, related_name='fruits', to='mainapp.TagEntity', verbose_name='所有标签'),
        ),
        migrations.AlterField(
            model_name='fruitentity',
            name='users',
            field=models.ManyToManyField(blank=True, db_table='t_collect', null=True, related_name='fruits', to='mainapp.UserEntity', verbose_name='收藏用户列表'),
        ),
    ]
