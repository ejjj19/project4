
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    #authentication urls
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #profile url
    path("profile/<str:username>/", views.profile, name="profile"),

    #create_post urls
    path("create", views.create_post, name="create-post"),

    #following urls
    path('following', views.following, name="following"),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)