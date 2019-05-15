from django.contrib import admin

# Register your models here.
from polls.models import GoodsInfo, StoreInfo
class contactAdmin(admin.ModelAdmin):
    list_display = ('goods_info','price','store_name','sale_rating','address','source_site')
admin.site.register(GoodsInfo)
admin.site.register(StoreInfo,contactAdmin)