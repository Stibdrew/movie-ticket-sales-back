from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from base.serializer import ProfileSerializer
from base.products import products

from base.models import Product
from base.serializer import ProductSerializer

from rest_framework import generics
from ..serializer import UserRegistrationSerializer

from django.http import JsonResponse

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    try:
        # Fetch the product based on the provided ID (pk)
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=404)


class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(_id=pk)  # Get the product by ID
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get updated stock from the request body
        stock = request.data.get("stock")
        if stock is not None:
            product.stock = stock
            product.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Stock value is required"}, status=status.HTTP_400_BAD_REQUEST)