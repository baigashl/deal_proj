from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Customer, Gem, Deal, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class GemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gem
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    gems = GemSerializer(many=True, read_only=True)
    # gem = serializers.ListField(
    #     child=serializers.CharField(),
    #     write_only=True
    # )

    class Meta:
        model = Deal
        fields = ['username', 'spent_money', 'gems']