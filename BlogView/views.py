import os
import django
import lxml
import lxml.etree as ET
import lxml.html

import urllib3
import logging
import filecmp
import requests
import binascii
import concurrent_log_handler

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from IlViale.settings import BASE_DIR
from BlogView.forms import RegisterForm
#from BlogView.tokens import account_activation_token
from django.core.mail import EmailMessage
from BlogView import LocalFileAdapter
from shutil import move
from shutil import copy2
from datetime import datetime
from html import unescape

# Create your views here.
from django.http import HttpResponse


import feedparser


def index(request):
    post_id = ""
    base_url = None
    if request.GET.get("Newsletter") == 'compila':
        return render(
            request,
            "newsletter.html",
            {
                'ext_templ':'base.html'
            },
        )
    try:
        server = os.environ["SERVER_TYPE"]
    except KeyError:
        server = "PROD"
    if server == "DEV":
        #http = urllib3.ProxyManager("http://cn-1998267631-nx10650.ibosscloud.com:80")
        
        base_url = request.build_absolute_uri("")
        http = urllib3.PoolManager()
    elif server == "DEVHOME":
        http = urllib3.PoolManager()
    else:
        base_url = request.build_absolute_uri("")
        http = urllib3.PoolManager()    
    logger = logging.getLogger("django")

    logger.warning("New request base_url:" + base_url )
    rss_response_data = ""      
    try:
        rss_response = http.request(
            "GET",
            "http://ilvialedellaformica.blogspot.com/feeds/posts/default?max-results=1500",
        )
        renamed_file = ""
        rss_cache_file_path = os.path.join(BASE_DIR, "media", "il_viale_rss_payload.rss")#.replace('/home/', 'home/')
        if not rss_response.status == 200:
            raise Exception("Load cache file")
        #logger.warning("check file exists:" + rss_cache_file_path)
        # logger.warning(os.listdir('home/ubuntu/django/IlViale/media/'))
        # move('home/ubuntu/django/IlViale/media/django.log2', 'home/ubuntu/django/IlViale/media/django.log2.rename')
        # logger.warning(os.listdir('home/ubuntu/IlViale/media/'))  
        # os.rename('home/ubuntu/django/IlViale/media/django.log1', 'home/ubuntu/django/IlViale/media/django.log1.rename')
        # logger.warning(os.listdir('home/ubuntu/IlViale/media/'))
        if os.path.exists(rss_cache_file_path):
            renamed_file = rss_cache_file_path.replace(
                ".", datetime.now().strftime("%Y%m%d_%H%M%S.%f.")
            )
            try:
                copy2(rss_cache_file_path, renamed_file)
            except (Exception) as identifier:
                logger.warning("error")
            
            #logger.warning("renaming:" +rss_cache_file_path + " in:" + renamed_file)
        # if os.path.exists(renamed_file):
        #     logger.warning("renamed correctly")
        # if os.path.exists(renamed_file):
        #     logger.warning("Deletion failed")
        rss_response_data = rss_response.data.replace(rb'imageanchor=&quot;1&quot;', rb'').replace(rb'&lt;img ', rb'&lt;img alt="Immagine dal blog" ').replace(rb'border=&quot;0&quot; ', rb' ')
        #position_byte = rss_response_data1.find(b'imageanchor')
        # data_chunk = rss_response_data[rss_response_data.find(b'<a title=&quot;Condividi su facebook&quot; ')-10: rss_response_data.find(b'<a title=&quot;Condividi su facebook&quot; ')+50]
        #data_chunk = rss_response_data1[2970:2970+50]
        #logger.warning(data_chunk)
        # binascii.hexlify(rss_response_data.find(b'imageanchor="1"')
        # a single replace isn't enough ?!?!?
        # rss_response_data = rss_response_data.replace(rb'imageanchor=&quot;1&quot; ', rb'')
        #rss_response_data = rss_response_data.replace(b'imageanchor="1"', b'')         
        with open(rss_cache_file_path, "wb") as cache_file:
            cache_file.write(rss_response.data)
            cache_file.close
        if filecmp.cmp(rss_cache_file_path, renamed_file):
            os.remove(renamed_file)
        else:
            logger.warning("New content, new file created")

            #logger.warning("Same content, removing created cache file")
        # logger.warning(">>>>+++ response data:" + rss_response_data.decode("utf-8"))
        
    except (Exception) as exception:
        logger.exception("general exception ")
        logger.warning(exception)
        try:
            requests_session = requests.session()
            requests_session.mount("file://", LocalFileAdapter.LocalFileAdapter())
            logger.warning("getting local content:" + 'file://' + rss_cache_file_path.replace("\\", "/"))
            rss_response = requests_session.get('file:///' + rss_cache_file_path.replace("\\", "/"))
            # rss_response = requests_session.get("file://" + "/Progetti/SitiWeb/IlViale/media/IlVialeRSSPayload.rss"            )
            rss_response_data = rss_response.content
            logger.warning( rss_response_data)
            logger.warning('Loading file from cache: ' + rss_cache_file_path)
            # before deploying code on aws server (ubuntu) loading data was after the try except block 
            # calling ET.XML(rss_response.content) failed with an error "can only parse strings"
            # same thing on windows worked correctly. So I workaround it loading file from filesystem
            # dom = ET.parse(rss_cache_file_path)
        except:
            logger.exception("Cache File not found or broken")
            raise
    # myfeed = feedparser.parse('http://ilvialedellaformica.blogspot.com/feeds/posts/default?max-results=1500')
    myfeed = feedparser.parse(rss_response_data)
    # myfeed.entries
    dom = ET.XML(rss_response_data)

    # logger.warning ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' + BASE_DIR)
    # logger.warning (os.path.join(BASE_DIR,'BlogView','RSS2HTMLUL.xslt'))
    #logger.warning("Server:" + server)
    xslt = ET.parse(os.path.join(BASE_DIR, "BlogView", "RSS2HTMLUL.xslt"))
    transform = ET.XSLT(xslt)
    HTMLTree = transform(dom)
    
    postToShow = request.GET.get("postToShow")
    maxPost = int(dom.xpath("count(//*[local-name() = 'entry'])")   )
    if postToShow is None or int(postToShow) < 5:
        postToShow = 5  
        
    # site = get_current_site(request)
    # logger.warning('current_site' + site.domain)
    # print(ET.tostring(HTMLTree, pretty_print=True))
    # return HttpResponse("Hello, world.")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            """     try:
            subscribe_model_instance = SubscribeModel.objects.get(email=email)
        except ObjectDoesNotExist as e:
            subscribe_model_instance = SubscribeModel()
            subscribe_model_instance.email = email
        except Exception as e:
            logging.getLogger("error").error(traceback.format_exc())
            return False """
            newsletter_registration = form.save()
            # indirizzo_mail = newsletter_registration.indirizzo_mail
            # nome = newsletter_registration.nome
            # cognome = newsletter_registration.cognome
            # localita = newsletter_registration.localita
            # current_site = get_current_site(request)
            # subject = 'Attiva la sottoscrizione della newsletter del Viale della Formica'
            # message = render_to_string('newsletter_activation_email.html', {
            #     'user': nome + cognome,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(newsletter_registration.pk)),
            #     'token': encrypt(indirizzo_mail + constants.SEPARATOR + str(time.time())),
            # })
            # email = EmailMessage(subject, message, to=[indirizzo_mail])
            # email.send()
            return redirect("newsletter_activation_sent")
    else:
        post_id = request.GET.get("post_id")
        form = RegisterForm()
        imgUrl = ""
        if not( post_id is None or post_id == ''):
            PostContent = dom.xpath("//*[local-name() = 'id' and .='" + post_id + "']/../*[local-name() = 'content']")
            imgTags = PostContent[0].text.split("<img ")
            for imgTag in imgTags:
                imgHeightArray = imgTag.split(" height=\"")
                if len(imgHeightArray) > 1:
                    if int(imgHeightArray[1].split("\"")[0])>200:
                        imgUrl =  imgTag.split("src=\"",2)[1]
                        imgUrl = imgUrl.split("\"",1)[0]
                        break
    if request.GET.get("Cronologia") == 'visualizza':
        return render(
        request,
        "cronologia.html",
        {
            "HTMLTree": HTMLTree,
            'ext_templ':'base.html'
        },
    )
    if request.GET.get("Prova") == "si":
        return render(
            request,
            "ProvaLayout.html",
            {
                "feed": myfeed,
                "post_id": post_id,
                "base_url": base_url,
                "form": form,
                "HTMLTree": HTMLTree,
            },
        )
    else:
        return render(
            request,
            "newsletter.html",
            {
                "feed": myfeed,
                "post_id": post_id,
                "base_url": base_url,
                "form": form,
                "HTMLTree": HTMLTree,
                "imgUrl": imgUrl,
                "postToShow": postToShow,
                "maxPost": maxPost,
                'ext_templ':'reader.html'
            },
        )


""" def signup(request):
    if request.method == 'POST':
        form = SignUpForm(re    quest.POST)
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
 """


def account_activation_sent(request):
    return render(request, "mail_sent.html",)


""" 
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
 """
