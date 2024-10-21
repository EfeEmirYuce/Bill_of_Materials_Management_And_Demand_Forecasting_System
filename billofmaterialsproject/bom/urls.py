from django.urls import path

from bom import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("products", views.products, name="products"),
    path("products/<str:product_sku>", views.product_details, name="product_details"),
    path("rawmaterials", views.raw_materials, name="rawmaterials"),
    path("rawmaterials/<slug:slug>", views.raw_material_details, name= "raw_material_details"),
    path("boms", views.boms, name= "boms"),
    path("boms/<str:product_sku>", views.bom_detail, name="bom_detail"),
    path('prediction/<str:product_sku>/', views.material_needs_view, name='material_needs'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-raw-material/', views.add_raw_material, name='add_raw_material'),
    path('add-bom/', views.add_bom, name='add_bom'),
    path('update-product/<str:product_sku>/', views.update_product, name='update_product'),
    path('update-raw-material/<slug:slug>/', views.update_raw_material, name='update_raw_material'),
    path('update-bom/<str:product_sku>/', views.update_bom, name='update_bom'),
]