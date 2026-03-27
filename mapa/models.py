from django.db import models

class Camara(models.Model):
    lat = models.DecimalField(max_digits=22, decimal_places=16)
    long = models.DecimalField(max_digits=22, decimal_places=16)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'Camara'

    def __str__(self):
        return f"Cámara {self.id} ({self.lat}, {self.long})"

class Camion(models.Model):
    patente = models.TextField()
    id_frame = models.TextField()

    class Meta:
        db_table = 'Camion'

    def __str__(self):
        return f"Camión {self.patente} (Frame: {self.id_frame})"

class Deteccion(models.Model):
    # Usamos db_column para coincidir con los nombres exactos en Neon
    id_camion = models.ForeignKey(Camion, on_delete=models.CASCADE, db_column='id_camion')
    id_camara = models.ForeignKey(Camara, on_delete=models.CASCADE, db_column='id_camara')
    fecha = models.DateField()

    class Meta:
        db_table = 'Deteccion'
        verbose_name_plural = "Detecciones"

    def __str__(self):
        return f"Detección {self.id} (Camión {self.id_camion_id} en Cámara {self.id_camara_id})"
