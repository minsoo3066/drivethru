from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from drive_restapi.models import prod, receipt, login, cafe
from django.shortcuts import redirect
import requests, json
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
global checked_prod_id
"""
1) 관리자
""" 
stffLogin = login.objects.all()

def manage_login(request):
    context = {
        'a':''
    }

    #POST 전송이 들어오면
    if request.method == 'POST':

        #POST 전송 데이터에 있는 'StaffLogin' 가져와서 restapi에 post로 전송 -> 데이터 집어넣기
        StaffLogin = request.POST['StaffLogin']
        url = 'http://localhost:8000/api/logins' #이부분 수정하기
        data = {"login_id":2,"password" : StaffLogin} #model에서 login_id 자동 증가하게 바꾸기
        response = requests.post(url, data=data)
        print(response.text) #-> 잘 들어갔는지 확인할 때 html 하단에 보면 나옴


        #로그인 패스워드 데이터와 동일하면 menu 페이지로 이동
        if StaffLogin:
            managerLoginCheck = cafe.objects.filter(manager_password=StaffLogin) #매니저 비밀번호라면
            messages.info(request,managerLoginCheck.exists())

            if (managerLoginCheck.exists() == True): #login에 존재하는 게 True라면
                return redirect('/manager/menu')

            staffLoginCheck = cafe.objects.filter(staff_password=StaffLogin) #일반 직원 비밀번호라면
            messages.info(request,staffLoginCheck.exists())

            if (staffLoginCheck.exists() == True): #login에 존재하는 게 True라면
                return redirect('/manager/staff-orders')

    return render(request, 'manager/manage_login.html', context)


def manage_menu(request):    
    class_prods = prod.objects.all()

    if request.method == "POST":
        if 'delete' in request.POST:#메뉴 삭제
            checked_prod_id  = request.POST.getlist('chk_box[]')
            for pk in checked_prod_id:
                print(pk)
                try:
                    delete_prod_id = prod.objects.get(prod_id = pk)
                    delete_prod_id.delete()
                    print("Record deleted successfully!")
                except:
                    print("Record doesn't exists")

        elif 'update' in request.POST:#메뉴 수정
            checked_prod_id = request.POST.getlist('chk_box[]')
            for pk in checked_prod_id:
                    print(pk)
                    try:
                        global update_prod
                        update_prod = prod.objects.get(prod_id = pk)
                        print("데이터 전달 완료")
                    except:
                        print("데이터 전달 에러")
            return render(request, 'manager/manage_menu_update.html', {'update_prod':update_prod})
        elif 'one_prod_update' in request.POST: #메뉴 수정
            try:
                print("try success")
                prod_category = request.POST.get('prod_category')
                prod_name = request.POST.get('prod_name')
                prod_price = request.POST.get('prod_price')
                prod_image = request.FILES['prod_image']
                prod_option = request.POST.getlist('prod_option[]')

                if 'HOT' in prod_option and "ICED" in prod_option:
                    prod_hot_cold = 3
                elif 'HOT' not in prod_option and "ICED" in prod_option:
                    prod_hot_cold = 2
                elif 'HOT' in prod_option and "ICED" not in prod_option:
                    prod_hot_cold = 1
                else:
                    prod_hot_cold = 0
                    
                if "카페인" in prod_option:
                    prod_caf_amount = True
                else:
                    prod_caf_amount = False

                if "시럽" in prod_option:
                    prod_syrup = 1
                else:
                    prod_syrup = 0

                if "샷" in prod_option:
                    prod_shot = True
                else:
                    prod_shot = False

                if "우유" in prod_option:
                    prod_milk = True
                else:
                    prod_milk = False

                if "휘핑크림" in prod_option:
                    prod_whip = True
                else:
                    prod_whip = False

                if "자바칩" in prod_option:
                    prod_java_chip = True
                else:
                    prod_java_chip = False

                if "드리즐" in prod_option:
                    prod_driz = True
                else:
                    prod_driz = False
                    
                    update_prod.prod_category=prod_category
                    update_prod.prod_name=prod_name
                    update_prod.prod_price=int(prod_price)
                    update_prod.prod_image=prod_image
                    update_prod.prod_hot_cold=prod_hot_cold
                    update_prod.prod_caf_amount=prod_caf_amount
                    update_prod.prod_syrup=prod_syrup
                    update_prod.prod_shot=prod_shot
                    update_prod.prod_milk=prod_milk
                    update_prod.prod_whip=prod_whip
                    update_prod.prod_java_chip=prod_java_chip
                    update_prod.prod_driz=prod_driz
                    update_prod.save()
                
                print("manage_menu 수정 완료")
            except:
                print("manage_menu 수정 에러")
    return render(request, 'manager/manage_menu.html', {'class_prods':class_prods})


def manage_menuadd(request):
    context = {
        'a':''
    }

    if request.method == "POST":
        prod_category = request.POST.get('prod_category')
        prod_name = request.POST.get('prod_name')
        prod_price = request.POST.get('prod_price')
        prod_image = request.FILES['prod_image']
        prod_option = request.POST.getlist('prod_option[]')

        if 'HOT' in prod_option and "ICED" in prod_option:
            prod_hot_cold = 3
        elif 'HOT' not in prod_option and "ICED" in prod_option:
            prod_hot_cold = 2
        elif 'HOT' in prod_option and "ICED" not in prod_option:
            prod_hot_cold = 1
        else:
            prod_hot_cold = 0
        
        if "카페인" in prod_option:
            prod_caf_amount = True
        else:
            prod_caf_amount = False

        if "시럽" in prod_option:
            prod_syrup = 1
        else:
            prod_syrup = 0

        if "샷" in prod_option:
            prod_shot = True
        else:
            prod_shot = False

        if "우유" in prod_option:
            prod_milk = True
        else:
            prod_milk = False

        if "휘핑 크림" in prod_option:
            prod_whip = True
        else:
            prod_whip = False

        if "자바칩" in prod_option:
            prod_java_chip = True
        else:
            prod_java_chip = False

        if "드리즐" in prod_option:
            prod_driz = True
        else:
            prod_driz = False

        prod_add = prod(prod_category=prod_category, prod_name=prod_name, prod_price=int(prod_price), prod_image=prod_image, prod_recommend = False, prod_hot_cold=prod_hot_cold ,prod_caf_amount=prod_caf_amount, prod_syrup=prod_syrup, prod_shot=prod_shot, prod_milk=prod_milk, prod_whip=prod_whip, prod_java_chip=prod_java_chip, prod_driz=prod_driz, prod_sales_rate=0)
        prod_add.save(force_insert=True)
        print("Record add successfully!")
    return render(request, 'manager/manage_menu_add.html', context)

def manage_menuupdate(request):
    context = {
        'a':''
    }
    print("이 함수 돌아가요")
    if request.method == "POST":
        try:
            global update_prod
            prod_category = request.POST.get('prod_category')
            prod_name = request.POST.get('prod_name')
            prod_price = request.POST.get('prod_price')
            prod_image = request.FILES['prod_image']
            prod_option = request.POST.getlist('prod_option[]')

            if 'HOT' in prod_option and "ICED" in prod_option:
                prod_hot_cold = 3
            elif 'HOT' not in prod_option and "ICED" in prod_option:
                prod_hot_cold = 2
            elif 'HOT' in prod_option and "ICED" not in prod_option:
                prod_hot_cold = 1
            else:
                prod_hot_cold = 0
            
            if "카페인" in prod_option:
                prod_caf_amount = True
            else:
                prod_caf_amount = False

            if "시럽" in prod_option:
                prod_syrup = 1
            else:
                prod_syrup = 0

            if "샷" in prod_option:
                prod_shot = True
            else:
                prod_shot = False

            if "우유" in prod_option:
                prod_milk = True
            else:
                prod_milk = False

            if "휘핑크림" in prod_option:
                prod_whip = True
            else:
                prod_whip = False

            if "자바칩" in prod_option:
                prod_java_chip = True
            else:
                prod_java_chip = False

            if "드리즐" in prod_option:
                prod_driz = True
            else:
                prod_driz = False

            update_prod.prod_category=prod_category
            update_prod.prod_name=prod_name
            update_prod.prod_price=int(prod_price)
            update_prod.prod_image=prod_image
            update_prod.prod_hot_cold=prod_hot_cold
            update_prod.prod_caf_amount=prod_caf_amount
            update_prod.prod_syrup=prod_syrup
            update_prod.prod_shot=prod_shot
            update_prod.prod_milk=prod_milk
            update_prod.prod_whip=prod_whip
            update_prod.prod_java_chip=prod_java_chip
            update_prod.prod_driz=prod_driz
            update_prod.save(force_insert=True)
            print("manage_menuupdate 수정 완료")
        except:
            print("manage_menuupdate 수정 에러")
    return render(request, 'manager/manage_menu_update.html', context)

def manage_recommendation_menu(request):
    class_prods = prod.objects.all()

    category = request.POST.get('prod_category')
    prod_list = prod.objects.filter(prod_category=category)
    context = {
            'class_prods':class_prods,
            'prod_list': prod_list,
    }

    if request.method == "POST":
        if 'update' in request.POST:#추천 설정
            checked_prod_id  = request.POST.getlist('chk_box[]')
            for pk in checked_prod_id:
                print(pk)
                try:
                    delete_prod_id = prod.objects.get(prod_id = pk)
                    delete_prod_id.prod_recommend = True
                    delete_prod_id.save()
                    print("Record prod_recommend = True successfully!")
                except:
                    print("Record doesn't exists")

        elif 'delete' in request.POST:#추천 취소
            checked_prod_id  = request.POST.getlist('chk_box[]')
            for pk in checked_prod_id:
                print(pk)
                try:
                    delete_prod_id = prod.objects.get(prod_id = pk)
                    delete_prod_id.prod_recommend = False
                    delete_prod_id.save()
                    print("Record prod_recommend = False successfully!")
                except:
                    print("Record doesn't exists")

        
    return render(request, 'manager/manage_recommendation_menu.html', context)
    

def manage_orders(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_orders.html', context)


def staff_orders(request):
    context = {
        'a':''
    }
    return render(request, 'manager/staff_orders.html', context)



"""
2) 고객
"""

# 전역 변수
today_user_id = ''
member_id = ''


# 1. 차 조회
from drive_restapi.models import member, today_user, receipt
members = member.objects.all() #member 데이터 db에서 가져오기
today_users = today_user.objects.all() #today_user 데이터 db에서 가져오기

def user_car(request):
    
    context = {
        'today_user_id':'',
        'member_id':''
    }

    global today_user_id
    global member_id

    #POST 전송이 들어오면
    if request.method == 'POST':

        #POST 전송 데이터에 있는 'todayUserCar' 가져와서 restapi에 post로 전송 -> 데이터 집어넣기
        todayuserCar = request.POST['todayUserCar']
        url = 'http://localhost:8000/api/todayusers'
        #url = 'http://3.37.186.91:8000/api/todayusers'
        data = {"today_user_car" : todayuserCar}
        response = requests.post(url, data=data)
        #messages.info(request, response.text) -> 잘 들어갔는지 확인할 때 html 하단에 보면 나옴


        #MEMBER 데이터와 동일하면 MEMBER-ORDER 페이지로 이동
        if todayuserCar:
            member = members.filter(member_car__icontains=todayuserCar) #memberCar와 동일한 차 번호 있는지 확인
            today = today_users.filter(today_user_car__icontains=todayuserCar)
            messages.info(request,member.exists())

            if (member.exists() == True): #member에 존재하는 게 True라면
                #전역변수 사용
                member_id = member.values()[0]['member_id']
                today_user_id = today.values().last()['today_user_id']
                return redirect('/client/menu/member-orders')
            else:
                #전역변수 사용
                today_user_id = today.values().last()['today_user_id']
                member_id = ''
                return redirect('/client/menu/non-member-orders')
        
    return render(request, 'client/user_car.html', context)


# 2. 고객 주문
from drive_restapi.models import prod
from drive_restapi.models import item
prods = prod.objects.all() #prod 데이터 db에서 가져오기
prods_val = prod.objects.values_list()
prod_list = list(prods_val)
print(prod_list[0])

receipts = receipt.objects.all() #receipt 데이터 가져오기
items = item.objects.all()


def member_order(request):
    #전역변수 사용
    global today_user_id
    global member_id
    global receipts
    global items
    
    context = {
        'today_user_id':today_user_id,
        'member_id':member_id
    }
    print(context)

    # 최근 주문 내역 2개 뽑아오기
    receipt_reverse = receipts.filter(member_id__exact=member_id) #거꾸로
    receipt_last = receipt_reverse[:2] #2개만 가져옴
    
    if (receipt_last):

        #마지막 영수증 아이디 두개 가져오기
        receipt_id_1 = receipt_last[0].receipt_id
        receipt_id_2 = receipt_last[1].receipt_id

        #아이템 중에 영수증 아이디 해당되는 거 가져오기
        item_reverse_1 = items.filter(receipt_id__exact=receipt_id_1)[::-1]
        item_reverse_2 = items.filter(receipt_id__exact=receipt_id_2)[::-1]

        item_last_1 = item_reverse_1[:2] #2개만 가져옴
        item_last_2 = item_reverse_2[:2]

        #마지막 아이템 아이디 두개 가져오기
        prod_id_1 = item_last_1[0].prod_id
        prod_id_2 = item_last_1[1].prod_id
        prod_id_3 = item_last_2[0].prod_id
        prod_id_4 = item_last_2[1].prod_id

        #거기에 있는 실제 상품 쿼리셋 가져오기
        prod_1 = prods.filter(prod_name__exact=prod_id_1)
        prod_2 = prods.filter(prod_name__exact=prod_id_2)
        prod_3 = prods.filter(prod_name__exact=prod_id_3)
        prod_4 = prods.filter(prod_name__exact=prod_id_4)
        
        #잘 왔나 확인하기
        print(prod_1,prod_2, prod_3, prod_4)


        #최다 주문 내역 확인하기
        receipt_list = []
        item_list = []
        receipt_reverse = receipts.filter(member_id__exact=member_id)[::-1] #거꾸로

        for i in receipt_reverse: 
            receipt_list.append(i.receipt_id) #id 리스트 가지고 넣어주기

        for i in receipt_list:
            item_list.append(items.filter(receipt_id__exact=i))
        

        


    #POST 전송이 들어오면 영수증 등록
    if request.method == 'POST':
        print("\n*************************************POST들어옴****************************************\n", request.POST)
        
        #1. receipt 영수증 form의 post인 경우
        if 'receiptPrice' in request.POST:
            print("\n1. receipt 요청\n", request.POST)
            #form에서 name에 해당하는 값 가져오기
            todayUserId = request.POST['todayUserId']  #ㅅㅂ 이거 차번호 말고 차 아이디가 들어가고 있는거지?
            memberId = request.POST['memberId']
            receiptPrice = request.POST['receiptPrice']
            receiptTodayId = request.POST['receiptTodayId']

            url = 'http://localhost:8000/api/receipt'
            #url = 'http://3.37.186.91:8000/api/receipt'
            data = {"today_user_id" : todayUserId, "member_id": memberId, "receipt_price": receiptPrice, "receipt_today_id": receiptTodayId}
            response = requests.post(url, data=data)
            #messages.info(request, response.text) #-> 잘 들어갔는지 확인할 때 html 하단에 보면 나옴
            print(response.text);

        #2. item 아이템 form의 post인 경우
        elif 'itemPrice' in request.POST: #!!!!!!!elif로 변경
            print("\n2. item 요청\n", request.POST)
            receipts = receipt.objects.all() #receipt 영수증 데이터 db에서
            itemQuantity = request.POST['itemQuantity']
            itemSize = request.POST['itemSize']
            itemPrice = request.POST['itemPrice']
            itemHotCold = request.POST['itemHotCold']
            itemCafAmount = request.POST['itemCafAmount']
            itemSyrup = request.POST['itemSyrup']
            itemShot = request.POST['itemShot']
            itemMilk = request.POST['itemMilk']
            itemWhip = request.POST['itemWhip']
            itemJavaChip = request.POST['itemJavaChip']
            itemDriz = request.POST['itemDriz']
            prodId = request.POST['prodId']
            receiptId = receipts.values().last()['receipt_id']

            """ 
            #prodName = request.POST['prodId']
            #prodId = prods.filter(prod_name__icontains=prodName) 
            """

            url2 = 'http://localhost:8000/api/item'
            #url = 'http://3.37.186.91:8000/api/item'
            data2 = {"item_quantity":itemQuantity, "item_size":itemSize, "item_price":itemPrice,
            "item_hot_cold":itemHotCold, "item_caf_amount": itemCafAmount, "item_syrup": itemSyrup,
            "item_shot":itemShot, "item_milk":itemMilk, "item_whip": itemWhip, "item_java_chip": itemJavaChip,
            "item_driz":itemDriz,"receipt_id": receiptId, "prod_id": prodId}
            response = requests.post(url2, data=data2)
            #messages.info(request, response.text) -> 잘 들어갔는지 확인할 때 html 하단에 보면 나옴
            print(response.text);

    return render(request, 'client/member_order.html', {'prods':prod_list, 'today_user_id':today_user_id, 'member_id':member_id, 'prod_1':prod_1, 'prod_2':prod_2, 'prod_3':prod_3, 'prod_4':prod_4})


def non_member_order(request):
    context = {
        'a':''
    }
    return render(request, 'client/non_member_order.html', context) 


def user_end(request):
    context = {
        'a':''
    }
    return render(request, 'client/user_end.html', context)\



#3) 형태소 분석기
"""
형태소 분석기
"""
from ckonlpy.tag import Postprocessor
from ckonlpy.tag import Twitter
import pandas as pd
from ckonlpy.utils import load_wordset
from ckonlpy.utils import load_replace_wordpair
from ckonlpy.utils import load_ngram

from django.http import JsonResponse
import os

def stem_analyzer(requests):
    print("stt로 받은 문자열")
    print(requests.GET['resText'])
    sent = requests.GET['resText']


    twitter = Twitter()

    #메뉴 추가하기
    cafemenu = pd.read_csv('cafemenu.csv')
    cafemenu['이름'].dropna()

    menudata=cafemenu['이름'].str.replace(' ', '')#데이터 형식 변경
    for i in menudata:
        twitter.add_dictionary(i, 'Noun')

    menudata=cafemenu['이름']
    for i in menudata:
        twitter.add_dictionary(i, 'Noun')
        
    #옵션 종류 추가하기
    cafeoption = pd.read_csv('cafeoption.csv')
    cafeoption['옵션 종류'].dropna()
    optiondata=cafeoption['옵션 종류'].str.replace(' ', '')

    for i in optiondata:
        twitter.add_dictionary(i, 'Noun')
        
    optiondata=cafeoption['옵션 종류']
    for i in optiondata:
        twitter.add_dictionary(i, 'Noun')
 
    #문장에 필요없는 단어
    stopwords = load_wordset('./tutorials/stopwords.txt')

    #의미가 같은 것으로 변경할 단어
    replace = load_replace_wordpair('./tutorials/replacewords.txt')

    #띄어쓰기 없애는 단어로
    ngrams = load_ngram('./tutorials/ngrams.txt')

    #첫번째 분석 하기
    postprocessor = Postprocessor(
            base_tagger = twitter, # base tagger
            replace = replace, # 해당 단어 set 치환
            stopwords = stopwords # 해당 단어 필터
        )

    mywords = ""
    for i in postprocessor.pos(sent):
        mywords+=i[0]

    #print("단어 변환+단어 삭제 결과:  "+mywords)

    #두번째 분석 하기
    postprocessor = Postprocessor(
        base_tagger = twitter, # base tagger
        replace = replace, # 해당 단어 set 치환
        stopwords = stopwords, # 해당 단어 필터
    )

    mywords2 = ""
    for i in postprocessor.pos(mywords):
        mywords2+=i[0]
    #print("단어 변환+단어 삭제2 결과:  "+mywords2)
        
    #띄어쓰기만 조정
    postprocessor = Postprocessor(
        base_tagger = twitter, # base tagger
        ngrams = ngrams # 해당 복합 단어 set을 한 단어로 결합
    )

    orderdata = []
    order = []
    delete_word = [' ', '-']

    for i in postprocessor.pos(mywords2):
        orderdata.append(i[0])
    #print("단어만 추가: ", orderdata)

    #부호 삭제하여 리스트에 추가

    for i in orderdata:
        for j in delete_word:
            i=i.replace(j, '')
        order.append(i)
    print("\n")
    print("결과:", order)

    return JsonResponse(order, safe=False)
