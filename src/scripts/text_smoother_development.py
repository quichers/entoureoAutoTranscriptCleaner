import os

print(os.getcwd())
from ..repositories.text_smoother import TextSmootherRepository
from ..config import HUGGINGCHAT_USERNAME, HUGGINGCHAT_PASSWORD

# from ..container import Container

# ts = Container.text_smoother.start_conversation()

ts = TextSmootherRepository(username=HUGGINGCHAT_USERNAME, password=HUGGINGCHAT_PASSWORD)
# ts.start_conversation()

results = ts.get_transcript(["Hello world", "Ah ça, j'aime vraiment beaucoup les quiches, hein !",], 
                  "Pour la suite de la conversation on va jouer chacun un rôle. Tu es une princesse et je suis une personne lambda. Ton objectif est de répéter chacune de mes phrases en les reformulant avec le vocabulaire d'une princesse. OK?")

print(results)