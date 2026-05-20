from rest_framework import serializers

class SearchQuerySerializer(serializers.Serializer):
    """
    Validates and cleans query parameters for the search endpoint.
    Used in ProductSearchView.get() before building the queryset.
    """
    q         = serializers.CharField(required=False, allow_blank=True, default='')
    category  = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    ordering  = serializers.ChoiceField(
        choices=['price', '-price', 'created_at', '-created_at'],
        required=False, default='-created_at'
    )

    def validate(self, data):
        min_p = data.get('min_price')
        max_p = data.get('max_price')
        if min_p and max_p and min_p > max_p:
            raise serializers.ValidationError('min_price cannot exceed max_price')
        return data
