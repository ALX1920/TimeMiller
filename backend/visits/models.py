from django.db import models


class VisitCounter(models.Model):
    """Uso esta fila única (singleton) para guardar el total acumulado de visitas."""

    total = models.PositiveBigIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contador de visitas"
        verbose_name_plural = "Contador de visitas"

    def __str__(self):
        return f"Total: {self.total}"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class VisitLog(models.Model):
    """
    Guardo aquí un registro por visitante único al día, identificado con un
    hash de su IP (nunca guardo la IP real). Me sirve para no contar dos
    veces a la misma persona el mismo día si recarga la página.
    """

    ip_hash = models.CharField(max_length=64, db_index=True)
    date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de visita"
        verbose_name_plural = "Registros de visitas"
        constraints = [
            models.UniqueConstraint(fields=["ip_hash", "date"], name="unique_visitor_per_day")
        ]

    def __str__(self):
        return f"{self.ip_hash[:8]}… — {self.date}"
