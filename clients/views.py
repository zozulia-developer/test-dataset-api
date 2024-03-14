import csv
import logging
from datetime import date, datetime

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .filters import ClientFilter
from .models import Client
from .serializers import ClientSerializer, ExportSerializer

logger = logging.getLogger(__name__)


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ExportAPIView(generics.GenericAPIView):
    serializer_class = ExportSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category", type=openapi.TYPE_STRING),
        openapi.Parameter('gender', openapi.IN_QUERY, description="Filter by gender", type=openapi.TYPE_STRING),
        openapi.Parameter('min_age', openapi.IN_QUERY, description="Filter by minimum age", type=openapi.TYPE_INTEGER),
        openapi.Parameter('max_age', openapi.IN_QUERY, description="Filter by maximum age", type=openapi.TYPE_INTEGER),
        openapi.Parameter('age', openapi.IN_QUERY, description="Filter by age", type=openapi.TYPE_INTEGER),
    ])
    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        filters = {}
        if 'category' in serializer.validated_data:
            filters['category'] = serializer.validated_data['category']
        if 'gender' in serializer.validated_data:
            filters['gender'] = serializer.validated_data['gender']
        if 'min_age' in serializer.validated_data and 'max_age' in serializer.validated_data:
            raise ValidationError("Only one of 'min_age' or 'max_age' can be specified")
        if 'min_age' in serializer.validated_data:
            today = date.today()
            min_age = serializer.validated_data['min_age']
            filters['birth_date__year__lte'] = today.year - min_age - 1
        if 'max_age' in serializer.validated_data:
            today = date.today()
            max_age = serializer.validated_data['max_age']
            filters['birth_date__year__gte'] = today.year - max_age
        if 'age' in serializer.validated_data:
            age = serializer.validated_data['age']
            filters['birth_date__year'] = date.today().year - age

        queryset = Client.objects.filter(**filters)

        response = HttpResponse(content_type='text/csv')
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        response['Content-Disposition'] = f'attachment; filename="exported_data_{timestamp}.csv"'
        writer = csv.writer(response)
        writer.writerow(['category', 'firstname', 'lastname', 'email', 'gender', 'birth_date'])
        for client in queryset:
            writer.writerow([
                client.category,
                client.first_name,
                client.last_name,
                client.email,
                client.gender,
                client.birth_date
            ])

        return response
