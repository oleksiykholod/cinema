from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
import time
import asyncio
from playwright.async_api import async_playwright
# Create your views here.
HDREZKA = 'https://rezka.ag'
def base(request):
    return render(request,'webapp/base.html')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def main(request,urlz):
    if is_ajax(request):
        page = requests.get(urlz,headers={'User-Agent': UserAgent().chrome})
        soup = BeautifulSoup(page.text, "html.parser")

        ##витягуєм урл фоток
        all = soup.find('div', class_="b-content__inline_items")
        s = BeautifulSoup(str(all),"html.parser")
        img = s.find_all('img')
        imgs = []
        for i in img:
            m = BeautifulSoup(str(i),"html.parser")
            n = m.find('img')['src']
            imgs.append(str(n))
        ###витягуєм назву і рік фільма
        allname = all.find_all('div', class_="b-content__inline_item-link")
        urls = []
        names = []
        infos = []
        for i in allname:
            m = BeautifulSoup(str(i),"html.parser")
            n = m.find('a')['href']
            urls.append(str(n))
            s = m.find('a').contents
            s = str(s)[2:-2]
            if len(s)>30:
                s = s[:20]+'...'
            names.append(str(s))
            v = m.find_all('div')[1].contents
            z = str(v).split(',' )[0]
            j = z[2:]
            x = j.find('- ...')
            if x == 5:
                j = j[:-6]  
            infos.append(str(j))
            ids = range(len(names))
            obj = []
            for i in range(len(names)):
                a = []
                a.append(names[i])
                a.append(infos[i])
                a.append(imgs[i])
                a.append(urls[i])
                a.append(ids[i])
                obj.append(a)
            context = {
        'obj': obj,}
            rendered = render_to_string('webapp/news.html', context)
            response = {'html': rendered}


        return JsonResponse(response)
    else:
        raise Http404

def now(request):
    url= HDREZKA+"/?filter=watching"
    return main(request,url)

def news(request):
    url=HDREZKA+"/new/"
    return main(request,url)

def films(request):
    url=HDREZKA+"/films/"
    return main(request,url)

def serials(request):
    url=HDREZKA+"/series/"
    return main(request,url)

def myltfilms(request):
    url=HDREZKA+"/cartoons/"
    return main(request,url)

def tele(request):
    url=HDREZKA+"/series/telecasts/"
    return main(request,url)

def anime(request):
    url=HDREZKA+"/animation/"
    return main(request,url)
    
def ozvuchka(request):
    if is_ajax(request):
        url = str(request.GET.get('p1'))
        objc = []
        lang = []
        typec = str()
        langid = []
        lv = []
        page = requests.get(url,headers={'User-Agent': UserAgent().chrome})
        soup = BeautifulSoup(page.text, "html.parser")
        try:
            for i in soup.find(id="translators-list").find_all('li'):
                langid.append(i['data-translator_id'])
        except AttributeError:
            pass
        try:
            for i in soup.find(id="translators-list").children:
                lang.append(i.get_text())
        except AttributeError:           
            pass
        try:
            if len(soup.find(id="simple-seasons-tabs").children) != 0:
                typec = 'serial'
                
        except AttributeError:           
            typec = 'film'
        for i in range(len(lang)):
            a = []
            a.append(lang[i])
            a.append(langid[i])
            a.append(i+1)
            objc.append(a)
        if len(objc)==0:
            b = []
            b.append('Ориг')
            b.append('0')
            b.append('1')
            objc.append(b)
        
        context = {"objc":objc,'typec': typec,'urlz':url}
        rendered = render_to_string('webapp/video.html', context)
        response = {'html': rendered}
        return JsonResponse(response)
    else:
        raise Http404
    
def film(request):
    if is_ajax(request):
        url = str(request.GET.get('url'))
        ozv = str(request.GET.get('ozv'))
        lv = str(request.GET.get('lv'))
        quality = []
        async def run(playwright, urlm):
            chromium = playwright.firefox
            browser = await chromium.launch()
            page = await browser.new_page()
            
            mp4_urls = []
            # Subscribe to "request" and "response" events.
            page.on("response", lambda response: mp4_urls.append(response.url) if ".mp4" in response.url else None)
            
            await page.goto(urlm, timeout=0)
            
            await browser.close()
            urlk = mp4_urls[0]
            return quality.append(str(urlk[0:-18]))
        async def main(urlm):
            async with async_playwright() as playwright:
                await run(playwright,urlm)

        asyncio.run(main(urlm=url))

        context = {'urlz':url,'quality':quality,'ozv':ozv}
        rendered = render_to_string('webapp/quality.html', context)
        response = {'html': rendered}
        return JsonResponse(response)
    else:
        raise Http404


    

    

