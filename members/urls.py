from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('create-admin/', views.create_admin, name='create_admin'),  # URL to access the create admin form

]

