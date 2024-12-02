from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm, RawMaterialForm, BillOfMaterialsForm

from bom.demand_prediction import sarima
from bom.demand_prediction import bom_calculator
from .models import Product, RawMaterial, BillOfMaterials

def index(request):
    return render(request, "bom/home.html")


def products(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "bom/products.html", context)


def product_details(request, product_sku):
    product = get_object_or_404(Product , sku = product_sku)
    context = {"product": product}
    return render(request, "bom/product_details.html", context)


def raw_materials(request):
    context = {"rawmaterials":RawMaterial.objects.all()}
    return render(request, "bom/rawmaterials.html", context)

def raw_material_details(request, slug):
    raw_material = get_object_or_404(RawMaterial , slug = slug)
    context = {"rawmaterial": raw_material}
    return render(request, "bom/rawmaterial_details.html", context)


def boms(request):
    context = {"boms":BillOfMaterials.objects.all()}
    return render(request, "bom/boms.html", context)


def bom_detail(request, product_sku):
    product = get_object_or_404(Product, sku=product_sku)
    bom_items = BillOfMaterials.objects.filter(final_product=product)

    context = {
        "product": product,
        "bom_items": bom_items,
    }
    return render(request, "bom/bom_details.html", context)

def material_needs_view(request, product_sku):
    product = Product.objects.get(sku=product_sku)
    
    predicted_sales = 100 #sarima.calculate_sarima()
    
    material_needs = bom_calculator.calculate_material_needs_recursive(product, predicted_sales)
    
    return render(request, 'bom/material_needs.html', {'material_needs': material_needs, 'product': product})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'bom/add_product.html', {'form': form})

def add_raw_material(request):
    if request.method == 'POST':
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rawmaterials')
    else:
        form = RawMaterialForm()
    return render(request, 'bom/add_raw_material.html', {'form': form})

from django.shortcuts import render, redirect
from .models import BillOfMaterials, Product, RawMaterial

def add_bom(request):
    products = Product.objects.all()
    raw_materials = RawMaterial.objects.all()
    
    if request.method == 'POST':
        final_product_id = request.POST['final_product']
        final_product = Product.objects.get(id=final_product_id)
        
        # Dinamik olarak eklenen hammaddeler ve yarı bitmiş ürünleri işleme
        item_counter = 0
        while f'node_type_{item_counter}' in request.POST:
            node_type = request.POST[f'node_type_{item_counter}']
            node_name = request.POST[f'node_name_{item_counter}']
            quantity = request.POST[f'quantity_{item_counter}']
            
            if node_type == 'raw_material':
                raw_material = RawMaterial.objects.get(id=node_name)
                BillOfMaterials.objects.create(
                    final_product=final_product,
                    raw_material=raw_material,
                    quantity=quantity
                )
            else:
                semi_finished_product = Product.objects.get(id=node_name)
                BillOfMaterials.objects.create(
                    final_product=final_product,
                    semi_finished_product=semi_finished_product,
                    quantity=quantity
                )

            item_counter += 1
        
        return redirect('boms')  # Reçetelerin listelendiği sayfaya yönlendir

    return render(request, 'bom/add_bom.html', {'products': products, 'raw_materials': raw_materials})


def update_product(request, product_sku):
    product = get_object_or_404(Product, sku=product_sku)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products') 
    else:
        form = ProductForm(instance=product)
    return render(request, 'bom/update_product.html', {'form': form, 'product': product})

def update_raw_material(request, slug):
    raw_material = get_object_or_404(RawMaterial, slug=slug)
    if request.method == 'POST':
        form = RawMaterialForm(request.POST, instance=raw_material)
        if form.is_valid():
            form.save()
            return redirect('rawmaterials') 
    else:
        form = RawMaterialForm(instance=raw_material)
    return render(request, 'bom/update_raw_material.html', {'form': form, 'raw_material': raw_material})

def update_bom(request, product_sku):
    bom = get_object_or_404(Product, sku=product_sku)
    if request.method == 'POST':
        form = BillOfMaterialsForm(request.POST, instance=bom)
        if form.is_valid():
            form.save()
            return redirect('boms') 
    else:
        form = BillOfMaterialsForm(instance=bom)
    return render(request, 'bom/update_bom.html', {'form': form, 'bom': bom})
