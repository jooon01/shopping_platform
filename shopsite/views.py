from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal

# 홈
def home(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'home.html', {'products': products})

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('home')

# 마이페이지
@login_required
def mypage(request):
    my_products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'mypage.html', {'my_products': my_products})

# 상품 등록
@login_required
def create_product(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')
        Product.objects.create(
            seller=request.user,
            title=title,
            description=description,
            price=price,
            image=image
        )
        messages.success(request, "상품이 성공적으로 등록되었습니다!")
        return redirect('home')
    return render(request, 'create_product.html')

# 상품 삭제
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "상품이 성공적으로 삭제되었습니다.")
        return redirect('mypage')
    return render(request, 'delete_product.html', {'product': product})

# 업데이트 상품
@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        product.title = request.POST['title']
        product.description = request.POST['description']
        product.price = request.POST['price']
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, "상품이 성공적으로 수정되었습니다!")
        return redirect('mypage')
    return render(request, 'update_product.html', {'product': product})

# 상품 상세
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# 검색
def search_products(request):
    keyword = request.GET.get('q', '')
    if keyword:
        results = Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        if request.user.is_authenticated:
            SearchLog.objects.create(user=request.user, keyword=keyword)
    else:
        results = []
    return render(request, 'search.html', {'results': results, 'keyword': keyword})

# 채팅
@login_required
def send_message(request):
    if request.method == 'POST':
        msg = request.POST['message']
        receiver_id = request.POST.get('receiver')
        is_group = receiver_id == ''
        receiver = None
        if not is_group:
            receiver = get_object_or_404(CustomUser, id=receiver_id)
        ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message=msg,
            is_group=is_group
        )
        return redirect('chat')
    users = CustomUser.objects.exclude(id=request.user.id)
    messages_list = ChatMessage.objects.filter(Q(is_group=True) | Q(receiver=request.user) | Q(sender=request.user)).order_by('timestamp')
    return render(request, 'chat.html', {'messages': messages_list, 'users': users})

# 구매 요청
@login_required
def request_purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller = product.seller

    # 메시지 내용 자동 생성
    content = f"[구매 요청] '{product.title}' 상품을 구매하고 싶습니다!"

    ChatMessage.objects.create(
        sender=request.user,
        receiver=seller,
        message=content,
        is_group=False
    )
    messages.success(request, "구매 요청이 전송되었습니다!")
    return redirect('chat')

# 구매 확정
@login_required
def confirm_purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.is_sold = True
    product.save()
    messages.success(request, "상품이 거래 완료 처리되었습니다!")
    return redirect('mypage')

# 유저 신고
@login_required
def report_user(request, user_id):
    reported_user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        reason = request.POST['reason']
        Report.objects.create(
            reporter=request.user,
            reported_user=reported_user,
            report_type='USER',
            reason=reason
        )
        return redirect('home')
    return render(request, 'report_user.html', {'target': reported_user})

# 상품 신고
@login_required
def report_product(request, product_id):
    reported_product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        reason = request.POST['reason']
        Report.objects.create(
            reporter=request.user,
            reported_product=reported_product,
            report_type='PRODUCT',
            reason=reason
        )
        return redirect('home')
    return render(request, 'report_product.html', {'target': reported_product})

# 송금
@login_required
def send_money(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        amount_str = request.POST.get('amount')
        memo = request.POST.get('memo', '')

        try:
            amount = Decimal(amount_str)
        except:
            messages.error(request, "올바른 금액을 입력해주세요.")
            return redirect('send_money')

        if amount <= 0:
            messages.error(request, "송금 금액은 1원 이상이어야 합니다.")
            return redirect('send_money')

        receiver = get_object_or_404(CustomUser, id=receiver_id)

        if receiver == request.user:
            messages.error(request, "자기 자신에게는 송금할 수 없습니다.")
            return redirect('send_money')

        Transaction.objects.create(
            sender=request.user,
            receiver=receiver,
            amount=amount,
            memo=memo
        )
        messages.success(request, f"{receiver.nickname}님에게 {amount}원을 송금했습니다.")
        return redirect('mypage')

    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'send_money.html', {'users': users})
