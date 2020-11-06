import random
import re
from . import settings


PHONE_PREFIX=['130','131','132','133','134','135','136','137','138','139',
             '150','151','152','153','156','158','159','170','183','182','185','186','188','189']

def phone_valid(phone_number):
    '''
    :param phone_number:13798063255
    :return:
    '''
    phone_number = str(phone_number)
    if len(phone_number)>11:
        return False
    if not phone_number.isdigit():
        return False
    if phone_number[:3] not in PHONE_PREFIX:
        return False

    return True


def get_sms_captcha(length=6):
    '''
    :param length: control the captcha's size by length
    '''
    captcha = ''
    for _ in range(length):
        number = random.randint(0,9)
        character = chr(random.randint(97, 122))
        captcha = captcha + str(random.choice([number, character]))
    return captcha


# 判断邮箱是否合法的函数
def email_valid(email):
    result = re.match('^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$',email)

    if not result:
        return False
    return True

def calc_weight(agreements=0,comments=0,**kwargs):

    weight = agreements*settings.WEIGHTS['agreement'] + comments*settings.WEIGHTS['comment']
    if "collections" in kwargs:
        weight += kwargs['collections'] * settings.WEIGHTS.get('collection',1)
    return weight













