from pydantic import BaseModel,Field
from typing import List, Optional,Dict
from PIL import Image

class Card(BaseModel):
    name: Optional[str]
    id: Optional[int]
    card: Optional[Image.Image]
    class Config:
        arbitrary_types_allowed = True

class Info(BaseModel):
    uid: Optional[str]
    lang: Optional[str]
    save: Optional[bool]

class EnkaCard(BaseModel):
    info: Optional[Info]
    card: Optional[List[Card]]
    character_id: Optional[List[str]]
    character_name: Optional[List[str]]

    async def get_charter(self, setting = False, name = False):
        if setting:
            card_ids = [str(card.id) for card in self.card]

            if name:
                return {name: id for id, name in zip(self.character_id, self.character_name) if id in card_ids}
            return {id: name for id, name in zip(self.character_id, self.character_name) if id in card_ids}
        
        if name:
            return {name: id for id, name in zip(self.character_id, self.character_name)}
        return {id: name for id, name in zip(self.character_id, self.character_name)}
            
class CardsSet(BaseModel):
    img: Image.Image
    card: List[Card]
    
    class Config:
        arbitrary_types_allowed = True

class Info(BaseModel):
    uid: str
    lang: str
    save: bool

class EnkaCardTeam(BaseModel):
    info: Optional[Info]
    c1_4: Optional[CardsSet]
    c5_8: Optional[CardsSet] 
    character_id: Optional[List[int]]
    character_name: Optional[List[str]]
    
    async def get_charter(self, setting = False, name = False):
        if setting:
            card_ids = [card.id for card in self.c1_4.card + self.c5_8.card]
            if name:
                return {name: str(id) for id, name in zip(self.character_id, self.character_name) if id in card_ids}
            
            return {str(id): name for id, name in zip(self.character_id, self.character_name) if id in card_ids}
        
        if name:
            return {name: str(id) for id, name in zip(self.character_id, self.character_name)}
        return {str(id): name for id, name in zip(self.character_id, self.character_name)}



class Artifact(BaseModel):
    name: Optional[str]
    card: Image.Image
    
    class Config:
        arbitrary_types_allowed = True

class Character(BaseModel):
    name: Optional[str]
    artifact: Optional[List[Artifact]]

class Info(BaseModel):
    uid: Optional[str]
    artifact_type: Optional[List[str]]

class EnkaCardArtifact(BaseModel):
    info: Optional[Info]
    card: Optional[List[Character]]
    
class CharacterInfo(BaseModel):
    name: Optional[str]
    rarity: Optional[int]
    image: Optional[str]
    element: Optional[str]
    id: Optional[str]

class EnkaCardProfile(BaseModel):
    character: Optional[List[CharacterInfo]]
    character_name: Optional[List[str]]
    character_id: Optional[List[str]]
    img: Optional[Image.Image]  # Или Image.Image, если вы хотите хранить изображение в коде, или оставьте как строку URL
    performed: Optional[float]
    
    class Config:
        arbitrary_types_allowed = True

    async def get_charter(self, name = False):
        if name:
            return {name: id for id, name in zip(self.character_id, self.character_name)}
        return {id: name for id, name in zip(self.character_id, self.character_name)}