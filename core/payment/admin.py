from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'course__title', 'transaction_id']
    readonly_fields = ['transaction_id', 'created_at', 'confirmed_at']
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'course', 'amount', 'payment_method')
        }),
        ('Статус платежа', {
            'fields': ('status', 'transaction_id')
        }),
        ('Даты', {
            'fields': ('created_at', 'confirmed_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Делаем все поля только для чтения после создания"""
        if obj:  # Если объект уже существует
            return ['user', 'course', 'amount', 'payment_method', 'transaction_id',
                    'created_at', 'confirmed_at', 'status']
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление платежей"""
        return False

    actions = ['mark_as_completed', 'mark_as_failed', 'mark_as_refunded']

    def mark_as_completed(self, request, queryset):
        """Действие: пометить как завершенные"""
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} платежей помечены как завершенные")

    mark_as_completed.short_description = "Пометить выбранные платежи как завершенные"

    def mark_as_failed(self, request, queryset):
        """Действие: пометить как неудачные"""
        updated = queryset.update(status='failed')
        self.message_user(request, f"{updated} платежей помечены как неудачные")

    mark_as_failed.short_description = "Пометить выбранные платежи как неудачные"

    def mark_as_refunded(self, request, queryset):
        """Действие: пометить как возвращенные"""
        updated = queryset.update(status='refunded')
        self.message_user(request, f"{updated} платежей помечены как возвращенные")

    mark_as_refunded.short_description = "Пометить выбранные платежи как возвращенные"