Django Rest Framework Query Tools

This package facilitates filter operations via query parameters, simplifying the filtering process for Django Rest Framework views.
Installation

Install via pip:

```bash
pip install django-rest-framework-query-tools
```

Usage
Quick Example

Suppose you have a Books model with fields like author, title, etc. To filter Books by author using query params:

In your views.py, specify the field(s) to filter using filter_fields:

```python

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_query_tools.filters import QueryParamsFilter

class BooksListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [QueryParamsFilter, DjangoFilterBackend]
    filter_fields = ('author',)
```

Now, you can perform filtering by passing query parameters:

```plaintext
/v1/books?author=name
```

Integration
Method 1: Integration in views.py

Import QueryParamsFilter and use it as a filter backend:

```python

from drf_query_tools.filters import QueryParamsFilter

class BooksListView(generics.ListAPIView):
    # ...
    filter_backends = [QueryParamsFilter]
    filter_fields = ('author',)
    # ...
```

Method 2: Global Integration via settings.py

Add the QueryParamsFilter to your Django Rest Framework settings:

```python

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'drf_query_tools.filters.QueryParamsFilter'
    ]
}
```

Contributing

Feel free to contribute by opening issues or submitting pull requests!
License

This project is licensed under the MIT License - see the LICENSE file for details