from rest_framework import serializers
from .models import Skill, SkillReview, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SkillReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SkillReview
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']

class SkillSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    reviews = SkillReviewSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    media_url = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            'id', 'user', 'title', 'description',
            'category', 'category_id', 'media', 'media_url',
            'tags', 'price', 'pricing_model', 'availability',
            'reviews'
        ]
        read_only_fields = ['user']

    def get_media_url(self, obj):
        request = self.context.get('request')
        if obj.media and request:
            return request.build_absolute_uri(obj.media.url)
        return None
