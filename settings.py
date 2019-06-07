#ресурсы с которых мы получаем данные о АЗС и топливе
SRC = ['https://testfd.ru', 'https://fdsfs.ru', 'https://tesdsffdst.ru']


try:
  from local_settings import *
except ImportError:
  pass