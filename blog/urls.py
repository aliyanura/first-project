from django.urls import path
from .views import post_list, post_detail, post_create, post_edit, post_delete, comment_delete


urlpatterns = [
    path('create/', post_create, name= 'post_create'),
    path('list/', post_list, name = 'posts_list'),
    path('edit/<int:pk>/', post_edit, name='post_edit'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
            post_detail, name='post_detail'),
    path('delete/<int:pk>/', post_delete, name='post_delete'),
    path('delete_comment/<int:pk>/', comment_delete, name='comment_delete'),
]