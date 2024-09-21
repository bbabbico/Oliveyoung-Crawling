'''
사이트 주소와 화장품 타입은 무조건 입력해야함.
추출 사이트는 올리브영으로 한정.
추출 사이트는 Entry에 직접입력.
화장품 타입은, 체크박스 아니면 Entry에 직접입력. (둘다 사용가능)
제작과정에서, DBMS는 MySQL을 사용.
'''


from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql

# MySQL 연결
ssql =pymysql.connect(
    host='localhost',
    user='newuser',
    password='(ehgus2003)',
    db='soloDB',
    charset='utf8')

path = ssql.cursor()

#infor(text) 에서 수정한 정보를 최종적으로 SQL에 INSERT
def insert():

    res = infor.get(1.0,END)

    #infor에서 받은 문자열 respomse에 SQL문 작성을 위해 리스트로 정렬하여 삽입
    res =res.split('\n')
    response = [url]

    for i in range(len(res)):
        temp = res[i].split(':',1)
        del temp[0]
        response.append(''.join(temp))

    #SQL로 INSERT문 보내기
    global SQL확인
    try:
        path.execute(f"insert into qqq values('{response[0]}','{response[1]}','{response[2]}','{response[3]}','{response[4]}','{response[5]}');")
        ssql.commit()  #보낸 SQL 요소 (url , img , name , brand , type , ingredient)
    except Exception as error:
        SQL확인.config(text='오류발생 : '+error)

    else: SQL확인.config(text="SQL 저장완료")


def form():
    '''
    url : String . 사이트 URL
    img : String (src). 대표 이미지
    name : String. 상품 이름
    brand : String. 브랜드 이름
    type : String. 화장품 타입
    ingredient : String. 전성분 (모든 성분을 하나의 문자열로 저장)
    '''
    global url
    global img
    global name
    global brand
    global type
    global ingredient

    #infor 초기화
    infor.delete("1.0", END)

    # 화장품 타입 입력 확인
    num = check()
    if (len(num)!=0) and (len(inputs_type.get())==0):
        type=num
    elif (len(num)==0) and (len(inputs_type.get())!=0):
        type=inputs_type.get()
    elif (len(num)!=0) and (len(inputs_type.get())!=0):
        type=num+', '+inputs_type.get()
    else :
        infor.insert(1.0,'화장품 종류를 입력하시오.')
        return
    
    #주소 입력 확인
    if len(inputs_link.get())!=0:
        url = inputs_link.get()
    else :
        infor.insert(2.0,'추출할 주소를 입력하시오.')
        return
    
    #selenium 크롤링 셋팅
    driver = webdriver.Chrome()
    driver.get(url) 

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #정적 크롤링 (품명 , 브랜드 , 메인 이미지)
    name = (driver.find_element(By.CLASS_NAME,'prd_name')).text
    brand = (driver.find_element(By.ID,'moveBrandShop')).text
    img = (driver.find_element(By.ID,'mainImg')).get_attribute('src')

    # 동적 크롤링 (전성분)
    driver.find_element(By.XPATH,'//a[@class="goods_buyinfo"]').click()
    time.sleep(2)
    ingredient = (driver.find_element(By.CSS_SELECTOR,'#artcInfo .detail_info_list:nth-child(8) dd')).text

    #GUI infor에 화장품 정보 입력
    infor.insert(1.0,'상품사진주소 :'+img+'\n'
        +'품명 :'+name+'\n'
        +'제작회사 :'+brand+'\n'
        +'종류 :'+type+'\n'
        +'전성분 :'+ingredient)

def check():
    num =[]
    if CheckVar1.get()==1:
        num.append('토너')
    if CheckVar2.get()==1:
        num.append('에센스')
    if CheckVar3.get()==1:
        num.append('세럼')
    if CheckVar4.get()==1:
        num.append('앰플')
    if CheckVar5.get()==1:
        num.append('로션')
    if CheckVar6.get()==1:
        num.append('크림')
    if CheckVar7.get()==1:
        num.append('클렌저')
    if CheckVar8.get()==1:
        num.append('미스트')

    num = ','.join(num)
    return num

def link_reset():
    inputs_link.delete(0,END)

# GUI 셋팅
win = Tk()  # tkinter 객체 생성
win.geometry("700x500")  # 화면 크기 설정
win.title("정보 추출기")  # 화면 이름 설정
win.resizable(False,False) # 창크기 조절 가능여부 상하,좌우

frame1=Frame(win, relief="solid", bd=2)
frame1.pack()

frame2=Frame(win, relief="solid")
frame2.pack()

frame2_1=Frame(frame2, relief="solid", bd=1)
frame2_1.pack(side='left')

frame2_2=Frame(frame2, relief="solid", bd=1)
frame2_2.pack(side='right')

frame3=Frame(win, relief="solid", bd=2)
frame3.pack()


# 화장품 종류 선택 frame Checkbutton
CheckVar1=IntVar()
CheckVar2=IntVar()
CheckVar3=IntVar()
CheckVar4=IntVar()
CheckVar5=IntVar()
CheckVar6=IntVar()
CheckVar7=IntVar()
CheckVar8=IntVar()

c1=Checkbutton(frame1,text="토너",variable=CheckVar1)
c2=Checkbutton(frame1,text="에센스",variable=CheckVar2)
c3=Checkbutton(frame1,text="세럼",variable=CheckVar3)
c4=Checkbutton(frame1,text="앰플",variable=CheckVar4)
c5=Checkbutton(frame1,text="로션",variable=CheckVar5)
c6=Checkbutton(frame1,text="크림",variable=CheckVar6)
c7=Checkbutton(frame1,text="클렌저",variable=CheckVar7)
c8=Checkbutton(frame1,text="미스트",variable=CheckVar8)

Tlqkf=Label(frame1,text="화장품 종류 선택 (복수선택가능)")
Tlqkf.pack(side='top')

c1.pack(side='left')
c2.pack(side='left')
c3.pack(side='left')
c4.pack(side='left')
c5.pack(side='left')
c6.pack(side='left')
c7.pack(side='left')
c8.pack(side='left')

# URL 화장품 종류 직접입력후 추출 frame input_text
Tlqkf=Label(frame2_1,text="추출할 올리브영 상품 페이지링크 입력")
Tlqkf.pack(side='top')

inputs_link=Entry(frame2_1,width=23)
inputs_link.pack(side='left')

button1 = Button(frame2_1,overrelief="solid",command=link_reset,text="링크초기화") #사이트 링크 Entry 초기화
button1.pack(side='left')

Tlqkf=Label(frame2_2,text="화장품 종류 직접입력 (체크박스 선택되어 있으면 그뒤에 추가됨)")
Tlqkf.pack(side='top')

inputs_type=Entry(frame2_2,width=23)
inputs_type.pack(side='left')

button = Button(frame2_2,overrelief="solid",command=form,text="정보추출") #정보 추출
button.pack(side='left')

#################

infor=Text(frame3,width=70,height=16)
infor.pack(side='top')

button = Button(frame3,overrelief="solid",command=insert,text="정보 SQL insert") #정보 SQL에 보내기
button.pack(side='top')

SQL확인 = Label(win,text='SQL 전송 여부 확인')
SQL확인.pack()

infor.insert(1.0,'상품사진주소 : \n'
        +'품명 : \n'
        +'제작회사 : \n'
        +'종류 : \n'
        +'전성분 : ')


win.mainloop()
