import cv2
import matplotlib.pyplot as plt
import easyocr
from _datetime import datetime
import re
from PIL import Image

#CUDA V11.2
#pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113

def make_card_data(my_file_name):
    name_pattern = r'^([가-힣]{2,4})$' #이름
    pnum_pattern = r'^\d{3}-\d{4}-\d{4}$' #핸드폰번호
    mail_pattern = r'(\S)+(@)(\w)+(\.)?(\w){2,3}(\.\w{2,3})?' #이메일
    str_pattern = r'.+\/.+' #부서 / 직급
    
    
    #시작 시간 체크
    bef = datetime.now()
    # easyocr을 이용하여 어떤 언어를 선택하여 분석할 것인지 설정
    reader = easyocr.Reader(['ko', 'en'], gpu=True)
    
    img_path = 'download/{}'.format(my_file_name)
    
    # 직접 받아온 이미지를 열어서
    # my_temp = Image.open(card_img)
    
    # img = cv2.imread(img_path)
    
    # 이미지를 읽어 드렸던 결과 반환
    # result = reader.readtext(my_temp)
    result = reader.readtext(img_path)
    
    # print(result)
        
    # 신뢰도 측정
    THRESHOLD = 0.25
    
    
    
    ocr_result_data = []
    
    for bbox, text, conf in result:
        if conf > THRESHOLD:
            #공백제거
            none_space_temp = text.replace(" " , "")
            if re.search(name_pattern, none_space_temp):
                ocr_result_data.append(none_space_temp)
                
            if re.search(pnum_pattern, none_space_temp):
                ocr_result_data.append(none_space_temp)
                
            if re.search(mail_pattern, none_space_temp):
                ocr_result_data.append(none_space_temp)
                
            if re.search(str_pattern, text):
                my_temp = text.split('/')
                #부서와 직급은 분리한 뒤 저장
                ocr_result_data.append(my_temp[0].strip())
                ocr_result_data.append(my_temp[1].strip())
                
            # cv2.rectangle(img, pt1=bbox[0], pt2=bbox[2], color=(0, 255, 0), thickness=3)
    
    # plt.figure(figsize=(8, 8))
    # plt.imshow(img[:, :, ::-1])
    # plt.axis('off')
    # plt.show()
    
    my_temp = {
               'osDeptNm' : ocr_result_data[0], 'osJbgdNm' : ocr_result_data[1]
               , 'osUserNm' : ocr_result_data[2], 'osCoNm' : ocr_result_data[4]
               , 'osTel' : ocr_result_data[5], 'osEml' : ocr_result_data[6]
            }
    
    
    
    #종료시간 측정
    aft = datetime.now()
    
    #경과 시간 측정
    diff = aft.timestamp() - bef.timestamp()
    print("diff: ", diff)
    
    return my_temp


if __name__ == '__main__':
    print(make_card_data(None))