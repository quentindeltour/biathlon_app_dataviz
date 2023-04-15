# Webapp de dataviz autour du biathlon

Cette app a été créée dans le cadre d'un projet pour le cours de Datavvisualisation à l'ENSAE. 

Le choix du sujet était libre, et j'ai choisi le biathlon car j'aime regarder ce sport et je voulais partager cette passion avec mes camarades. Les données sont celles de la saison 2020-2021.

## Utilisation 

Cette app n'est plus hébergée, il faut donc la lancer localement : 

Pour la mise en place, éxécuter les commandes suivantes : 
```
git clone https://github.com/quentindeltour/biathlon_app_dataviz.git
cd biathlon_app_dataviz
pip install virtualenv
virtualenv env
env\Scripts\activate
pip install -r requirements.txt
```

Un token Mapbox est nécessaire pour lancer l'application : 
Il faudra vous créer un compte Mapbox (si ce n'est pas déja le cas), et récupérer le token gratuit fourni par le site. 
Ensuite, créez un fichier que vous appelerez `.env` au même niveau que le fichier ``app.py`` et le remplir de la manière suivante : 

```
MAPBOX_TOKEN=<VOTRE_TOKEN_ICI>
```

Puis pour lancer l'application, utiliser la commande : 

```
python ./app.py
```

Et vous pouvez ensuite ouvrir la webapp, en utilisant le lien affiché dans votre console ou en vous rendant dans votre navigateur au lien suivant : http://127.0.0.1:8050/ . 



