from django.urls import path
from .views import (
    home,
    product_list,
    product_create,
    product_detail,
    product_update,
    product_delete,
    index,
)

app_name = 'products'

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('list/', product_list, name='product_list'),  # Product list
    path('create/', product_create, name='product_create'),  # Product create
    path('<int:pk>/', product_detail, name='product_detail'),  # Product detail
    path('<int:pk>/edit/', product_update, name='product_update'),  # Product update
    path('<int:pk>/delete/', product_delete, name='product_delete'),  # Product delete
    path('index/', index, name='products_index'),  # Index
]
