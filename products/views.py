from django.http import JsonResponse
from django.shortcuts import render
from .forms import ProductForm
from .models import Product
from django.shortcuts import render, redirect ,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from slugify import slugify
from .models import Product
import json

def book_list(request):
    books = Product.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, handle):
    book = get_object_or_404(Product, handle=handle)
    return render(request, 'book_detail.html', {'book': book})

@login_required(login_url="/users/signin/")
def create_product(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        request_data["handle"] = slugify(request_data["name"])
        form = ProductForm(request_data)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({"message": "신규 도서 등록이 완료되었습니다.", "redirect_url": "/products/book/"})
        else:
            return JsonResponse({"message": form.errors.as_json()})
    else:
        return render(request, 'create_product.html')
    
@login_required(login_url="/users/signin/")
def update_product(request, handle):
    book = get_object_or_404(Product, handle=handle)
    context = {"book": book}

    if request.method == "PATCH":
        request_data = json.loads(request.body)
        request_data["handle"] = slugify(request_data["name"])
        form = ProductForm(request_data, instance=book)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({"message": "도서 정보가 수정되었습니다.", 'redirect': '/products/book/'}, status = 200)
        else:
            if Product.objects.filter(name=request_data["name"]).exists():
                return JsonResponse({"message": "이미 존재하는 이름입니다.", 'redirect': ''}, status = 400)
            if not isinstance(request_data["price"], int):
                return JsonResponse({"message": "가격은 숫자로 입력해야 합니다.", 'redirect': ''}, status=400)
            return JsonResponse({"message": form.errors.as_json(), 'redirect': ''}, status = 400)
    if not Product.objects.filter(handle=handle).exists():
        return JsonResponse({"message": "존재하지 않는 상품입니다."}, status = 404)
    else:
        form = ProductForm(instance=book)
        return render(request, "update_product.html", context)

def delete_product(request, handle):
    book = Product.objects.get(handle=handle)
    user = request.user
    
    if request.method == 'DELETE':    
        if not user.is_authenticated:
            return JsonResponse({'result': False, 'redirect': '/users/signin/', 'statusCode': 401})
        
        if book.user == user:
            book.delete()
            return JsonResponse({'result': True, 'redirect': '/products/book', 'statusCode': 200})
        return JsonResponse({'result': False, 'statusCode': 403})
    
    return render(request, 'book_detail.html', {'book': book})

