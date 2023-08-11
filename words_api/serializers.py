from rest_framework import serializers
from .models import *


class MiniWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word', 'length', 'type', 'is_common', 'frequency']

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['id', 'key', 'value']