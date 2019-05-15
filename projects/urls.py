from django.urls import path
from . import views
app_name='projects'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:project_id>/', views.project_details, name="project_details"),
    path('<int:project_id>/addComment', views.new_comment, name="addComment"),
    path('<int:project_id>/deleteComment/<int:comment_id>', views.delete_comment, name="deleteComment"),
    path('<int:project_id>/editComment/<int:comment_id>', views.edit_comment, name="editComment"),
    path('<int:project_id>/updateComment/<int:comment_id>', views.update_comment, name="updateComment"),
    path('<int:project_id>/comments/<int:comment_id>/newReply', views.new_reply, name="newReply"),
    path('<int:project_id>/comments/<int:comment_id>/addReply', views.add_reply, name="addReply"),
    path('<int:project_id>/comments/<int:comment_id>/deleteReply/<int:reply_id>', views.delete_reply, name="deleteReply"),
    path('<int:project_id>/comments/<int:comment_id>/editReply/<int:reply_id>', views.edit_reply, name="editReply"),
    path('<int:project_id>/comments/<int:comment_id>/updateReply/<int:reply_id>', views.update_reply, name="updateReply"),
    path('<int:project_id>/donate', views.donate, name="donate"),

    path('create', views.create, name="create"),

]