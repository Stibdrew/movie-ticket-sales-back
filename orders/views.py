import qrcode
from io import BytesIO
from django.core.files import File
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer
from tickets.models import TicketType  # Ensure this import is added

from rest_framework.permissions import IsAuthenticated
from tickets.models import TicketType
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.db.models import Sum, F  # <-- Make sure Sum and F are imported
from orders.models import OrderItem  # Add this import for OrderItem

User = get_user_model()

class CreateOrderAPI(APIView):

    @transaction.atomic
    def post(self, request):
        # Extract data from request
        ticket_type_id = request.data.get('ticket_type')
        quantity = request.data.get('quantity')

        # Check if both ticket_type and quantity are provided
        if not ticket_type_id or not quantity:
            return Response({"error": "ticket_type and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            return Response({"error": "Ticket type not found"}, status=status.HTTP_404_NOT_FOUND)

        total_price = ticket_type.price * quantity

        # Create the order and set default status
        order = Order.objects.create(
            user=user,  # Set user as None or the authenticated user
            ticket_type=ticket_type,
            quantity=quantity,
            total_price=total_price,
            status="pending",  # Ensure status is set properly
            payment_intent_id=request.data.get('payment_intent_id'),
        )

        # Generate QR code for the order
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"ORDER:{order.id}:{user.email if user else 'Anonymous'}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code to the model
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        order.qr_code.save(f'qrcode_{order.id}.png', File(buffer))

        # Ensure the order is saved properly
        order.save()

        # ✅ Now the order will appear in the Django admin panel under Orders ✅
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    


class OrderHistoryAPI(APIView):
    def get(self, request):
        # Retrieve orders for the authenticated user
        orders = Order.objects.filter(user=None).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def order_summary(request):
    # Aggregate total sales by ticket type (sum of the total_price for each ticket_type)
    order_summary_data = Order.objects.values('ticket_type__category') \
        .annotate(
            total_orders=Sum('quantity'),
            total_revenue=Sum('total_price')
        ).order_by('ticket_type__category')

    summary = []
    for item in order_summary_data:
        summary.append({
            'category': item['ticket_type__category'],
            'total_orders': item['total_orders'],
            'total_revenue': str(item['total_revenue'])  # Convert total_revenue to string for clarity
        })

    return Response(summary)