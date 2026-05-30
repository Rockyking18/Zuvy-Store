from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from apps.core.pagination import StandardPagination
from .serializers import SearchQuerySerializer

class ProductSearchView(APIView):
    """
    GET /api/search/?q=shoes&category=3&min_price=10&max_price=200&ordering=-price
    No auth required. Results are always active products only.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Validate query params via serializer
        params = SearchQuerySerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        data = params.validated_data

        qs = Product.objects.filter(is_moderated=True, is_active=True).select_related('vendor','category')

        # 2. Full-text search (PostgreSQL)
        if data['q']:
            vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
            query  = SearchQuery(data['q'])
            qs = qs.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1).order_by('-rank')
        else:
            qs = qs.order_by(data['ordering'])

        # 3. Filters
        if data.get('category'):  qs = qs.filter(category_id=data['category'])
        if data.get('min_price'): qs = qs.filter(price__gte=data['min_price'])
        if data.get('max_price'): qs = qs.filter(price__lte=data['max_price'])

        # 4. Paginate and return
        paginator = StandardPagination()
        page      = paginator.paginate_queryset(qs, request)
        serializer = ProductListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
