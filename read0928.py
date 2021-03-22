#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import discord
from discord.ext import commands
import random
import openpyxl
import json
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, date, time
import asyncio
import re
from lxml import html
import requests


# Naver Developer 페이지에서 받아온 토큰을 입력합니다.
naver_client_id = 'token_id'
naver_client_pw = 'token_pw'

def translate(source, target, text):
    client_id = naver_client_id
    client_secret = naver_client_pw
    encText = urllib.parse.quote(text)
    data = "source={0}&target={1}&text={2}".format(source, target, encText)
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = json.loads(response.read())
        return response_body['message']['result']['translatedText']
    else:
        return "Error Code:" + rescode


def dice(count, value): #아직 익혀야함
    return list(map(lambda x: random.randint(1, value), range(count)))

cho_quizs = {}  # 초성퀴즈


HAN_BASE, CHO, JUNG = 44032, 588, 28
CHO_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
            'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
CHO_LITE_LIST = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ',
                 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
PARSED_CHO_LIST = ['%A1', '%A2', '%A4', '%A7', '%A8', '%A9',
                   '%B1', '%B2', '%B3', '%B5', '%B6', '%B7', '%B8', '%B9',
                   '%BA', '%BB', '%BC', '%BD', '%BE']


def cho(keyword):
    """단어를 초성으로"""
    split_keyword_list = list(keyword)
    result = []
    for letter in split_keyword_list:
        if re.match('.*[가-힣]+.*', letter) is not None:
            char_code = ord(letter) - HAN_BASE
            cho_code = int(char_code / CHO)
            result.append(CHO_LIST[cho_code])
        else:
            result.append(letter)

    return ''.join(result)


def cho_gen_lite(length):
    result = ''
    for _ in range(length):
        result += CHO_LITE_LIST[random.randint(0, 13)]

    return result


def jaum_search(genre=None, chos=cho_gen_lite(random.randint(2, 3))):
    """genre: movie, music, animal, dic, game, people, book"""
    BASE = 'http://www.jaum.kr/index.php?w='
    query = ''
    for i in range(len(chos)):
        query += '%A4' + PARSED_CHO_LIST[CHO_LIST.index(chos[i])]
    if genre is None:
            page = requests.get(BASE + query)
    else:
        page = requests.get(BASE + query + '&k=' + genre)
    tree = html.fromstring(page.content)

    result = tree.xpath('//*[@id="container"]//td[1]//text()')

    return result


def jaum_quiz(genre=None):
    GENRES_KOR = ['영화', '음악', '동식물', '사전', '게임', '인물', '책']
    GENRES_ENG = ['movie', 'music', 'animal', 'dic', 'game', 'people', 'book']
    if genre in GENRES_KOR:
        genre = GENRES_ENG[GENRES_KOR.index(genre)]
    else:
        return None

    answers = []
    while len(answers) == 0:
        answers = jaum_search(genre, cho_gen_lite(random.randint(2, 3)))
    answer = random.choice(answers)
    answer = re.sub(r'\s+$', '',
                    re.sub(r'^\s+', '',
                           re.sub(r'(?i)[A-Z().]', '', answer)))

    print('정답 : '+answer)  # DEBUG
    return answer


def josa(word, j):
    last_char = word[-1]
    has_jong = True if (ord(last_char) - HAN_BASE) % 28 > 0 else False
    if j in ['은', '는']:
        return '은' if has_jong else '는'
    elif j in ['이', '가']:
        return '이' if has_jong else '가'
    elif j in ['을', '를']:
        return '을' if has_jong else '를'
    elif j in ['으로', '로']:
        return '으로' if has_jong else '로'
    elif j in ['과', '와']:
        return '과' if has_jong else '와'
    else:
        raise Exception('josa 함수에 잘못된 인수 전달.')


class ChoQuiz:
    def __init__(self):
        self.genre = None
        self.count = None
        self.answer = None
        self.score = None

    @staticmethod
    def find(channel):
        global cho_quizs

        return cho_quizs[channel] if channel in cho_quizs else None

    @staticmethod
    def start(channel, genre, count, answer):
        global cho_quizs

        cho_quizs[channel] = ChoQuiz()
        cho_quizs[channel].genre = genre
        cho_quizs[channel].count = count
        cho_quizs[channel].answer = answer

        return cho_quizs[channel]

    @staticmethod
    def end(channel):
        global cho_quizs

        if channel in cho_quizs:
            del cho_quizs[channel]
            ret = '초성퀴즈를 종료했어요.'
        else:
            ret = '진행중인 초성퀴즈가 없어요.'

        return ret

    def correct(self, channel):
        self.count -= 1
        if self.count > 0:
            self.answer = jaum_quiz(self.genre)
            return cho(self.answer)
        else:
            return ChoQuiz.end(channel)






