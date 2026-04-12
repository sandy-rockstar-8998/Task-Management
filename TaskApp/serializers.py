from rest_framework import serializers
from .models import user_register, add_student

class register_serializer(serializers.ModelSerializer):
    class Meta:
        model=add_student
        fields='__all__'