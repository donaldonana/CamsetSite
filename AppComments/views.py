from django.shortcuts import render, redirect
from .models import Comment
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

from django.http import JsonResponse
from AppAuth.models import comments
from django.db.models import Sum, Count
import json
import itertools
import re
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.



@login_required
def index(request):

    comments_user = list(request.user.commentaires.get_queryset() )
    # comments_user = request.user.commentaires.all().values_list('id', flat=True)

    # comments_list = Comment.objects.get_queryset().exclude(id__in = comments_user ).order_by('id')
    comments = list(Comment.objects.get_queryset()  )
    comments_list = []


    for el in comments:
        if el not in comments_user:
            comments_list.append(el)
             


    random.shuffle(comments_list)
    paginator = Paginator(comments_list, 6)

  
    request.user.save()

    page = request.GET.get('page', 1)

    try:
        comments = paginator.page(page)
        nbr_page =  comments.paginator.num_pages - 1
    except PageNotAnInteger:
        comments = paginator.page(page)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    

     
    context = {'comments': comments, 'nbr_page' : nbr_page}
    context['user'] = request.user
    return render(request, 'AppComments/index.html', context)

 

def format(a):
    # url = re.sub('\.com$', '', url)
    b = a.removesuffix(']')     
    b = b.removeprefix('items[][')

    return b

def MAX(non_offensif, offensif, haineux):
    if non_offensif > offensif and non_offensif > haineux:
        return "normal"
    elif offensif > non_offensif and offensif > haineux :
        return "offensif"
    elif haineux > non_offensif and haineux > offensif:
        return "haineux"
    else:
        return ""

@login_required
def save(request):

    num = re.compile('[0-9]+')
    alpha = re.compile('[a-z]+')

    items = dict(request.GET.items())
    result = [dict((num.sub('', w[0]), w[1]) for z, w in v) for i, v in itertools.groupby(((alpha.sub('', k), (k, v)) for k, v in items.items()), lambda x: x[0])]
    final = [dict((format(a), b) for a, b in v.items()) for v in result ]
 
    for item in final:

        try:
            comment = Comment.objects.get(id = int(item["id"]))
        except Comment.DoesNotExist:
            pass

        if item["reponse"] == "furieux":
            comment.haineux = comment.haineux + 1 
        elif item["reponse"] == "offensif":
            comment.offensif = comment.offensif + 1 
        else :
            comment.non_offensif = comment.non_offensif + 1 
        vote = MAX( comment.non_offensif, comment.offensif , comment.haineux )
        comment.vote_final = vote

        comment.save()
        com_user = comments.objects.create(reponse=item["reponse"] , person = request.user, comment = comment)
        com_user.save()

 

    return JsonResponse({"data":"success"})


@login_required
def stats(request):

    # Comment.objects.values_list('haineux', flat=True)


    comments_list = Comment.objects.get_queryset().order_by('id')

    paginator = Paginator(comments_list, 6)

  
    request.user.save()

    page = request.GET.get('page', 1)

    try:
        comments = paginator.page(page)
        nbr_page =  comments.paginator.num_pages - 1
    except PageNotAnInteger:
        comments = paginator.page(page)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
 

    context = {'comments': comments, 'nbr_page' : nbr_page}
     

    var = Comment.objects.all().aggregate(Sum('haineux'))
    context['haineux__sum'] = var['haineux__sum']
    var = Comment.objects.all().aggregate(Sum('offensif'))
    context['offensif__sum'] = var['offensif__sum']
    var = Comment.objects.all().aggregate(Sum('non_offensif'))
    context['non_offensif__sum'] = var['non_offensif__sum']
    nbr_cat = Comment.objects.values('categorie').annotate(Count('categorie'))
    context['nbr_cat'] = len(nbr_cat)
    context['nbr_texte'] = len(comments_list)
    context['user_vote'] = len(request.user.commentaires.get_queryset())
    



    return render(request, 'AppComments/stats.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def admin(request):

    # if is_ajax(request=request):

        # filters = request.GET.get('filter')  
        # print(filters)


        # comments_list = Comment.objects.filter(texte__contains=filters).order_by('id')

    # else : 
    #     print("hellooooo world 2333333.")

    comments_list = Comment.objects.get_queryset().order_by('id')

    paginator = Paginator(comments_list, 10)

  
    request.user.save()

    page = request.GET.get('page', 1)

    try:
        comments = paginator.page(page)
        nbr_page =  comments.paginator.num_pages - 1
    except PageNotAnInteger:
        comments = paginator.page(page)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
 

    path =  os.path.join(BASE_DIR, 'staticfiles/JsonFiles') 

    dir_list = os.listdir(path) 
    dir_list_filters = []
    regex = re.compile(r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.+')
    for e in dir_list:
        if regex.search(e):
            pass
        else:
            dir_list_filters.append(e)
    context = {"comments" : comments, "dir_list" : dir_list_filters, 'nbr_page' : nbr_page}
    return render(request, 'AppComments/admin.html', context)

@login_required
def upload(request):

    file_name = request.GET.get('file_name', None)

    file_path =  os.path.join(BASE_DIR, 'staticfiles/JsonFiles/' + file_name)  

    try:
        with open(file_path , 'r', encoding="utf-8" ) as handle:
            parsed = json.load(handle)
        print(file_name)
        

    except Exception as e  :

        status = False
        message = "File not Found"
        print(e)
         
        return JsonResponse({"status":status, "message" : message})

 

    print("-----------begin-----")
    for texte in parsed["commentaires"]:
        try:
            c = Comment(categorie=parsed["categorie"] , post_titre = parsed["post_titre"], post_img = parsed["post_img"] , post_url = parsed["post_url"], texte = texte , file_name = file_name )

            c.save()
        except Exception as e:
            print("Maybe The Comment Alredy Exist")
    print("-----------successfuly end----------")
    status = True
    message = "successfuly add the file"

         
    return JsonResponse({"status":status, "message" : message})

@login_required
def DeleteAll(request):

    Comment.objects.all().delete()
    status = "successfuly delete all comments"
    return JsonResponse({"status":status})

@login_required
def delete(request):

    # ids = request.GET.getlist('ids[]')
    id = request.GET.get('id')  
    comment = Comment.objects.get(pk=int(id))
    comment.delete()


    return JsonResponse({"status":"success"})



def filtering(request, id):

    comment_list = Comment.objects.filter(texte__contains="femme")

    return render(request, 'AppComments/admin.html', context)
    


@login_required
def help(request):
 
    return render(request, 'AppComments/help.html') 