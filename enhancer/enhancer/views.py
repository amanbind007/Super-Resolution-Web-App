from webbrowser import get
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from users.forms import InputImageForm
from django.contrib import messages
from PIL import Image, ImageEnhance
import os
import cv2
from cv2 import dnn_superres
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def home(request):
    if request.method == "POST":
        im_form = InputImageForm(request.POST,request.FILES, instance=request.user.profile)
        if im_form.is_valid():
            current_user = request.user
            if current_user.profile.premium == True or current_user.profile.trials != 0:
                current_user.profile.trials = current_user.profile.trials - 1
                im_form.save()
                return redirect('enhancer-ai_app')
            else:
                messages.warning(request, f'Your free membership is expired. Please purchase to continue using AI Image Enhancer')
                return redirect('enhancer-home')
    im_form = InputImageForm()
    context = {
        'title':'Home',
        'im_form':im_form,
    }
    return render(request, 'enhancer/home.html', context)

@login_required(login_url='/login/')
def ai_app(request):
    if request.method == 'POST' and 'to_upscale' in request.POST:
        getMethod = request.POST['inlineRadioOptions']
        upscaleFactor = request.POST['theOptions']
        img_path = os.getcwd()+request.user.profile.image.url
        img_path = img_path.replace('\\', '/')
        img = Image.open(img_path)
        my_scale(img, request, getMethod, upscaleFactor)
        request.user.profile.save()
        return redirect('enhancer-result')
    return render(request, 'enhancer/ai_app.html', {'title':'Workspace'})

@login_required(login_url='/login/')
def result(request):
    if request.method == 'POST':
        save_path = os.getcwd()+'/media/converted/conv.jpg'
        save_path = save_path.replace('\\', '/')
        filename = 'conv.jpg'
        im = Image.open(save_path)
        response = HttpResponse(mimetype='image/jpg')
        response['Content-Disposition'] = 'attachment; filename=%s.png' % filename
        im.save(response, 'jpg')
    return render(request, 'enhancer/result.html', {'title':'Result'})


def aboutus(request):
    return render(request, 'enhancer/aboutus.html', {'title':'About Us'})

def first(request):
    return render(request, 'enhancer/first.html', {'title':'Welcome'})


def my_scale(img, request, getMethod, upscaleFactor):
    sr = dnn_superres.DnnSuperResImpl_create()
    temp_path = os.getcwd()+ request.user.profile.image.url
    temp_path = temp_path.replace('\\', '/')

    image = cv2.imread(temp_path)
    print(temp_path)
    

    path = selectModel(getMethod, upscaleFactor)
    
    sr.readModel(path)

    sr.setModel(getMethod, int(upscaleFactor))

    result = sr.upsample(image)
    save_path = os.getcwd()+'/media/converted/conv.jpg'
    save_path = save_path.replace('\\', '/')
    
    cv2.imwrite("media/converted/conv.jpg", result)
    request.user.profile.image = save_path


def selectModel(getMethod, upscaleFactor):
    if getMethod == 'edsr' and upscaleFactor == '2':
        return 'model/EDSR_x2.pb'
    elif getMethod == 'edsr' and upscaleFactor == '3':
        return 'model/EDSR_x3.pb'
    elif getMethod == 'edsr' and upscaleFactor == '4':
        return 'model/EDSR_x4.pb'

    
    if getMethod == 'espcn' and upscaleFactor == '2':
        return "model/ESPCN_x2.pb"
    elif getMethod == 'espcn' and upscaleFactor == '3':
        return "model/ESPCN_x3.pb"
    elif getMethod == 'espcn' and upscaleFactor == '4':
        return "model/ESPCN_x4.pb"
    
    if getMethod == 'fsrcnn' and upscaleFactor == '2':
        return "model/FSRCNN_x2.pb"
    elif getMethod == 'fsrcnn' and upscaleFactor == '3':
        return "model/FSRCNN_x3.pb"
    elif getMethod == 'fsrcnn' and upscaleFactor == '4':
        return "model/FSRCNN_x4.pb"
    
    if getMethod == 'lapsrn' and upscaleFactor == '2':
        return "model/LapSRN_x2.pb"
    elif getMethod == 'lapsrn' and upscaleFactor == '4':
        return "model/LapSRN_x4.pb"
    elif getMethod == 'lapsrn' and upscaleFactor == '8':
        return "model/LapSRN_x8.pb"