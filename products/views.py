import http
import json
import base64
from django.core.exceptions import RequestDataTooBig
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from slugify import slugify
from django.core.files.base import ContentFile
from .forms import ProductForm, CommentForm
from .models import Product, Comment
from django.views.decorators.http import require_POST


def book_list(request):
    books = Product.objects.all()
    return render(request, 'book_list.html', {'books': books})


def book_detail(request, handle):
    book = get_object_or_404(Product, handle=handle)
    comments = Comment.objects.filter(book=book)
    context = {
            'book': book,
            'comments': comments,
        }
    return render(request, 'book_detail.html', context)


def new_id():
    """
    get unique id from last id of the models
    """
    last_product = Product.objects.order_by('id').last()
    if last_product:
        return last_product.pk + 1
    return 1


@login_required(login_url="/users/signin/")
def create_product(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        image_data = request_data.get('image')
        handle = slugify(f"{request_data['name']}-{new_id()}")

        if float(request_data.get('price')) < 100:
            return JsonResponse({"message": '가격은 100원 이상으로 설정해야합니다.', "redirect_url": "/products/book/create/"})
        
        form = ProductForm(request_data)
        if form.is_valid():
            product = form.save(commit=False)
            if image_data:
                image_data = base64.b64decode(image_data)
                product.image.save(handle, ContentFile(image_data), save=False)
            product.handle = handle
            product.user = request.user
            try:
                product.save()
            except RequestDataTooBig as e:
                return JsonResponse({"message": e}, status=http.HTTPStatus.FORBIDDEN)

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

        if float(request_data.get('price')) < 100:
            url = f"/products/book/update/{handle}"
            return JsonResponse({"message": "가격은 100원 이상으로 설정해야합니다.", "redirect": url}, status=400)
        
        request_data["handle"] = slugify(f"{request_data['name']}-{new_id()}")
        handle = request_data["handle"]
        

        form = ProductForm(request_data, instance=book)
        if form.is_valid():
            product = form.save(commit=False)
            if book.user == request.user:
                product.handle = handle
                product.save()
                return JsonResponse({"message": "도서 정보가 수정되었습니다.", 'redirect': '/products/book/'}, status=200)
            else:
                return JsonResponse({"message": "상품을 수정할 권한이 없습니다.", 'redirect': '/products/book/'}, status=403)

        else:
            if not isinstance(request_data["price"], int):
                return JsonResponse({"message": "가격은 숫자로 입력해야 합니다.", 'redirect': ''}, status=400)
            return JsonResponse({"message": form.errors.as_json(), 'redirect': ''}, status=400)
    if not Product.objects.filter(handle=handle).exists():
        return JsonResponse({"message": "존재하지 않는 상품입니다."}, status=404)
    else:
        form = ProductForm(instance=book)
        return render(request, "update_product.html", context)


def delete_product(request, handle):
    book = Product.objects.get(handle=handle)
    user = request.user

    if user == book.user:
        book.delete()
        redirect_url = reverse('book:book_list')
        return JsonResponse({"message": "도서 정보가 삭제되었습니다.", 'redirect': redirect_url, 'statusCode': 200}, status=200)
    else:
        return JsonResponse({"message": "상품을 삭제할 권한이 없습니다.", 'redirect': '/products/book/', 'statusCode': 403}, status=403)


def create_comment(request, handle):
    if request.method == "POST":
        request_data = json.loads(request.body)
        comment_content = request_data.get('content')
        book = get_object_or_404(Product, handle=handle)
        user = request.user

        if comment_content:
            comment = Comment(comment=comment_content, book=book, user=user)
            comment.save()

            comment_data = {
                'id': comment.id,
                'content': comment.comment,
                'date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            return JsonResponse({"message": "댓글이 작성되었습니다.", 'redirect': f'/products/book/{handle}'},status=200)
        else:
            return JsonResponse({'error': '댓글 내용을 제공해야 합니다.'}, status=400)
    comments = Comment.objects.filter(book=book)
    context = {
        'book': book,
        'comments': comments,
    }
    return render(request, "book_detal.html", context)

def delete_comment(request, handle, comment_id):
    book = get_object_or_404(Product, handle=handle)
    comment = get_object_or_404(Comment, id=comment_id, book=book)

    if request.method == "DELETE":
        comment.delete()
        return JsonResponse({"message": "댓글이 삭제되었습니다.", 'redirect': f'/products/book/{handle}'}, status=200)
    else:
        return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
