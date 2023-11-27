from re import search

# from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationErrror
from django.db.models import QuerySet
from rest_framework.exceptions import \
    ValidationError as RestFrameworkValidationError
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.request import Request


class URLFilter(BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view: ListAPIView) -> QuerySet:
        if queryset.exists():
            DATE_PATTERN = r'(\d{4})-((0[0-9])|(1[0-2]))-(([0-2][0-9])|(3[01]))'
            if not hasattr(view, 'filter_fields'):
                return queryset
            if view.filter_fields == '__all__':
                filter_fields = [i.name for i in queryset.first()._meta.fields]
            else:
                filter_fields = view.filter_fields
            filter_data = {}
            for key, value in request.GET.items():
                if key in filter_fields:
                    try:
                        if search(DATE_PATTERN, value):
                            filter_data[key] = str(value)
                            continue
                        filter_data[key] = eval(value)
                    except:
                        filter_data[key] = str(value)
            try:
                queryset = queryset.filter(**filter_data)
            except (ValueError, DjangoValidationErrror) as e:
                raise RestFrameworkValidationError(e)
        return queryset


# class CustomOrderingFilter(OrderingFilter):
#     def get_default_ordering(self, view: ListAPIView):
#         ordering = getattr(view, 'ordering', None)
#         if isinstance(ordering, list) or isinstance(ordering, tuple) or isinstance(ordering, set):
#             return ordering
#         return settings.DEFAULT_ORDER_BY_VALUE
