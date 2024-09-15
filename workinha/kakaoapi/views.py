from django.shortcuts import render

def kakaoapi_view(request):
    return render(request, 'kakaoapi/map.html')
