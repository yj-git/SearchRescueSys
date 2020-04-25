# Generated by Django 3.0.3 on 2020-04-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SelectModel',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=50)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('val', models.CharField(max_length=50)),
                ('parent', models.IntegerField(default=0)),
                ('type_select', models.IntegerField(choices=[(0, 'NULL'), (1, 'OPTIONWRECK'), (2, 'EQUATION'), (3, 'NULL'), (4, 'COVERAGE_TYPE')], default=0)),
                ('menu_title', models.CharField(max_length=100)),
                ('menu_content', models.CharField(max_length=100)),
                ('menu_level', models.IntegerField(default=99)),
                ('menu_url', models.CharField(max_length=500)),
                ('menu_sort', models.IntegerField(default=99)),
                ('menu_class', models.CharField(default='default', max_length=100)),
            ],
            options={
                'db_table': 'common_select',
            },
        ),
    ]