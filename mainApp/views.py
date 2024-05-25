from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, HttpResponseBadRequest, Http404
import json
from .forms import *
from datetime import datetime, timedelta
from .manager import *
from django.urls import reverse
from .consumers import *

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




# Create your views here.

@account_confirm_required
def loadTempVideo(request, *args, **kwargs):
    data = kwargs.get("data") or dict()

    if request.method == 'POST' and request.FILES['originalVideo']:
        myfile = request.FILES['originalVideo']
        
        filename = str(myfile)
        if not any(filename.lower().endswith(i) for i in ['mov','avi','mp4','webm','mkv']):
            return JsonResponse({"status": 415, "message": "Unsupported Media Type"})
        u = User.authUser(request)
        tempVideo = TempVideo()
        tempVideo.author = u
        tempVideo.video = myfile
        tempVideo.save()
        print(str(myfile) + " loaded")
        return JsonResponse({"status": 200, "backID": tempVideo.id})

@sendPublicUserData
@account_confirm_required
def loadVideo(request, *args, **kwargs):
    data = kwargs.get("data") or dict()
    print(f"data: {data}")

    if request.method=="GET":
        fr = VideoForm()

        data["form"] = fr

        return render(request, "loadVideo.html", data)
    elif request.method == "POST":
        

        print("a")
        v = Video()
        print("b")


        form = VideoForm(request.POST, request.FILES, instance=v)

        print("c")

        print(form.data)

        if form.is_valid():

            try:
                tempVID = TempVideo.objects.get(id = int(form.data["backID"]))
                print(tempVID)
                print("d")
                if User.authUser(request) == tempVID.author:
                    print("e")
                    v.author = tempVID.author
                    v.originalVideo = tempVID.video
                    form.save()

                    send_message_to_group(f"follow_{v.author.id}", f"{v.author.nickname} - new video - {v.title} ")

                    return redirect("main")
                print("f")
                

            except Exception as ex:
                print(ex)
                print("g")
                ...

            # form.save()

            # v.author = User.authUser(request)

            # v.save()
            # proccessVid(v)

            


        else:
            print("h")

            print(form.errors)

            data["form"] = form
            return render(request, "loadVideo.html", data)

        


@sendPublicUserData
def video(request, *args, **kwargs):
    data = kwargs.get("data") or dict()

    try:
        videoID = request.GET.get('id')
        # v = Video.objects.get(id=videoID)
        v = Video.get_video_by_id(videoID)
        print(v.originalVideo.path)
        data["video"] = v
        data["comments"] = Comment.objects.filter(destination=v)

        data["like"] = Like.objects.filter(destination=v, source=User.authUser(request)).first()
        data["dislike"] = Dislike.objects.filter(destination=v, source=User.authUser(request)).first()

        return render(request, "videoById.html", data)

    except Exception as ex:
        print(ex)
        return HttpResponse("Not found")


def returnRequestTEST(request):
    killRegCodes()
    print(f"url: {reverse('me')}")

    if request.method == "POST":
        data = json.loads(request.body)
        print(f"data type = {type(data)}")
        print(data)


    #return JsonResponse({"status": 1, "message": "Data received"})

    context = {'request_data': request.META}
    return render(request, 'showRequest.html', context)






# def videoProcTest(request):
#     if request.method == "GET":
#         data = {
#             "videoForm": VideoTestForm()
#         }

#         return render(request, "videoProccesingTest.html", data)
#     elif request.method == "POST":

#         v = VideoTest()



#         form = VideoTestForm(request.POST, request.FILES, instance=v)
#         if form.is_valid():
#             print("video form is valid")
#             form.save()

#             proccessVid(v.video.path)

#             return HttpResponse("200")
#         else:
#             print(form.errors)
#             return HttpResponse(form.errors)

@login_required
def loadAvatar(request):

    if request.method == "POST":
        u = User.authUser(request)
        if u:
            form = AvatarForm(request.POST, request.FILES, instance=u)

            if form.is_valid():
                print("form is valid")
                form.save()
                return redirect('me')
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()



@sendPublicUserData
def index(request, *args, **kwargs):
    data = kwargs.get("data") or dict()
    print("main loaded")

    data["videos"] = Video.objects.all()

    return render(request, "main.html", data)






@login_forbidden
def registration(request, *args, **kwargs):
    data = kwargs.get("data") or dict()
    if(request.method == "GET"):
        return render(request, "registration.html", data)
    else:

        try:
            login_data = json.loads(request.body)
        except:
            return HttpResponseBadRequest()
        reg = User.register(login_data)

        print(reg)

        if reg.isSuccesful():
            createAndSendRegCode(User.objects.get(email=login_data.get("email")))
            return JsonResponse({"status": 1})
        else:
            
            return JsonResponse({"status": 0, "message": " ".join(reg.getErrors())})



@login_required
@sendPublicUserData
def newMailConfirmationCode(request, *args, **kwargs):

    data = kwargs.get("data") or dict()
    if request.method == "GET":
        return HttpResponseBadRequest()
    
    u = User.authUser(request)

    if u:
        try:
            code = VerificationCode.objects.get(user=u, codeType="Reg")

            if code.isDeltaMinute():
                if code.completed:
                    return JsonResponse({"status": 0, "message":"code not found"})
                else:
                    s = generateCode()
                    to = code.user.email
                    subject = "GemboTube verification code"

                    code.updateCode(s)

                    send_mail(subject, s, None, [to], fail_silently=False)
                    return JsonResponse({"status": 1, "codeTimer": code.getTimeDelta()})
            else:
                return JsonResponse({"status": 0, "message":"wait a minute"})

        except:
            return JsonResponse({"status": 0, "message":"code not found"})
    else:
        return HttpResponseForbidden


@login_required
@sendPublicUserData
def mailconfirmation(request, *args, **kwargs):

    data = kwargs.get("data") or dict()

    u = User.authUser(request)

    if request.method == "GET":

        try:
            code = VerificationCode.objects.get(user = u, codeType = "Reg")

            data ["codeTimer"] = code.getTimeDelta()
            
            return render(request, "mailconfirmation.html", context=data)

        except Exception as ex:
            print(ex)
            return HttpResponse("Code not found")

        
    else:
        login_data = json.loads(request.body)
        print(login_data)
        gettedCode = login_data.get("confirmCode")

        try:
            code = VerificationCode.objects.get(user = u, codeType = "Reg")
            res = code.checkCode(gettedCode)

            if res:
                code.completed = True
                code.save()
                u.activated = True
                u.save()
                return JsonResponse({"status": 1, "message":"OK"})
            else:
                return JsonResponse({"status": 0, "message":"wrong code"})

        except Exception as ex:
            print(ex)
            return JsonResponse({"status": 0, "message":"code not found"})

                

@login_forbidden
def login(request, *args, **kwargs):
    data = kwargs.get("data") or dict()
    if request.method == "GET":
        return render(request, "Login.html", data)
    if request.method == "POST":
        login_data = json.loads(request.body)
        print(login_data)
        email = login_data.get("email")
        password = login_data.get("password")

        try:
            user = User.objects.get(email=email)
            if User.validateUser(email, password) != None:
                request.session["userID"] = user.id
                print("loggined")
                #return redirect("me")
                return JsonResponse({"status": 1, "message": "Success"})
            else:
                print("cheto ne tak")
                data = dict()
                data["loginError"] = "Wrong email or password!"

                #return render(request, "Login.html", data)
                return JsonResponse({"status": 0, "message": "Wrong email or password!"})
        except:
            print("cheto ne tak")
            data = dict()

            data["loginError"] = "Wrong email or password!"

            #return render(request, "Login.html", data)
            return JsonResponse({"status": 0, "message": "Wrong email or password!"})


def clearCache(request):
    cache.clear()
    return redirect("main")


@login_required
@sendPublicUserData
def myProfile(request, *args, **kwargs):
    data = kwargs.get("data") or dict()
    u = User.authUser(request)
    data["user"] = u
    data["uploadAvatarForm"] = AvatarForm()

    return render(request, "profile.html", data)
    


@login_required
def logout(request):
    if request.method == "POST":
        request.session["userID"] = ""

        return redirect("main")
    else:
        return HttpResponseForbidden()
    
def passwordRecovery(request):
    return render(request, "passwordRecovery.html")




@sendPublicUserData
def channel(request, slugname, *args, **kwargs):
    data = kwargs.get("data") or dict()
    try:
        #EchoConsumer.send_to_every(slugname)

        send_broadcast_notification(slugname)

        channel = User.getChannel(slugname)
        videos = Video.get_videos_by_author_id(channel.id)
        data ["channel"] = channel
        data["videos"] = videos

        return render(request, "channel.html", data)

    except Exception as ex:
        print(ex)
        return HttpResponse("Not foundd")



@account_confirm_required
def like(request, *args, **kwargs):
    if request.method!="POST":
        return HttpResponseBadRequest()


    data = kwargs.get("data") or dict()
    u = User.authUser(request)
    print(request.POST)

    post = json.loads(request.body)

    video_id = int(post.get('video_id'))
    v = Video.objects.get(id = video_id)
    if v:
        if Like.objects.filter(source=u, destination=v).first():
            return JsonResponse({"status": 200, "message": "OK"})
        else:
            like = Like(source=u, destination=v)
            v.likes+=1
            v.save()
            like.save()
            # send_message_to_group(f"user{v.author.id}", f"{v.author.nickname} - new video - {v.title} ")
            send_notification(f"user_{v.author.id}", {
                "link":f"/video/?id={v.id}",
                "title":"New like",
                "text": f"User {u.nickname} liked your video: {v.title}"
            })
            return JsonResponse({"status": 200, "message": "OK"})

    else:
        return JsonResponse({"status": 404, "message": "Video not found"})


@account_confirm_required
def unlike(request, *args, **kwargs):
    if request.method!="POST":
        return HttpResponseBadRequest()


    data = kwargs.get("data") or dict()
    post = json.loads(request.body)
    u = User.authUser(request)
    video_id = int(post.get('video_id'))
    v = Video.objects.get(id = video_id)
    if v:
        l = Like.objects.filter(source=u, destination=v).first()
        if l:
            l.delete()
            v.likes-=1
            v.save()
            return JsonResponse({"status": 200, "message": "OK"})
        else:
            return JsonResponse({"status": 200, "message": "OK"})

    else:
        return JsonResponse({"status": 404, "message": "Video not found"})


@account_confirm_required
def dislike(request, *args, **kwargs):
    if request.method!="POST":
        return HttpResponseBadRequest()

    data = kwargs.get("data") or dict()
    post = json.loads(request.body)
    u = User.authUser(request)
    print(request.POST)
    video_id = int(post.get('video_id'))
    v = Video.objects.get(id = video_id)
    if v:
        if Dislike.objects.filter(source=u, destination=v).first():
            return JsonResponse({"status": 200, "message": "OK"})
        else:
            dislike = Dislike(source=u, destination=v)
            v.dislikes+=1
            v.save()
            dislike.save()
            return JsonResponse({"status": 200, "message": "OK"})

    else:
        return JsonResponse({"status": 404, "message": "Video not found"})


@account_confirm_required
def undislike(request, *args, **kwargs):
    if request.method!="POST":
        return HttpResponseBadRequest()


    data = kwargs.get("data") or dict()
    u = User.authUser(request)
    post = json.loads(request.body)
    video_id = int(post.get('video_id'))
    v = Video.objects.get(id = video_id)
    if v:
        dl = Dislike.objects.filter(source=u, destination=v).first()
        if dl:
            dl.delete()
            v.dislikes-=1
            v.save()
            return JsonResponse({"status": 200, "message": "OK"})
        else:
            return JsonResponse({"status": 200, "message": "OK"})

    else:
        return JsonResponse({"status": 404, "message": "Video not found"})

@account_confirm_required
def comment(request, *args, **kwargs):
    if request.method!="POST":
        return HttpResponseBadRequest()

    data = kwargs.get("data") or dict()
    post = json.loads(request.body)
    u = User.authUser(request)
    video_id = int(post.get('video_id'))
    v = Video.objects.get(id = video_id)
    text = post.get('comment_text')

    if v:
        try:
            comment = Comment(source=u, destination=v, text=text)
            comment.save()
            return JsonResponse({"status": 200, "message": "OK"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"status": 500, "message": "Something went wrong"})
    else:
        return JsonResponse({"status": 404, "message": "Video not found"})


def follow(request, *args, **kwargs):
    if request.method!="POST":
        return HttpResponseBadRequest()

    data = kwargs.get("data") or dict()
    u = User.authUser(request)
    post = json.loads(request.body)
    channel_id = int(post.get('channel_id'))
    channel = User.objects.filter(id = channel_id).first()

    if (channel):
        f = Following.objects.filter(source=u, destination=channel).first()
        if f:
            return JsonResponse({"status": 200, "message": "OK"})
        f = Following(source=u, destination=channel)
        f.save()
        return JsonResponse({"status": 200, "message": "OK"})
    else:
        return JsonResponse({"status": 404, "message": "Video not found"})


def unfollow(request, *args, **kwargs):
    if request.method!="POST":
        return HttpResponseBadRequest()

    data = kwargs.get("data") or dict()
    post = json.loads(request.body)
    u = User.authUser(request)
    channel_id = int(post.get('channel_id'))
    channel = User.objects.filter(id = channel_id).first()

    if (channel):
        f = Following.objects.filter(source=u, destination=channel).first()
        if f:
            f.delete()
            return JsonResponse({"status": 200, "message": "OK"})
        return JsonResponse({"status": 200, "message": "OK"})
    else:
        return JsonResponse({"status": 404, "message": "Video not found"})
    
