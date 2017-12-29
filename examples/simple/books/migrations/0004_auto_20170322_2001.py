# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='stock_count',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='books', to='books.Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.PositiveIntegerField(default=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(related_name='books', to='books.Publisher', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='book',
            field=models.ForeignKey(related_name='order_lines', to='books.Book', on_delete=models.CASCADE),
        ),
    ]
