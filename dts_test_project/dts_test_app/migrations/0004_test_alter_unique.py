from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dts_test_app', '0003_test_add_db_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='DummyModel',
            name='indexed_value',
            field=models.CharField(max_length=255, unique=True),
        ),

        migrations.RemoveField(
            model_name='DummyModel',
            name='indexed_value',
        ),
    ]
