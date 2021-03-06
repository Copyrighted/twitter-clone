import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Tweet
from .forms import TweetForm
from django.utils.http import is_safe_url
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from .serializers import TweetSerializer
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, template_name="pages/home.html", context={}, status=200)

def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript or Swift/Java/iOS/Android
    return json data
    """

    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]

    data = {
        "isUser": False,
        "response": tweet_list
    }

    return JsonResponse(data)

@api_view(['POST']) #http method that client has to send is post
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    tweet_list = [x.serialize() for x in qs]

    data = {
        "isUser": False,
        "response": tweet_list
    }
    return Response(serializer.data)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You can't delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed"}, status=200)

#
# def tweet_create_view(request, *args, **kwargs):
#     '''
#     REST API Create View -> DRF
#     '''
#     user = request.user
#     if not request.user.is_authenticated:
#         user = None
#         if request.is_ajax():
#             return JsonResponse({}, status=401)
#         return redirect(settings.LOGIN_URL)
#     form = TweetForm(request.POST or None)  #sends data with the post method if theres data being sent
#     # next_url=request.POST.get("next") or None
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = user
#         obj.save()
#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201) #201 is for created items
#
#         # if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
#         #     return redirect(next_url)
#         form=TweetForm() #re-initialize new blank form
#     if form.errors:
#         if request.is_ajax():
#             return JsonResponse(form.errors, status=400)
#
#     return render(request, 'pages/components/form.html', context={"form": form})

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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
