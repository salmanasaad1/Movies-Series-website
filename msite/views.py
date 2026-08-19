from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import pandas as pd
from django.db.models import Case, When

# Create your views here.

### Sign-up
def sign(request):
    
    if request.method=='POST':
      username=request.POST['username']
      email=request.POST['email']
      pass1=request.POST['pass1']
      if User.objects.filter(username=username):
        messages.error(request, 'this username was created before')
      else:
        myuser = User.objects.create_user(username,email,pass1)
        myuser.save()
        Userprofile.objects.create(
            user=myuser,
        )  
        messages.success(request, 'Welcome to our WebSite')      
        return redirect('login')    
    return render(request, 'pages/sign-up.html')

### Login
def login_view(request):

    if request.method=='POST':
         username=request.POST['username']
         pass1=request.POST['pass1']

         user= authenticate(username=username,password=pass1)

         if user is not None:
            login(request,user)
            return redirect('index')

         else:
            messages.error(request, "worng entiers")
            return redirect('sign-up')
        
    return render(request, 'pages/login.html')


### User Profile
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request , 'we have successfully updated your profile')
            return redirect('profile-page')
               
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context ={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'pages/profile3.html',context)



### Main Page
def index(request):
    Tv_obj=TvShows.objects.all()
    movies_obj= MainMovie.objects.all()
    mid=MainMovie.objects.last()
    last_movie=MainMovie.objects.filter(id=mid.id)
    site=SiteRecom.objects.all() 
    

    paginator=Paginator(movies_obj,8)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    paginator2=Paginator(Tv_obj,8)
    page_number2=request.GET.get('page')
    page_obj2=paginator2.get_page(page_number)
    context={'movie':page_obj ,'tv':page_obj2,'lastm':last_movie,'site':site}
    return render(request, 'pages/index.html',context)


### Movie Page
def movie_detail(request,movie_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    
    movie = MainMovie.objects.get(id=movie_id)
    
    temp = list(MyList.objects.all().values().filter(movie_id=movie_id,user=request.user))
    if temp:
        update = temp[0]['watch']
    else:
        update = False
    if request.method == "POST":
        # For my list
        if 'watch' in request.POST:
            watch_flag = request.POST['watch']
            if watch_flag == 'on':
                update = True
            else:
                update = False
            if MyList.objects.all().values().filter(movie_id=movie_id,user=request.user):
                MyList.objects.all().values().filter(movie_id=movie_id,user=request.user).update(watch=update)
            else:
                q=MyList(user=request.user,movie=movie,watch=update)
                q.save()
            if update:
                messages.success(request, "Movie added to your list!")
            else:
                messages.success(request, "Movie removed from your list!")

    # For rating
        elif 'rating' in request.POST :
            rate = request.POST['rating']
            if Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user):
                Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user).update(rating=rate)
            else:
                q=Myrating(user=request.user,movie=movie,rating=rate)
                q.save()

            messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(Myrating.objects.filter(user=request.user.id).values())

    # To display ratings in the movie detail page
    rat=Myrating.objects.filter(user=request.user.id,movie=movie_id).values()

    movie_obj=MainMovie.objects.filter(id=movie_id)

    return render(request, 'pages/movie_detail.html',{'movies':movie_obj ,'update':update,'rat':rat})



### Seaarch Page
def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        result = MainMovie.objects.filter(name__contains=search)
        result2 = TvShows.objects.filter(name__contains=search)
        # result3 = list(Category.objects.filter(cate__contains=search).values_list())
        
        # print(result3)
        # result4 = MainMovie.objects.filter(category=result3[0][0])
        

        return render(request,'pages/search.html',{'posts':result,'tv':result2})
 

### All Movies Page
def more_movies(request):
    movies_obj= MainMovie.objects.all()

    paginator=Paginator(movies_obj, 8)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'pages/movies.html',{'movie':page_obj })


### Actor Movies Page
def actor_movies(request,actor_id):
    actor_obj=Actors.objects.filter(id=actor_id)
    actor_movies=MainMovie.objects.filter(actors=actor_id)
    actor_show=TvShows.objects.filter(actors=actor_id)

    return render(request, 'pages/actor_movies.html',{'actor':actor_obj,'movi':actor_movies,'tv':actor_show})


### Category Movies Page
def category_movie(request,category_id):
    cat_obj=Category.objects.filter(id=category_id)
    cat_movie=MainMovie.objects.filter(category=category_id)
    cat_show=TvShows.objects.filter(category=category_id)

    return render(request, 'pages/category_movie.html',{'cat':cat_obj,'movi':cat_movie,'tv':cat_show})


### TvShows page

def Tv(request,tv_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    
    tv = TvShows.objects.get(id=tv_id)
    
    temp = list(MyTvList.objects.all().values().filter(tv_id=tv_id,user=request.user))
    if temp:
        update = temp[0]['watch']
    else:
        update = False
    if request.method == "POST":
        # For my list
        if 'watch' in request.POST:
            watch_flag = request.POST['watch']
            if watch_flag == 'on':
                update = True
            else:
                update = False
            if MyTvList.objects.all().values().filter(tv_id=tv_id,user=request.user):
                MyTvList.objects.all().values().filter(tv_id=tv_id,user=request.user).update(watch=update)
            else:
                q=MyTvList(user=request.user,tv=tv,watch=update)
                q.save()
            if update:
                messages.success(request, "Movie added to your list!")
            else:
                messages.success(request, "Movie removed from your list!")


    tv_obj=TvShows.objects.filter(id=tv_id)

    return render(request, 'pages/tv.html',{'tv':tv_obj,'update':update})


### Season Page

def season(request,season_id):
    season_obj=Part.objects.filter(id=season_id)

    return render(request, 'pages/season.html',{'season':season_obj})

### Episode Page

def episode(request,episode_id):
    episode_obj=Episode.objects.filter(id=episode_id)

    return render(request, 'pages/episode.html',{'episode':episode_obj})


### All shows Page
def more_shows(request):
    tv_obj= TvShows.objects.all()

    paginator=Paginator(tv_obj, 8)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'pages/shows.html',{'tv':page_obj })

### Favorit

def watch(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404

    movies = MainMovie.objects.filter(mylist__watch=True,mylist__user=request.user)
    tv = TvShows.objects.filter(mytvlist__watch=True,mytvlist__user=request.user)

    query = request.GET.get('q')

    if query:
        movies = MainMovie.objects.filter(Q(name__icontains=query)).distinct()
        tv = TvShows.objects.filter(Q(name__icontains=query)).distinct()

        return render(request, 'pages/favo.html', {'movies': movies,'tv':tv})

    return render(request, 'pages/favo.html', {'movies': movies,'tv':tv})


def get_similar(movie_name,rating,corrMatrix):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

# Recommendation Algorithm
def recommend(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404


    movie_rating=pd.DataFrame(list(Myrating.objects.all().values()))

    new_user=movie_rating.user_id.unique().shape[0]
    
    current_user_id= request.user.id
    
	# if new user not rated any movie
    if current_user_id>new_user:
        movie=MainMovie.objects.get(id=5)
        q=Myrating(user=request.user,movie=movie,rating=0)
        q.save()


    userRatings = movie_rating.pivot_table(index=['user_id'],columns=['movie_id'],values='rating')
    userRatings = userRatings.fillna(0,axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(Myrating.objects.filter(user=request.user).values())).drop(['user_id','id'],axis=1)
    user_filtered = [tuple(x) for x in user.values]
    


    movie_id_watched = [each[0] for each in user_filtered]

    similar_movies = pd.DataFrame()
    for movie,rating in user_filtered:
        similar_movies = similar_movies._append((get_similar(movie,rating,corrMatrix)))

    movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
    movies_id_recommend = [each for each in movies_id if each not in movie_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
    
    movie_list=list(MainMovie.objects.filter(id__in = movies_id_recommend).order_by(preserved)[:10])

    context = {'movie_list': movie_list}
    return render(request, 'pages/recommend.html', context)
