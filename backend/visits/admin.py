from django.contrib import admin

from .models import VisitCounter, VisitLog


@admin.register(VisitCounter)
class VisitCounterAdmin(admin.ModelAdmin):
    list_display = ("total", "updated_at")

    def has_add_permission(self, request):
        # Es un singleton: no me tiene sentido crear más de una fila.
        return not VisitCounter.objects.exists()


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ("ip_hash", "date", "created_at")
    list_filter = ("date",)
    readonly_fields = ("ip_hash", "date", "created_at")

    def has_add_permission(self, request):
        return False
