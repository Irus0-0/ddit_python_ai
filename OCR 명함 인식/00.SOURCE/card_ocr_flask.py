from flask import Flask, request , render_template
from flask.json import jsonify
from flask_cors.extension import CORS
import json
from card import my_ez_ocr
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/card.ajax', methods=['POST'])
def ajax_card_data():
    # 사진 정보 받기
    data = request.files.get('cardImg')
    my_file_name = "{}_{}".format(uuid.uuid1(), data.filename)
    data.save("download/{}".format(my_file_name))
    
    card_data = my_ez_ocr.make_card_data(my_file_name)
    
    jsondata = json.dumps(card_data)
    # jsondata = json.dumps(cnt)
    return card_data


if __name__ == '__main__':
    app.run(host='192.168.141.26')