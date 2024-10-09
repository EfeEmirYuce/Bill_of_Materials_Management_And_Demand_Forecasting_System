from django.contrib import admin
from .models import Product, RawMaterial, BillOfMaterials

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku']
    search_fields = ['name', 'sku']

@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']
    search_fields = ['name']

@admin.register(BillOfMaterials)
class BillOfMaterialsAdmin(admin.ModelAdmin):
    list_display = ['final_product', 'raw_material', 'quantity']
    list_filter = ['final_product', 'raw_material']
