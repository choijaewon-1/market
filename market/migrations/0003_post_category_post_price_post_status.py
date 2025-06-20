# Generated by Django 4.2.18 on 2025-06-06 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('도서', '도서'), ('전자기기', '전자기기'), ('생활용품', '생활용품'), ('기타', '기타')], default='기타', max_length=20),
        ),
        migrations.AddField(
            model_name='post',
            name='price',
            field=models.PositiveIntegerField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('판매 중', '판매 중'), ('예약 중', '예약 중'), ('판매 완료', '판매 완료')], default='판매 중', max_length=20),
        ),
    ]
