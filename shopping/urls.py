from django.contrib import admin
from django.urls import path
from shopsite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 메인 페이지
    path('', views.home, name='home'),

    # 회원가입/로그인/로그아웃
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 마이페이지
    path('mypage/', views.mypage, name='mypage'),

    # 상품 등록 및 상세 및 삭제
    path('create_product/', views.create_product, name='create_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/update/', views.update_product, name='update_product'),

    # 상품 검색
    path('search/', views.search_products, name='search'),

    # 채팅
    path('chat/', views.send_message, name='chat'),

    # 구매 요청
    path('product/<int:product_id>/purchase/', views.request_purchase, name='request_purchase'),

    # 구매 확정
    path('product/<int:product_id>/confirm/', views.confirm_purchase, name='confirm_purchase'),

    # 신고
    path('report_user/<int:user_id>/', views.report_user, name='report_user'),
    path('report_product/<int:product_id>/', views.report_product, name='report_product'),

    # 송금
    path('send_money/', views.send_money, name='send_money'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
