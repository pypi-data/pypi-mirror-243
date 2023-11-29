# Copyright 2022 DEViantUa <t.me/deviant_ua>
# All rights reserved.
__all__ = ["weaponAdd", 
    "nameBanner", 
    "stats",
    "constant", 
    "create_picture", 
    "talants",
    "naborArtifact", 
    "artifacAdd", 
    "addConst",
    "addTallants", 
    "addArtifact", 
    "signature",
    "appedFrame",
    "openUserImg" 
    ]

import math,re,os,re,os,asyncio
from PIL import ImageDraw
from .Generation import * 
from .FunctionsPill import imgD,imagSize,centrText
from .options import *
from . import openFile

try:
    os.path.dirname(__file__).split("\\aioenkanetworkcard")[0]
    path = os.path.dirname(__file__).split("\\aioenkanetworkcard")[0]
except:
    try:
        os.path.dirname(__file__).split("/aioenkanetworkcard")[0]
        path = os.path.dirname(__file__).split("/aioenkanetworkcard")[0]
    except:
        pass


def signature(hide,uid):
    SignatureText = openFile.SignatureOne.copy()
    d = ImageDraw.Draw(SignatureText)

    if not hide:
        d.text((440,7), str(uid), font= fontSize(18), fill=coloring)
    else:
        d.text((440,7), "Hidden", font= fontSize(18), fill=coloring)

    return SignatureText
    
async def openUserImg(img):
    if type(img) != str:
        img = img
    elif type(img) == str:
        linkImg = re.search("(?P<url>https?://[^\s]+)", img)
        if linkImg:
            img = await imgD(link=linkImg.group())
        else:
            img = Image.open(f'{path}/{img}')
    else:
        return None
    return img.convert("RGBA")
    

class Creat:
    def __init__(self,characters,assets,img,signatureRes,lvl) -> None:
        self.characters = characters
        self.assets = assets
        self.img = img
        self.signatureRes = signatureRes
        self.lvl = lvl

    async def weaponAdd(self):
        weapon_data = self.characters.equipments[-1]
        if weapon_data.detail.artifact_name_set != "":
            return None
        WeaponBg = openFile.WeaponBgTeampleOne.copy()
        WeaponBgUp = openFile.WeaponBgUpTeampleOne.copy()
        proc = False    
        d = ImageDraw.Draw(WeaponBg)
        name = weapon_data.detail.name
        lvl = weapon_data.level
        lvlUp = weapon_data.refinement
        baseAtt = weapon_data.detail.mainstats.value
        imageStats = None
        dopStat = 0
        for substate in weapon_data.detail.substats:
            imageStats = getIconAdd(substate.prop_id, icon = True, size = (26,26))
            if not imageStats:
                continue
            dopStat = substate.value
            if str(substate.type) == "DigitType.PERCENT":
                proc = True
        if imageStats:
            WeaponBg.alpha_composite(imageStats,(300,53))
        
        stars = star(weapon_data.detail.rarity)
        image = await imagSize(link = weapon_data.detail.icon.url,size = (114,121))
        WeaponBg.alpha_composite(image,(0,0))
        WeaponBg.alpha_composite(WeaponBgUp,(0,0))
        position,font = await centrText(name, witshRam = 315, razmer = 24, start = 159, Yram = 30, y = 13)
        d.text(position, str(name), font= font, fill=coloring) 
        d.text((435 ,53), f"R{lvlUp}", font= fontSize(24), fill=(248,199,135,255)) 
        position,font = await centrText(f"{self.lvl}: {lvl}/90", witshRam = 152, razmer = 17, start = 235, Yram = 28, y = 90)
        d.text(position, f"{self.lvl}: {lvl}/90", font= font, fill=coloring) 

        position,font = await centrText(baseAtt, witshRam = 90, razmer = 24, start = 180, Yram = 30, y = 50)    
        d.text(position, str(baseAtt), font= font, fill=coloring)
        if proc:
            position,font = await centrText(f'{dopStat}%', witshRam = 90, razmer = 24, start = 320, Yram = 30, y = 50)
            d.text(position, f'{dopStat}%', font= font, fill=coloring)
        else:
            position,font = await centrText(str(dopStat), witshRam = 90, razmer = 24, start = 320, Yram = 30, y = 50)
            d.text(position, str(dopStat), font= font, fill=coloring) 
        WeaponBg.alpha_composite(stars,(0,0))

        return WeaponBg

    async def nameBanner(self,person):
        NameBg = openFile.NameBgTeampleOne.copy()
        d = ImageDraw.Draw(NameBg)
        centrName,fonts = await centrText(self.characters.name, witshRam = 220, razmer = 33,start = 2)
        d.text((centrName,28), self.characters.name, font = fonts, fill=coloring) 
        d.text((187,-1), str(self.characters.friendship_level), font = fontSize(24), fill= coloring) 
        centrName,fonts = await centrText(f"{self.lvl}: {self.characters.level}/90", witshRam = 148, razmer = 17, start = 5)
        d.text((centrName,2), f"{self.lvl}: {self.characters.level}/90", font = fonts, fill= coloring) 
        stars = star(person.rarity)
        NameBg.alpha_composite(stars,(59,68))
        return NameBg

    async def stats(self):
        g = self.characters.stats
        elementUp = True
        dopVal = {}
        postion = (26,37)
        AttributeBg = openFile.AttributeBgTeampleOne.copy()

        for key in g:
            if key[0] in ["BASE_HP","FIGHT_PROP_BASE_ATTACK","FIGHT_PROP_BASE_DEFENSE"]:
                if not key[0] in dopVal:
                    dopVal[key[0]] = int(key[1].value)
            if key[1].id in [2000,2001,2002]:
                iconImg = getIconAdd(key[0])
                Attribute = openFile.AttributeTeampleOne.copy()
                d = ImageDraw.Draw(Attribute)
                txt = self.assets.get_hash_map(key[0])
                icon = await imagSize(image = iconImg,fixed_width = 23)
                Attribute.alpha_composite(icon, (4,0))
                if not key[1].id in stat_perc:
                    value = str(math.ceil(key[1].value))
                else:
                    value = f"{round(key[1].value * 100, 1)}%"
                pX,fnt = await centrText(value, witshRam = 119, razmer = 20, start = 325)
                d.text((pX,3), value, font = fnt, fill=coloring)

                d.text((42,4), str(txt), font = fontSize(18), fill=coloring)

                AttributeBg.alpha_composite(Attribute,(postion[0],postion[1]))
                
                postion = (postion[0],postion[1]+39)
        
        for key in g:
            if key[1].id in [40,41,42,43,44,45,46]:
                if elementUp:
                    key = max((x for x in g if 40 <= x[1].id <= 46), key=lambda x: x[1].value)
                    elementUp = False
                else:
                    continue
            if key[1].value == 0 or key[1].id in [2000,2001,2002]:
                continue        
            iconImg = getIconAdd(key[0])
            if not iconImg:
                continue
            Attribute = openFile.AttributeTeampleOne.copy()
            d = ImageDraw.Draw(Attribute)
            
            txt = self.assets.get_hash_map(key[0])
            icon = await imagSize(image = iconImg,fixed_width = 23)
            Attribute.alpha_composite(icon, (4,0))

            if not key[1].id in stat_perc:
                value = str(math.ceil(key[1].value))
            else:
                value = f"{round(key[1].value * 100, 1)}%"
            pX,fnt = await centrText(value, witshRam = 119, razmer = 20, start = 325)
            d.text((pX,3), value, font = fnt, fill=coloring)

            d.text((42,4), str(txt), font = fontSize(18), fill=coloring)

            AttributeBg.alpha_composite(Attribute,(postion[0],postion[1]))

            postion = (postion[0],postion[1]+39)
        return AttributeBg

    async def constant(self):
        constantRes = []  
        for key in self.characters.constellations:
            closeConstBg = openFile.ClossedBg.copy()
            closeConsticon = openFile.Clossed.copy()
            openConstBg = openImageElementConstant(self.characters.element.value)  
            imageIcon = await imgD(link = key.icon.url)
            imageIcon = imageIcon.resize((43,48))
            if not key.unlocked:
                closeConstBg.alpha_composite(imageIcon, (19,20))
                closeConstBg.alpha_composite(closeConsticon, (-1,0))
                const = closeConstBg
            else:
                openConstBg.alpha_composite(imageIcon, (19,20))
                const = openConstBg
            constantRes.append(const)
        return constantRes

    async def create_picture(self):
        if self.img:
            frame = userImage(self.img, element = self.characters.element.value, adaptation = True)
        else:
            banner = await imagSize(link = self.characters.image.banner.url,size = (2048,1024))
            frame = maskaAdd(self.characters.element.value,banner)
        return frame

    async def talants(self):
        count = 0
        tallantsRes = []
        for key in self.characters.skills:
            if key.level > 9:
                talantsBg = openFile.TalantsFrameGoldLvlTeampleOne.copy()
            else:
                talantsBg = openFile.TalantsFrameTeampleOne.copy()
            talantsCount = openFile.TalantsCountTeampleOne.copy()
            d = ImageDraw.Draw(talantsCount)
            imagesIconTalants = await imgD(link = key.icon.url)
            imagesIconTalants = imagesIconTalants.resize((50,50))
            talantsBg.alpha_composite(imagesIconTalants, (8,7))
            if len(str(key.level)) == 2:
                d.text((6,-1), str(key.level), font = fontSize(15), fill=(248,199,135,255))
            else:
                d.text((9,-1), str(key.level), font = fontSize(15), fill=(248,199,135,255))
                                                    
            talantsBg.alpha_composite(talantsCount, (19,53))
            tallantsRes.append(talantsBg)
            count+=1
            if count == 3:
                break
        return tallantsRes
    async def naborArtifact(self,info,ArtifactNameBg):
        naborAll = []
        for key in info:
            if info[key] > 1:
                ArtifactNameFrame = openFile.ArtifactNameFrameTeampleOne.copy()
                d = ImageDraw.Draw(ArtifactNameFrame)
                centrName,fonts = await centrText(key, witshRam = 240, razmer = 15, start = 4, Yram = 24, y = 1) 
                d.text(centrName, str(key), font= fonts, fill=coloring)
                d.text((267,-2), str(info[key]), font= fontSize(24), fill=coloring)
                naborAll.append(ArtifactNameFrame)
        position = (151,34)
        for key in naborAll:
            if len(naborAll) == 1:
                ArtifactNameBg.alpha_composite(key,(151,54))
            else:
                ArtifactNameBg.alpha_composite(key,position)
                position = (position[0],position[1]+29)
        return ArtifactNameBg

    async def creatDopStat(self,infpart):
        res = []
        for key in infpart:
            imageStats = getIconAdd(key.prop_id, icon = True)
            if not imageStats:
                continue
            ArtifactDopStat = openFile.ArtifactDopValueTeampleOne.copy()
            v = f"+{key.value}"
            if str(key.type) == "DigitType.PERCENT":
                v = f"{v}%"
            imageStats= await imagSize(image = imageStats,fixed_width = 17) 
            ArtifactDopStat.alpha_composite(imageStats,(3,1))
            px,fnt = await centrText(v, witshRam = 142, razmer = 24, start = 33) 
            d = ImageDraw.Draw(ArtifactDopStat)
            d.text((px,-2), v, font= fnt, fill=coloring)
            res.append(ArtifactDopStat)
    
        return res

    async def creatArtifact(self,infpart,imageStats):
        dopVaulImg = await self.creatDopStat(infpart.detail.substats)
        ArtifactBgUp = openFile.ArtifactBgUpTeampleOne.copy()
        ArtifactBg = openFile.ArtifactBgTeampleOne.copy()
        artimg = await imagSize(link = infpart.detail.icon.url,size = (175,175))
        ArtifactBg.alpha_composite(artimg,(-32,-27))
        ArtifactBg.alpha_composite(ArtifactBgUp,(0,0))
        d = ImageDraw.Draw(ArtifactBg)
        if str(infpart.detail.mainstats.type) == "DigitType.PERCENT":
            val = f"{infpart.detail.mainstats.value}%"
        else:
            val = infpart.detail.mainstats.value
        centrName,fonts = await centrText(val, witshRam = 52, razmer = 17, start = 65)
        d.text((centrName,62), str(val), font= fonts, fill=coloring)
        ArtifactBg.alpha_composite(imageStats,(3,0))
        d.text((77,82), str(infpart.level), font= fontSize(17), fill=coloring)
        starsImg = star(infpart.detail.rarity)
        ArtifactBg.alpha_composite(starsImg,(16,96))
        positions = (159,8)
        for k in dopVaulImg:
            ArtifactBg.alpha_composite(k,(positions))
            positions = (positions[0],positions[1]+28)
        return ArtifactBg
        
    async def artifacAdd(self):
        count = 0
        listArt = {}
        artifacRes = []
        ArtifactNameBg = openFile.ArtifactNameBgTeampleOne.copy()
        for key in self.characters.equipments:
            if key.detail.artifact_name_set == "":
                continue
            if not key.detail.artifact_name_set in listArt:
                listArt[key.detail.artifact_name_set] = 1
            else:
                listArt[key.detail.artifact_name_set] += 1

            imageStats = getIconAdd(key.detail.mainstats.prop_id, icon = True, size = (19,24))
            if not imageStats:
                continue

            count += 1
            
            artifacRes.append(await self.creatArtifact(key,imageStats))
        
        rezArtSet = await self.naborArtifact(listArt,ArtifactNameBg)

        return {"artifact": artifacRes, "nabor": rezArtSet}
        
        
    async def addConst(self,frameConst,constantRes):
        y = 157
        for key in constantRes:
            frameConst.alpha_composite(key ,(2,y))
            y += 84
        return frameConst

    async def addTallants(self,frameTallants,talatsRes):
        y = 342
        for key in talatsRes:
            frameTallants.alpha_composite(key ,(530,y))
            y += 95
        return frameTallants

    async def addArtifact(self,frameArtifact,artifacRes):
        y = 42
        for key in artifacRes:
            frameArtifact.alpha_composite(key ,(1141,y))
            y += 143
        return frameArtifact
        
    async def appedFrame(self,frame,weaponRes,nameRes,statRes,constantRes,talatsRes,artifacRes,artifactSet):
        banner = await self.addConst(frame.convert("RGBA"),constantRes) 
        banner = await self.addTallants(banner,talatsRes)
        banner = await self.addArtifact(banner,artifacRes)
        banner.alpha_composite(weaponRes ,(610,39))
        banner.alpha_composite(nameRes ,(138,646))
        banner.alpha_composite(statRes ,(610,189))
        banner.alpha_composite(artifactSet ,(610,617))
        banner.alpha_composite(self.signatureRes ,(910,747))
        
        return banner

    async def start(self):
        person = self.assets.character(self.characters.id)

        task = []
        try:
            task.append(self.create_picture())
            task.append(self.weaponAdd())
            task.append(self.stats())
            task.append(self.constant())
            task.append(self.talants())
            task.append(self.artifacAdd())

            picture,weapon,stats,const,talants,artifact = await asyncio.gather(*task)
            nameRes = await self.nameBanner(person)
            result =  await self.appedFrame(picture,weapon,nameRes,stats,const,talants,artifact["artifact"],artifact["nabor"])
            
            return result
        
        except Exception as e:
            raise
