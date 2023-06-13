from django.shortcuts import render
from .forms import ProductForm
from .models import Product
from django.shortcuts import render, get_object_or_404

def book_list(request):
    books = Product.objects.all()
    return render(request, 'book_list.html', {'books': books})


def book_detail(request, handle):
    book = get_object_or_404(Product, handle=handle)
    return render(request, 'book_detail.html', {'book': book})


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm()
    
    return render(request, 'create_product.html', {'form': form})

