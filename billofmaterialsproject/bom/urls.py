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
]