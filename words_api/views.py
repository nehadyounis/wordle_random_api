from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
import csv
from django.templatetags.static import static
from django.conf import settings
from random import choice


@api_view(['GET'])
def add_all_words(request):
    return JsonResponse({'error': 'Cannot add all words to database'})
    file = open(str(settings.BASE_DIR) + "/static/" + 'words_pos.csv')
    csvreader = csv.reader(file)
    response = []
    for row in csvreader:
        word = Word()
        word.word = row[1].lower()
        word.type = row[2]
        try:
            word.save()
        except:
            pass
        response.append(row[0])
    return JsonResponse(response, safe=False)


@api_view(['GET'])
def mark_unique(request):
    file = open(str(settings.BASE_DIR) + "/static/" + 'common_words.csv')
    csvreader = csv.reader(file)
    response = 0
    for row in csvreader:
        try:
            Word.objects.filter(word=row[0]).update(is_common='true')
        except:
            pass
        response = response + 1
    return JsonResponse(response, safe=False)


@api_view(['GET'])
def get_word_info(request, word):
    cheese_blog = Word.objects.get(word=word)
    ser = WordSerializer(cheese_blog)
    return JsonResponse(ser.data, safe=False)


@api_view(['GET'])
def get_random_word(request):
    amount = int(request.GET.get('amount', 1))

    common_only = bool(request.GET.get('amount', True))

    reg = request.GET.get('reg', None)

    length = int(request.GET.get('length', None))
    min_length = int(request.GET.get('min_length', None))
    max_length = int(request.GET.get('max_length', None))

    contains = request.GET.get('contains', None)

    pattern = request.GET.get('pattern', None)

    word_type = request.GET.get('type', None)

    if amount > 25:
        resp = JsonResponse({"error": "amount beyond limit"}, safe=False)
        resp.status_code = 400
        return resp

    if reg is not None and (length and max_length and min_length and contains and pattern and word_type) is not None:
        resp = JsonResponse({"error": "when regex is applied, please don't use any other parameters"}, safe=False)
        resp.status_code = 400
        return resp

    random = Word.objects.filter(word__regex=r'.{10}.*').order_by('?')[0:amount]
    ser = WordSerializer(random, many=True)
    return JsonResponse(ser.data, safe=False)


@api_view(['GET'])
def get_all_words(request):
    cheese_blog = Word.objects.filter(word__regex=r'.{10}.*').order
    ser = WordSerializer(cheese_blog, many=True)
    return JsonResponse(ser.data, safe=False)
