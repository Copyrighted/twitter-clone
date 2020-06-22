import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Tweet
from .forms import TweetForm

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, template_name="pages/home.html", context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript or Swift/Java/iOS/Android
    return json data
    """
    qs = Tweet.objects.all()
    tweet_list = [{"id": x.id, "content": x.content, "likes": random.randint(0,955 )} for x in qs]

    data = {
        "isUser": False,
        "response": tweet_list
    }

    return JsonResponse(data)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)  #sends data with the post method if theres data being sent
    next_url=request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None:
            return redirect(next_url)
        form=TweetForm() #re-initialize new blank form
    return render(request, 'pages/components/form.html', context={"form": form})

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript or Swift/Java/iOS/Android
    return json data
    """
    data = {
        "id": tweet_id,
    }

    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    #return HttpResponse(f"<h1> {tweet_id} - { obj.content } </h1>")
    return JsonResponse(data, status=status) #json.dumps content_type='application/json'
