
from django.urls import path
from . import views
from .views import MyTokenObtainPairView, UserRegistrationView
from .views import ProductUpdateView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('profile/', views.get_profile),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    # path('products/', views.get_products, name='products'),
    # path('products/<str:pk>/', views.getProduct, name='product'),
    # path('api/products/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
]
