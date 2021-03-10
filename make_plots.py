import plotly.graph_objects as go
import plotly.express as px

def draw_map_sites(token):
     fig = go.Figure(go.Scattermapbox(
        lat=['46.3667','45.950001','49.5614400', '63.1792', '59.91273',
        '47.46667', '46.7833333', '50.7052778', '47.7620099', '62.766667'],
        lon=['14.1085','6.43333','16.0741800', '14.63566', '10.74609',
        '12.61667', '12.05', '10.725833333333334', '12.6459934', '29.85'],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=9,
            color='red'
        ),
        text=["Polkujka","Grand-bornand","Nove Miesto", 'Ostersund', 'Oslo',
        'Hochfilzen', 'Antholz-Anterstelva', 'Oberhof', 'Ruhpolding', 'Kontiolahti'],
        hovertext=["Slovénie","France","République Tchèque", 'Suède', 'Norvège',
        'Autriche', 'Italie', 'Allemagne', 'Allemagne', 'Finlande'],
        hovertemplate="Site de %{text}<extra>%{hovertext}</extra>",
        textposition = "bottom center"))

     fig.update_layout(
     paper_bgcolor='#e9ecef',
     title={
          'text':'<b>' + 'Sites prévus pour la saison 2020/2021 de biathlon' + '</b>',
          'y':0.92,
          'x':0.5,
          'xanchor': 'center',
          'yanchor': 'top'
     },
     title_font_family='Courier New, monospace',
     hovermode='closest',
     mapbox=dict(
          accesstoken=token,
          bearing=0,
          center=dict(
               lat=55.5,
               lon=13
          ),
          pitch=0,
          zoom=3.1
     ),
     )
     fig.add_annotation(text="En plus de ces sites classiques,<br>une étape était prévue à Pékin<br>pour préparer les JO qui auront lieu<br>l'année prochaine(début 2022)",
               xref="paper", yref="paper",
               x=0, y=1, showarrow=False,font=dict(
          family="Courier New, monospace",
          size=12,
          color="black"
          ),
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8
     )
     fig.update_layout(
          font_family="Courier New, monospace",
     )
     return fig

def draw_ski_shoot_from_df_H(df):
     color_list =['#d6af36', '#a7a7ad', '#a77044']+['#636EFA' for i in range(4, len(df)+1)]
     color_sequence = {'Premier': '#d6af36', 'Second':'#a7a7ad', 'Troisieme':'#a77044', 'Francais':'#EF553B', 'Autres':'#636EFA'}
     df['Rank']=df['Rank'].astype(str)
     fig = px.scatter(df, x="ski", y="shoot_demeaned", 
               size='Score', custom_data=['Name', 'Rank'], color='Rank_lettres',
               color_discrete_map=color_sequence,)
     #fig.update_traces(hovertemplate='Ski: %{x} <br>Tir: %{y}')
     fig.update_yaxes(title='Performance au tir',zeroline=True, zerolinewidth=2, zerolinecolor='#2fa4e7')
     fig.update_xaxes(title='Performance sur les skis',zeroline=True, zerolinewidth=2, zerolinecolor='#2fa4e7')
     fig.update_layout(     title={
          'text':'<b>' + 'Est-il plus important de bien tirer ou de bien skier ?' + '</b>',
          'y':0.96,
          'x':0.4,
          'xanchor': 'center',
          'yanchor': 'top'
     })
     fig.update_layout(
          xaxis=dict(
               showgrid=False,
               showline=False,
               showticklabels=False,
          ),
          yaxis=dict(
               showgrid=False,
               showline=False,
               showticklabels=True,
          ),
     )

     shooter_index = df.shoot.idxmax()
     skiier_index = df.ski.idxmax()

     fig.update_layout(legend_title_text='Classement Coupe du Monde', paper_bgcolor="#e9ecef",plot_bgcolor='#e9ecef',)
     fig.update_traces(
          hovertemplate="<br>".join([
               "<b>%{customdata[0]}</b>",
               "Classement géneral: %{customdata[1]}",
               "Performance en ski: %{x:.2f}",
               "Performance au tir: %{y:.2f}",
          ])
     )
     fig.add_annotation(x=df.ski.loc[shooter_index], y=df.shoot_demeaned.loc[shooter_index],
          text="Le meilleur<br>tireur",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=14,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=90,
          ay=-50,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)
     fig.add_annotation(x=df.ski.loc[skiier_index], y=df.shoot_demeaned.loc[skiier_index],
          text="Le meilleur<br>skieur",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=14,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=0,
          ay=-60,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)

     fig.add_annotation(text="Excellent Tireur<br>Excellent Skieur",
                  xref="paper", yref="paper",
                  x=1, y=1, showarrow=False, font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"),)
     fig.add_annotation(text="Excellent Tireur<br>Mauvais Skieur",
                  xref="paper", yref="paper",
                  x=0, y=1, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"
            ),)
     fig.add_annotation(text="Mauvais Tireur<br>Excellent Skieur",
                  xref="paper", yref="paper",
                  x=1, y=0, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"
            ),)
     fig.add_annotation(text="Mauvais Tireur<br>Mauvais Skieur",
                  xref="paper", yref="paper",
                  x=0, y=0, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"
            ),)
     fig.add_annotation(text="Plus le point est gros,<br>plus l'athlète a réalisé<br>de bonnes perormances<br>en Coupe du Monde<br>cette saison",
                  xref="paper", yref="paper",
                  x=1.35, y=0.5, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="black"
            ),)
     fig.update_layout(
          legend=dict(
               x=1.01,
               y=1,
               title_font_family="Courier New, monospace",
               font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="black"
               ),
          )
     )
     fig.update_layout(
          font_family="Courier New, monospace",
     )
     return fig

def draw_ski_shoot_from_df_F(df):
     color_list =['#d6af36', '#a7a7ad', '#a77044']+['#636EFA' for i in range(4, len(df)+1)]
     color_sequence = {'Première': '#d6af36', 'Seconde':'#a7a7ad', 'Troisieme':'#a77044', 'Francaise':"#EF553B", 'Autres':'#636EFA'}
     df['Rank']=df['Rank'].astype(str)
     fig = px.scatter(df, x="ski", y="shoot_demeaned", 
               size='Score', custom_data=['Name', 'Rank'], color='Rank_lettres',
               color_discrete_map=color_sequence,size_max=20)
     #fig.update_traces(hovertemplate='Ski: %{x} <br>Tir: %{y}')
     fig.update_yaxes(title='Performance au tir',zeroline=True, zerolinewidth=2, zerolinecolor='#2fa4e7')
     fig.update_xaxes(title='Performance sur les skis',zeroline=True, zerolinewidth=2, zerolinecolor='#2fa4e7')
     fig.update_layout(title={
          'text':'<b>' + 'Est-il plus important de bien tirer ou de bien skier ?' + '</b>',
          'y':0.96,
          'x':0.4,
          'xanchor': 'center',
          'yanchor': 'top'
     })

     shooter_index = df.shoot.idxmax()
     skiier_index = df.ski.idxmax()
     fig.update_layout(
          xaxis=dict(
               showgrid=False,
               showline=False,
               showticklabels=False,
          ),
          yaxis=dict(
               showgrid=False,
               showline=False,
               showticklabels=True,
          ),
     )
     fig.update_layout(legend_title_text='Classement Coupe du Monde', paper_bgcolor="#e9ecef", plot_bgcolor='#e9ecef',)
     fig.update_traces(
          hovertemplate="<br>".join([
               "<b>%{customdata[0]}</b>",
               "Classement géneral: %{customdata[1]}",
               "Performance en ski: %{x:.2f}",
               "Performance au tir: %{y:.2f}",
          ])
     )
     fig.add_annotation(x=df.ski.loc[shooter_index], y=df.shoot_demeaned.loc[shooter_index],
          text="La meilleure<br>tireuse",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=14,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=120,
          ay=-50,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)
     fig.add_annotation(x=df.ski.loc[skiier_index], y=df.shoot_demeaned.loc[skiier_index],
          text="Les meilleures<br>skieuses",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=14,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=80,
          ay=-60,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)

     fig.add_annotation(x=df.ski.iloc[1], y=df.shoot_demeaned.iloc[1],
          text="",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=50,
          ay=-25)

     fig.add_annotation(text="Excellente Tireuse<br>Excellente Skieuse",
                  xref="paper", yref="paper",
                  x=1, y=1, showarrow=False, font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"),)
     fig.add_annotation(text="Excellente Tireuse<br>Mauvaise Skieuse",
                  xref="paper", yref="paper",
                  x=0, y=1, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"
            ),)
     fig.add_annotation(text="Mauvaise Tireuse<br>Excellente Skieuse",
                  xref="paper", yref="paper",
                  x=1, y=0, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"
            ),)
     fig.add_annotation(text="Mauvaise Tireuse<br>Mauvaise Skieuse",
                  xref="paper", yref="paper",
                  x=0, y=0, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="#2fa4e7"
            ),)
     fig.add_annotation(text="Plus le point est gros,<br>plus l'athlète a réalisé<br>de bonnes perormances<br>en Coupe du Monde<br>cette saison",
                  xref="paper", yref="paper",
                  x=1.35, y=0.5, showarrow=False,font=dict(
            family="Courier New, monospace",
            size=12,
            color="black"
            ),)
     fig.update_layout(
          legend=dict(
               x=1.01,
               y=1,
               title_font_family="Courier New, monospace",
               font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="black"
               ),
          )
     )
     fig.update_layout(
          font_family="Courier New, monospace",
     )
     return fig


def draw_PU_SP_correlation_from_groupby(df):
     fig = px.line(df, x='StartOrder', y='ResultOrder', color='Sexe',width=800, height=600, custom_data=['Sexe'])
     fig.update_traces(mode="markers+lines")
     fig.update_traces(
          hovertemplate="Chez les %{customdata[0]}, en partant en position %{x:.0f},<br>le classement d'arrivée moyen est %{y:.0f}ème")
     fig.update_yaxes(title="Classement à l'arrivée de la poursuite", )
     fig.update_xaxes(title="Classement au départ de la poursuite (arrivée du sprint)")
     fig.update_layout(     title={
          'text':'<b>' + "Est ce que la poursuite est jouée d'avance ?" + '</b>',
          'y':0.95,
          'x':0.5,
          'xanchor': 'center',
          'yanchor': 'top'
     })

     fig.update_layout(
          shapes=[
          dict(
               type= 'line',
               yref= 'y', y0= 1, y1= 60,
               xref= 'x', x0= 1, x1= 60
          )
          ],
          hovermode='x',
          paper_bgcolor="#e9ecef",
          plot_bgcolor="#e9ecef"
     )
     fig.add_annotation(text="<b>y=x</b>",
                    xref="paper", yref="paper",
                    x=0.9, y=1, showarrow=False,font=dict(
               family="Courier New, monospace",
               size=20,
               color="black"
               ),)
     fig.add_annotation(x=1, y=round(df[(df.Sexe=='Hommes')&(df.StartOrder==1)].ResultOrder.values[0]),
          text="Chez les Hommes,<br>le premier a partir <br>arrive en moyenne 4ème",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=0,
          ay=-160,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)
     fig.add_annotation(x=1, y=round(df[(df.Sexe=='Femmes')&(df.StartOrder==1)].ResultOrder.values[0]),
          text="Chez les Femmes,<br>la première a partir <br>arrive en moyenne 3ème",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=50,
          ay=50,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)
     fig.update_layout(
          font_family="Courier New, monospace",
     )
     fig.update_layout(legend=dict(
          yanchor="top",
          y=0.99,
          xanchor="left",
          x=0.01
     ))
     return fig


def draw_tv_audiences_tnt_tf1(df, y='TlspMoyen',title="<b>7 Meilleure audience de sport des chaines traditionnelles<br>contre les 7 meilleures audiences sportives sur la TNT en 2020</b>", tf1=False):
     fig = px.bar(df, x=df.index, y=y, color="Sport", title=title,
               color_discrete_map={'Biathlon':'#EF553B','Football(F)':'#AB63FA', 'Football':"#636EFA", 'Rugby':'#00CC96'}, custom_data=['Affiche', 'Sport','Chaine'])
     fig.update_layout(
          font_family="Courier New, monospace",
          paper_bgcolor='#e9ecef',
     )
     fig.update_xaxes(title="Meilleures audiences sportives TNT",tickangle=45)
     if tf1:
          fig.update_xaxes(title="Meilleures audiences sportives en 2020")

     fig.add_annotation(x=8, y=df.iloc[8][y],
     text="Dernière course<br>de la carrière<br>de Martin Fourcade",
     showarrow=True,
     font=dict(
          family="Courier New, monospace",
          size=12,
          color="#ffffff"
          ),
     align="left",
     arrowhead=2,
     arrowsize=0.8,
     arrowwidth=1.5,
     arrowcolor="#636363",
     ax=30,
     ay=-100,
     bordercolor="#c7c7c7",
     borderwidth=2,
     borderpad=4,
     bgcolor="#2fa4e7",
     opacity=0.8)

     if y=='TlspMoyen':
          fig.update_yaxes(title="Nombre de téléspectateurs moyens")
          fig.update_traces(hovertemplate="L'évènement %{customdata[0]} (%{customdata[1]} sur %{customdata[2]})<br>a rassemblé %{y} téléspectateurs en moyenne<extra></extra>",)
          fig.add_annotation(text="7 meilleures audiences<br> TV traditionnelle",
               xref="paper", yref="paper",
               x=0.08, y=0.75, showarrow=False,font=dict(
          family="Courier New, monospace",
          size=12,
          color="black"
          ),)

          fig.add_annotation(text="7 meilleures audiences TNT",
               xref="paper", yref="paper",
               x=0.96, y=0.15, showarrow=False,font=dict(
          family="Courier New, monospace",
          size=12,
          color="black"
          ),)
     elif y=='PdA':
          fig.update_yaxes(title="Part d'audiences moyenne")
          fig.update_traces(hovertemplate="L'évènement %{customdata[0]} (%{customdata[1]} sur %{customdata[2]})<br>a rassemblé %{y} % de part d'audiences<extra></extra>",)
          fig.update_layout(
               yaxis = dict(
                    tickmode = 'array',
                    tickvals = [0,10,20,30,40,50],
                    ticktext = ['0', '10%', '20%', '30%', '40%', '50%']
               )
          )
          fig.add_annotation(text="7 meilleures audiences<br> TV traditionnelle",
               xref="paper", yref="paper",
               x=0.08, y=0.9, showarrow=False,font=dict(
          family="Courier New, monospace",
          size=12,
          color="black"
          ),)

          fig.add_annotation(text="7 meilleures audiences TNT",
                    xref="paper", yref="paper",
                    x=1, y=0.3, showarrow=False,font=dict(
               family="Courier New, monospace",
               size=12,
               color="black"
               ),)
     else:
          raise ValueError('Unknown y parameter')

     fig.update_layout(
          xaxis = dict(
               tickmode = 'array',
               tickvals = df.index,
               ticktext = df.Affiche.tolist()
          ),
          plot_bgcolor='#e9ecef',
     )

     return fig

def draw_medals_pays(df, title):
     fig = px.bar(
          df.set_index(['Pays', 'text'])[['Or', 'Argent', 'Bronze']].stack().reset_index().rename(columns={0:'Nombre de médailles', 'level_2':'Métal'}),
          x='Pays', y='Nombre de médailles', color="Métal", custom_data=['Métal','text'],
          color_discrete_sequence=['#d6af36', '#a7a7ad', '#a77044'],
          title=title,
     )
     fig.update_layout(
          font_family="Courier New, monospace",
          hovermode='x',
          paper_bgcolor="#e9ecef",
          plot_bgcolor='#e9ecef',
          title={
               'text':'<b>' + title + '</b>',
               'y':0.9,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top'
          }
     )
     fig.update_layout(legend=dict(
          yanchor="top",
          y=0.99,
          xanchor="right",
          x=0.99
          )
     )
     fig.update_traces(
          hovertemplate="%{customdata[1]} a remporté %{y:.0f} médailles de %{customdata[0]} aux JO")
     fig.update_xaxes(tickangle=45)
     return fig

def draw_medals_indiv_JO_H(df, title):
     fig = px.bar(
          df.set_index('Nom')[['Or', 'Argent', 'Bronze']].stack().reset_index().rename(columns={0:'Nombre de médailles', 'level_1':'Métal'}),
          x='Nom', y='Nombre de médailles', color="Métal", custom_data=['Métal'],
          color_discrete_sequence=['#d6af36', '#a7a7ad', '#a77044'],
          title=title,
          width=800, height=600,
     )
     fig.update_layout(
          font_family="Courier New, monospace",
          hovermode='x'
     )
     fig.update_traces(
          hovertemplate="%{x} a remporté %{y:.0f} médailles de %{customdata} aux JO")
     fig.add_annotation(x='Ole Einar Bjørndalen', y=13,
          text="Bjørndalen est l'athlète<br>le plus titré des JO d'hiver",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=50,
          ay=-50,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)
     fig.add_annotation(x='Martin Fourcade', y=7,
          text="Martin Fourcade<br>est l'athlète Français<br>le plus titré des JO<br>(été et hiver cofondus)",
          showarrow=True,
          font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=60,
          ay=-80,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)
     return fig

def draw_medals_indiv_JO_F(df, title):
     fig = px.bar(
          df.set_index('Nom')[['Or', 'Argent', 'Bronze']].stack().reset_index().rename(columns={0:'Nombre de médailles', 'level_1':'Métal'}),
          x='Nom', y='Nombre de médailles', color="Métal", custom_data=['Métal'],
          color_discrete_sequence=['#d6af36', '#a7a7ad', '#a77044'],
          title=title,
          width=800, height=700,
     )
     fig.update_layout(
          font_family="Courier New, monospace",
          hovermode='x'
     )
     fig.update_traces(
          hovertemplate="%{x} a remporté %{y:.0f} médailles de %{customdata} aux JO")
     return fig



def draw_win_by_season(df):
     fig = px.bar(df, x='0', y='saison', color="Pays", title="Médailles par saisons par pays", orientation='h',
     color_discrete_map={'France':'#636EFA','Norvège':'#EF553B', 'Allemagne':'#FECB52', 'Russie':'#FFF5EE'}, custom_data=['text'], opacity=0.9)
     fig.update_traces(texttemplate='%{x:.Of}', textposition='auto')
     fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
     fig.update_traces(textangle=0)
     fig.update_layout(
          font_family="Courier New, monospace", plot_bgcolor='#e9ecef',

     )
     fig.update_traces(
          hovertemplate="%{customdata[0]} a remporté %{x:.0f} courses lors de la saison %{y}")
     fig.update_yaxes(title="Saison", )
     fig.update_xaxes(title="Nombre de victoires")
     fig.update_layout(
          title={
               'text':'<b>' + "Nombre de victoires par saison pour les 4 nations majeures" + '</b>',
               'y':0.9,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top'
          },
          title_font_family="Courier New, monospace",
          paper_bgcolor="#e9ecef"
     )
     return fig


def make_comparaison(df, sexe='H'):
     fig = px.bar(
          df,
          x='différence', 
          y ="comp",
          color='Vainqueur',
          orientation='h',
          text='difftext',
          category_orders={"comp": ['Victoires', 'Pourcentage<br>de victoires', "Or Olympique", "Medailles<br>Olympiques", "Or Mondial", "Médailles<br>Mondiales", "Gros Globes", 'Petits Globes']},
          custom_data = ["text", "a1", "a2"],
          )

     fig.update_traces(
          hovertemplate="%{customdata[0]} (%{customdata[2]} contre %{customdata[1]})<extra></extra>")

     fig.update_layout(
          xaxis=dict(
               showgrid=False,
               showline=False,
               showticklabels=False,
               zeroline=True,
          ),
          yaxis=dict(
               showgrid=False,
               showline=False,
               showticklabels=True,
               zeroline=False,
          ),
          barmode='stack',
          paper_bgcolor='#e9ecef',
          plot_bgcolor='#e9ecef',
          showlegend=False,
          title_font_family="Courier New, monospace",
          font_family="Courier New, monospace",
     )
     fig.update_yaxes(title='',zeroline=False, fixedrange=True)
     fig.update_xaxes(title='',zeroline=True, zerolinewidth=2, zerolinecolor='#2fa4e7', fixedrange=True)
     fig.update_layout(
          title={
               'text':'<b>' + "Comparaison des Trophées gagnés" + '</b>',
               'y':0.95,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top',
               'font':{'size':20}
          },
     )
     if sexe=='H':
          fig.add_annotation(text="Ole Einar Bjoerndalen",
                    xref="paper", yref="paper",
                    x=0.1, y=1.05, showarrow=False, font=dict(
               family="Courier New, monospace",
               size=12,
               color="#2fa4e7"),)
          fig.add_annotation(text="Martin Fourcade",
                    xref="paper", yref="paper",
                    x=0.8, y=1.05, showarrow=False, font=dict(
               family="Courier New, monospace",
               size=12,
               color="#2fa4e7"),)
          fig.add_annotation(y='Or Mondial', x=0,
               text="Les 2 ont gagné 11 titres<br>mondiaux en individuel<br>La différence se fait<br>sur les résultats en relais.",
               showarrow=True,
               font=dict(
               family="Courier New, monospace",
               size=12,
               color="#ffffff"
               ),
               align="center",
               arrowhead=2,
               arrowsize=0.8,
               arrowwidth=1.5,
               arrowcolor="#636363",
               ax=130,
               ay=0,
               bordercolor="#c7c7c7",
               borderwidth=2,
               borderpad=4,
               bgcolor="#2fa4e7",
               opacity=0.8)
          fig.add_annotation(y='Or Olympique', x=0,
               text="Bjørndalen est<br>l'athlète le plus titré<br>des JO d'hiver",
               showarrow=True,
               font=dict(
               family="Courier New, monospace",
               size=12,
               color="#ffffff"
               ),
               align="center",
               arrowhead=2,
               arrowsize=0.8,
               arrowwidth=1.5,
               arrowcolor="#636363",
               ax=130,
               ay=10,
               bordercolor="#c7c7c7",
               borderwidth=2,
               borderpad=4,
               bgcolor="#2fa4e7",
               opacity=0.8)
          fig.add_annotation(text="<b>Note de lecture</b> :<br>C'est la différence de palmarès qui est représentée ici.<br>Ole Einar Bjoerndalen a remporté 12 courses de plus<br>que Martin Fourcade dans toute sa carrière.",
                    xref="paper", yref="paper",
                    x=0.1, y=-0.25, showarrow=False, 
                    font=dict(
                         family="Courier New, monospace",
                         size=12,
                         color="black"),

                    )
     elif sexe=='F':
          fig.update_xaxes(range=[-15,10])
          fig.add_annotation(text="Magdalena Forsberg",
                    xref="paper", yref="paper",
                    x=0.2, y=1.05, showarrow=False, font=dict(
               family="Courier New, monospace",
               size=12,
               color="#2fa4e7"),)
          fig.add_annotation(text="Magdalena Neuner",
                    xref="paper", yref="paper",
                    x=0.9, y=1.05, showarrow=False, font=dict(
               family="Courier New, monospace",
               size=12,
               color="#2fa4e7"),)
          fig.add_annotation(y='Or Olympique', x=0,
               text="Magdalena Forsberg<br>n'a jamais gagné<br>de titre olympique.",
               showarrow=True,
               font=dict(
               family="Courier New, monospace",
               size=12,
               color="#ffffff"
               ),
               align="center",
               arrowhead=2,
               arrowsize=0.8,
               arrowwidth=1.5,
               arrowcolor="#636363",
               ax=-130,
               ay=20,
               bordercolor="#c7c7c7",
               borderwidth=2,
               borderpad=4,
               bgcolor="#2fa4e7",
               opacity=0.8)
          fig.add_annotation(text="<b>Note de lecture</b> :<br>C'est la différence de palmarès qui est représentée ici.<br>Magdalena Forsberg a remporté 8 courses de plus<br>que Magdalena Neuner au cours de sa carrière.",
               xref="paper", yref="paper",
               x=0.1, y=-0.25, showarrow=False, 
               font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="black"),

          )
     return fig


def draw_trend(df):
     fig = px.area(df, x='Mois', y='Biathlon: (France)')
     fig.update_traces(hovertemplate='Google Trend de "Biatlon" : %{y}')
     fig.update_yaxes(title='Google Trend Biathlon')
     fig.update_xaxes(
          title='',
          #rangeslider_visible=True,
          rangeselector=dict(
               buttons=list([
                    dict(count=10, label="10 ans", step="year", stepmode="backward"),
                    dict(count=5, label="5 ans", step="year", stepmode="backward"),
                    dict(count=1, label="1 an", step="year", stepmode="backward"),
                    dict(step="all", label="depuis 2004")
               ])
          )
     )

     fig.update_layout(
          paper_bgcolor='#e9ecef',
          plot_bgcolor='#e9ecef',
          title_font_family="Courier New, monospace",
          font_family="Courier New, monospace",
          title={
               'text':'<b>' + "Evolution de la Google Trend du Biathlon en France depuis 2004" + '</b>',
               'y':0.99,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top',
               'font':{'size':20}
          },
          hovermode='x'
     )
     fig.update_xaxes(
          dtick="M6",
          tickformat="%b\n%Y",
          ticklabelmode="period"
     )

     fig.add_annotation(x='2010-02-01', y=13,
          text="JO de Vancouver",
          showarrow=True,
          font=dict(
          family="Courier New, monospace",
          size=12,
          color="#ffffff"
          ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=0,
          ay=-40,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)

     fig.add_annotation(x='2006-02-01', y=13,
          text="JO de Turin",
          showarrow=True,
          font=dict(
          family="Courier New, monospace",
          size=12,
          color="#ffffff"
          ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=0,
          ay=-40,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)

     fig.add_annotation(x='2014-02-01', y=34,
          text="JO de Sotchi",
          showarrow=True,
          font=dict(
          family="Courier New, monospace",
          size=12,
          color="#ffffff"
          ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=0,
          ay=-40,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)

     fig.add_annotation(x='2018-02-01', y=68,
          text="JO de Pyeongchang",
          showarrow=True,
          font=dict(
          family="Courier New, monospace",
          size=12,
          color="#ffffff"
          ),
          align="center",
          arrowhead=2,
          arrowsize=0.8,
          arrowwidth=1.5,
          arrowcolor="#636363",
          ax=0,
          ay=-40,
          bordercolor="#c7c7c7",
          borderwidth=2,
          borderpad=4,
          bgcolor="#2fa4e7",
          opacity=0.8)

     fig.add_annotation(text="Créé à partir de Google Trends",
          xref="paper", yref="paper",
          x=0, y=1, showarrow=False, 
          font=dict(
               family="Courier New, monospace",
               size=12,
               color="black")
     )
     return fig