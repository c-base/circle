from rest_framework import serializers
from models import Circle

class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle