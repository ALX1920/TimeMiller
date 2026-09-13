import hashlib
from datetime import date

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import VisitCounter, VisitLog


def _client_ip(request):
    """Obtiene la IP del visitante, considerando un proxy/reverse-proxy delante."""
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def _hash_ip(ip_address):
    """Anonimiza la IP: nunca se guarda en texto plano, solo su hash con salt."""
    salted = f"{settings.VISIT_SALT}:{ip_address}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


@require_http_methods(["GET"])
def get_visits(request):
    """Consulta el total sin incrementar el contador."""
    counter = VisitCounter.get_solo()
    return JsonResponse({"visits": counter.total})


@csrf_exempt
@require_http_methods(["POST"])
def register_visit(request):
    """
    Registra una visita. Cuenta como "persona única" solo una vez por día
    por IP (hasheada); recargas el mismo día no incrementan el total pero
    igual devuelven el total actual.
    """
    ip_hash = _hash_ip(_client_ip(request))
    today = date.today()
    counted = False

    try:
        with transaction.atomic():
            VisitLog.objects.create(ip_hash=ip_hash, date=today)
            VisitCounter.objects.filter(pk=1).update(total=F("total") + 1)
            counted = True
    except IntegrityError:
        # Ya existe un registro para esta IP hoy: no se incrementa de nuevo.
        pass

    counter = VisitCounter.get_solo()
    return JsonResponse({"visits": counter.total, "counted": counted})
