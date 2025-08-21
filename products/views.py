from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm


# product_list view
def product_list(request):
    # get all products from the database with proper ordering
    products = Product.objects.all().order_by('-created_at')
    # create a paginator with 12 products per page
    paginator = Paginator(products, 12)
    # get the page number from the request
    page_number = request.GET.get('page')
    # get the page object
    page_obj = paginator.get_page(page_number)
    # render the product_list template with the page object
    return render(request, 'products/product_list.html', {'page_obj': page_obj})

# product_detail view
def product_detail(request, pk):
    # get the product by the primary key
    product = get_object_or_404(Product, pk=pk)
    # render the product_detail template with the product
    return render(request, 'products/product_detail.html', {'product': product})

# product_create view
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully')
            return redirect('products:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

# product_update view
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('products:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})    

# product_delete view
@login_required
def product_delete(request, pk):
    # get the product by the primary key
    product = get_object_or_404(Product, pk=pk)
    # delete the product
    product.delete()
    # show a success message
    messages.success(request, 'Product deleted successfully')
    # redirect to the product list page
    return redirect('products:product_list')

# home view
def home(request):
    # get the 6 products that are in stock and order them by the created_at field in descending order
    products = Product.objects.filter(in_stock=True).order_by('-created_at')[:6]
    # render the home template with the products
    return render(request, 'products/home.html', {'products': products})

# index view
@login_required
def index(request):
    # get the 6 products that are in stock and order them by the created_at field in descending order
    products = Product.objects.filter(in_stock=True).order_by('-created_at')[:6]
    # render the index template with the products
    return render(request, 'products/index.html', {'products': products})



