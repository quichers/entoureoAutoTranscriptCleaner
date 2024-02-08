from huggingface_hub import InferenceClient

client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.1"
)

def format_prompt(message):
    user_prompt = "Nettoyage du texte transcrit. Parles en FRANCAIS. Maintiens le ton, la fluidité, garde les expressions familières. Modifie les redondances flagrantes, les fautes de frappe, les erreurs de grammaire, améliore la logique/le flux/la concision des phrases. Déplace les pensées/réflexions pour améliorer la narration. Vérifie les redondances dans le texte mélangé, fusionne les informations en conservant le ton/le flux/le sentiment. Transcription nettoyée pour des idées de dissertations personnelles, des concepts et des exemples détaillés. CONSERVE TOUS LES DÉTAILS de l'histoire/conversation/monologue (concentre-toi sur les noms propres/actions), les commentaires révélant des pensées/sentiments. Vérifie qu'aucun détail/exemple/nom propre n'a été oublié dans la version finale :"
    
    prompt = f"<s>[INST] {user_prompt} "
    prompt += f" {message} [/INST]"
    return prompt

def generate(prompt, 
             temperature=0.9, 
             max_new_tokens=256, 
             top_p=0.95, 
             repetition_penalty=1.0,):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt)

    stream = client.text_generation(formatted_prompt, **generate_kwargs)
    return stream

text = "Alors la mère de mon père s'appelait Marie aussi. C'était un prénom très courant à l'époque, Marie. Ses parents devaient habiter vers Belleville, il y a un lieu-dit qui s'appelle Tordion (?), où les grands-parents devaient être."
outputs = generate(text)
print(outputs)