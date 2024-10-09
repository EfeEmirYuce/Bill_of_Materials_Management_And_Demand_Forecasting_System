from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class RawMaterial(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=20)
    slug = models.SlugField(null=False,unique=True, db_index=True, blank=True, editable=False)

    def __str__(self):
        return (self.name + "(" + self.unit + ")")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class BillOfMaterials(models.Model):
    final_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bom')
    raw_material = models.ForeignKey(RawMaterial, null=True, blank=True, on_delete=models.CASCADE, related_name='bom_items')
    semi_finished_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name='bom_items')
    quantity = models.FloatField()

    def __str__(self):
        if self.raw_material:
            return f"{self.raw_material.name} - {self.quantity}"
        else:
            return f"{self.semi_finished_product.name} - {self.quantity}"