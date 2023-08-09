from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import *
import csv
from django.conf import settings
import re


# @api_view(['GET'])
# def add_all_words(request):
#     """
#     :param request:
#     :return: Added words
#     Adds words to database according to CSV file
#     """
#     return bad_request('Cannot add words to database currently')
#     file = open(str(settings.BASE_DIR) + "/static/" + 'words_pos.csv')
#     csvreader = csv.reader(file)
#     response = []
#     for row in csvreader:
#         word = Word()
#         word.word = row[1].lower()
#         word.type = row[2]
#         try:
#             word.save()
#         except:
#             pass
#         response.append(row[0])
#     return JsonResponse(response, safe=False)
#
# @api_view(['GET'])
# def mark_unique(request):
#     """
#     :param request:
#     :return: Number of words altered in a JsonResponse
#     This function marks unique words in the database according to external CSV.
#     """
#     return bad_request('Cannot modify the database currently')
#     file = open(str(settings.BASE_DIR) + "/static/" + 'common_words.csv')
#     csvreader = csv.reader(file)
#     response = 0
#     for row in csvreader:
#         try:
#             Word.objects.filter(word=row[0]).update(is_common=True)
#             response = response + 1
#         except:
#             pass
#     return JsonResponse(response, safe=False)
#
# @api_view(['GET'])
# def calc_len(request):
#     """
#
#     :param request:
#     :return: Number of words altered in a JsonResponse
#     This function calculates len of every word in the database
#     """
#     return bad_request('Cannot modify the database currently')
#     response = 0
#     words = Word.objects.all()
#     for word in words:
#         word.length = len(word.word)
#         word.save()
#         response = response + 1
#
#     return JsonResponse(response, safe=False)

@api_view(['GET'])
def get_random_word(request):
    try:
        show_info = int(request.GET.get('show_info', 0))

        amount = int(request.GET.get('amount', 1))  # Done

        common_only = int(request.GET.get('common_only', 0))
        uncommon_only = int(request.GET.get('uncommon_only', 0))

        length = int(request.GET.get('len', 0))
        min_length = int(request.GET.get('min_len', 0))
        max_length = int(request.GET.get('max_len', 0))
    except:
        return bad_request("one or more numeric parameters contain bad characters")

    word_type = request.GET.get('type', None)

    reg = request.GET.get('reg', None)

    contains_any = request.GET.get('contains_any', None)
    contains_all = request.GET.get('contains_all', None)
    contains_only = request.GET.get('contains_only', None)
    contains_none = request.GET.get('contains_none', None)

    pattern = request.GET.get('pattern', None)

    if amount > 25:
        bad_request("amount beyond limit.")

    if (reg is not None) and (length or max_length or min_length or contains_none or contains_only or contains_all or contains_any or pattern):
        bad_request("no parameters can be used while using regex.")

    if length and (max_length or min_length):
        bad_request("min_length and max_length parameters cannot be used with length parameter.")

    if (max_length and min_length) and (min_length > max_length):
        bad_request("min_length must be less than max_length.")

    if common_only and common_only:
        bad_request("common_only and common_only cant both be true (1).")

    if pattern and length:
        bad_request("you either use pattern or length parameter.")

    if pattern and length:
        bad_request("you either use pattern or length parameter.")

    if common_only:
        commonQ = Q(is_common=True)
    elif uncommon_only:
        commonQ = Q(is_common=False)
    else:
        commonQ = Q()

    if word_type:
        typeQ = Q(type=word_type)
    else:
        typeQ = Q()

    if reg:
        random = Word.objects.filter(commonQ & typeQ & Q(word__regex=reg)).order_by('?')[0:amount]
        if show_info:
            ser = WordSerializer(random, many=True)
        else:
            ser = MiniWordSerializer(random, many=True)
        return JsonResponse(ser.data, safe=False)

    if length:
        lenQ = Q(length=length)
    elif min_length and max_length:
        lenQ = Q(length__range=(min_length, max_length))
    elif min_length:
        lenQ = Q(length__gte=min_length)
    elif max_length:
        lenQ = Q(length__lte=max_length)
    else:
        lenQ = Q()

    if contains_any:
        checker = check_parameter_string(contains_any)
        if checker:
            return checker
        contains_anyQ = Q(word__regex='[' + str(contains_any) + ']')
    else:
        contains_anyQ = Q()

    if contains_all:
        checker = check_parameter_string(contains_all)
        if checker:
            return checker
        regex = ''
        for letter in contains_all:  # (?=.*[a-z])
            regex += '(?=.*' + letter + ')'
        contains_allQ = Q(word__regex='' + str(regex) + '.*')
    else:
        contains_allQ = Q()

    if contains_only:
        checker = check_parameter_string(contains_only)
        if checker:
            return checker
        regex = '^[' + str(contains_only) + ']+$'
        contains_onlyQ = Q(word__regex = regex)
    else:
        contains_onlyQ = Q()

    if contains_none:
        checker = check_parameter_string(contains_none)
        if checker:
            return checker
        regex = '^[^' + str(contains_none) + ']+$'
        contains_noneQ = Q(word__regex = regex)
    else:
        contains_noneQ = Q()

    if pattern:
        checker = check_parameter_string(pattern)
        if checker:
            return checker
        regex = ''
        for letter in pattern: #(?=.*[a-z])
            if letter == '*':
                regex += '[a-z]{1}'
            else:
                regex += '(' + letter +'){1}'
        patternQ = Q(word__regex = '^'+str(regex) +'$')
    else:
        patternQ = Q()

    random = Word.objects.filter(commonQ & typeQ & lenQ & contains_anyQ & contains_allQ &
                                 contains_onlyQ & contains_noneQ & patternQ).order_by('?')[0:amount]
    if show_info:
        ser = WordSerializer(random, many=True)
    else:
        ser = MiniWordSerializer(random, many=True)
    return JsonResponse(ser.data, safe=False)

@api_view(['GET'])
def is_a_word(request, word):
    try:
        show_info = int(request.GET.get('show_info', 0))
    except:
        return bad_request("one or more numeric parameters contain bad characters")

    checker = check_parameter_string(word)
    if checker:
        return bad_request("provided word contains bad characters")
    try:
        obj = Word.objects.get(word=word)
    except:
        return JsonResponse(False, safe=False)

    if obj:
        if show_info:
            ser = WordSerializer(obj)
            return JsonResponse(ser.data, safe=False)
        else:
            return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)


def bad_request(msg):
    resp = JsonResponse({"error": msg}, safe=False)
    resp.status_code = 400
    return resp

def check_parameter_string(string):
    pattern = re.compile("^[a-z*]+$")
    if not pattern.match(str(string)):
        return bad_request("One or more parameters contains bad characters")
    else:
        return None
