from django.db import models
from decimal import Decimal

class Bancas(models.Model):

    TIPOS_DE_BANCAS = [
        ( 'clasica', 'Clasica'),
        ('moderna' , 'Moderna')
    ]


    codigo = models.CharField(max_length=10, unique=True)
    nombre_ticket = models.CharField(max_length=50, null=True, blank=True)

    tipo_de_bancas =  models.CharField(max_length=20 , choices=TIPOS_DE_BANCAS , default='clasica')

    nombre = models.CharField(max_length=100 , unique=True)
    direcccion = models.CharField(max_length=100 , null=True,)
    telefono = models.CharField(max_length=15,blank=True, null=True,)
    usar_presupuesto_propio = models.BooleanField(default=False)

    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    premios = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ganancias = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activa = models.BooleanField(default=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    mensaje_creacion_jugada = models.TextField(null=True, blank=True)
    mensaje_cancelacion_jugada = models.TextField(null=True, blank=True)
    mensaje_jugada_premiada = models.TextField(null=True, blank=True)

    # daily_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # monthly_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=[('ACTIVA', 'Activa'), ('INACTIVA', 'Inactiva')], default='ACTIVA')

     # Propiedad para ingresos diarios
    @property
    def daily_revenue(self):
        # Ejemplo: calcular el 10% de las ganancias diarias
        return self.ganancias * Decimal('0.1')  # Ajusta la lógica según tu caso

    # Propiedad para ingresos mensuales
    @property
    def monthly_revenue(self):
        # Ejemplo: calcular el 30% de las ganancias mensuales
        return self.ganancias * Decimal('0.3')  # Ajusta la lógica según tu caso


    def __str__(self):
        return self.nombre