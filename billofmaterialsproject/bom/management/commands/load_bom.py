import json
from django.core.management.base import BaseCommand
from bom.models import Product, RawMaterial, BillOfMaterials

class Command(BaseCommand):
    help = 'Load BOM data from a JSON file'

    def handle(self, *args, **kwargs):
        with open('bom/fixtures/running_shoe_bom.json', 'r', encoding="utf-8") as f:
            bom_data = json.load(f)

        final_product_data = bom_data['final_product']
        final_product, created = Product.objects.get_or_create(
            name=final_product_data['name'],
            defaults={
                'sku': final_product_data['sku'],
                'description': final_product_data['description'],
            }
        )

        def process_components(components, parent_product):
            for component in components:
                if component['type'] == 'Raw Material':
                    raw_material, created = RawMaterial.objects.get_or_create(
                        name=component['name'],
                        defaults={
                            'description': component['description'],
                            'unit': component['unit'],
                        }
                    )
                    BillOfMaterials.objects.create(
                        final_product=parent_product,
                        raw_material=raw_material,
                        quantity=component['quantity']
                    )

                elif component['type'] == 'Semi-Finished Product':
                    semi_finished_product, created = Product.objects.get_or_create(
                        name=component['name'],
                        defaults={
                            'sku': component['sku'],
                            'description': component['description'],
                        }
                    )
                    BillOfMaterials.objects.create(
                        final_product=parent_product,
                        semi_finished_product=semi_finished_product,
                        quantity=component['quantity']
                    )
                    process_components(component['components'], semi_finished_product)

        process_components(final_product_data['components'], final_product)

        self.stdout.write(self.style.SUCCESS('BOM data successfully loaded.'))
