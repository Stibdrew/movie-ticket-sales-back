from django.contrib import admin
from .models import Order, OrderTicket
from django.utils.html import format_html

class OrderTicketInline(admin.TabularInline):
    model = OrderTicket
    extra = 1  # Allows adding more tickets inline in Order admin

class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('id', 'user', 'display_ticket_types', 'display_total_quantity', 'total_price', 'status', 'created_at', 'view_qr_code')
    
    # Fields that can be searched in the admin interface
    search_fields = ('user__email', 'status')
    
    # Add filters for easy navigation in the admin
    list_filter = ('status', 'created_at')
    
    # Make the "created_at" field sortable
    ordering = ('-created_at',)

    # Inline Ticket Types within Order Admin
    inlines = [OrderTicketInline]

    def display_ticket_types(self, obj):
        """
        Show all ticket types in the order.
        """
        return ", ".join([f"{ot.ticket_type.get_category_display()} x{ot.quantity}" for ot in obj.orderticket_set.all()])
    display_ticket_types.short_description = "Ticket Types"

    def display_total_quantity(self, obj):
        """
        Show total number of tickets in the order.
        """
        return sum(ot.quantity for ot in obj.orderticket_set.all())
    display_total_quantity.short_description = "Total Quantity"

    def view_qr_code(self, obj):
        """
        Display QR Code in the Admin panel.
        """
        if obj.qr_code:
            return format_html('<img src="{}" width="100" height="100" />', obj.qr_code.url)
        return "No QR Code"
    view_qr_code.short_description = "QR Code"

# Register the Order model with the custom admin class
admin.site.register(Order, OrderAdmin)
