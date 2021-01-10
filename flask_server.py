from flask import Flask, render_template, jsonify, request, session, escape, url_for, redirect
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import glob
import os

client = MongoClient('localhost', 27017)
db = client.dbheejin
app = Flask(__name__)


@app.route('/')
def home():
    db.user_data.drop()
    return render_template('onepage.html')


@app.route('/page3')
def page3():
    return render_template('page3.html')


@app.route('/page4')
def page4():
    return render_template('page4.html')


@app.route('/get_data', methods=['GET'])
def listing():
    result = list(db.user_data.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'user_data': result})


@app.route('/get_result1', methods=['POST'])
def get_result1():
    word = request.form['word']
    meaning = request.form['meaning']

    files_path = os.path.join('C:/MAVE_RawData', '*')
    files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
    tmp = str(files[0])
    print(files[0])

    a = ""
    tmp = tmp + '/Fp1_FFT.txt'
    inFile = open(tmp, "r", encoding="ANSI")

    inList = inFile.readlines()
    for inString in inList:
        a += inString
    inFile.close()

    # print(a)

    b = list(a.split('오전')[1].split(':')[2].split('\t'))
    n = b[0].rstrip(' ')
    b[0] = n

    for i in range(len(b) - 1):
        # print(i)
        # print(b[i])

        # 여기서 범위 조절해서 맥스값 뽑아내기
        if float(b[i]) > 10:
            b.pop(i)
    # 우리가필요한 데이터를 뽑아낸 b리스트. 여기 요소들 중에서 맥스를 뽑아서 O를 선택했는지 X를 선택했는지 알아내기
    # print(b)

    temp_list = []
    for i in range(30, 91):
        num = b[i]
        temp_list.append(float(num))

    a = 0.0
    cnt1 = 0
    cnt2 = 0
    for i in temp_list:
        cnt1 += 1
        if (float(a) < float(i)):
            a = i
            cnt2 = cnt1
    cnt2 -= 1
    hz = 6 + (0.2) * cnt2
    print("Hz: ", hz)
    print("Max: ", a)
    if ((hz >= 6.2) & (hz <= 9.5) & (float(a) > 1.000000000e-11)):
        result = "O"
    else:
        result = "X"

    # 여기에 진영님이 만든 파이썬 코드 넣으면 된다. 리턴값 result 에는 사용자의 선택값인 x or o 가 들어간다.

    # 사용자가 O 주파수에 동기화 되었으면 -> 정답을 맞게 고름 !
    if result == "O":
        db.user_data.update_one({'word': word}, {'$inc': {'total_cnt': 1}})
        db.user_data.update_one({'meaning': meaning}, {'$inc': {'total_cnt': 1}})
        return jsonify({'result': 'success', 'result': 0})

    # ran1 == ran 2 인데도  X를 고른 사용자. -> 정답을 못맞춘거임!
    elif result == "X":
        db.user_data.update_one({'word': word}, {'$inc': {'total_cnt': 1}})
        db.user_data.update_one({'word': word}, {'$inc': {'err_cnt': 1}})
        return jsonify({'result': 'success', 'result': 1})




    # 옳은 영단어와 뜻이 츌력된다.
    # if (len(dd) != 0):
    #     print(dd)
    #     return jsonify({'result': 'success', 'result': 0})
    #
    # else:
    #     return jsonify({'result': 'fail', 'result': 1})

    # xlsx = pd.read_excel('test.xlsx')
    # print(xlsx.head())
    # print(xlsx.tail())
    # # 엑셀 처리


@app.route('/get_result2', methods=['POST'])
def get_result2():
    word = request.form['word']
    meaning = request.form['meaning']


    files_path = os.path.join('C:/MAVE_RawData', '*')
    files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
    tmp = str(files[0])
    print(files[0])


    a = ""
    tmp = tmp + '/Fp1_FFT.txt'
    inFile = open(tmp, "r", encoding="ANSI")

    inList = inFile.readlines()
    for inString in inList:
        a += inString
    inFile.close()

    # print(a)
    b = list(a.split('오전')[1].split(':')[2].split('\t'))
    n = b[0].rstrip(' ')
    b[0] = n

    for i in range(len(b) - 1):
        # print(i)
        # print(b[i])

        # 여기서 범위 조절해서 맥스값 뽑아내기
        if float(b[i]) > 10:
            b.pop(i)
    # 우리가필요한 데이터를 뽑아낸 b리스트. 여기 요소들 중에서 맥스를 뽑아서 O를 선택했는지 X를 선택했는지 알아내기
    # print(b)

    # 여기에 진영님이 만든 파이썬 코드 넣으면 된다. 리턴값 result 에는 사용자의 선택값인 x or o 가 들어간다.
    temp_list = []
    for i in range(30, 91):
        num = b[i]
        temp_list.append(float(num))

    a = 0.0
    cnt1 = 0
    cnt2 = 0
    for i in temp_list:
        cnt1 += 1
        if (float(a) < float(i)):
            a = i
            cnt2 = cnt1
    cnt2 -= 1
    hz = 6 + (0.2) * cnt2
    print("Hz: ", hz)
    print("Max: ", a)
    if ((hz >= 6.2) & (hz <= 9.5) & (float(a) > 5.000000000e-11)):
        result = "O"
    else:
        result = "X"

    # 사용자가 O 주파수에 동기화 되었으면 -> 정답을 맞게 고름 !
    if result == "X":
        db.user_data.update_one({'word': word}, {'$inc': {'total_cnt': 1}})
        db.user_data.update_one({'meaning': meaning}, {'$inc': {'total_cnt': 1}})
        return jsonify({'result': 'success', 'result': 0})

    # ran1 != ran 2 인데도  O를 고른 사용자. -> 정답을 못맞춘거임!
    elif result == "O":
        db.user_data.update_one({'word': word}, {'$inc': {'total_cnt': 1}})
        db.user_data.update_one({'word': word}, {'$inc': {'err_cnt': 1}})
        return jsonify({'result': 'success', 'result': 1})


@app.route('/order', methods=['POST'])
def saving():
    word = request.form['word']
    meaning = request.form['meaning']

    data = {
        'word': word,
        'meaning': meaning,
        'total_cnt': 0,
        'err_cnt': 0
    }

    db.user_data.insert_one(data)
    return jsonify({'result': 'success'})


@app.route('/receipt', methods=['GET'])
def get_receipt():
    all_list = list(db.user_data.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'all_list': all_list})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
