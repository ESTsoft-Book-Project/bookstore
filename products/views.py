from django.http import JsonResponse
from django.shortcuts import render
from .forms import ProductForm
from .models import Product
from django.shortcuts import render ,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from slugify import slugify
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
import json
import uuid

@api_view(["GET"])
def book_list(request):
    serializer = ProductSerializer(Product.objects.all(), many = True)
    return render(request, "book_list.html", {"books": serializer.data})

@api_view(["GET"])
def book_detail(request, handle):
    serializer = ProductSerializer(get_object_or_404(Product, handle=handle))
    return render(request, "book_detail.html", {"book": serializer.data})

@api_view(["GET", "POST"])
@login_required(login_url="/users/signin/")
def create_product(request):
    if request.method == "GET":
        return render(request, 'create_product.html')
    elif request.method == "POST":
        request_data = json.loads(json.dumps(request.data))
        request_data["user"] = request.user.pk
        # request_data["handle"] = slugify(f"{request_data['name']}-{request_data['user']}")
        request_data["handle"] = slugify(f"{uuid.uuid4()}")
        serializer = ProductSerializer(data = request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "신규 도서 등록이 완료되었습니다.", "redirect_url": "/products/book/"})
        return JsonResponse({"message": serializer.error_messages})

@api_view(["GET", "PATCH"])
@login_required(login_url="/users/signin/")
def update_product(request, handle):
    if request.method == "PATCH":
        original_data = get_object_or_404(Product, handle=handle)
        request_data = json.loads(json.dumps(request.data))
        request_data["handle"] = slugify(f"{uuid.uuid4()}")
        serializer = ProductSerializer(original_data, data = request_data, partial = True)
        if serializer.is_valid() and (request.user == original_data.user):
            serializer.save()
            return JsonResponse({"message": "도서 정보가 수정되었습니다.", 'redirect': '/products/book/'}, status = 200)
        else:
            if request.user != original_data.user:
                return JsonResponse({"message": "이 상품에 대한 수정 권한이 없습니다.", "redirect": ""}, status = 400)
            if Product.objects.filter(name=request_data["handle"]).exists():
                return JsonResponse({"message": "이미 존재하는 상품입니다.", 'redirect': ''}, status = 400)
            if not isinstance(request_data["price"], int):
                return JsonResponse({"message": "가격은 숫자로 입력해야 합니다.", 'redirect': ''}, status=400)
            return JsonResponse({"message": serializer.errors, 'redirect': ''}, status = 400)
    if not Product.objects.filter(handle=handle).exists():
        return JsonResponse({"message": "존재하지 않는 상품입니다."}, status = 404)
    else:
        serializer = ProductSerializer(get_object_or_404(Product, handle=handle))
        return render(request, "update_product.html", {"book": serializer.data})

@api_view(["DELETE"])
def delete_product(request, handle):
    book = get_object_or_404(Product, handle=handle)
    user = request.user
    
    if request.method == 'DELETE':    
        if not user.is_authenticated:
            return JsonResponse({'result': False, 'redirect': '/users/signin/', 'statusCode': 401})
        
        if book.user == user:
            book.delete()
            return JsonResponse({'result': True, 'redirect': '/products/book', 'statusCode': 200})
        return JsonResponse({'result': False, 'statusCode': 403})
    
    return render(request, 'book_detail.html', {'book': book})

