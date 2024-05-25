from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="main"),
    # path("testvideo/", views.videoTest, name="test_video"),
    path("login/", views.login, name="login"),
    path("clearcache/", views.clearCache), #test
    path("registration/", views.registration, name="registration"),
    path("mailconfirmation/", views.mailconfirmation, name="mailconfirmation"),
    path("me", views.myProfile, name="me"),
    path("logout/", views.logout, name="logout"),
    path("testJSON/", views.returnRequestTEST, name="testJSON"), #test
    path("resendregcode/", views.newMailConfirmationCode, name="resendregcode"),
    path("uploadavatar/", views.loadAvatar, name="uploadAvatar"),
    # path("videoproctest/", views.videoProcTest, name="videoProcTest"), #test
    path("video/", views.video, name="video"), #test
    path("passwordRecovery/", views.passwordRecovery, name="passwordRecovery"),
    path("loadVideo/", views.loadVideo, name="loadVideo"),
    path('@<str:slugname>/', views.channel, name='channel'),
    path("loadTempVideo/", views.loadTempVideo, name = "loadTempVideo"),
    path("like/", views.like, name="like"),
    path("unlike/", views.unlike, name="unlike"),
    path("dislike/", views.dislike, name="dislike"),
    path("undislike/", views.undislike, name="undislike"),
    path("comment/", views.comment, name="comment"),
    path("follow/", views.follow, name="follow"),
    path("unfollow/", views.unfollow, name="unfollow"),

]
