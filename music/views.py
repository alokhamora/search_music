from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import base64
from django.contrib.auth import authenticate, login
import requests
from global_var import API_KEY
from .models import Track

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    # context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Track.objects.order_by('name')[:5]


@csrf_exempt
def register(request):
    body = request.body
    decode_body = json.loads(body)
    response_data = {}
    if 'name' not in decode_body:
        response_data['status'] = 'ERROR'
        response_data['message'] = 'Name required'
        return HttpResponseBadRequest(json.dumps(response_data), content_type="application/json")
    elif 'mail' not in decode_body:
        response_data['status'] = 'ERROR'
        response_data['message'] = 'Mail required'
    elif 'password' not in decode_body:
        response_data['status'] = 'ERROR'
        response_data['message'] = 'Password required'
        return HttpResponseBadRequest(json.dumps(response_data), content_type="application/json")
    else:
        try:
            user = User.objects.create_user(decode_body['name'], decode_body['mail'], decode_body['password'])
            user.save()
        except:
            response_data['status'] = 'ERROR'
            response_data['message'] = 'User already exists'
            return HttpResponseBadRequest(json.dumps(response_data), content_type="application/json")
        response_data['status'] = 'OK'
        response_data['message'] = 'User was created'
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def view_or_auth(view):
    def authorization(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    auth1 = auth[1].encode('ascii')
                    name, password = base64.b64decode(auth1).split(b':')
                    name = name.decode('ascii')
                    password = password.decode('ascii')
                    user = authenticate(username=name, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            request.user = user
                            return view(request)
                    else:
                        response_data = {}
                        response_data['status'] = 'ERROR'
                        response_data['message'] = 'Authorisation error'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % ""
        return response
    return authorization

@csrf_exempt
@view_or_auth
def search(request):
    search_request = request.GET['track']
    response = requests.get('http://ws.audioscrobbler.com/2.0/?',
                            params={'method': 'track.search', 'track': search_request, 'api_key': API_KEY, 'format': 'json'})
    json_response = response.json()
    try:
        result = json_response['results']['trackmatches']['track'][0]
    except:
        response_data = {}
        response_data['status'] = 'ERROR'
        response_data['message'] = 'Track not found'
        return HttpResponseBadRequest(json.dumps(response_data), content_type="application/json")
    q = Track.objects.create(name=result['name'], artist=result['artist'], url=result['url'])
    q.save()
    return HttpResponse(json.dumps(result), content_type="application/json")


