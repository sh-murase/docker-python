import pytest
from taskformat_use_pandas import to_hyphen_dateformat as to_hyphen_dateformat1
from taskformat import to_hyphen_dateformat as to_hyphen_dateformat2

@pytest.fixture(scope="module")
def data_fromfile():
    dataFilePath = 'data_file.csv'
    data_set_list = []
    with open(dataFilePath,mode='r',encoding='UTF-8') as f:
       for line in f:
          
          data_set = line.split(',')
          data_set = [x.strip().rstrip() for x in data_set]
          #空行読み込みを除外
          if not len(data_set) == 0 :
            if data_set[1] == 'None' :
              data_set[1] = None

            data_set_list.append(data_set)
    print(data_set_list)
    
    return data_set_list



def test_1(data_fromfile):
    for data_set in data_fromfile :
      preformat , aftformat = data_set[0] , data_set[1]
      
      assert to_hyphen_dateformat1(preformat) == aftformat

def test_2(data_fromfile):
    for data_set in data_fromfile :
      preformat , aftformat = data_set[0] , data_set[1]
      
      assert to_hyphen_dateformat2(preformat) == aftformat


