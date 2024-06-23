import re
from datetime import datetime
import pandas as pd


# 和暦→西暦変換関数
# 変換できない場合は、変換できないことをprintしてNoneを返す
def to_seireki(s_input : str, era : str, year : str, month : str, day : str) -> str:

    WAREKI_CSV_PATH = 'wareki_data.csv'
    
    df = pd.read_csv(WAREKI_CSV_PATH, header=0 , encoding='utf-8')
    df_tmp = df.eq(era)

    df_res = df[(df_tmp['wareki'] == True)|(df_tmp['waryaku'] == True)|(df_tmp['letterupper'] == True)|(df_tmp['letterlower'] == True)]
    
    if not df_res.empty :
      era = df_res.iat[0, 0]
    else :
      print(f"{s_input}:和暦でないため、処理終了")
      return None

    era_start, era_end = pd.to_datetime(df_res.iat[0,4] , format='%Y-%m-%d') , pd.to_datetime(df_res.iat[0,5] , format='%Y-%m-%d')

    ad_year = era_start.year + int(year) - 1

    try:
      todate = pd.Timestamp(ad_year,int(month),int(day))

    except ValueError as e:
      print(e)
      print(f'{s_input}:日付として正しくないため、処理終了')
      return None

    
    if not pd.notnull(todate):
      print(f'{s_input}:日付として正しくないため、処理終了')
      return None

    if era_start <= todate <= era_end :
      restr = todate.strftime('%Y-%m-%d')
      return restr

    else :
      print(f'{s_input}:和暦として正しくないため、処理終了')
      return None


# 様々なフォーマットの日付を"yyyy-mm-dd"形式(0埋め)に変換した文字列を返す
# 変換できない場合は、変換できない旨をprintしてNoneを返す
def to_hyphen_dateformat(s_input_date : str) -> str:
  
  #年月日形式の2桁を%yで解釈する時とそれ以外の2桁年の時の解釈を合わせる基準年
  two_digits_year_threshold = datetime.now().year + 50
  
  #引数の日付文字列内の全角文字(英数記号)を半角に変換
  s_date = s_input_date.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

  res = None

  str_matches = re.search(r'^\D+', s_date)

  #数字でない文字が頭=和暦の場合、
  if str_matches is not None :
    year = ''
    month = ''
    day = ''
    wareki_era = str_matches.group()
    num_list = re.findall(r'\d+', s_date)
    
    gannen_pos = wareki_era.find('元')
    if gannen_pos > 0 :
      year = '1'
      wareki_era = wareki_era[:gannen_pos]
      if len(num_list) != 2 :
        print(f'{s_input_date}:年月日の情報が正しく取得できないため、処理終了')

        return None
      month , day = num_list[0] , num_list[1]
    else :
      if len(num_list) != 3 :
        print(f'{s_input_date}:年月日の情報が正しく取得できないため、処理終了')

        return None
      year , month , day = num_list[0] , num_list[1] , num_list[2]
     
    res = to_seireki(s_input_date, wareki_era, year, month, day)

    return res
    

  #"数字頭"の場合、
  else :

    todate = pd.to_datetime(s_date,yearfirst=True,errors='coerce')
    
    if not pd.notnull(todate):
      
      todate = pd.to_datetime(s_date,format="%Y年%m月%d日",errors='coerce')
      
      if not pd.notnull(todate):

        todate = pd.to_datetime(s_date,format="%y年%m月%d日",errors='coerce')

        if not pd.notnull(todate):
          print(f'{s_input_date}:日付として認識できないため、処理終了')
          return None
        
        else :
          
          if todate.year < two_digits_year_threshold - 100 :
            
            modify_date = str(todate.year + 100) + s_date[2:]
            todate = pd.to_datetime(modify_date,format="%Y年%m月%d日",errors='coerce')
            
            if not pd.notnull(todate):
              print(f'{s_input_date}:日付として認識できないため、処理終了')
              return None

          elif todate.year >= two_digits_year_threshold :
            
            modify_date = str(todate.year - 100) + s_date[2:]
            todate = pd.to_datetime(modify_date,format="%Y年%m月%d日",errors='coerce')
            
            if not pd.notnull(todate):
              print(f'{s_input_date}:日付として認識できないため、処理終了')
              return None
    
    
    res = todate.strftime('%Y-%m-%d')
    
    return res



#python [このファイル].pyで実行した場合の動作
if __name__ == '__main__':

  val = input('年月日の情報を入力してください : ')

  res = to_hyphen_dateformat(val)

  print(f'入力値:{val}・出力値:{res}')


