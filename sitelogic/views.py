import random
import zoneinfo
from datetime import datetime

import pytz
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from functools import wraps
from django.db import transaction
from django.utils import timezone

from .forms import PostForm, CommentPostForm, CommentReplyForm
from .models import *


def get_client_timezone(request):
    if 'timezone' in request.COOKIES:
        print('ЧАСОВОЙ ПОЯС НАЙДЕН')
        print('КУКИ ТАЙМЗОН', request.COOKIES.get('timezone'))
        print('ПРОСТО КУКИ 1', request.COOKIES)
        print('МЕТОД', pytz.timezone(request.COOKIES['timezone']))
        return pytz.timezone(request.COOKIES['timezone'])
    else:
        return timezone.get_current_timezone()


def get_ip(request):
    proxy_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if proxy_ip:
        real_ip = proxy_ip.split(',')[0]
    else:
        real_ip = request.META.get('REMOTE_ADDR')
    return real_ip


# def counted(f):
#     def decorator(request, *args, **kwargs):
#         counter = PostViews.objects.get()
#         counter.count += 1
#         counter.save()
#         return f(request, *args, **kwargs)
#
#     return decorator
#
#
# def countedtwo(f):
#     @wraps(f)
#     def decorator(request, *args, **kwargs):
#         with transaction.atomic():
#             counter, created = PostViews.objects.get_or_create(url=request.path)
#             counter.count = F('count') + 1
#             counter.save()
#         return f(request, *args, **kwargs)
#
#     return decorator

# def counted(f):
#     @wraps(f)
#     def decorator(request, *args, **kwargs):
#         with transaction.atomic():
#             counter, created = Hit.objects.get_or_create(url=request.path)
#             counter.count = F('count') + 1
#             counter.save()
#         return f(request, *args, **kwargs)
#     return decorator

# def views_increase(f):
#     def wrapped(request, *args, **kwargs):
#         counts = Post.objects.all()
#         counts.views_count += 1
#         counts.save()
#         return f(request, *args, **kwargs)
#     return views_increase


def homepage(request):
    content = Post.objects.all()
    # timee = Post.objects.values('post_time_create')
    # current_timezone = timezone.get_current_timezone()
    # my_datetime = Post.objects.first().post_time_create
    # my_datetime = current_timezone.localize(my_datetime)
    # my_datetimee = datetime.now()
    # target_timezone = zoneinfo.ZoneInfo('Europe/Moscow')
    # my_datetime = my_datetime.astimezone(target_timezone)
    # my_time = my_datetime.strftime('%H:%M:%S')
    random_content_one = Post.objects.order_by("?")[:30]
    content_popular = Post.objects.order_by("-views_count")
    search_query = request.GET.get('search', '')
    cats = PostCategory.objects.all()
    form = PostForm()
    # post_views = Hit.objects.all()
    # tz = request.META.get('TZ', None)
    # tzc = request.COOKIES.get('timezone', None)
    # moscow_tz = pytz.timezone('Europe/Moscow')
    client_tz = get_client_timezone(request)

    if search_query:
        random_content_one = Post.objects.filter(
            Q(post_title__icontains=search_query) | Q(post_content__icontains=search_query)).order_by(
            "-post_time_create")
    else:
        random_content_one = Post.objects.order_by("?")[:30]

    # print('TIMEE TIME', timee)
    # print('UNKNOWN METHOD', my_datetime)
    # print('UNKNOWN METHOD BUT EVOLVED', my_datetime)
    # print('MOSCOW TIME', my_time)
    # if request.method == "POST":
    #     if 'pop' in request.POST:
    #         print('ТУТ ПОСТ РЕКВЕСТ ТУТ ПОСТ РЕКВЕСТ ТУТ ПОСТ РЕКВЕСТ ТУТ ПОСТ РЕКВЕСТ ТУТ ПОСТ РЕКВЕСТ')
    #         return redirect('http://127.0.0.1:8000/post/kak-vy-otsenite-interstellar13636798391647678924135418102955015715-/')

    # for zx in content:
    #     zx.post_time_create = timezone.localtime(zx.post_time_create)

    context = {
        'content': content,
        'content_popular': content_popular,
        'random_content_one': random_content_one,
        'cats': cats,
        'cat_selected': 0,
        'form': form,
        'client_tz': client_tz,
        # 'post_views': post_views,
    }

    # for dd in context:
    #     print('ДИКТ', dd)
    # for jj in content:
    #     jj.post_time_create.replace(tzinfo=pytz.utc).astimezone(moscow_tz)
    #     print('САМОЕ СУПЕР ЛОКАЛЬНОЕ ВРЕМЯ В МИРЕ')
    #     # print('ЛОКАЛТАЙМ 1', timezone.localtime(jj.post_time_create))
    # if tz:
    #     timezone.activate(pytz.timezone(tz))
    #     print('ВРЕМЕННАЯ ЗОНА', tz)
    # print('TIME ZONE COOCKIE', tzc)
    # for a in content:
    #     print('САМОЕ СУПЕР ЛОКАЛЬНОЕ ВРЕМЯ В МИРЕ', a.post_time_create)
    #
    # print('ОСКОВСКОЕ ВРЕМЯ', moscow_tz, type(moscow_tz))

    print(client_tz)

    return render(request, 'sitelogic/base.html', context=context)


class About(APIView):
    def get(self, request):
        return render(request, 'sitelogic/about.html')


# @views_increase
def ShowPost(request, post_title_slug):
    # tzname = request.session.get('django_timezone')
    # if tzname:
    #     timezone.activate(pytz.timezone(tzname))
    # else:
    #     timezone.deactivate()
    cats = PostCategory.objects.all()
    post = get_object_or_404(Post, post_slug=post_title_slug)
    # c = post.post_comment
    search_query = request.GET.get('search', '')
    comments = Comment.objects.filter(post_comment=post, parent=None)
    form = CommentPostForm
    reply_form = CommentReplyForm
    ck = request.COOKIES

    ip = get_ip(request)

    # if UserIp.objects.filter(IP=ip):
    #     post.viewed_ip.add(UserIp.objects.get(IP=ip))
    # else:
    #     UserIp.objects.create(IP=ip)
    #     post.viewed_ip.add(UserIp.objects.get(IP=ip))

    # if request.method == 'GET':
    #     ip_address = request.META.get('REMOTE_ADDR')
    #     if ip_address not in post.views_by_ip:
    #         post.views_by_ip.append(ip_address)
    #         post.cviews += 1
    #         post.save()

    # ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    # if ip_address not in post.views.all():
    #     post.views.add(ip_address)
    #     post.views_count += 1
    #     post.save()

    viewed_post = UserIp.objects.filter(post=post, IP=ip)
    ip_address = request.META.get('REMOTE_ADDR')
    # tr = Post.objects.filter(post_comment=c)

    if not viewed_post:
        post.views_count += 1
        post.save()
        viewed_post = UserIp(post=post, IP=ip)
        viewed_post.save()

    context = {
        'cats': cats,
        'post': post,
        'title': post.post_title,
        'cat_selected': post.cat_id,
        'comments': comments,
        'form': form,
        'reply_form': reply_form,
        'local_time': timezone.localtime(post.post_time_create),
    }

    if request.method == "POST":
        # if 'add_comm' in request.POST:
        request_keep = CommentPostForm(request.POST)
        # print("CLEANED DATA0", request_keep)
        if request_keep.is_valid():
            # if not Comment.objects.filter(comment_content=request_keep.cleaned_data['comment_content']).exists():
            print("ЧИСТАЯ ДАТА ЧИСТАЯ ДАТА ЧИСТАЯ ДАТА", request_keep.cleaned_data)
            print("ВРЕМЯ ВРЕМЯ ВРЕМЯ", Comment)
            # print("CLEANED DATA1", request_keep.cleaned_data)
            print("CLEANED DATA2", request_keep.cleaned_data['comment_content'])
            print("CLEANED\n", request_keep)
            # content_data = request_keep.cleaned_data.get('comment_content')
            # uuid_data = request_keep.cleaned_data.get('uuid')
            # relate = request_keep.cleaned_data.get('post_comment')
            parent_obj = None
            try:
                parent_id = int(request.POST.get('pa'))
                print('PARENT ID PARENT ID PARENT ID PARENT ID PARENT ID PARENT ID', parent_id)
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.get(id=parent_id)
                print('PARENT QS PARENT QS PARENT QS PARENT QS PARENT QS PARENT QS', parent_qs)
                parent_obj = parent_qs
                print('PARENT OBJ PARENT OBJ PARENT OBJ PARENT OBJ PARENT OBJ', parent_obj)

            comment = request_keep.save(commit=False)
            print('comment create 1', comment.comment_create)
            comment.post_comment = post
            print('comment create 2', comment.comment_create)
            comment.parent = parent_obj
            print('comment create 3', comment.comment_create)
            comment.save()
            comment_create_str = str(comment.comment_create)[:19]
            last_comment = Comment.objects.filter().order_by('-id')[1]
            last_comment_create = str(last_comment.comment_create)[:19]
            # last_com = Comment.objects.latest('id')
            # last_co = Comment.objects.all()
            # last_c = Comment.objects.filter()
            # print('Последняя запись такая : ', last_comm, 'Время последней записи: ', last_comm.comment_create)
            # # print('Эта запись такая: ', comment, 'Время этой записи: ', comment.comment_create)
            # print('Текущая запись: ', comment, 'Время текущей записи: ', comment_create_str)
            # print('ВРЕМЯ', last_comm_cc)
            # print('последняя запись такая2: \n', last_com)
            # print('последняя запись такая3: \n', last_co)
            # print('последняя запись такая4: \n', last_c)
            # if '+' in str_cc:
            #     print('есть стринговый плюс', str_cc)
            #     str_cc = str_cc.replace('+', '').replace(' ', '').replace('-', '').replace('.', '').replace(':', '')
            #     print('уже нету стринового плюса', str_cc)
            # print("ПОСТ БЫЛ СОЗДАН", comment.comment_create)
            if last_comment_create == comment_create_str and last_comment.comment_content == comment.comment_content:
                print('Есть одинаковые записи')
                print('Последняя запись: ', last_comment, 'Тип последний записи: ', type(last_comment), 'Время создания последней записи: ', last_comment_create)
                print('Текущая запись: ', comment, 'Тип текущей записи: ', type(comment), 'Время создания текущей записи: ', comment_create_str)
            else:
                print('Одинаковых записей нет')
            # else:
            #     return redirect('https://www.youtube.com/')

            # new_comment, created = Comment.objects.get_or_create(
            #     uuid=uuid_data,
            #     comment_content=content_data,
            #     post_comment=relate,
            #     parent=parent_obj,
            # )
        return redirect(request.path_info)
        return render(request, 'sitelogic/showpost.html', context={'form': request_keep})
    # if 'add_rep' in request.POST:
    #     request_keep = CommentReplyForm(request.POST)
    #     if request_keep.is_valid():
    #         # parent_comment_id = request_keep.cleaned_data['parent_comment']
    #         # parent_comment = Comment.objects.get(id=parent_comment_id)
    #         # reply_content = request.cleaned_data['reply_content']
    #         # reply = CommentReply.objects.create(parent_comment=parent_comment, reply_content=reply_content)
    #         comment_reply = request_keep
    #
    #         # comment_reply.parent_comment = parent_comment
    #         comment_reply.save()
    #
    #         return redirect(request.path_info)
    #     return render(request, 'sitelogic/showpost.html', context={'form': request_keep})

    if search_query:
        return redirect('http://127.0.0.1:8000/', random_content_one=Post.objects.filter(
            Q(post_title__icontains=search_query) | Q(post_content__icontains=search_query)).order_by(
            "-post_time_create"))
    else:
        random_content_one = Post.objects.order_by("?")[:30]

    # print(c)
    print(ck)

    return render(request, 'sitelogic/showpost.html', context=context)


def showpopularposts(request):
    content_popular = Post.objects.order_by("-views_count")

    context = {
        'content_popular': content_popular,
    }

    return render(request, 'sitelogic/showpopularposts.html', context=context)


class ShowCategory(APIView):

    def get(self, request, cat_slug):

        content = Post.objects.all()
        random_content_one = Post.objects.order_by("?")[:3]
        cats = PostCategory.objects.all()

        if 'pop' in request.GET:

            posts = Post.objects.filter(cat__slug=cat_slug).order_by('-views_count')
            context = {
                'content': content,
                'random_content_one': random_content_one,
                'posts': posts,
                'cats': cats,
                'cat_selected': cat_slug,
            }
            return render(request, 'sitelogic/showcat.html', context=context)
        elif 'def' in request.GET:

            posts = Post.objects.filter(cat__slug=cat_slug).order_by('views_count')
            context = {
                'content': content,
                'random_content_one': random_content_one,
                'posts': posts,
                'cats': cats,
                'cat_selected': cat_slug,
            }
            return render(request, 'sitelogic/showcat.html', context=context)

        content = Post.objects.all()
        random_content_one = Post.objects.order_by("?")[:3]
        posts = Post.objects.filter(cat__slug=cat_slug).order_by('views_count')
        cats = PostCategory.objects.all()
        context = {
            'content': content,
            'random_content_one': random_content_one,
            'posts': posts,
            'cats': cats,
            'cat_selected': cat_slug,
        }
        return render(request, 'sitelogic/showcat.html', context=context)


class Cabinet(APIView):

    def get(self, request):
        return render(request, 'sitelogic/cabinet.html')


class FormAdd(View):

    def get(self, request):
        search_query = request.GET.get('search', '')
        form = PostForm

        if search_query:
            return redirect('http://127.0.0.1:8000/', random_content_one=Post.objects.filter(
                Q(post_title__icontains=search_query) | Q(post_content__icontains=search_query)).order_by(
                "-post_time_create"))
        else:
            random_content_one = Post.objects.order_by("?")[:30]

        return render(request, 'sitelogic/addpost.html', context={'form': form})

    def post(self, request):
        request_keep = PostForm(request.POST, request.FILES)
        if request_keep.is_valid():
            request_keep.save()
            return redirect('home_page')
        return render(request, 'sitelogic/addpost.html', context={'form': request_keep})


def user_register(request):
    return render(request, 'sitelogic/register.html')


class Base(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return HttpResponse("<h1>HI</h1>")


class Response200(APIView):

    def get(self, request):
        json_response = {'Response200': 'OK'}
        return Response(json_response, status=status.HTTP_200_OK)


# def ppost_form(request):
#     form = PostForm()
#     context = {
#         'form': form
#     }
#     if request.method == 'POST':
#         print("МЕТОД ПОСТ, МЕТОД ПОСТ, МЕТОД ПОСТ, МЕТОД ПОСТ, МЕТОД ПОСТ, МЕТОД ПОСТ, МЕТОД ПОСТ, МЕТОД ПОСТ")
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 form.save()
#                 print("ПОСТ УСПЕШНО СОЗДАН, ПОСТ УСПЕШНО СОЗДАН, ПОСТ УСПЕШНО СОЗДАН, ПОСТ УСПЕШНО СОЗДАН, ПОСТ УСПЕШНО СОЗДАН, ПОСТ УСПЕШНО СОЗДАН")
#                 return redirect('home_page')
#             except:
#                 form.save()
#                 print("EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT, EXCEPT")
#                 form.add_error(None, 'Ошибка добавления поста')
#     else:
#         print("НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН, НЕ СОЗДАН")
#         form = PostForm
#
#     return render(request, 'sitelogic/addpost.html', context=context)

# if request.method == 'POST':
#     form = PostForm(request.POST, request.FILES)
#     if form.is_valid():
#         try:
#             form.save()
#             return redirect('home_page')
#         except:
#             form.add_error(None, 'Ошибка добавления поста')
# else:
#     form = PostForm


class kek(APIView):

    def get(self, request):
        return HttpResponseForbidden('jestkiy riskoviy')
