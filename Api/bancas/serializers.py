from rest_framework import serializers
from .models import Bancas


class BancasSerializer(serializers.ModelSerializer):
    daily_revenue = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    monthly_revenue = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Bancas
        fields = '__all__'  # Incluye todos los campos del modelo, además de los definidos manualmente
