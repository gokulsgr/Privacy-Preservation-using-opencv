

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm,ImageUploadForm

from django.core.files.storage import FileSystemStorage

import cv2, os
import numpy as np
from PIL import Image
from .models import posts,imagesmodel

def home(request):

	return render(request,'siteapp/home.html')

def profile(request):
    temp=User.objects.filter(username=request.user.username)
    userobj=temp[0]
    context={
    'userobj':userobj
    }
    return render(request,'siteapp/profile.html',context)
subjects=["","krish","bala"]
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            first_name = userObj['first_name']
            last_name=  userObj['last_name']
            
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user( userObj['username'], first_name=userObj['first_name'],last_name=userObj['last_name'], password=userObj['password'], email=userObj['email'])
                user = authenticate(username = username, password = password)
                subjects.append(username)
                stri=str(subjects.index(username))  
                stri="C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/s"+stri  
                if os.path.isdir(stri)==False:  
                    os.mkdir(stri)
                login(request, user)
                return HttpResponseRedirect('/feed')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'siteapp/signup.html', {'form' : form})




cascadePath = "C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/opencv-files/lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
    
# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.face.LBPHFaceRecognizer_create()



def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    dirs = os.listdir(path)
    print(dirs)
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue;
        label = int(dir_name.replace("s", ""))
        subject_dir_path = path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue;
            image_path = subject_dir_path + "/" + image_name
            print(image_path)
            image_pil = Image.open(image_path).convert('L')

            image = np.array(image_pil, 'uint8')

        # Get the label of the image
            nbr = int(dir_name.replace("s", ""))
        # Detect the face in the image
         
            faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
            for (x, y, w, h) in faces:
                images.append(image[y: y + h, x: x + w])
                labels.append(nbr)
            
    # return the images list and labels list
    return images, labels




def post(request):
    username = None
    username = request.user.username
    string=str(subjects.index(username))
    # feedpath="C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/s"+string
    # image_names = os.listdir(feedpath)
    # imagelist=[]
    # for image_name in image_names:
    #         if image_name.startswith("."):
    #             continue;
    #         image_name1="s"+string+"/"+image_name
    #         imagelist.append(image_name1)
    imgobj=imagesmodel.objects.filter(uname=username).order_by('-created')
    
    context={
    'images':imgobj,
    'stringnum':string,

    }
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        print(type(myfile))
        

       
        location='C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/test'
        fs = FileSystemStorage(location=location)
        filename = fs.save(myfile.name, myfile)
        filenme=myfile.name
        uploaded_file_url = fs.url(filename)
        images, labels = get_images_and_labels("C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static")
        print("Total faces: ", len(images))
        print("Total labels: ", len(labels))
        recognizer.train(images, np.array(labels))
        temp_url="C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/test/"+uploaded_file_url
        predict_image_pil = Image.open(temp_url).convert('L')
        predict_image = np.array(predict_image_pil, 'uint8')
        faces = faceCascade.detectMultiScale(predict_image)
        print(type(faces))
        message=None
        noface=False
        nbr_predicted=None
        predicted_name=None
        predicted_array=[]
        if type(faces) is np.ndarray:
            for (x, y, w, h) in faces:
                nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
                
                predicted_name=subjects[nbr_predicted]
                predicted_array.append(predicted_name)
                print(conf)
        else:
            noface=True
        print(username)
        print(predicted_name)
        print(noface)
        location='C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/s'+string
        if noface:
            fs = FileSystemStorage(location=location)
            fs.save(myfile.name, myfile)
            message="Successfully posted"
            imgob=imagesmodel()
            imgob.image=filenme
            imgob.uname=username
            imgob.save()
        elif(len(predicted_array)==1 and predicted_array[0]== username):
            fs = FileSystemStorage(location=location)
            fs.save(myfile.name, myfile)
            message="Successfully posted"
            imgob=imagesmodel()
            imgob.image=filenme
            imgob.uname=username
            imgob.save()
        else:
            for predicted_name in predicted_array:
                if predicted_name != username:
                    message="Looks like you are trying to add a photo "+predicted_name+" in . Sent request to the concern user.Please wait for the approval"
                    obj = posts() #gets new object
                    obj.fromuser= username
                    obj.touser = predicted_name
                    obj.message = username+" is trying to post a photo you might be in"
                    obj.permission = False
                    obj.image=temp_url
                    obj.location=subjects.index(username)
                    obj.typeof="req"
                    obj.testimageloc=uploaded_file_url
                    obj.save()




        
        context={
        'images':imgobj,
        'stringnum':string,
        'uploaded_file_url': uploaded_file_url,
        'message':message
        }
        return render(request, 'siteapp/feed.html',context)
    return render(request, 'siteapp/feed.html',context)


def notification(request):
    username = request.user.username
    queryset=posts.objects.filter(touser=username)
    if request.method == 'POST':
        idval=list(request.POST.keys())[1]
        temp=posts.objects.filter(id=idval)    
        tempobj=temp[0]
        if(tempobj.typeof=="req"):
            sendobj = posts()
            sendobj.fromuser= username
            sendobj.touser = tempobj.fromuser
            sendobj.message = "Status updated with "+username+"'s permission"
            sendobj.permission =False
            sendobj.location="/"
            sendobj.typeof="ack"
            sendobj.image=tempobj.image
            sendobj.testimageloc=tempobj.testimageloc
            sstring="C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/test/"+tempobj.testimageloc
            print(sstring)
            imagefile=cv2.imread(sstring)
            open_cv_image = imagefile
            print(open_cv_image)
            path="C:/Users/rajgoku/Desktop/python pro/privacy/siteapp/static/s"+tempobj.location
            cv2.imwrite(os.path.join(path , tempobj.testimageloc), open_cv_image)
            sendobj.save()
            imgobj=imagesmodel()
            imgobj.image=tempobj.testimageloc
            imgobj.uname=tempobj.fromuser
            imgobj.save()
            tempobj.delete()
        else:
            tempobj.delete()





    context={
    'posts':queryset
    }
    return render(request, 'siteapp/notification.html',context)
    
# def feed(request):

#     image_names = os.listdir(path)
#     imagelist=[]
#     for image_name in image_names:
#             if image_name.startswith("."):
#                 continue;
#             image_name1="s"+string+"/"+image_name
#             imagelist.append(image_name1)
#     print(imagelist)
#     context={
#     'images':imagelist
#     }

#     return render(request, 'siteapp/feed.html',context)