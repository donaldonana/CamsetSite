from django.shortcuts import render, redirect
from .models import Comment
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from AppAuth.models import comments
from django.db.models import Sum, Count
import json
import itertools
import re
import os


# Create your views here.



@login_required
def index(request):

    comments_user = request.user.commentaires.all().values_list('id', flat=True)
    comments_list = Comment.objects.get_queryset().exclude(id__in = comments_user ).order_by('?')

    paginator = Paginator(comments_list, 6)

  
    request.user.save()

    page = request.GET.get('page', 1)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(page)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

     
     
    context = {'comments': comments}
    context['user'] = request.user
    return render(request, 'AppComments/index.html', context)
    





@login_required
def create_todo(request):
    form = TodoForm()
    context = {'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo = Todo()

        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.owner = request.user
        todo.save()

        messages.add_message(request, messages.SUCCESS, "Todo created successfully"

                             )

        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))

    return render(request, 'todo/create-todo.html', context)

 
    return JsonResponse({"data":"success"})


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


    # empty = Comment.objects.none()

    # if non_offensif > offensif and non_offensif > haineux:
    #         comment.vote_final = "normal"
    #     elif offensif > non_offensif and offensif > haineux :
    #         comment.vote_final = "offensif"
    #     elif haineux > non_offensif and haineux > offensif:
    #         comment.vote_final = "haineux"


    # # print(request.user.temporaire.all())


    # for c in request.user.temporaire.all():

    #     if c.temp_haineux > 0 :
    #         c.haineux = c.haineux + c.temp_haineux
    #         com_user = comments.objects.create(reponse="haineux", person = request.user, comment = c)
    #         com_user.save()

    #     if c.temp_offensif > 0 :
    #         c.offensif = c.offensif + c.temp_offensif
    #         com_user = comments.objects.create(reponse="offensif", person = request.user, comment = c)
    #         com_user.save()


    #     if c.temp_non_offensif > 0 :
    #         c.non_offensif = c.non_offensif + c.temp_non_offensif
    #         com_user = comments.objects.create(reponse="normal", person = request.user, comment = c)
    #         com_user.save()

    #     c.temp_haineux = 0
    #     c.temp_offensif = 0
    #     c.temp_non_offensif = 0
    #     c.save()



    # request.user.temporaire.set(empty)   
    # request.user.save()

    # print("save ddddddddddddddddd")

    return JsonResponse({"data":"success"})


@login_required
def ListResult(request):

    # Comment.objects.values_list('haineux', flat=True)

    comments_list = Comment.objects.all()

     

    context = {'comments': comments_list}

    var = Comment.objects.all().aggregate(Sum('haineux'))
    context['haineux__sum'] = var['haineux__sum']
    var = Comment.objects.all().aggregate(Sum('offensif'))
    context['offensif__sum'] = var['offensif__sum']
    var = Comment.objects.all().aggregate(Sum('non_offensif'))
    context['non_offensif__sum'] = var['non_offensif__sum']
    nbr_cat = Comment.objects.values('categorie').annotate(Count('categorie'))
    context['nbr_cat'] = len(nbr_cat)
    context['nbr_texte'] = len(comments_list)
    



    return render(request, 'AppComments/ListResult.html', context)



@login_required
def admin(request):
    comments = Comment.objects.all()
    path = "./Camset/static/jsonFiles"

    dir_list = os.listdir(path) 
    context = {"comments" : comments, "dir_list" : dir_list}
    return render(request, 'AppComments/admin.html', context)


def upload(request):

    file_name = request.GET.get('file_name', None)

    file_path =  "./Camset/static/jsonFiles/" + file_name

    try:
        with open(file_path , 'r', encoding='latin-1' ) as handle:
            parsed = json.load(handle)
        print(file_name)
        

    except  :

        status = False
        message = "File not Found"
         
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


def DeleteAll(request):

    Comment.objects.all().delete()
    status = "successfuly delete all comments"
    return JsonResponse({"status":status})


def delete(request):

    ids = request.GET.getlist('ids[]')

    print(ids)

    for id in ids :
        comment = Comment.objects.get(pk=id)
        comment.delete()


    return JsonResponse({"status":"success"})

    