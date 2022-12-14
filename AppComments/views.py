from django.shortcuts import render, redirect
from .models import Comment
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from AppAuth.models import User
from django.http import JsonResponse
from AppAuth.models import comments
from django.db.models import Sum, Count
import json
import itertools
import re
from pathlib import Path
import os
from django.db.models import Q
from django.db.models import BigAutoField
import pymongo
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.
# 3.12.3
def getdb():
    url = "mongodb+srv://donaldonana:nanojunior92@cluster0.clm4i.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(url)
    db = client.Camset
    return db

@login_required
def index(request):

    # comments_user = list(request.user.commentaires.get_queryset() )

    db = getdb()
    comment_user = [id for id in db.AppAuth_comments.find({"person_id" : request.user.id}).distinct('comment_id')]


    
    comments_list = db.AppComments_comment.aggregate(
   [ {"$match": {"id" : { '$nin':comment_user } , "totaux_votes": { '$lt': 7 } }} , { '$sample': { 'size': 9 } } 
   ])

    context = {'comments': comments_list }
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
    elif offensif >= non_offensif and offensif > haineux :
        return "offensif"
    elif haineux >= non_offensif and haineux >= offensif:
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
        comment.totaux_votes = comment.totaux_votes + 1
        request.user.vote = request.user.vote + 1

         

        comment.save()
        com_user = comments.objects.create(reponse=item["reponse"] , person = request.user, comment = comment)
        com_user.save()
           
        request.user.save()


 

    return JsonResponse({"data":"success"})


@login_required
def stats(request):

    db = getdb()


    comments_list = Comment.objects.all().order_by('id')
     
    Users = User.objects.all().order_by('-vote')


    per_page = 5
    # Paginator in a view function to paginate a queryset
    # show 4 news per page
    obj_paginator = Paginator(Users, per_page)
    # list of objects on first page
    users = obj_paginator.page(1).object_list
    # range iterator of page numbers
    page_range = obj_paginator.page_range

    nbr_page_user = obj_paginator.page(1).paginator.num_pages


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
 

    context = {'comments': comments_list, 
    'nbr_page' : nbr_page, 
    'users' : users, 
    'page_range' : page_range,
    'nbr_page_user' : nbr_page_user}
     

    context['haineux__sum'] = db.AppComments_comment.count_documents({"vote_final" : "haineux"})
    context['offensif__sum'] = db.AppComments_comment.count_documents({"vote_final" : "offensif"})
    context['non_offensif__sum'] = db.AppComments_comment.count_documents({"vote_final" : "normal"})
    context['nbr_cat'] = len(db.AppComments_comment.distinct("categorie"))
    context['nbr_texte'] = db.AppComments_comment.count_documents({})

    print("tttt")



    



    return render(request, 'AppComments/stats.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def admin(request):

     
    comments = list(Comment.objects.filter(totaux_votes__lt=40).order_by('-id')[:100])




    paginator = Paginator(comments, 15)
    page_range = paginator.page_range

  

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
    context = {"comments" : comments, 
    "dir_list" : dir_list_filters, 
    'nbr_page' : nbr_page,
    'page_range' : page_range}
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
    i = 0
    for texte in parsed["commentaires"]:
        try:
            c = Comment(categorie=parsed["categorie"] , post_titre = parsed["post_titre"], post_img = parsed["post_img"] , post_url = parsed["post_url"], texte = texte , file_name = file_name )

            c.save()
        except Exception as e:
            print("Maybe The Comment Alredy Exist")
        print(i)
        i = i + 1
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


@login_required
def StatsPagination(request):

    per_page = 5


    page_no = int(request.GET.get('page_no'))  
    current_page = int(request.GET.get('current_page'))  
    numItems = int(request.GET.get('numItems')) 
    lastNum =  int(request.GET.get('lastNum'))

    ecart = abs(page_no - current_page) 

    if numItems < per_page:
        lastNum = lastNum + (per_page - numItems)

    if page_no < current_page:
        index = lastNum - ecart*per_page

    if page_no > current_page:
        index = lastNum + ecart*per_page

    index = index - (per_page - 1)



    Users = User.objects.get_queryset().order_by('-vote')
    # Paginator in a view function to paginate a queryset
    # show 4 news per page
    obj_paginator = Paginator(Users, per_page)
    # list of objects on first page
    results = list(obj_paginator.page(page_no).object_list.values('email', 'username', 'vote'))

    for el in results:
        el["index"] = index
        index = index + 1
     
 
    # print(numItems)
    


    return JsonResponse({"results":results , "status":"success"})



 
# @login_required
# def finduser(request):

     
#     Users = User.objects.get_queryset().order_by('-vote')
#     # Paginator in a view function to paginate a queryset
#     # show 4 news per page
#     obj_paginator = Paginator(Users, per_page)
#     # list of objects on first page
#     user_list = list(obj_paginator.page(page_no).object_list.values('email', 'username', 'vote'))

#     for user in user_list:
#         el["index"] = index
#         index = index + 1
     
 
#     # print(numItems)
    


#     return JsonResponse({"results":results , "status":"success"})



 
#   