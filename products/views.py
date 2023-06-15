from django.shortcuts import render
from .forms import ProductForm
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from slugify import slugify
from .models import Product
import json

def book_list(request):
    books = Product.objects.all()
    return render(request, 'book_list.html', {'books': books})


def book_detail(request, handle):
    book = get_object_or_404(Product, handle=handle)
    return render(request, 'book_detail.html', {'book': book})


def create_product(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        request_data["handle"] = slugify(request_data["name"])
        form = ProductForm(request_data)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({"message": "신규 도서 등록이 완료되었습니다."})
        else:
            print(form.errors.as_json())
            return JsonResponse({"message": "오류가 발생했습니다."})
    else:
        return render(request, 'create_product.html')