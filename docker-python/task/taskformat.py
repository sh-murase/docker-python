import re
from datetime import datetime


# 和暦情報
ERA_DICT = {
    '令和': (datetime(2019, 5, 1) , datetime(9999, 12, 31)),
    '平成': (datetime(1989, 1, 8) , datetime(2019, 4, 30)),
    '昭和': (datetime(1926, 12, 25) , datetime(1989, 1, 7)),
    '大正': (datetime(1912, 7, 30) , datetime(1926, 12, 25)),
    '明治': (datetime(1868, 10, 23) , datetime(1912, 7, 30))
}


# 和暦→西暦変換関数
# 変換できない場合は、変換できないことをprintしてNoneを返す
def to_seireki(s_dateval : str, era : str, year : str, month : str, day : str) -> str:

    if era == '令' or era == 'R' or era == 'r' :
      era = '令和'
    elif era == '平' or era == 'H' or era == 'h' :
      era = '平成'
    elif era == '昭' or era == 'S' or era == 's' :
      era = '昭和'
    elif era == '大' or era == 'T' or era == 't' :
      era = '大正'
    elif era == '明' or era == 'M' or era == 'm' :
      era = '明治'

    try:
      era_start, era_end = ERA_DICT[era]
    except KeyError as e:
      print(e)
      print(f'{s_dateval}:和暦対応外のため、処理終了')

      return None

    else :

      ad_year = era_start.year + int(year) - 1

      try:
        todate = (datetime(ad_year, int(month) , int(day)))

      except ValueError as e:
        print(e)
        print(f'{s_dateval}:日付として正しくないため、処理終了')

        return None

      if era_start <= todate <= era_end :
        restr = todate.strftime('%Y-%m-%d')
        return restr

      else :
        print(f'{s_dateval}:和暦として正しくないため、処理終了')

        return None


# 様々なフォーマットの日付を"yyyy-mm-dd"形式(mmとddは0埋め)に変換した文字列を返す
# 変換できない場合は、変換できない旨をprintしてNoneを返す
# (2024gre6kl5などの４桁数字頭の３つの数字を文字列が区切っている値も変換を行う挙動となります。)
def to_hyphen_dateformat(str_dateval : str) -> str:

  TWO_DIGITS_YEAR_THRESHOLD = 74
  ZenHan=lambda x:x.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
  
  year = ''
  month = ''
  day = ''

  wareki_flg = 0
  gannen_flg = 0
  wareki_era = ''
  res = ''

  str_matches = re.search(r'^\D+', str_dateval)
  
  #数字でない文字が頭=和暦として処理
  if str_matches is not None :

    wareki_era = str_matches.group()
    gannen_pos = wareki_era.find('元')
    if gannen_pos > 0 :
      year = '1'
      wareki_era = wareki_era[:gannen_pos]
      gannen_flg = 1

    wareki_flg = 1


  num_list = re.findall(r'\d+', str_dateval)
  num_list = list(map(ZenHan, num_list))
  
  if len(num_list) == 1 :

    try:

      res = datetime.strptime(num_list[0], '%Y%m%d').strftime('%Y-%m-%d')

    except ValueError as e:
      print(e)
      print(f'{str_dateval}:日付として正しくないため、処理終了')
      return None



  elif len(num_list) != 3 and not ( wareki_flg and  gannen_flg  and len(num_list) == 2):

    print(f'{str_dateval}:年月日の情報が正しく取得できないため、処理終了')
    return None

  else :

    if wareki_flg and gannen_flg :
      month , day = num_list[0] , num_list[1]
    else :
      year , month , day = num_list[0] , num_list[1] , num_list[2]


    if wareki_flg :

      res = to_seireki(str_dateval, wareki_era, year, month, day)


    else :

      if len(year) == 2 :
        if int(year) < TWO_DIGITS_YEAR_THRESHOLD :
          year = '20' + year
        else :
          year = '19' + year

      date_string = year + '-' + month + '-' + day

      try:

        res = datetime.strptime(date_string, '%Y-%m-%d').strftime('%Y-%m-%d')

      except ValueError as e:
        print(e)
        print(f'{str_dateval}:日付として正しくないため、処理終了')

        return None


  return res



#python [このファイル].pyで実行した場合の動作
if __name__ == '__main__':

  val = input('年月日の情報を入力してください : ')

  res = to_hyphen_dateformat(val)

  print(f'入力値:{val}・出力値:{res}')

