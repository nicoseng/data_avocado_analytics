# app.py

import pandas as pd 
from dash import Dash, dcc, html

data = (
    # On récupère avec la méthode .read_csv notre fichier avocado.csv 
    # pour pouvoir lire les données
    pd.read_csv("avocado.csv")
    
    # On filtre avec la méthode .query en sélectionnant uniquement 
    # les colonnes du fichier avocado.csv qui nous intéresse pour le dashboard
    # Ici, on veut simplement sélectionner le type (conventional) et une ville américaine (Albany)
    .query("type == 'conventional' and region == 'Albany'")
    
    # La méthode .assign() permet d'ajouter une nouvelle colonne (ici Date)
    # .assign prend en paramètre un dictionnaire
    # où les clés sont des variables data quelconques, d'où: Date=lambda data 
    # et où les valeurs sont égales à des dates : pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    # La méthode .to_datetime() permet de convertir des données sous forme de date.
    # Ici, on récupère la valeur de data["Date"] et on le convertit en date pour que pandas puisse l'exploiter
    # format="%Y-%m-%d signifie qu'on affiche les dates sous la forme année-mois-jour (%Y-%m-%d)
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    
    # On trie les valeurs par Date
    .sort_values(by="Date")
)
print(data)
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(
                    children="", 
                    className="header-emoji"
                ),
                html.H1(
                    children="Avocado Analytics", 
                    className="header-title"
                ),
                html.P(
                    children=(
                        "Analyse du comportement du prix des avocats et "
                        "le nombre d'avocats vendus dans la ville d'Albany aux USA entre 2015 et 2018"
                    ),
                    className="header-description",
                ),
            ],
            className="header"
        ),
                html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": True}, # Pour activer le mode Bar ou pas (regarder en haut à droite)
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["AveragePrice"],
                                    "type": "lines",
                                    "hovertemplate": ( # Pour afficher qqch quand on passe la souris dessus
                                        "$%{y:.2f}<extra></extra>" # on veut que la valeur soit arrondie à 2 décimales près
                                    ),
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Average Price of Avocados",
                                    "x": 0.05,
                                    "xanchor": "left", #
                                },
                                "xaxis": {"fixedrange": True},#
                                "yaxis": {
                                    "tickprefix": "$", #
                                    "fixedrange": True, #
                                },
                                "colorway": ["#17b897"], #
                            },
                        },
                    ),
                    className="card",
                ),

                # ...

            ],
            className="wrapper",
        )
        

        # dcc.Graph(
        #     figure={ # On veut introduire un graphique
        #         "data": [ # On veut à l'intérieur de ce graphique introduire des données
        #             {
        #                 "x": data["Date"], # Axe des abscisses
        #                 "y": data["AveragePrice"], # Axe des ordonnées
        #                 "type": "lines", # Choix du type de graphique, ici on prend des lignes
        #             },
        #         ],
        #         "layout": {"title": "Évolution du prix de l'avocat entre 2015 et 2018 "} # Titre du graphique
        #     },
        # ),

        # dcc.Graph(
        #     figure={
        #         "data":[
        #             {
        #                 "x": data["Date"],
        #                 "y": data["Total Volume"],
        #                 "type": "lines",
        #             }
        #         ],
        #         "layout":{"title":"Nombre d'avocats vendus entre 2015 et 2018"}
        #     }
        # )
    ]
)

# On exécute notre application Dash localement à l'aide du serveur intégré de Flask
if __name__ == "__main__":
    # Le paramètre debug=True active l'option de rechargement à chaud dans notre application. 
    # Cela signifie que lorsque vous apportez une modification à votre application, 
    # elle se recharge automatiquement, sans que vous ayez à redémarrer le serveur.
    # Elle permet aussi d'afficher les erreurs d'exécution, le cas échéant.
    app.run_server(debug=True) 
