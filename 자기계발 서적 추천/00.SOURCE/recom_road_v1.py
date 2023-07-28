import numpy as np
import keras
from book.dao_book import DaoBook
from book.book_recom_data import make_test_set

db = DaoBook()

# 소유한 책의 리스트를 조회
def check_own_book(check_id, my_arg):
    own_book = db.select_own_book()
    
    for i in own_book:
        user_id =  i['USER_ID']
        book_no =  i['BOOK_NO']
        
        
        if user_id == check_id:
            if book_no == my_arg:
                return True
       
    return False

# 중복되거나 다음 순위의 추천 정보를 받기위한 함수
def next_book_recom(my_arg):
    pre[my_arg] = 0
    my_arg = np.argmax(pre)
    return my_arg
    
# 테스트 또는 추천 결과를 알기위한 데이터 셋
x_test, user_id = make_test_set()

model = keras.models.load_model("book_recom.h5")

predict = model.predict(x_test)

recom_list = []

for idx, pre in enumerate(predict):
    my_arg = np.argmax(pre)
    
    # 내가 추천 받은 책을 산 기록이 있으면 바꿔줌
    if check_own_book(user_id[idx], my_arg):
        my_arg = next_book_recom(my_arg)
        
    my_arg1 = next_book_recom(my_arg)
    my_arg2 = next_book_recom(my_arg1)
    my_arg3 = next_book_recom(my_arg2)
    
    #DB 컬럼에 맞춰서 insert
    my_result = [idx, user_id[idx], my_arg1, my_arg2, my_arg3]
    db.insert_result(my_result)

