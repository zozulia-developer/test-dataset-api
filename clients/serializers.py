from datetime import date

from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        today = date.today()
        age = today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
        return age

    class Meta:
        model = Client
        fields = ['category', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'age']


class ExportSerializer(serializers.Serializer):
    category = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    min_age = serializers.IntegerField(required=False)
    max_age = serializers.IntegerField(required=False)
    age = serializers.IntegerField(required=False)
