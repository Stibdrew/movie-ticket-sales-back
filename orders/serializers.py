from rest_framework import serializers
from .models import Order
from tickets.models import TicketType

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'category', 'price', 'total_quantity', 'remaining_quantity']  # Adjust fields as necessary

class OrderSerializer(serializers.ModelSerializer):
    # Nested serializer for ticket_type
    ticket_type = TicketTypeSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'ticket_type',  # Will display detailed ticket information
            'quantity',
            'total_price',
            'status',
            'payment_intent_id',
            'qr_code',
            'created_at'
        ]
        read_only_fields = ['total_price', 'status', 'created_at']
