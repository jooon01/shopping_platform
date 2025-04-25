# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, ChatMessage, Report, Transaction, SearchLog

# 사용자 관리 커스터마이징
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'nickname', 'is_active', 'is_suspended', 'balance')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'introduction', 'is_suspended', 'balance')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', 'introduction')}),
    )

# 상품
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)

# 채팅
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp', 'is_group')
    search_fields = ('message',)

# 신고
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'report_type', 'reported_user', 'reported_product', 'created_at')
    list_filter = ('report_type',)

# 송금
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'memo', 'created_at')
    search_fields = ('memo',)

# 검색 로그
@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'keyword', 'searched_at')
    search_fields = ('keyword',)

# 사용자 등록
admin.site.register(CustomUser, CustomUserAdmin)
