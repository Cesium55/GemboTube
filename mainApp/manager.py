from .models import User, VerificationCode, Video
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail
from random import randint
from django.shortcuts import redirect
from django.core.files import File
import re

import moviepy.editor as mp


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


moscow_tz = timezone(timedelta(hours=3))


def send_broadcast_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'broadcast_group',
        {
            'type': 'broadcast_message',
            'message': message
        }
    )
def send_message_to_group(group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            'type': 'chat_message',
            'message': message
        }
    )


def send_notification(group, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            'type': 'chat_message',
            "message":data,
            # 'link': data["link"],
            # 'title': data["title"],
            # 'text': data["text"]
        }
    )



def login_required(view_func):
    def wrapper(*args, **kwargs):

        if User.authUser(args[0]):
            return view_func(*args, **kwargs)
        else:
            return redirect('login')

    return wrapper

def account_confirm_required(view_func):
    def wrapper(*args, **kwargs):

        if User.authUser(args[0]):
            ...
        else:
            return redirect("login")
        if User.authUser(args[0]).activated:
            return view_func(*args, **kwargs)
        else:
            return redirect('mailconfirmation')

    return wrapper

def login_forbidden(view_func):
    def wrapper(*args, **kwargs):

        if User.authUser(args[0]):
            
            return redirect('main')
        else:
            return view_func(*args, **kwargs)

    return wrapper

def sendPublicUserData(view_func):
    def wrapper(*args, **kwargs):

        data = kwargs.get("data") or dict()

        u = User.authUser(args[0])

        if u:
            newData = u.getPublicData()

            for i in newData.keys():
                data[i] = newData[i]
            kwargs["data"] = data

        return view_func(*args, **kwargs)
            
    return wrapper

def killRegCodes():
    codes = VerificationCode.objects.filter(codeType = "Reg", completed=False)
    now = datetime.now(moscow_tz)
    day = timedelta(days=1)

    
    
    for code in codes:
        if (code.completed == False) and (now - code.created > day):
            print(code)
            print(code.user)
            code.user.delete()

def generateCode(l=6):
    s = ""
    for _ in range(l):
        s += str(randint(0, 9))

    return s
    
def createAndSendRegCode(user: User):
    s = generateCode()
    
    to = user.email
    subject = 'GemboTube verification code'
    send_mail(subject, s, None, [to], fail_silently=False)


    print(f"{s} {user} ")

    code = VerificationCode(
        user=user,
        code = s,
        codeType="Reg"
    )

    print(code)

    code.save()

def logString(string : str) -> str:
    return f"[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {string}"

def proccessVid(video: Video):
    filename = video.originalVideo.path
    print(filename)
    clip = mp.VideoFileClip(filename)
    arr = [240, 360, 480, 720, 1080, 1440, 2160]


    steps = filename.split("\\")

    path = "\\".join(steps[:-1])
    temp_name = steps[-1].split(".")

    name = ".".join(temp_name[:-1])
    ext = temp_name[-1]
    print(video.originalVideo.name)
    newFilepath = ".".join(re.search(r"media/.*$", video.originalVideo.name).group(0).split(".")[:-1])

    print(path, name, ext)

    for mx in reversed(range(len(arr))):
        if arr[mx] >= clip.size[1]:
            break
        

    for i in range(len(arr)):
        if arr[i] <= clip.size[1]:
            clip_resized = clip.resize(height=arr[i]) 
            clip_resized.write_videofile(f"{path}\\{name}__{arr[i]}.mp4", verbose=True) # change to false
            video.setProgres((i+1)//(mx+1)*100)
            video.log(f"Quality {arr[i]} proccessed")
            print(f"Quality {arr[i]} proccessed")
            print((i+1)/(mx+1)*100//1)

            setattr(video, f"video_{arr[i]}", f"{newFilepath}__{arr[i]}.mp4")
            video.save()
            


class SocketManager():
    def __init__(self) -> None:
        raise Exception("initialization baned")

    __connections = dict()

    @staticmethod
    def add_connection(connection, id: int):
        print(f"connection: {connection}, id - {id}")
        SocketManager.__connections[id] = connection

    @staticmethod
    def send_message_to_everyone(message):
        for i in SocketManager.__connections.values():
            i.sendMessage(message)
            print(i)
        print(f"{message} sended to everyone")








