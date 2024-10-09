from bom.models import BillOfMaterials

def calculate_material_needs_recursive(product, product_sales):
    bom_items = BillOfMaterials.objects.filter(final_product=product)
    
    material_needs = {}
    
    for item in bom_items:
        if item.raw_material:
            material_needed = item.quantity * product_sales
            material_unit = item.raw_material.unit 
            
            if item.raw_material.name in material_needs:
                material_needs[item.raw_material.name]['quantity'] += material_needed
            else:
                material_needs[item.raw_material.name] = {
                    'quantity': material_needed,
                    'unit': material_unit
                }
        elif item.semi_finished_product:
            semi_finished_sales = item.quantity * product_sales
            semi_finished_needs = calculate_material_needs_recursive(item.semi_finished_product, semi_finished_sales)
            
            for material, details in semi_finished_needs.items():
                if material in material_needs:
                    material_needs[material]['quantity'] += details['quantity']
                else:
                    material_needs[material] = details
    
    return material_needs
