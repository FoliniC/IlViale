import os

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from BlogView.forms import RegisterForm
from BlogView.tokens import account_activation_token

# Create your views here.
from django.http import HttpResponse


import feedparser

def index(request):
    post_id = ""
    base_url = None
    try: 
        server = os.environ["SERVER_TYPE"]
    except KeyError:  
        server = "PROD"
    if server != 'DEV':
        base_url = request.build_absolute_uri
    myfeed = feedparser.parse('http://ilvialedellaformica.blogspot.com/feeds/posts/default')
    
    # return HttpResponse("Hello, world.")
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('account_activation_sent')
    else:
        post_id = request.GET.get("post_id")
        form = RegisterForm()
    return render(request, "reader.html", {"feed" : myfeed,"post_id" : post_id,"base_url" : base_url,'form': form} )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your BlogView Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):   
    return render(request, 'mail_sent.html', )
 
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')