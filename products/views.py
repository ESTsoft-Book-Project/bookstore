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
import base64
from django.core.files.base import ContentFile

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
        image_data = request_data.get('image')
        handle = slugify(request_data["name"])
        
        num = 1
        while Product.objects.filter(handle=handle).exists():
            handle = f'{handle}-{num}'
            num += 1

        form = ProductForm(request_data)
        if form.is_valid():
            product = form.save(commit=False)
            if image_data:
                image_data = base64.b64decode(image_data)
                product.image.save(handle, ContentFile(image_data), save=False)
            product.handle = handle
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
        handle = request_data["handle"]
        num = 1
        while Product.objects.filter(handle=handle).exists():
            name = f'{request_data["name"]}-{num}'
            request_data["handle"] = slugify(name)
            handle = request_data["handle"]
            num += 1
        form = ProductForm(request_data, instance=book)
        if form.is_valid():
            product = form.save(commit=False)
            if book.user == request.user:
                product.save()
                return JsonResponse({"message": "도서 정보가 수정되었습니다.", 'redirect': '/products/book/'}, status = 200)
            else:
                return JsonResponse({"message": "상품을 수정할 권한이 없습니다.", 'redirect': '/products/book/'}, status=403)
            
        else:
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