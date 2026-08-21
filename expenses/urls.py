from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logs/<int:log_id>/delete/', views.delete_log_view, name='delete_log'),
    path('groups/<int:group_id>/settle/', views.settlement_view, name='settlement'),
    path('groups/<int:group_id>/expenses/create/', views.create_expense_view, name='create_expense'),
    path('groups/<int:group_id>/', views.group_detail_view, name='group_detail'),
    path('groups/create/', views.create_group_view, name='create_group'),
    path('groups/join/', views.join_group_view, name='join_group'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home_view, name='home'),
]