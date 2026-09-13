# NOTA MÍA: no tengo este backend desplegado todavía. Lo dejo aquí listo
# para el día que quiera mis propias estadísticas en vez del badge externo.

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
    """Obtengo la IP del visitante, considerando que puede haber un proxy/reverse-proxy delante."""
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def _hash_ip(ip_address):
    """Anonimizo la IP: nunca la guardo en texto plano, solo su hash con sal."""
    salted = f"{settings.VISIT_SALT}:{ip_address}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


@require_http_methods(["GET"])
def get_visits(request):
    """Consulto el total sin incrementar el contador."""
    counter = VisitCounter.get_solo()
    return JsonResponse({"visits": counter.total})


@csrf_exempt
@require_http_methods(["POST"])
def register_visit(request):
    """
    Registro una visita. La cuento como "persona única" solo una vez por
    día por IP (hasheada); si recarga la página el mismo día no incremento
    el total, pero igual devuelvo el total actual.
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
        # Ya tengo un registro de esta IP hoy: no lo incremento de nuevo.
        pass

    counter = VisitCounter.get_solo()
    return JsonResponse({"visits": counter.total, "counted": counted})
