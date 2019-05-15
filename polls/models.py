# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class GoodsInfo(models.Model):
    goods_sort = models.CharField(primary_key=True, max_length=50)
    keys = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goods_info'


class SearchHistory(models.Model):
    create_time = models.CharField(max_length=50)
    user_name = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='user_name', blank=True, null=True)
    goods_sort = models.ForeignKey(GoodsInfo, models.DO_NOTHING, db_column='goods_sort', blank=True, null=True)
    search_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'search_history'


class StoreInfo(models.Model):
    goods_info = models.CharField(max_length=50, blank=True, null=True)
    store_name = models.CharField(primary_key=True, max_length=110)
    goods_sort = models.ForeignKey(GoodsInfo, models.DO_NOTHING, db_column='goods_sort', blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    sale_rating = models.IntegerField(blank=True, null=True)
    key1 = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    source_site = models.CharField(max_length=50, blank=True, null=True)
    image_file_path = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'store_info'


class UserInfo(models.Model):
    user_name = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'
