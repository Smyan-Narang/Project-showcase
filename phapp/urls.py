from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('Login', views.login, name='login'),
    path('Signup', views.signup, name='signup'),
    path('Logout', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('AddProject/', views.add, name='addproject'),
    path('ViewProject/<int:pk>/', views.viewproject, name='ViewProject'),
    path('Viewhomeproject/<int:pk>/', views.viewhomeproject, name='Viewhomeproject'),
    path('EditProject/<int:pk>/', views.EditProject, name='EditProject'),
    path('DeleteProject/<int:pk>/', views.deleteproject, name='DeleteProject'),
    path('deleteAccount/', views.deleteaccount, name='deleteaccount'),
    path('EditProfile/', views.saveaccount, name='EditProfile')
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
