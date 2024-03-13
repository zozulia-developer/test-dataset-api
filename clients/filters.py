from datetime import date

import django_filters

from .models import Client


class ClientFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='icontains',
        label='Filter by category',
        help_text='Filter by category.',
    )
    gender = django_filters.CharFilter(
        field_name='gender',
        lookup_expr='icontains',
        label='Filter by gender',
        help_text='Filter by gender.',
    )
    birth_date = django_filters.DateFilter(
        field_name='birth_date',
        lookup_expr='icontains',
        label='Filter by birth_date',
        help_text='Filter by birth_date.',
    )
    age_range = django_filters.CharFilter(
        method='filter_age_range',
        label='Filter by age range (e.g., 25-30).',
        help_text='Filter by age range (e.g., 25-30).',
    )

    def filter_min_age(self, queryset, name, value):
        today = date.today()
        min_birth_year = today.year - int(value)
        return queryset.filter(birth_date__year__gte=min_birth_year)

    def filter_max_age(self, queryset, name, value):
        today = date.today()
        max_birth_year = today.year - int(value) - 1
        print(max_birth_year, flush=True)
        return queryset.filter(birth_date__year__lte=max_birth_year)

    def filter_age_range(self, queryset, name, value):
        min_age, max_age = value.split('-')
        return self.filter_min_age(self.filter_max_age(queryset, 'max_age', min_age), 'min_age', max_age)

    class Meta:
        model = Client
        fields = ['category', 'gender', 'birth_date']
