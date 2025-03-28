from django.db import models
from concerts.models import Concert  

class TicketType(models.Model): # Add a default value
    CATEGORIES = [
        ('VIP', 'VIP (200 pax)'),
        ('LB', 'Lower Box (500 pax)'),
        ('UB', 'Upper Box (800 pax)'),
        ('GA', 'General Admission (1500 pax)')
    ]

    concert = models.ForeignKey(
        Concert, 
        on_delete=models.CASCADE,
        related_name="ticket_types"  
    )
    category = models.CharField(
        max_length=3,
        choices=CATEGORIES,
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_quantity = models.PositiveIntegerField(default=0)
    remaining_quantity = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.remaining_quantity = self.total_quantity
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_category_display()} tickets for {self.concert.title}" if self.category else "Custom Ticket Type"
