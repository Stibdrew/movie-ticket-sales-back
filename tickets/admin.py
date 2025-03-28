from django.contrib import admin
from .models import TicketType

class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('concert', 'category', 'price', 'total_quantity', 'remaining_quantity')  # Removed 'name'
    search_fields = ('concert__title', 'category')
    list_filter = ('category', 'concert')
    ordering = ('concert',)

admin.site.register(TicketType, TicketTypeAdmin)