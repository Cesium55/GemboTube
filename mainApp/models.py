from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from random import randint
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.cache import cache


# Create your models here.

class User(models.Model):

    alf = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890 йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ_-.,@$'



    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    password = models.CharField(max_length=254, verbose_name="Password")

    nickname = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, blank=True, null = True, unique=True)
    avatar = models.ImageField(upload_to ='media/%Y/%m/%d/', max_length=100, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["PNG", "JPEG", "JPG", "BMP", "webp"])])

    activated = models.BooleanField(default=False)

    def __str__(self):
        return  f"[{self.id}] {self.email} - {self.nickname}"
    
    def getAvatarUrl(self):
        if self.avatar:
            return self.avatar.url
        return "/static/img/defaultAvatar.jpg"

    
    

    @staticmethod
    def validateUser(email, password):

        if not(email and password):
            return None

        try:
            u = User.objects.get(email=email)
            if (password == u.password) or (check_password(password, u.password)):
                print(f"Model validate: pass == u pass : {password == u.password} ----- check pass: {check_password(password, u.password)}")
                return u
        except:
            ...
        return None
        
    

    class AuthInfo:

        def __init__(self, result: bool, errors=[]):
            self.__result = result
            self.__errors = errors
        
        def isSuccesful(self):
            return self.__result
        def getErrors(self):
            return self.__errors
        def __str__(self) -> str:
            return f"{self.isSuccesful()} --- errors: {self.getErrors()}"


    @staticmethod
    def register(data_dict):
        email = data_dict.get("email")
        password = data_dict.get("password")
        password2 = data_dict.get("passwordConf")

        nick = data_dict.get("nickname")

        if (email and password and nick and password2):

            try:
                u = User.objects.get(email=email)
                print(u)
            except:
                try:
                    if len(password)<6:
                        return User.AuthInfo(False, ["password length must be >= 6"])
                    if password != password2:
                        return User.AuthInfo(False, ["passwords are not equal"])
                    if not all(i in User.alf for i in nick):
                        return User.AuthInfo(False, ["Incorrect nickname symbols"])
                    u = User(email=email, nickname=nick, password = make_password(password))
                    u.save()
                    return User.AuthInfo(True, [])
                except Exception as ex:
                    print(ex)
                    return User.AuthInfo(False, ["Error while creating"])
            else:
                return User.AuthInfo(False, ["User with such email already exists"])
        else:
            return User.AuthInfo(False, ["Invalid form"])
        

    @staticmethod
    def authUser(request):

        try:
            u = User.objects.get(id=request.session.get("userID"))
            return u
        except:
            return False
    
    def getPublicData(self):
        return {
            "nickname":self.nickname, 
            "avatar":self.getAvatarUrl(),
            "notActivated" : not self.activated
            }

    @staticmethod
    def getChannel(slugname):
        channel = cache.get(f'channel_{slugname}')
        if not channel:
            channel = User.objects.get(slug=slugname)
            cache.set(f'channel_{slugname}', channel, timeout=3600)
        return channel
    @staticmethod
    def AuthBySession(session):
        try:
            u = User.objects.get(id=session.get("userID"))
            return u
        except:
            return False

    def getFollowings(self):
        return list(Following.objects.filter(source=self))



    # def createRegistrationCode(self):
    #     code = VerificationCode(
    #         user = self,
    #         code = "666666",
    #         completed = False,
    #         codeType = "Reg"
    #     )
    



class VerificationCode(models.Model):
    codeTypes = (
        ('Reg', 'Reg'),
        ('Inf', 'Inf'),
        ('Restore', 'Restore'),
        ('Test', 'Test')
    )



    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    lastCreated = models.DateTimeField(default=timezone.now)
    codeType = models.CharField(max_length=20, choices=codeTypes)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.expires = datetime.now() + timedelta(days=1)
        

    def __str__(self):
        return f"{self.user.nickname}: {self.code} - {self.created}"


    def updateCode(self, code: str):
        self.code = code
        self.lastCreated = datetime.now()
        self.save()


    def getTimeDelta(self):

        tm = 60 - (timezone.now() - self.lastCreated).total_seconds()

        return tm if tm > 0 else 0
    
    def isDeltaMinute(self):
        return timezone.now() - self.lastCreated > timedelta(minutes=1)
    

    def checkCode(self, code):
        return self.code == code


class VideoTest(models.Model):
    video = models.FileField(upload_to='videos_uploaded',null=True, 
                                validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])



    def __str__(self) -> str:
        return f"video - {self.id}"




class Video(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length = 500)

    description = models.TextField(default="", blank=True)

    pubDT = models.DateField(null=True, blank=True)

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    published = models.BooleanField(default=True, verbose_name="Public")
    

    proccessed = models.IntegerField(default=0)
    
    @staticmethod
    def getUploadPath(video, filename):
        return f'media/viedos/{video.author.id or "0"}/%Y/%m/%d/'

    @staticmethod
    def get_video_by_id(video_id):
        
        video = cache.get(f'video_{video_id}')
        
        if not video:
            
            video = Video.objects.get(id=video_id)

            print("video taken from db")
            
            cache.set(f'video_{video_id}', video, timeout=1)
        else:
            print("video taken from cache")
        print(video.description)
        
        return video
    


    thumbImage = models.ImageField(upload_to="media/thumbs/%Y/%m/%d/", null=True, blank=True)

    originalVideo = models.FileField(
        upload_to = 'media/videos/%Y/%m/%d/', 
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])], blank=True)

    video_240 = models.FileField(null=True, blank=True, upload_to='media/videos/%Y/%m/%d')
    video_360 = models.FileField(null=True, blank=True, upload_to='media/videos/%Y/%m/%d')
    video_480 = models.FileField(null=True, blank=True, upload_to='media/videos/%Y/%m/%d')
    video_720 = models.FileField(null=True, blank=True, upload_to='media/videos/%Y/%m/%d')
    video_1080 = models.FileField(null=True, blank=True, upload_to='media/videos/%Y/%m/%d')
    video_1440 = models.FileField(null=True, blank=True, upload_to='media/videos/%Y/%m/%d')
    video_2160 = models.FileField(null=True, blank=True, upload_to='media/videos/%Y/%m/%d')

    logs = models.TextField(null=True, blank=True, default = "")


    def log(self, string: str):
        self.logs += string + "\n"
        self.save()
    def setProgres(self, p):
        self.proccessed = p

    def getShortPublicData(self):
        return {
            "thumbURL": self.thumbImage.url,
            "id": self.id,
            "title": self.title,
            "authorName": self.author.nickname,
            "views": self.views
        }

    def __str__(self):
        return self.title

    @staticmethod
    def get_videos_by_author_id(id):
        return Video.objects.filter(author = User.objects.get(id=id))


class TempVideo(models.Model):

    add_time = models.DateTimeField(auto_now=True, blank=True, null = True)
    video = models.FileField(
        upload_to = 'media/videos/%Y/%m/%d/', 
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    completeStatus = models.BooleanField(default=False, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    




class Like(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Video, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.nickname} --> {self.destination.title}"


class Dislike(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Video, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.nickname} --> {self.destination.title}"


class Comment(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Video, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.source.nickname} --> {self.destination.title} - {self.text}"



class VideoView(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Video, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.nickname} --> {self.destination.title}"


class Following(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destionation")
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.nickname} --> {self.destination.title}"




