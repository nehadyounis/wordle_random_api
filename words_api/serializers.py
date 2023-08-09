from rest_framework import serializers
from .models import *


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word', 'language', 'frequency', 'is_common']

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['id', 'key', 'value']