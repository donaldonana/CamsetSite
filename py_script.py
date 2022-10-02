from AppComments.models import Comment
import json


file_name = "1438741079947221.json"

with open(file_name , 'r', encoding='latin-1' ) as handle:
    parsed = json.load(handle)
print("-----------begin-----")
for texte in parsed["commentaires"]:
	c = Comment(categorie=parsed["categorie"] , post_titre = parsed["post_titre"], post_img = parsed["post_img"] , post_url = parsed["post_url"], texte = texte , file_name = file_name )

	c.save()


print("-----------successfuly end----------")
