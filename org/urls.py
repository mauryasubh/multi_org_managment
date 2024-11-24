from django.urls import path
from . import views

urlpatterns = [
    path('', views.organization_list, name='organization_list'),  # org list for specific user
    # crud for sub-org 
    path('create-sub-organization/', views.create_sub_organization, name='create_sub_organization'),
    path('update-sub-organization/<int:org_id>/', views.update_sub_organization, name='update_sub_organization'),
    path('delete-sub-org/<int:org_id>/', views.delete_sub_org, name='delete_sub_org'),

    # craeting user for sub-organization and role as well with CRUD
    path('create-user/', views.create_user, name='create_user'),
    # path('sub-org-users/<str:org_name>/', views.sub_organization_users, name='sub_organization_users'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/', views.list_users, name='user_list'),


    # logout user
    path('logout/', views.user_logout, name='logout'),



        

]