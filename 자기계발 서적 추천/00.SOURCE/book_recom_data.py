import numpy as np
from book.dao_book import DaoBook


db = DaoBook()

# 뇌를 학습 시키기 위한 함수
# 인풋 데이터(부서번호, 직급번호, 연차, 나이, 관심분야코드)와 라벨데이터(구매한 책 번호)를 모두 가져와 사용

#{'USER_ID': 'NAVER_2023060017', 'DEPT_NO': 2, 'JBGD_CD': 'JG002', 'YEAR': 7, 'OLD': 30,
# 'BOOK_NO': 24, 'BOOK_NM': '2023 이공자 ITQ 엑셀 2016 (일반형)', 'BOOK_TP': 'FV035'}
def make_train_set():

    t_data = db.select_input_data()
    
    train_data = []
    train_label = []
    for idx, i in enumerate(t_data):
        dept = i['DEPT_NO']
        jbgd = int(i['JBGD_CD'][-3:]) # 코드구분을 위한 앞 2자리를 제외한 뒤 숫자 3자리만 가져옴
        year = i['YEAR']
        old = i['OLD']
        itrst = int(i['BOOK_TP'][-3:]) # 코드구분을 위한 앞 2자리를 제외한 뒤 숫자 3자리만 가져옴
        
        train_tmp = []
        train_tmp.append(dept)
        train_tmp.append(jbgd)
        train_tmp.append(year)
        train_tmp.append(old)
        train_tmp.append(itrst)
        
        train_data.append(train_tmp)
        
        book_no = i['BOOK_NO']
        train_label.append(book_no)
    
    # 인풋 데이터
    np_train = np.array(train_data)
    np_train = np_train.reshape(-1, 5)
    
    # 라벨
    np_lable = np.array(train_label)
    np_lable = np_lable.reshape(-1, 1)
    return np_train, np_lable


# 학습된 뇌를 이용하여 test 또는 예측하고자 하는 데이터를 넣기 위한 함수
#
def make_test_set():

    t_data = db.select_predict_data()

    train_data = []
    user_label = []
    for idx, i in enumerate(t_data):
        user_id = i['USER_ID']
        
        dept = i['DEPT_NO']
        jbgd = int(i['JBGD_CD'][-3:])
        year = i['YEAR']
        old = i['OLD']
        itrst = int(i['ITRST_CD'][-3:])
        
        train_tmp = []
        train_tmp.append(dept)
        train_tmp.append(jbgd)
        train_tmp.append(year)
        train_tmp.append(old)
        train_tmp.append(itrst)
        
        user_label.append(user_id)
        train_data.append(train_tmp)
    
    np_test = np.array(train_data)
    np_test = np_test.reshape(-1, 5)
    
    return np_test, user_label