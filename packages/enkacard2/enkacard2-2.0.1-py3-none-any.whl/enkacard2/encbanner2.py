import asyncio
import aiofiles
import io
from PIL import Image
from enkanetwork import EnkaNetworkAPI, Assets
import os
import datetime
from .src.utils.CreatBannerSix import generationSix
from .src.utils.CreatBannerFive import generationFive
from .src.utils.CreatBannerTree import generationTree
from .src.utils.CreatBannerTwo import generationTwo, creatUserInfo
from .src.utils import CreatBannerOne
from .src.utils.CreatBannerFour import generationFour
from .src.utils.CreatBannerSeven import generationSeven
from .src.utils.userProfile import creatUserProfile
from .src.utils.ArtifactRate import get_artifact_rate
from .src.utils.options import get_charter_id, get_info_enka,get_character_art,get_uid
from .src.utils.openFile import change_Font
from .src.utils.translation import translationLang, supportLang
from .src.modal import enkacardCread
from .enc_error import ENCardError


async def upload():
    async with EnkaNetworkAPI(user_agent= "ENC Library: 2.2.5") as ena:
        await ena.update_assets()



async def saveBanner(uid, image_data, name):
    data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
    path = os.getcwd()
    
    try:
        os.makedirs(f'{path}/EnkaCardImg/{uid}', exist_ok=True)
    except FileExistsError:
        pass
    
    file_name = f"{path}/EnkaCardImg/{uid}/{name}_{data}.png"
    
    async with aiofiles.open(file_name, 'wb') as file:
        if isinstance(image_data, Image.Image):
            img_bytes = io.BytesIO()
            image_data.save(img_bytes, format='PNG')
            await file.write(img_bytes.getvalue())


async def get_signature(template,hide,uid,player,translateLang):
    if template == 1:
        signatureRes = CreatBannerOne.signature(hide,uid)
    elif template == 2:
        signatureRes = await creatUserInfo(hide,uid,player,translateLang)
    else:
        if hide:
            signatureRes = "UID: Hide"
        else:
            signatureRes = f"UID: {uid}"
    
    return signatureRes

async def set_lang(lang):
    if lang != "kh":
        typelang = 0
        assets = Assets(lang=lang)
        lang = lang
        translateLang = translationLang[lang]
        change_Font(0)
    else:
        typelang = 1
        assets = Assets(lang="en")
        lang = "en"
        translateLang = translationLang[lang]
        change_Font(1)
    
    return typelang,assets,lang,translateLang

class ENC:
    def __init__(self,lang = "ru", uid = None, character_art = None,
            character_id = None, hide_uid = False, save = False, nameCards = False, agent = "Library: 2.2.5") :
        self.character_ids = []
        self.character_name = []
        self.USER_AGENT = f"ENC {agent}"
        self.lang  = lang
        self.save = save
        self.img = None
        
        self.nameCards = nameCards
        self.hide_uid = hide_uid
        self.character_id = character_id
        self.uid = uid
        self.character_art = character_art
        
    async def __aenter__(self):
        self.uid = await get_uid(self.uid)
        
        if self.uid is None:
            raise ENCardError(5,"The UIDS parameter must be a number or a string. To pass multiple UIDs, separate them with commas.\nExample: uids = 55363")
        if self.lang in supportLang:
            self.typelang,self.assets,self.lang,self.translateLang = await set_lang(self.lang)
        else:
            self.lang = "en"
        
        self.enc = await get_info_enka(self.uid,self.USER_AGENT,self.lang)

        if self.enc is None:
            raise ENCardError(1001, "Enable display of the showcase in the game or add characters there")
        
        if self.character_id:
            self.character_id = await get_charter_id(self.character_id)
        
        if self.character_art:
            if not isinstance(self.character_art, dict):
                raise ENCardError(4,"The character_art parameter must be a dictionary, where the key is the name of the character, and the parameter is an image.\nExample: character_art = {'1235': 'img.png', '1235': ['img.png','http.../img2.png']} or {'123596': 'img.png', '123854': 'http.../img2.png', ...}")
            else:
                self.character_art = await get_character_art(self.character_art)
        
        return self

    async def __aexit__(self, *args):
        pass
    
    
    def sortingArt(self,result,artifact_type):
        enc_card = {"info": {"uid": self.uid, "artifact_type": artifact_type }, "card": []}

        for character_info in result:
            for name, artifacts in character_info.items():
                artifact_list = []
                for artifact_name, image in artifacts.items():
                    artifact_list.append({"name": artifact_name, "card": image})
                
                enc_card["card"].append({"name": name, "artifact": artifact_list})

        return enkacardCread.EnkaCardArtifact(**enc_card)
    
    def sorting(self,result):
        enc_card = {"info": {
            "uid": self.uid,
            "lang": self.lang,
            "save": self.save
            },
            "card": [], 
            "character_id": self.character_ids,
            "character_name": self.character_name       
        }
        for key in result:
            enc_card["card"].append({"name": key["name"], "id": key["id"], "card": key["card"]})
            
        return enkacardCread.EnkaCard(**enc_card)
    
    async def profile(self, teample = 1, image = True): 
        itog = await creatUserProfile(image,self.enc.player,self.translateLang,self.hide_uid,self.uid,self.assets,teample)

        return enkacardCread.EnkaCardProfile(**itog)

    async def characterImg(self,character_id):
        if str(character_id) in self.character_art:
            self.img = await CreatBannerOne.openUserImg(self.character_art[str(character_id)])
        else:
            self.img = None

    async def artifact(self, artifact_type = ""):
        task = []
        if artifact_type != "":
            if type(artifact_type) == str:
                artifact_type = str(artifact_type).replace(' ', '').split(",")
                artifactTypeList = []
                for key in artifact_type:
                    if key.lower() == "flower":
                        artifactTypeList.append("EQUIP_BRACER")
                    elif key.lower() == "feather":
                        artifactTypeList.append("EQUIP_NECKLACE")

                    elif key.lower() == "sands":
                        artifactTypeList.append("EQUIP_SHOES")

                    elif key.lower() == "goblet":
                        artifactTypeList.append("EQUIP_RING")
                    elif key.lower() == "circlet":
                        artifactTypeList.append("EQUIP_DRESS")
                if len(artifactTypeList) == 0:
                    return ENCardError(10,"Invalid parameter passed: artifact_type\n\nAvailable values: Flower,Feather,Sands,Goblet,Circlet\nTo get all types, leave the field blank.")
            else:
                return ENCardError(10,"Invalid parameter passed: artifact_type\n\nAvailable values: Flower,Feather,Sands,Goblet,Circlet\nTo get all types, leave the field blank.")
        else:
            artifactTypeList = ["EQUIP_BRACER","EQUIP_NECKLACE","EQUIP_SHOES","EQUIP_RING","EQUIP_DRESS"]

        if not self.enc:
            return None
        for charter in self.enc.characters:
            imageCharter = charter.image.icon.url
            if self.character_id:
                if not charter.id in self.character_id:
                    continue
                else:
                    task.append(get_artifact_rate(charter,1,artifactTypeList,imageCharter))
            else:
                task.append(get_artifact_rate(charter,1,artifactTypeList,imageCharter))
        s = await asyncio.gather(*task)
        
        return self.sortingArt(s,artifact_type)

    async def creat(self, template = 1, background = None, cards = None, mini_info = False):

        template = int(template)
        task = []
        if template in [1,2,3,5,7]:
            if not self.enc:
                return None
            
            signatureRes = await get_signature(template,self.hide_uid,self.uid,self.enc.player,self.translateLang)
            
            for key in self.enc.characters:
                self.character_ids.append(key.id)
                self.character_name.append(key.name)
                if self.character_id:
                    if not str(key.id) in self.character_id:
                        continue
                if self.character_art:
                    await self.characterImg(key.id)

                if self.nameCards and template == 2:
                    signatureRes = await creatUserInfo(self.hide_uid,self.enc.player,self.translateLang,key.image.icon.filename.replace("CostumeFloral","").split("AvatarIcon_")[1],self.nameCards)
                
                task.append(self.generation(key,self.img,signatureRes,template,self.enc.player))

            result = await asyncio.gather(*task)
            
            return self.sorting(result)
        
        
        elif template == 6:
            return await self.teampleSix(cards)
        else:
            if background != None:
                background = await CreatBannerOne.openUserImg(background)
            return await self.teampleFour(background,cards,mini_info)

    async def generation(self,charter,img,signatureRes,teample = 1, player = None):
        if teample == 1:
            result = await CreatBannerOne.Creat(charter,self.assets,img,signatureRes,self.translateLang["lvl"]).start()
        elif teample == 2:
            result =  await generationTwo(charter,self.assets,img,signatureRes,self.translateLang)
        elif teample == 5:
            result =  await generationFive(charter,self.assets,img, self.translateLang["lvl"],signatureRes)
        elif teample == 7:
            result =  await generationSeven(charter,self.assets,img, self.translateLang,signatureRes,player, typelang = self.typelang) 
        else:
            result =  await generationTree(charter,self.assets,img,signatureRes,self.translateLang,)
        if self.save:
            await saveBanner(self.uid,result, charter.name)
        return {"uid": self.uid, "name": charter.name, "card": result, "id": charter.id}

    async def teampleSix(self,cards):
        charterList = []
        result = {"1-4": None, "5-8": None}
        task = []
        if type(cards) != dict:
            cards = None
        if not self.enc:
            return None
        if self.hide_uid:
            signatureRes = "UID: Hide"
        else:
            signatureRes = f"UID: {self.uid}"
        for key in self.enc.characters:
            self.character_ids.append(key.id)
            self.character_name.append(key.name)
            if self.character_art:
                await self.characterImg(key.id)
                
            if self.character_id:
                if not str(key.id) in self.character_id:
                    continue
            charterList.append([key,self.img])
            if len(charterList) == 4:
                task.append(generationSix(charterList,self.assets,self.translateLang,signatureRes, cards))
                charterList = []
        if charterList != []:
            task.append(generationSix(charterList,self.assets,self.translateLang,signatureRes, cards))
        if len(task) == 2:
            result["1-4"], result["5-8"] = await asyncio.gather(*task)
        else:
            result["1-4"] = await task[0]  

        if self.save:
            for key in result:
                for image in result[key]["cards"]:
                    await saveBanner(self.uid,result[key]["cards"][image]["img"],image)
                await saveBanner(self.uid,result[key]["img"],key)
                
        c1_4 = {"img": result["1-4"].get("img", None), "card": []}
        for key in result["1-4"]['cards']:
            c1_4["card"].append({"name": key, "id": result["1-4"]['cards'][key]["id"], "card": result["1-4"]['cards'][key]["img"]})
        
        c5_8 = {"img": result["5-8"].get("img", None), "card": []}
        for key in result["5-8"]['cards']:
            c5_8["card"].append({"name": key, "id": result["5-8"]['cards'][key]["id"], "card": result["5-8"]['cards'][key]["img"]})
            
        result = {
            "info": {"uid": self.uid, "lang": self.lang, "save": self.save}, "c1_4": c1_4, "c5_8": c5_8,"character_id": self.character_ids, "character_name": self.character_name
        }
                
        return enkacardCread.EnkaCardTeam(**result)
            
        #return {"uid": self.uid,"card": result, "character_id": self.character_ids, "character_name": self.character_name}

    async def teampleFour(self,background,cards,miniInfo):
        charterList = []
        result = {"1-4": None, "5-8": None}
        task = []
        if type(cards) != dict:
            cards = None
        if self.hide_uid:
            signatureRes = "UID: Hide"
        else:
            signatureRes = f"UID: {self.uid}"
        for key in self.enc.characters:
            self.character_ids.append(key.id)
            self.character_name.append(key.name)
            
            if self.character_art:
                await self.characterImg(key.id)
                
            if self.character_id:
                if not str(key.id) in self.character_id:
                    continue
            charterList.append([key,self.img])
            if len(charterList) == 4:
                task.append(generationFour(charterList,self.assets,self.translateLang,miniInfo,self.enc.player.nickname,signatureRes, background, cards))
                charterList = []
        if charterList != []:
            task.append(generationFour(charterList,self.assets,self.translateLang,miniInfo,self.enc.player.nickname,signatureRes,background, cards))
        if len(task) == 2:
            result["1-4"], result["5-8"] = await asyncio.gather(*task)
        else:
            result["1-4"] = await task[0]  

        if self.save:
            for key in result:
                for image in result[key]["cards"]:
                    await saveBanner(self.uid,result[key]["cards"][image]["img"],image)
                await saveBanner(self.uid,result[key]["img"],key)
                
        c1_4 = {"img": result["1-4"].get("img", None), "card": []}
        for key in result["1-4"]['cards']:
            c1_4["card"].append({"name": key, "id": result["1-4"]['cards'][key]["id"], "card": result["1-4"]['cards'][key]["img"]})
        
        c5_8 = {"img": result["5-8"].get("img", None), "card": []}
        for key in result["5-8"]['cards']:
            c5_8["card"].append({"name": key, "id": result["5-8"]['cards'][key]["id"], "card": result["5-8"]['cards'][key]["img"]})
            
        result = {
            "info": {"uid": self.uid, "lang": self.lang, "save": self.save}, "c1_4": c1_4, "c5_8": c5_8,"character_id": self.character_ids, "character_name": self.character_name
        }
                
        return enkacardCread.EnkaCardTeam(**result)


