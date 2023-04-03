from django.db import models

# Create your models here.
class Inventory(models.Model):
    
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    
    def can_reduce(self, amount_used):
        return self.stock >= amount_used
           
    def reduce_stock(self, amount_used):
        if self.can_reduce(amount_used):
            self.stock -= amount_used
            return True
        else:
            return False
    
    
    def __str__(self):
        return f"{self.name} ({self.stock} remaining)"