from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지 URL
    path('signup/', views.signup, name='signup'),  # 회원가입
    path('login/', views.login_view, name='login'),  # 로그인
    path('logout/', views.logout_view, name='logout'),  # 로그아웃
    path('posts/', views.get_all_posts, name='get_all_posts'),
    path('posts/search/', views.search_posts, name='search_posts'),
    path('posts/<int:post_pk>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),  # 게시물 상세 페이지 URL 추가
    path('qna/', views.QnaListView.as_view(), name='qna_list'),
    path('category/', views.category, name='category'),  # category 페이지
    path('apply-injury/choose/', views.choose_injury_type, name='choose_injury_type'),  # 최초 요양 급여신청서 or 승인 후 절차 선택 페이지
    path('apply-injury/initial-options/', views.initial_injury_options, name='initial_injury_options'),  # 최초 요양 급여신청서 세부 옵션 페이지
    path('apply-injury/post-approval-options/', views.post_approval_options, name='post_approval_options'),  # 승인 후 절차 세부 옵션 페이지
    path('apply/', views.apply_injury, name='apply_injury'),  # 산재 신청 폼을 표시하고 제출하는 URL
    path('success/', views.application_success, name='success'),  # 신청 성공 페이지
    path('apply-injury/after/', views.after_apply_injury, name='after_apply_injury'),  # 승인 후 신청 페이지
    path('apply-injury/danger/', views.danger, name='danger'),  # 경고 메시지 페이지
    path('apply-injury/initial-after/', views.initial_after, name='initial_after'),  # 최초 요양 급여신청서 세부 옵션 페이지
]

