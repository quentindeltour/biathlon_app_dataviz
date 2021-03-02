import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import os

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from make_plots import draw_map_sites, draw_ski_shoot_from_df_H, draw_ski_shoot_from_df_F,draw_PU_SP_correlation_from_groupby, draw_tv_audiences_tnt_tf1
from make_plots import draw_medals_indiv_JO_F, draw_medals_indiv_JO_H, draw_medals_pays, draw_win_by_season, make_comparaison

# PLOT MEDAILLES JO
jo_all = pd.read_csv('./data/classement_jo_all_time.csv')
jo_pays_all = draw_medals_pays(jo_all, "Nombre de médailles aux Jeux Olympiques d'Hiver")

#PLOT WIN BY SEASON
df_barchart_win_season = pd.read_csv('./data/victoires_par_saison_pays_top_4.csv')
barchart_win_season = draw_win_by_season(df_barchart_win_season)

#PLOT COMPARAISON FOURCADE BJOERNDALEN
mf_ole_comparaison = pd.read_csv('./data/mf_ole_comparaison.csv')
plot_comparaison_H = make_comparaison(mf_ole_comparaison)

#PLOT COMPARAISON NEUNER FORSBERG
mn_mf_comparaison = pd.read_csv('./data/mn_mf_comparaison.csv')
plot_comparaison_F = make_comparaison(mn_mf_comparaison, sexe='F')

#MAP SITES COUPE DU MONDE
#TOKEN = os.getenv("MAPBOX_TOKEN") #local
#TOKEN = os.environ['MAPBOX_TOKEN'] #deploy
#map = draw_map_sites(TOKEN)

#SCATTER PERFORMANCES SKI SHOOT
df_H = pd.read_csv('./data/ski_shoot_2021_H.csv')
df_F = pd.read_csv('./data/ski_shoot_2021_F.csv')

scatter_H = draw_ski_shoot_from_df_H(df_H)
scatter_F = draw_ski_shoot_from_df_F(df_F)

# LINE SCATTER POURSUITE H F 
poursuite = pd.read_csv('./data/poursuite_plot.csv')
plot_poursuite = draw_PU_SP_correlation_from_groupby(poursuite)

#AUDIENCES

audiences = pd.read_csv('./data/audiences.csv')
plot_audiences_spec = draw_tv_audiences_tnt_tf1(audiences, y='TlspMoyen', tf1=True)
plot_audiences_pda = draw_tv_audiences_tnt_tf1(audiences, tf1=True, y='PdA')

# CH MONDE 2021

ch_monde_2021 = pd.read_csv('./data/ch_mond_2021.csv')
table = dbc.Table.from_dataframe(ch_monde_2021, striped=True, bordered=True, hover=True, size='sm')



app = dash.Dash(__name__,
    external_stylesheets=[
        dbc.themes.CERULEAN,
        {"href":"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "rel":"stylesheet"},
        'https://use.fontawesome.com/releases/v5.9.0/css/all.css'
    ],
    title='La France dans le monde du biathlon',
    update_title='En cours de chargement...',
    meta_tags=[{"name": "viewport", "content": "width=device-width", "charset":"utf-8"},]
)

server = app.server

#HEADER LAYOUT 


#PAGE ACCEUIL :

acceuil_layout=dbc.Row(
    dbc.Col(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H1("La France, une grande nation du biathlon ? ",className='custom-heading-primary-main'),
                                    html.H1("Découvrez l'histoire de ce sport, et la place qu'y jouent les Français", className="custom-heading-primary-sub")
                                ],
                                className='custom-heading-primary'
                            ),
                            dbc.Button("Commencer l'histoire", color="light", className="mr-1", href="#introduction",external_link=True),
                        ],
                        className='text-box'
                    ),
                ],
                className='header'
            ),
        ], width={"size":12, "offset":0}
    )
)


# Intro LAYOUT
introduction_layout = html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1('La France et le biathlon'),
                                html.Hr(),
                                html.P(
                                    [
                                        "Le Biathlon est un sport mêlant deux disciplines : le tir à la carabine, et le ski de fond.",
                                        html.Br(),
                                        "Il est très populaire dans les pays du Nord de l'Europe, mais est moins connu en France par exemple.",
                                        html.Br(),
                                        "Nous allons essayer de situer la France dans le monde du Biathlon, en la comparant aux autre pays !"
                                    ]
                                )
                            ], width={"size":10, "offset":1}
                        )
                    ]
                )
            ],
        ),
    ], id='introduction'
)


#HISTORIQUE BIATHLON : 

historique_layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H1('Origine du biathlon', className='card-title'),
                            html.Hr(),
                            html.P("Il a été créé par Oscar Wergeland en Norvège à la fin du 19ème siècle. Ce dernier souhaitait un exercice qui combine le ski et le tir pour créer une nouvelle entité militaire : "
                                "les patrouilles à ski. Ces patrouilles participèrent à la première guerre mondiale."),
                            html.P("En 1924, lors des premiers jeux Olympiques d'Hiver à Chamonix, une discipline nommée patrouille militaire est crée. "
                                "Elle n'aura lieu qu'une fois, et sera remplacée par des démonstrations à partir de 1928. "
                                "Les patrouilles à ski furent à nouveau utilisées lors de la seconde guerre mondiale, et furent même l'objet de campagnes de propagande."),
                            html.P("En 1960, les jeux Olympiques reconnaissent officiellement une nouvelle épreuve, appelée biathlon. Bien que désormais dénué de sens militaire, il en a conservé les charactéristiques : l'enchainement rapide entre l'effort physique (le ski) et l'effort mental (le tir.)"),
                            html.Br(),
                            dbc.Button("Vidéo expliquant l'origine de ce sport", color="primary", className="mr-1",
                                        href="https://www.youtube.com/watch?v=14NTlDvmzyc",
                                        target="_blank",
                            ),
                        ],
                    ),
                ),
            ]),
        ],),
    ],
)

collapse_histoire = html.Div(
    [
        dbc.Button(
            "Découvrir l'origine du biathon",
            id="collapse-button",
            className="mb-3",
            color="primary",
        ),
        dbc.Collapse(
            historique_layout,
            id="collapse",
        ),
    ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


#DEROULEMENT COURSE :

deroulement_layout = html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Row([
                    dbc.Col(
                        [
                            html.H1("Qu'est ce que le biathlon ?"),
                            html.Hr(),
                            html.P(
                                [
                                    "Une course de biathlon est composée d'un enchainement de tour de piste qui varie de 2 à 4 kilomètres en ski de fond, "
                                    "chaque tour étant séparé par un passage sur le pas de tir. Lors de chaque tir, les athlètes doivent blanchir 5 cibles situées à une distance de 50 mètres."
                                    " Les tirs sont alternés entre debout et couchés. Le diamètre de la cible à viser est de 4.5cm pour un tir couché, contre 11.5cm pour un tir debout.",
                                ]
                            ),
                            html.P(
                                [
                                    "Lorsque les athlètes ratent une cible, une pénalité leur est infligée. Celle ci peut être un rajout de parcours (appelé tour de pénalité) "
                                    "ou un rajout de temps en fonction de la course."
                                ]
                            ),
                            html.P("Lorsqu'ils s'élancent, les biathlètes sont préparés à un effort pouvant aller d'une vingtaine de minutes à quasiment une heure, selon les courses. "),
                        ]
                    , width={"size":4, "offset":1}),
                    dbc.Col(
                        [
                            html.Img(src="/assets/images/KD_on_unsplash.jpg", className='resize-bis'),
                            html.P([
                                "Crédit photo : ",
                                html.A('KD on unsplash', href="https://unsplash.com/@k_d?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText")],)
                        ], width={"size":6, "offset":0}
                    )
                ],),
                dbc.Row(dbc.Col([collapse_histoire], width={"size":10, "offset":1}))
            ],
        ),
    ],
    id="deroulement"
)

# COURSES :
popover_poursuite = html.Div(
    [
        dbc.Button(
            "Est ce que la poursuite est jouée d'avance ?", id="popover-target", color="primary"
        ),
        dbc.Popover(
            [
                dbc.PopoverBody(
                    [
                        dbc.Card(
                            dcc.Graph(
                                id='poursuite_plot',
                                figure=plot_poursuite
                            ),
                        )
                    ]
                ),
            ],
            id="popover",
            is_open=False,
            target="popover-target",
        ),
    ]
)


@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

courses_layout = html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1('Les différentes courses au biathlon'),
                            html.Hr(),
                            html.P("Au biathlon, chaque athlète représente sa nation, et non des sponsors comme au cyclisme par exemple."),
                            html.P([
                                "Chacune de ces courses permets aux athlètes de marquer des points pour le classement général de la coupe du monde, qui décèrne le gros globe à son vainqueur.",
                                html.Br(),
                                "Il existe également un classement pour chacune des spécialités, qui détermine le vainqueur des petits globes."
                            ]),
                        ], width={"size":10, "offset":1}
                    )
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.CardDeck(
                                    [
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H2("Les courses individuelles", className='card-title'),
                                                    html.Hr(),
                                                    html.P([
                                                        html.Strong("Le Sprint"),
                                                        " : Course contre la montre d'une distance totale de 10 km chez les Hommes (7,5km chez les Femmes), entrecoupés de 2 tirs (un couché et un debout).",
                                                        html.Br(),
                                                        "Chaque balle ratée impose un tour de pénalité de 150 mètres supplémentaires à effectuer à ski.",
                                                        html.Br(),
                                                        "Son classement final détermine l'ordre de départ de ",
                                                        html.Strong("la poursuite"),
                                                    ], className='class-text'),
                                                    html.Hr(),
                                                    html.P([
                                                        html.Strong("La poursuite"),
                                                        " : Les 60 meilleurs athlètes du sprint partent pour une course en confrontation directe, en gardant les écarts finaux du sprint.",
                                                        html.Br(),
                                                        "La course dure 12.5km (10km chez les Femmes) entrecoupées de 4 tirs (2 couchés puis 2 debouts). "
                                                        "La pénalité est la même que pour le sprint (150m de pénalité).",
                                                    ],className='class-text'),
                                                    popover_poursuite,
                                                    html.Hr(),
                                                    html.P([
                                                        html.Strong("L'individuel"),
                                                        " : La course la plus longue du biathlon : un contre la montre de 20km (15km pour les femmes) avec 4 tirs (couché et debout alternés).",
                                                        html.Br(),
                                                        dbc.Alert(
                                                            [
                                                                html.Strong("Particularité"),
                                                                " : Chaque balle ratée entraine une pénalité de 60 secondes sur le temps final, mais pas de tour de pénalité."
                                                            ], color="warning"
                                                        )   
                                                    ], className='class-text'),
                                                    html.Hr(),
                                                    html.P([
                                                        html.Strong("La massstart"),
                                                        " : Course en confrontation directe entre les 25 meilleurs athlètes.",
                                                        html.Br(),
                                                        "Le vainqueur est le premier athlète à franchir la ligne d'arrivée au bout des 15 km (12.5 pour les femmes)"
                                                        " et 4 tirs (2 couchés puis 2 debouts). La pénalité est la même que pour le sprint et la poursuite (150m de pénalité)."
                                                    ], className='class-text')
                                                ]
                                            )
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                [                        
                                                    html.H2("Les courses par équipes"),
                                                    html.Hr(),
                                                    dbc.Alert(
                                                        [
                                                            html.Strong('Particularité des relais'),
                                                            " : Chaque athlète dispose de 3 balles supplémentaires par tir (appelées balles de pioches) pour blanchir ses 5 cibles"
                                                        ], color="warning"
                                                    ),
                                                    html.Hr(),
                                                    html.P([
                                                        html.Strong("Le Relais Simple Hommes et Femmes"),
                                                        " : Chaque pays aligne une équipe de 4 athlètes de même sexe qui vont s'affrontent dans un relais."
                                                        "Chacun des athlètes réalise 3 boucles de 2.5km (2km chez les Femmes) coupés par 2 tirs (1 couché puis un debout) avant de passer le relais."
                                                    ]),
                                                    html.Hr(),
                                                    html.P([
                                                        html.Strong("La Relais Mixte"),
                                                        " : Chaque pays aligne une équipe composé de 2 Hommes et 2 Femmes. La course est identique au relais simple."
                                                        "L'ordre de passage ainsi que les distances parcourues dépend des organisateurs."
                                                    ]),
                                                    html.Hr(),
                                                    html.P([
                                                        html.Strong("Le relais Mixte Simple"),
                                                        " : La dernière course créée par la fédération internationale, avec son introduction lors de la saison 2014/2015.",
                                                        html.Br(),
                                                        "Chaque équipe est composée d'un Homme et d'une Femme d'un même pays, et qui effectuent 2 relais chacun."
                                                        "Chaque relais est composé de 2 boucles de 1.5km avec 2 tirs (couché puis debout), sauf le dernier relayeur qui effectue un tour de piste supplémentaire "
                                                        "avant de passer la ligne d'arrivée.",
                                                        html.Br(),
                                                        "Pour des raisons d'équité, les organisateurs alternent entre Hommes et Femmes pour décider qui termine la course"
                                                    ]),
                                                ],
                                            ),
                                        )
                                    ],
                                )
                            ],width={"size":10, "offset":1}
                        ),
                    ]
                ),
            ],
        ),
    ],
    id='courses'
)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "10rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#e9ecef",
}

navbar = html.Div(
    [
        html.H4("Biathlon"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Acceuil", href="#", active="exact", external_link=True),
                dbc.NavLink("Introduction", href="#introduction", active="exact", external_link=True),
                dbc.NavLink("Biathlon", href="#deroulement", active="exact", external_link=True),
                dbc.NavLink("Résultats", href="#sport", active="exact", external_link=True),
                dbc.NavLink("Audiences", href="#audiences", active="exact", external_link=True),
                dbc.NavLink("Conclusion", href="#conclusion", active="exact", external_link=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


map_layout = html.Div(
    [
        dcc.Graph(
            id='map_sites',
            #figure=map
        )
    ],
    id='map'
)
sites_map_layout = html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("Une saison au biathlon"),
                                html.Hr(),
                                html.P(
                                    [
                                        "Une saison de biathlon prend généralement place entre la fin du mois de novembre et le mois de mars de l'année suivante. "
                                        "Elle est composée de plusieurs étapes, ayant lieu sur des sites différents (dans différents pays). ",
                                        html.Br(),
                                        "Parmi ces étapes, les championnats du monde ont lieu en février, et décèrnent les titres de champions du monde de chaque spécialité.",
                                        html.Br(),
                                        "Tous les 4 ans, les JO d'hiver viennent remplacer les championnats du monde, et décèrnent les titres olympiques. ",
                                        html.Br(),
                                        "A la fin de la saison, le classement général de la coupe du monde décèrne le ",
                                        html.Strong("gros globe de cristal"),
                                        " au meilleur athlète de la saison, ainsi que les ",
                                        html.Strong('petits globes de cristal'),
                                        " pour chacune des spécialités. "
                                        "Le calendrier est aménagé pour que les sites ayant de la neige plus tôt dans la saison soient ceux qui accueillent les premières courses, tandis que les sites moins bien enneigés accueillent les courses en milieu de saison. "
                                        "Chaque site n'organise qu'une partie de toutes les courses possibles. Il n'y à qu'aux Championnats du Monde et aux JO que toutes les courses sont enchainées.",
                                        html.Br(),
                                        "Cette saison, le calendrier à été modifié à cause du Covid, et certaines étapes (dont celle du Grand-Bornand) ont été remplacées."
                                    ]
                                ),
                                html.P([
                                    "La France dispose de son site pour accueillir les compétitions de biathlon (Annecy-Le Grand Bornand), et sa bonne organisation en 2019 lui permet d'être programmé pour les 3 prochaines saisons, "
                                    "même s'il est utilisé moins souvent que d'autres sites mythiques tels que Ruhpolding en Allemagne, surnommée la mecque du biathlon"
                                ]),
                                dbc.Alert([ 
                                    html.Div([
                                        html.Span(html.Strong(['Site de biathlon ',html.Span(className="flag-icon flag-icon-fr"), ' : ']),),
                                        html.Span(className="fa fa-star checked"),
                                        html.Span(className="fa fa-star checked"),
                                        html.Span(className="fa fa-star checked"),
                                        html.Span(className="fa fa-star checked"),
                                        html.Span(className="fa fa-star"),
                                ]),],color='info'),
                            ],width={"size":4, "offset":1}
                        ),
                        dbc.Col(map_layout, width={"size":6, "offset":0})
                    ],
                ),
            ],
        ),
    ],
    id='blabla_sites'
)



performance_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Quid de cette saison ? "),
                        html.Hr(),
                        html.P([
                            "En fin de saison dernière, Martin Fourcade à décidé de mettre un terme à sa carrière."
                            "Au vu de son palmarès le placant parmi les 2 plus grands biathlètes de l'Histoire, il est légitime de se demander ce qu'il va se passer"
                            " maintenant qu'il a pris sa retraite.",
                            html.Br(),
                            "Je ne vous en dit pas trop, mais la relève est assurée!"
                        ]),
                        html.P(
                            [
                                "Comme tout sport composé de plusieurs disciplines, il est nécessaire au biathlon d'être performant à la fois au tir et sur les skis. "
                                "Nous allons analyser les données de l'IBU, qui met à disposition les statistiques de tirs et de ski des athlètes pour en avoir le coeur net."
                                "Cette analyse porte sur tous les biathlètes ayant concouru pour la coupe du monde 2020/2021."
                            ]
                        )
                    ], width={"size":10, "offset":1}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Tabs(id='tabs-performance-ho-fe', active_tab='tab-ho', children=[
                            dbc.Tab(label='Hommes', tab_id='tab-ho'),
                            dbc.Tab(label='Femmes', tab_id='tab-fe'),
                            ]),
                    ], width={"size":10, "offset":1}
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col([html.Div(id='tabs-plot-performance-ho-fe')],width={"size":5, "offset":1}),
                dbc.Col([html.Div(id="tabs-text-performance-ho-fe")],width={"size":4, "offset":1})
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            [
                                "Deux elements ressortent de ces visualisations :"
                            ],
                        ),
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem(["Premièrement, il faut faire partie des meilleurs en skis pour jouer la victoire au classement général. Martin Fourcade était le meilleur sur les skis, "
                                "ce qui combiné à son excellent tir lui à permis de remporter tant de gros globes et de victoires."]),
                                dbc.ListGroupItem("Deuièmement, cette saison à clairement été dominée par les Norvégiens : ils sont aux trois premières places chez les Hommes, et première et troisième chez les femmes.")
                            ]
                        ),
                    ], width={"size":5, "offset":1}
                ),
                dbc.Col(
                    [
                        html.P("Cette tendance peut se confirmer en regadant les résultats des derniers championnats du monde : ",),
                        table
                    ], width={"size":4, "offset":1}
                )
            ]
        ),
        dbc.Row(dbc.Col(                        
            html.P(
                [
                    "La Norvège à donc largement dominé le biathlon mondial cette saison, chez les Hommes et chez les Femmes et dans les relais. ",
                    html.Br(),
                    "Néanmoins, la France continue de se positionner comme l'adversaire numéro un de la Norvège, comme l'ont montré les derniers championnats du monde."
                ]
            ), width={"size":10, "offset":1}
        ))
    ],
    id='performance'
)


@app.callback([Output("tabs-plot-performance-ho-fe", "children"),Output("tabs-text-performance-ho-fe", "children")], [Input("tabs-performance-ho-fe", "active_tab")])
def switch_tab(at):
    if at == "tab-ho":
        plot = html.Div([
            dcc.Graph(
                id='scatter_H',
                figure=scatter_H
            ),
        ])
        text = html.Div(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.P(
                                [
                                    "Chez les Hommes, Johannes Boe est en tête du classement de la coupe du monde, notamment grâce à ses excellentes performances sur les skis et ce marlgré une certaine irrégularité sur le pas de tir.",
                                    html.Br(),
                                    "A son opposée, la jeune surprise de la saison Sturla Holm Laegrid excelle au tir et est régulier sur les skis, ce qui lui permet d'être toujours bien placé et à la deuxième place du classement général.",
                                    html.Br(),
                                    "Côté Français, Quentin Fillon Maillet et Emilien Jacquelin sont respectivement 4eme et 6eme. Leurs temps de ski et leur performance au tir sont bons, mais pas suffisant pour aller jouer la victoire au classement général cette saison."
                                    "A l'heure ou j'écris, Quentin peut encore se battre pour une 3ème place au classement général, et Emilien pour le petit globe de la poursuite.",
                                    dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Résultats des Hommes ', html.Span(className="flag-icon flag-icon-fr"), ' cette saison: ']),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star"),
                            ]),],color='info'),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        )
        return plot, text
    elif at == "tab-fe":
        plot = html.Div([
            dcc.Graph(
                id='scatter_F',
                figure=scatter_F
            )
        ])
        text = html.Div(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.P(
                                [
                                    "Chez les Femmes, Tiril Eckhoff est en tête de la coupe du monde grâce à son aisance sur les skis, malgré des statistiques de tir à peine au dessus de la moyenne."
                                    "Certaines filles sont moins performantes sur les skis mais plus précises au tir commme Hannah Oeberg qui est actuellement deuxième au classement général",
                                    html.Br(),
                                    "Pour les Française, la saison à été plus compliquée. Cela semble être dû à une performance globale très moyenne au tir, puisque seule Anais Bescond "
                                    "est au dessus de la moyenne des biathlètes du circuit."
                                    "Julia Simon à été capable de belles victoires sur des Mass Starts qui lui permette de concourir pour le petit globe de la spécialité.",
                                    dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Résultats des Femmes ',html.Span(className="flag-icon flag-icon-fr"), ' cette saison : ']),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star"),
                                html.Span(className="fa fa-star"),
                            ]),],color='info'),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        )
        return plot, text
    return html.P("This shouldn't ever be displayed...")

sport_layout = html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("Les performances sportives"),
                                html.Hr(),
                                html.P(["La France fait partie des 4 pays ayant récolté le plus de médailles aux Jeux Olympiques de biathlon, mais est loin derrière la Norvège, la Russie et l'Allemagne"
                                    "et ce malgré les nombreux changements géopolitiques. Par exemple, le compte de médaille de la Russie est divisé en trois, entre l'URSS, la Russie moderne et l'équipe de l'ex URSS, qui à été utilisé lors des JO de 1992.",
                                    dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Résultats sportifs ',html.Span(className="flag-icon flag-icon-fr"),' de tous les temps : ']),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star"),
                            ]),],color='info'),
                                ]),
                            ],width={"size":4, "offset":1}
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                figure=jo_pays_all 
                                ),
                            ],width={"size":5, "offset":0}
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("Décomposition temporelle"),
                                html.Hr(),
                                html.P([
                                    "Rentrons un peu dans le détail. Le biathlon à beaucoup évolué dans le temps. En 1960, il n'y avait que ",
                                    html.Strong("l'individuel"),
                                    " et une course par équipe. Comme nous l'avons vu, il y a maintenant bien plus de courses. "
                                    "Le graphique que nous avons vu plus haut cache cependant des disparités. "
                                    "La France à été médaillé lors de l'édition des JO 1924, mais à ensuite dû attendre 1992 pour obtenir une nouvelle médaille.",
                                    dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Résultats sportifs ',html.Span(className="flag-icon flag-icon-fr"), ' avant 1992 : ']),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star "),
                                html.Span(className="fa fa-star "),
                                html.Span(className="fa fa-star"),
                                html.Span(className="fa fa-star"),
                            ]),],color='info'),
                                    "Au contraire, depuis les années 2000, la France semble clairement rivaliser avec les autres grandes nations, voir être la plus forte chez les Hommes notamment.",
                                    html.Br(),
                                    "Le graphique à droite montre que la France à été la Nation qui à gagné le plus de courses plusieurs fois, et à souvent rivalisé avec la Norvège."
                                    "A l'inverse, la Russie et l'Allemagne semblent légèrement sur le déclin, notamment sur ces 3 dernières saisons.",
                                    dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Résultats sportifs ',html.Span(className="flag-icon flag-icon-fr"), ' depuis 2000 : ']),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                            ]),],color='info'),
                                ]),
                            ],width={"size":5, "offset":1}
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    figure=barchart_win_season
                                ),
                            ],width={"size":5, "offset":0}
                        ),
                    ],
                ),
                html.Br(),
                dbc.Row(dbc.Col(
                    [
                        html.H1("Les performances sportives individuelles"),
                        html.Hr(),
                        html.P(
                            [
                                "Nous avons jusqu'ici beaucoup parlé de pays. Comme n'importe quel sport, ce sont avant tout des athlètes.",
                                html.Br(),
                                "Nous allons maintenant nous intéresser à certains des plus grands (voir les plus grands) biathlètes de l'Histoire, à la fois chez les Hommes et chez les Femmes."
                            ]
                        )
                    ],width={"size":10, "offset":1})
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2('Hommes', style={'textAlign':'center'}),
                                html.P(
                                    [
                                        "Du côté des Hommes, deux noms ressortent loin en tête: Ole Einar Bjoerndalen et Martin Fourcade. "
                                        "Nous allons comparer les palmarès de ces 2 champions."
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                            html.Div([
                                                html.Img(src='./assets/images/olebjo.jpg', className='resize',alt='Ole Einar Bjoerndalen', title='Ole Einar Bjoerndalen'),
                                            ]),
                                            html.Div([
                                                html.H4([html.Div([html.Span(className="flag-icon flag-icon-no"),' Ole Einar'], style={"marginLeft":"15px"}), html.Div('Bjoerndalen', style={"marginLeft":"20px"})]),
                                                html.P(["47 ans", html.Br(), "Actif de 1993 à 2018"]),
                                            ])
                                            ],
                                            width={"size":4, "offset":2}),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                                html.Img(src='./assets/images/marfou.jpg',className='resize', alt='Martin Fourcade', title='Martin Fourcade'),
                                                            html.Div([
                                                html.H4([html.Div([html.Span(className="flag-icon flag-icon-fr"),' Martin'], style={"marginLeft":"30px"}), html.Div('Fourcade', style={"marginLeft":"32px"})]),
                                                                html.P(["32 ans", html.Br(), "Actif de 2008 à 2020"]),
                                                            ])
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            width={'size':4,"offset":1}
                                        ),
                                    ]
                                ),
                                dcc.Graph(figure=plot_comparaison_H)
                            ], width={"size":5, "offset":1}, className='column-left'
                        ),
                        dbc.Col(
                            [
                                html.H2('Femmes', style={'text-align':'center'}),
                                html.P(
                                    [
                                        "Du côté des Femmes, le choix est moins évident. D'autres athlètes méritaient d'y figurer, comme Liv Poirée ou Uschi Disl par exemple, mais je ne pouvais en garder que 2."
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src='./assets/images/magfor.jpg',className='resize', alt='Magdalena Forsberg', title='Magdalena Forsberg'),
                                                    html.Div(
                                                        [
                                                            html.H4([html.Div([html.Span(className="flag-icon flag-icon-se"),' Magdalena'], style={"marginLeft":"3px"}), html.Div('Forsberg', style={"marginLeft":"42px"})]),
                                                                    html.P(["53 ans", html.Br(), "Active de 1994 à 2002"]),
                                                        ]
                                                    )
                                                ]
                                            ),
                                            width={'size':4,'offset':3 }                                        
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src='./assets/images/Magdalena_Neuner.jpg',className='resize', alt='Magdalena Neuner', title='Magdalena Neuner'),
                                                    html.Div(
                                                        [
                                                            html.H4([html.Div([html.Span(className="flag-icon flag-icon-de"),' Magdalena'], style={"marginLeft":"1px"}), html.Div('Neuner', style={"marginLeft":"50px"})]),
                                                            html.P(["34 ans", html.Br(), "Active de 2006 à 2012"]),
                                                        ]
                                                    )
                                                ]
                                            ),
                                            width={'size':4,"offset":1}
                                        )
                                    ],
                                ),
                                dcc.Graph(figure=plot_comparaison_F)
                            ], width={"size":5, "offset":0}
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row(dbc.Col(
                    [
                        html.P(
                            [
                                "En plus de Martin Fourcade (qui est tout de même le Francais le plus titré aux Jeux Olympiques, été et hiver confondus),"
                                "la France compte de nombreux autres athlètes ayant réussi de grandes carrières.",
                                html.Br(),
                                "Chez les Hommes, Raphael Poirée à gagné la Coupe du Monde à 4 reprises au début des années 2000, "
                                "Vincent Defrasne est champion olympique",
                                html.Br(),
                                "Chez les Femmes, Marie Dorin Habert à gagné de nombreux titres modiaux et terminé à la deuxième place de la coupe du monde lors de la saison 2015/2016",
                                html.Br(),
                                "Et plein d'autres encore..."
                            ]
                        ),
                        dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Individualités ',html.Span(className="flag-icon flag-icon-fr"), " : "]),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                            ]),],color='info'),
                    ], width={"size":10, "offset":1}
                )),
            ]
        ),
        dbc.Jumbotron(
            [
                performance_layout
            ]
        )
    ],
    id="sport"
)


audiences_layout = html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("Audiences télévisuelles"),
                                html.Hr(),
                                html.P([
                                    "En France, la chaine l'Equipe diffuse les commpétitions de biathlon depuis 2015, et jusqu'en 2022 au moins."
                                    "Grâce à des commentateurs et des analystes de qualité, ils ont fait du biathlon un sport populaire."
                                    "Le biathlon réalise les meilleurs scores d'audience de la chaine et est le sport le plus regardé sur les chaines non traditionnelles."
                                    "En revanche, il n'a pas (encore) la portée des sports tels que le Football ou le Rugby, qui sont diffusés sur les grandes chaînes nationales, "
                                    "et font toujours des cartons en terme d'audiences"
                                ]),
                                html.P(
                                    [
                                        "Cependant, si les scors d'audiences du biathlon en France sont bons, ils sont très éloignés des scores réalisés dans d'autres pays"
                                        "tels que l'Allemagne et la Norvège par exemple.",
                                        html.Br(),
                                        "En Norvège, le biathlon est diffusé sur la plus grand chaine de télévision du pays (NRK). Lors des derniers championnat du monde, la chaîne"
                                        " à atteint un pic avec 85% d'audiences nationales.",
                                        html.Br(),
                                        "En allemagne, ils sont diffusés sur la première chaine nationale, l'ARD, et ont dépassé les 5 millions de téléspectateurs en même temps lors des dernires chammpionnats du monde."
                                    ],
                                ),
                                html.P([
                                    "Un autre point important à noter, est que les courses les plus récemment créés, i.e. la poursuite, la massstart ainsi que les relais"
                                    "sont les courses qui ont le plus de succès en termes d'audiences"
                                    "La raison est simple, ce sont des courses en confrontation directe, ce qui les rend beaucoup plus facilement compréhensibles par un public non avisé."
                                    "Ce sont également des courses très rythmées, avec de nombreu rebondissements."
                                    "A l'inverse, l'individuel est beaucoup plus difficile à suivre."
                                ]),
                                dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Audiences TV en ',html.Span(className="flag-icon flag-icon-fr"), ' : ']),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star"),
                            ]),],color='info'),
                            ],width={"size":4, "offset":1}
                        ),
                        dbc.Col(
                                    [
                                        dbc.Tabs(id='tabs-audiences', active_tab='tab-spec', children=[
                                            dbc.Tab(label="Téléspectateurs Moyens", tab_id='tab-spec'),
                                            dbc.Tab(label="Part d'audiences", tab_id='tab-pda'),
                                            ]),
                                        html.Div(id='tabs-plot-audiences'),
                                    ]
                                ,width={"size":6, "offset":0}
                        )
                    ],
                ),                
            ],
        ),
    ],
    id='audiences'
)

@app.callback(Output('tabs-plot-audiences', 'children'),
              Input('tabs-audiences', 'active_tab'))
def render_content(tab):
    if tab == 'tab-spec':
        return html.Div([
            dcc.Graph(
            figure=draw_tv_audiences_tnt_tf1(audiences, y='TlspMoyen', tf1=True)
            ),
        ])
    elif tab == 'tab-pda':
        return html.Div([
            dcc.Graph(
            figure=draw_tv_audiences_tnt_tf1(audiences, y='PdA', tf1=True)
            ),
        ])

conclusion_layout = html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1('Conclusion'),
                            html.Hr(),
                            html.P([
                                "Revenons en à la question à la base de cette analyse : quelle est la place du biathlon en France ? ",
                                html.Br(),
                                "Côté sportif d'abord : "
                                "la France est une des nations majeures du biathlon. Cela est notamment dû aux 20 dernières années, aucours desquelles les Français ont très bien performés en compétitions, "
                                "dans le sillage de Martin Fourcade, qui a dominé les épreuves masculines pendant près de 10 ans. "
                                "Maintenant que ce dernier à pris sa retraite, les membres de l'équipe de France doivent continuer sur sa lancée, pour que la France continue d'être parmi les plus grandes nation du biathlon, "
                                "voir pourquoi pas devenir la plus grande !",
                                html.Br(),
                                "Coté populaire, grâce à un bon engouement du public (notamment en lors de l'édition 2019), l'étape Française de la coupe du Monde au Grand Bornand semble s'installer dans le calendrier de l'IBU pour les années à venir. "
                                "De plus, la diffusion du biathlon est un succès pour la chaine L'équipe, qui réalise de très bons score en terme d'audience, et croît tous les ans.",
                                html.Br(),
                                "Tout cela est de bonne augure pour les JO d'hiver qui auront lieu en février 2022 à Pékin ! Le record à battre est celui établi en 2018 à Pyeongchang, "
                                "avec 3 médailles d'or (2 en individuel pour Martin Fourcade, et 1 en relais mixte) et 2 de bronze." 
                            ]),
                            dbc.Alert([                            html.Div([
                                html.Span(html.Strong(['Résultats global de la ', html.Span(className="flag-icon flag-icon-fr"), ': ']),),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                                html.Span(className="fa fa-star checked"),
                            ]),], color='info'),
                        ],width={"size":10,"offset":1}
                    )
                )

            ]
        )
    ], id="conclusion"
)



footer = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2('Menu'),
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("Accueil", href="#", external_link=True)),
                                dbc.NavItem(dbc.NavLink("Introduction", href="#introduction", external_link=True)),
                                dbc.NavItem(dbc.NavLink("Résultats sportifs", href="#sport", external_link=True)),
                                dbc.NavItem(dbc.NavLink("Audiences TV", href="#audiences", external_link=True)),
                                dbc.NavItem(dbc.NavLink("Conclusion", href="#conclusion",external_link=True)),
                            ],
                            vertical="md",
                        )
                    ], width={"size":2, 'offset':2}
                ),
                dbc.Col(
                    [
                        html.H2('Quentin Deltour'),
                        html.P(
                            [
                                "Passionné de biathlon (et de plein d'autres sport), de dataviz, et "
                                "étudiant à l'ENSAE.",
                                html.Br(),
                                "N'hésitez pas à me faire des retours, je suis preneur de tous commentaires."
                            ], 
                        ),
                        dbc.Button(" Mail", className='fas fa-envelope-square mr-1 footer-button', href='mailto:quentindeltour77@gmail.com', external_link=True),
                        dbc.Button(" Linkedin", className='fab fa-linkedin mr-1 footer-button', href='https://www.linkedin.com/in/quentin-deltour/', external_link=True, target='_blank'),
                        dbc.Button(" Github",className='fab fa-github-square mr-1 footer-button', href='https://github.com/quentindeltour', external_link=True, target='_blank'),
                        html.Br(),
                        html.Hr(style={"color":"white"}),
                        html.P(
                            [
                                "Toutes cette analyse à été possible grâce aux données de l'IBU, accessible ",
                                html.A("ici", href="https://www.biathlonresults.com/", target="_blank"),
                                " grâce à une API gratuite.",
                                html.Br(),
                                "Ce site à été créé avec ",
                                html.A("Plotly", href="https://plotly.com/python/", target="_blank"),
                                " et ",
                                html.A("Dash", href="https://plotly.com/dash/", target="_blank"),
                                " (thème utilisé : ",
                                html.A("Bootstrap Cerulean", href="https://bootswatch.com/cerulean/", target="_blank"),
                                ")"
                            ]
                        )                        
                    ], width={"size":5, 'offset':2}
                )
            ]
        ),
    ], className='footer-dark'
)



app.layout = html.Div(
    [
        html.Div(
            [
                #navbar,
                acceuil_layout,
            ],
        ),
        dbc.Jumbotron(
            [
                introduction_layout,
                deroulement_layout,
                courses_layout,
                sites_map_layout,
                sport_layout,
                #performance_layout,
                audiences_layout,
                conclusion_layout,
            ]
        ),
        html.Div(
            footer
        )
    ]
)



if __name__ == '__main__':
    app.run_server(debug=True)
