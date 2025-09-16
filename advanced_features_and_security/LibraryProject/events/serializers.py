from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    is_upcoming = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer']

    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)