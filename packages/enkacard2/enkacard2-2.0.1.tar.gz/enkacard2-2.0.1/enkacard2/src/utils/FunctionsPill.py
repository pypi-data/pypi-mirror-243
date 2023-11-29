# Copyright 2022 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image, ImageFont
from . import openFile
from io import BytesIO
import aiohttp
from asyncache import cached
from cachetools import TTLCache
import json

xId = "91470304"
ccokie = "first_visit_datetime_pc=2022-08-06+03:53:37; p_ab_id=1; p_ab_id_2=5; p_ab_d_id=1897822829; yuid_b=IFV4MVY; privacy_policy_agreement=5; c_type=23; privacy_policy_notification=0; a_type=0; b_type=1; __utmc=235335808; __utmz=235335808.1675712222.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gcl_au=1.1.1586580017.1675934633; _gid=GA1.2.67267752.1677021212; PHPSESSID=91470304_hbEoBFwL6Ss8hQHDiSkc26NAN2BgUaww; device_token=cbf72f380348bc4dcc9910df20a3b368; QSI_S_ZN_5hF4My7Ad6VNNAi=v:100:0; __utmv=235335808.|2=login ever=yes=1^3=plan=premium=1^5=gender=male=1^6=user_id=91470304=1^9=p_ab_id=1=1^10=p_ab_id_2=5=1^11=lang=en=1; _ga_MZ1NL4PHH0=GS1.1.1677021212.1.1.1677021635.0.0.0; __utma=235335808.1013236179.1675712222.1677021201.1677023923.4; login_ever=yes; __cf_bm=uIwLHChsA9lvfHUYdc_qU3KBp.pYrFxzrlv_4crFoE4-1677024971-0-AaFldWtGUM9OmDn1Kfcwc03QpGNuGGlE8Ev1PZtv6Q6PavyffvJ2dmVVIDVdeTM6cD8GNSLlL8ta93GxurhWiQqj+rxXEWgO3LDUqV0uXNORvDhI4+KP930Hf962s6ivFp1Zz6aG5fVGtpySkJBAEcVUAoxfpO6+KGijUP4sJAvftKvKK8NZaD6zcqDr47mOMJsHCvdck/DW4GqbSDeuIJo=; __utmt=1; tag_view_ranking=_EOd7bsGyl~ziiAzr_h04~azESOjmQSV~Ie2c51_4Sp~Lt-oEicbBr~WMwjH6DkQT~HY55MqmzzQ~yREQ8PVGHN~MnGbHeuS94~BSlt10mdnm~tgP8r-gOe_~fg8EOt4owo~b_rY80S-DW~1kqPgx5bT5~5oPIfUbtd6~KN7uxuR89w~QaiOjmwQnI~0Sds1vVNKR~pA1j4WTFmq~aPdvNeJ_XM~vzTU7cI86f~HHxwTpn5dx~pnCQRVigpy~eVxus64GZU~rOnsP2Q5UN~-98s6o2-Rp~EZQqoW9r8g~iAHff6Sx6z~jk9IzfjZ6n~PsltMJiybA~TqiZfKmSCg~IfWbVPYrW4~0TgyeJ7TQv~g2IyszmEaU~28gdfFXlY7~DCzSewSYcl~n15dndrA2h~CActc_bORM~U51WZv5L6G~-7RnTas_L3~zyKU3Q5L4C~QwUeUr8yRJ~j3leh4reoN~vgqit5QC27~t1Am7AQCDs~5cTBH7OrXg~-HnQonkV01~oCqKGRNl20~ba025Wj3s2~TAc-DD8LV2~p0NI-IYoo2~wqBB0CzEFh~U-RInt8VSZ~oiDfuNWtp4~fAWkkRackx~i54EuUSPdz~Js5EBY4gOW~ZQJ8wXoTHu~Cm1Eidma50~CMvJQbTsDH~ocDr8uHfOS~pzZvureUki~ZNRc-RnkNl~nWC-P2-9TI~q1r4Vd8vYK~hZzvvipTPD~DpYZ-BAzxm~096PrTDcN1~3WI2JuKHdp~faHcYIP1U0~1n-RsNEFpK~Bd2L9ZBE8q~txZ9z5ByU7~r01unnQL0a~EEUtbD_K_n~cb-9gnu4GK~npWJIbJroU~XbjPDXsKD-~lkoWqucyTw~P8OX_Lzc1b~RmnFFg7HS4~6rYZ-6JKHq~d80xTahBd1~OYl5wlor4w~2R7RYffVfj~1CWwi2xr7g~c7QmKEJ54V~rlExNugdTH~wO2lnVhO8m~vc2ipXnqbX~Is5E1jIZcw~c_aC4uL3np~vzxes78G4k; _ga=GA1.2.714813637.1675712223; _gat_UA-1830249-3=1; _ga_75BBYNYN9J=GS1.1.1677023923.4.1.1677025390.0.0.0; __utmb=235335808.52.9.1677024704913"

headers = {
    "accept-type": "application/json",
    "accept-encoding": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,af;q=0.6",
    "language": "gzip, deflate, br",
    "cookie": ccokie,
    "dnt": "1",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "x-user-id": xId,
    "referer": "https://www.pixiv.net/",
}

cache = TTLCache(maxsize=1000, ttl=300)  

async def dowloadImg(link,size = None, thumbnail_size = None):
    cache_key = json.dumps((link, size, thumbnail_size), sort_keys=True)  # Преобразовываем в строку
        
    if cache_key in cache:
        return cache[cache_key]
    

    try:
        if "pximg" in link:
            async with aiohttp.ClientSession(headers=headers) as session, session.get(link) as r:
                try:
                    image = await r.read()
                finally:
                    await session.close()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    try:
                        image = await response.read()
                    finally:
                        await session.close()
    except:
        raise
    
    image = Image.open(BytesIO(image)).convert("RGBA")
    if size:
        image = image.resize(size)
        cache[cache_key] = image
        return image
    elif thumbnail_size:
        image.thumbnail(thumbnail_size)
        cache[cache_key] = image
        return image
    else:
        cache[cache_key] = image
        return image

async def imagSize(link = "", image = None, fixed_width = 0, size = None):
    if not image:
        if link == "https://enka.network/ui/UI_Gacha_AvatarImg_PlayerGirl.png":
            imgs = openFile.PlayerGirl.copy()
        else:
            imgs = await dowloadImg(link = link)
    else:
        imgs = image
    if size:
        new_image = imgs.resize(size)
    else:
        if imgs.size[0] != imgs.size[1]:
            ratio = (fixed_width / float(imgs.size[0]))
            height = int((float(imgs.size[1]) * float(ratio)))
            new_image = imgs.resize((fixed_width, height), Image.LANCZOS)
        else:
            new_image = imgs.resize((fixed_width,fixed_width))
    return new_image

async def imgD(link = ""):
    imgs = await dowloadImg(link = link)
    return imgs.convert("RGBA")

@cached(TTLCache(80, ttl=30))  
async def centrText(text, witshRam = 100, razmer = 24, start = 0, Yram = 20, y = None, aling = "centry"):
    Text = ImageFont.truetype(openFile.font, razmer)
    maxDlina = witshRam
    while True:
        Text = ImageFont.truetype(openFile.font, razmer)
        withText = int(Text.getlength(str(text)))
        r = witshRam/2 
        t = withText/2 
        itog = r-t 

        if withText > maxDlina:
            razmer -= 1
            if razmer <= 2:
                break
            continue
        break
    if y:
        while True:
            Text = ImageFont.truetype(openFile.font, razmer)
            HegText = Text.getbbox(str(text))[3]
            maxHeg = Yram
            r = Yram/2 
            t = HegText/2 
            itogs = r-t 

            if HegText > maxHeg:
                razmer -= 1
                if razmer <= 2:
                    break
                continue
            break
        
        if aling == "centry":
            return (int(start + itog),int(y + itogs)),Text
        else:
            return (int(start),int(y)),Text

    if aling == "centry":
        return int(start + itog),Text
    else:
        return int(start),Text
