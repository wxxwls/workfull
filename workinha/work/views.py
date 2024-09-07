from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout  # 여기에서 authenticate를 가져옴
from django.utils import timezone
from django.conf import settings
from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q, Count
from django.db import transaction
import json
import datetime
from .serializers import *
from .models import *
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import activate, get_language
from django.shortcuts import render, redirect
from .models import InjuryApplication
from django.utils.dateparse import parse_date

def signup(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.POST)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                # 회원가입 성공 시 로그인 페이지로 리디렉션
                return redirect('login')  # 'login' URL 이름으로 리디렉션

        else:
            print("Serializer errors:", serializer.errors)
            return JsonResponse(serializer.errors, status=400)
    else:
        return render(request, 'signup.html')  # 회원가입 페이지 렌더링



def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.POST)
        
        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            password = serializer.validated_data.get('password')
            user = authenticate(request, id=id, password=password)
            if user is not None:
                user.last_login = timezone.now()  # 마지막 로그인 시간 갱신
                user.save()
                login(request, user)
                
                # '/category/' 페이지로 리디렉션
                return redirect('category')
                
            else:
                # 잘못된 자격 증명 오류 메시지 반환
                error_message = "ID나 비밀번호가 일치하지 않습니다."
                return render(request, 'login.html', {"error": error_message})
        
        else:
            # serializer 유효성 검사 실패 시 오류 메시지 출력
            error_message = "ID나 비밀번호가 일치하지 않습니다."
            return render(request, 'login.html', {"error": error_message})
    
    # GET 요청 시 로그인 페이지 렌더링
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return JsonResponse({
        'message': '로그아웃 성공'
    }, status=200)

def home(request):
    if request.method == 'POST':
        selected_language = request.POST.get('language')
        next_url = request.POST.get('next', '/work/')
        
        if selected_language in dict(settings.LANGUAGES):
            activate(selected_language)
            request.session[settings.LANGUAGE_COOKIE_NAME] = selected_language
            return redirect(next_url)  # 선택 후 'next_url'로 리디렉트

    current_language = get_language()
    return render(request, 'home.html', {
        'languages': settings.LANGUAGES,
        'current_language': current_language,
        'next': request.path
    })

@api_view(['GET'])
def get_all_posts(request):
    query = request.GET.get('q', '')
    
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    return render(request, 'posts.html', {'posts': posts})

@api_view(['GET'])
def search_posts(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    valid_sort_options = ['latest', 'oldest', 'popular']

    if sort_by not in valid_sort_options:
        return Response({'error': f"Invalid sort option: {sort_by}. Valid options are 'latest', 'oldest', and 'popular'."}, status=400)

    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if sort_by == 'latest':
        posts = posts.order_by('-created_at')
    elif sort_by == 'oldest':
        posts = posts.order_by('created_at')
    elif sort_by == 'popular':
        posts = posts.annotate(likes_count=Count('likes')).order_by('-likes_count')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)

def toggle_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    liked = False
    post_like, created = PostLike.objects.get_or_create(user=request.user, post=post)

    if created:
        # 사용자가 처음 좋아요를 눌렀을 때
        post.like_count += 1
        liked = True
    else:
        # 사용자가 이미 좋아요를 눌렀을 때 (좋아요 취소)
        post_like.delete()
        post.like_count -= 1
        liked = False

    post.save()

    return JsonResponse({'success': True, 'like_count': post.like_count, 'liked': liked})

def posts_view(request):
    return render(request, 'postsearch.html')  



class QnaListView(APIView):
    def get(self, request):
        qna_list = qna.objects.all()  # 모든 QnA 데이터를 가져옵니다.
        return render(request, 'qna.html', {'qna_list': qna_list})  # 데이터를 'qna.html' 템플릿으로 전달합니다.

def category(request):
    # 예시 데이터를 템플릿에 전달
    categories = ['산재신청', '사례검색', '자주 묻는 질문', '주변 지원센터 검색']
    return render(request, 'category.html', {'categories': categories})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})

def apply_injury(request):
    if request.method == 'POST':
        # POST 요청에서 데이터 추출
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        job_type = request.POST.get('job_type')
        relation_with_insured = request.POST.get('relation_with_insured')
        family_relation = request.POST.get('family_relation')
        application_type = request.POST.get('application_type')
        business_name = request.POST.get('business_name')
        business_owner_name = request.POST.get('business_owner_name')
        business_management_number = request.POST.get('business_management_number')
        business_address = request.POST.get('business_address')
        accident_description = request.POST.get('accident_description')
        checkbox_one = request.POST.get('checkbox_one') == 'on'
        checkbox_two = request.POST.get('checkbox_two') == 'on'
        checkbox_three = request.POST.get('checkbox_three') == 'on'
        witness_name = request.POST.get('witness_name')
        witness_contact = request.POST.get('witness_contact')
        witness_relation = request.POST.get('witness_relation')
        has_received_compensation = request.POST.get('has_received_compensation') == 'on'
        receipt_date = request.POST.get('receipt_date')
        receipt_amount = request.POST.get('receipt_amount')
        payment_source = request.POST.get('payment_source')
        attached_documents = request.FILES.get('attached_documents')

        # 데이터베이스에 저장
        injury_application = InjuryApplication(
            name=name,
            id_number=id_number,
            address=address,
            phone=phone,
            start_time=start_time,
            end_time=end_time,
            job_type=job_type,
            relation_with_insured=relation_with_insured,
            family_relation=family_relation,
            application_type=application_type,
            business_name=business_name,
            business_owner_name=business_owner_name,
            business_management_number=business_management_number,
            business_address=business_address,
            accident_description=accident_description,
            checkbox_one=checkbox_one,
            checkbox_two=checkbox_two,
            checkbox_three=checkbox_three,
            witness_name=witness_name,
            witness_contact=witness_contact,
            witness_relation=witness_relation,
            has_received_compensation=has_received_compensation,
            receipt_date=parse_date(receipt_date) if receipt_date else None,
            receipt_amount=receipt_amount if receipt_amount else None,
            payment_source=payment_source,
            attached_documents=attached_documents
        )

        injury_application.save()


    return render(request, 'apply.html')  # 신청 폼을 렌더링

def application_success(request):
    return render(request, 'application_success.html')

def choose_injury_type(request):
    return render(request, 'choose_injury_type.html')  # 이 페이지에서 최초/승인 후 선택

# 최초 요양 급여신청서 세부 항목 페이지
def initial_injury_options(request):
    return redirect('success')  # 성공 페이지로 리다이렉트
    return render(request, 'initial_injury_options.html')  # 최초 요양 급여신청서의 세부 항목 선택

# 승인 후 절차 세부 항목 페이지
def post_approval_options(request):
    return render(request, 'post_approval_options.html')  # 승인 후 절차의 세부 항목 선택

