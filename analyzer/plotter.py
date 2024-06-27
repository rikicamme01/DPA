#%%
import pandas as pd
import plotly.graph_objects as go
import plotly as pl
import numpy as np
import plotly.express as px
from useful_data import COLS_ALLOWED_PLOTTER, dict_RD_color, bg_color, column_color, dict_RD_group, RD
from data import Data
from pandas import DataFrame

class Plotter():
   def __init__(self, df) -> None:
      #genererici controlli sul path passato
      if isinstance(df, DataFrame):
         self.df = df

   def table(self, first_column, description = False, ref_column='', ref_value=''):
      #useful parameters
      color_header = '#B1E2E1'
      color_cell = '#F8F8F8'
      color_axes = '#FCFCFC'
      color_tot = '#408D8E'
      cell_font = 18
      header_font = 20
      # modifico colonna 'Classe' in maiuscolo
      self.df['Classe']=self.df['Classe'].apply(lambda x: x.upper())
      tot = self.df['Num'].sum()
      self.df.loc[len(self.df.index)] = ['TOTALE', tot, 100]
      len_df = self.df.shape[0]

      # Creazione della tabella Plotly
      fig = go.Figure(data=[go.Table(
            header=dict(values=[first_column, 'nº', 'Frequenza'],
                        fill_color=color_header,
                        height = header_font * 1.55,
                        align=['left', 'center'],
                        font=dict(family='Arial', size=header_font, color='black')),

            cells=dict(values=[self.df[col] if col != 'Frequenza' else (self.df['Frequenza']).astype(str) + ' %' for col in self.df.columns],
                     fill_color=[[color_tot if i ==len_df -1 else color_cell for i in range(len_df)]],
                     line_color= color_axes,
                     height = cell_font* 1.66,
                     align=['left', 'center'],
                     font = dict(family='Arial', size=cell_font, color='black'),
                     #font_size = 18,
                     #format =[None, None, '.2f%', None],
                     ),
            columnwidth=[50, 20, 30]
            )])

      # Aggiornamento del layout per migliorare l'estetica
      fig.update_layout(width=400, height=600)  # Modifica le dimensioni della tabella
      fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))  # Rimuove i margini
      if description == True:
         fig.update_layout(title_text=f"{ref_column}: {ref_value}",
                           title_font=dict(family="Arial", size=24, color="blue"))

      return fig

   def filter_format(self, lista):
      return ', '.join(lista).upper()

   def chart_histo_RD(self, list_filter, title='Distribuzione delle frequenze dei repertori'):
      # Creazione istogramma plotly
      fig = px.histogram(self.df.loc[self.df['Classe'].isin(list_filter)],
                        x='Classe',
                        y='Frequenza',
                        text_auto = True,
                           opacity = 1,
                           color='Classe',
                           color_discrete_map= dict_RD_color)

      fig.update_layout(xaxis_title=None,
                        yaxis_title ='Frequenza',
                        yaxis=dict(title_font=dict(size=18)),
                        autosize = True,
                        width = 800,
                        height = 600,
                        plot_bgcolor = bg_color
                        )
      fig.update_traces(texttemplate = '%{y:.2f}%', textposition='auto', textfont = dict(size = 14))
      fig.update_yaxes(gridcolor='#A2ABB5')
      fig.update_xaxes(tickfont=dict(size=16))
      #fig.update_layout(title = title,
      #                  annotations=[dict(text=self.filter_format(list_filter), visible = False)]
      #                  )

      for trace in fig.data:
         trace.legendgroup = dict_RD_group[trace.name]
         trace.name = trace.legendgroup  # Imposta il nome della legenda come il gruppo
         trace.showlegend = True

      unique_legend_groups = set()
      for trace in fig.data:
         if trace.name in unique_legend_groups:
            trace.showlegend = False  # Nasconde i duplicati nella legenda
         else:
            unique_legend_groups.add(trace.name)

      fig.update_layout(legend=dict(
                                    title='Gruppi',
                                    itemsizing='constant'
                                    ),
                        legend_traceorder="normal"
                        )

      return fig

   def chart_histo_Ads(self,list_filter, title='Distribuzione delle frequenze degli arcipelaghi'):
      # Funzione per modificare il df passato con Maiuscole del caso

      # Creazione istogramma plotly
      fig = px.histogram(self.df.loc[self.df['Classe'].isin(list_filter)],
                        x='Classe',
                        y='Frequenza',
                        text_auto = True,
                        opacity = 1,
                        color='Classe',
                        color_discrete_sequence = [column_color],
                           )

      fig.update_layout(xaxis_title=None,
                        yaxis_title ='Frequenza',
                        yaxis=dict(title_font=dict(size=18)),
                        autosize = True,
                        width = 800,
                        height = 600,
                        plot_bgcolor = bg_color
                        )
      fig.update_traces(texttemplate = '%{y:.2f}%', textposition='auto', textfont = dict(size = 14))
      fig.update_yaxes(gridcolor='#A2ABB5')
      fig.update_xaxes(tickfont=dict(size=16))
      #fig.update_layout(title = title,
      #                  annotations=[dict(text=self.filter_format(list_filter), visible = False)]
      #                  )
      fig.update_traces(showlegend=False)

      return fig

   def chart_pie_RD(self):
      fig = px.pie(self.df,
                     values= self.df['Num'],
                     names= self.df['Classe'],
                     labels = self.df['Classe'],
                     #title=
                     #color_discrete_sequence=px.colors.sequential.RdBu)
                  )
      fig.update_layout(legend=dict(font=dict(size=14,
                                                #family="Arial",
                                                )))

      fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide')
      fig.update_layout(showlegend=False)
      fig.update_layout(width=700, height=500)
      fig.update_traces(hovertemplate='%{label}: %{value}')
      dict_color = {'Mantenimento':'#E85B55', 'Ibridi':'#F3CB74', 'Generativi': '#5BC69A'}
      fig.update_traces(marker=dict(colors=[dict_color[label] for label in self.df['Classe']]))

      return fig

   def chart_treemap(self, root):
      fig = px.treemap(self.df,
                        path=[px.Constant(root),
                              'Riferimento',
                                 'Classe'],
                        values='Num',
                        #title='prova',
                        #custom_data =['Frequenza'],
                        width = 1000,
                        height = 600,
                              )

      fig.update_traces(
                        textposition ='middle center',
                        texttemplate ='%{label}<br>%{percentParent} di %{parent} <br> %{percentRoot} del totale'
                        )
      #fig.update_layout(margin = dict(t=50, l=50, r=50, b=50))
      fig.update_traces(hovertemplate='labels=%{label}<br>count=%{value}<extra></extra>')

      config = {
      'toImageButtonOptions': {
         'format': 'png', # one of png, svg, jpeg, webp
         'filename': 'custom_image',
         'height': 500,
         'width': 700,
         'scale':5 # Multiply title/legend/axis/canvas sizes by this factor
         }
      }

      return fig
   
   def chart_sunbrust(self, dictio):
      group_map ={key.upper(): value for key, value in dict_RD_color.items()}

      #df_values=data.df_freq(new_df, 'Repertorio')
      #freq_dict =dict(zip(df_values['Classe'], df_values['Frequenza']))

      parents = self.df['Riferimento'].apply(lambda x: x.upper())
      n_parents =len(self.df['Riferimento'].unique())

      leaves = self.df['Classe'].apply(lambda x: x.upper())

      fig = px.sunburst(self.df,
                        path=[
                              parents,
                              leaves],
                        values='Frequenza',
                        #title = 'Legami fra Repertori Discorsivi',
                        width = 1000,
                        height = 700,
                        )
      fig.update_layout(
         title_font=dict(size=25, family='Arial',
                                    #color='blue',
                        ),
         title_x=0.5,
         #title_y=0.8
      )
      fig.update_traces(marker_colors=[group_map[cat] for cat in fig.data[-1].labels])

      fig.update_traces(
            insidetextorientation='horizontal'
            )

      fig.for_each_trace(lambda t: t.update(hovertemplate='<b>%{label}</b><br>%{value}%'),)

      # Aggiornare le tracce del grafico con il texttemplate personalizzato
      labels = fig.data[0].labels
      str_labels =[str(label).lower() for label in labels]

      text_template = ['%{label}<br>%{percentParent}' for _ in range(len(leaves))]
      for i in str_labels[-n_parents:]:
         text_template.append('%{label}<br>'+ str(dictio[i]) + '%')

      fig.update_traces(texttemplate=text_template)

      fig.update_traces(
            marker=dict(
                  line=dict(
                     color='black',  # Colore dei bordi
                     width=0.4  # Spessore dei bordi
                  )
            )
         )

      config = {
      'toImageButtonOptions': {
         'format': 'png', # one of png, svg, jpeg, webp
         'filename': 'custom_image',
         'height': 500,
         'width': 700,
         'scale':5 # Multiply title/legend/axis/canvas sizes by this factor
         }
      }

      return fig

   def chart_gauge_index(self, value, title=''):
      index_color = '#2A3F5F'
      #index_color = '#A1C8D7'
      fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = value,
            mode = "gauge+number",
            #title = {'text': title, 'font':{'size': 30}},
            number = {'font': {'color': index_color}},
            gauge = {'axis': {'range': [None, 10],
                              'tickvals': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Valori delle etichette
                              #'ticktext': ['0', '2', '4', '6', '8', '10'],  # Testo delle etichette
                              'tickfont': {'size': 16,} ,
                              'tickcolor': index_color
                           },
                  'bar': {'color': index_color,
                           'thickness': 0.5,
                           },
                  'steps' : [
                        {'range': [0, 4], 'color': "#EE8C88"},
                        {'range': [4, 8], 'color': "#F6DA9D"},
                        {'range': [8, 10], 'color': "#8CD7B8"}],
                  #'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
            }))

      fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
         )


      return fig


#%%
path ='/Users/riccardo/Desktop/Network_Analysis/Shared_module/Prova_denominazione (6).xlsx'
data = Data(path)
dup_filt_df = data.duplica_ads(data.filt_df)
df_freq_rep = data.df_freq(data.filt_df, 'Repertorio')
df_freq_rep_group = data.count_rep_group(data.filt_df)
df_freq_ads = data.df_freq(dup_filt_df, 'Ads')
print(data.df)
print(data.filt_df)
print(df_freq_rep)
print(df_freq_ads)

# %%
#PROVA TREEMAP (Rep)
df = data.df_freq_refe(dup_filt_df, 'Repertorio', 'Ads')
plt = Plotter(df)
figure = plt.chart_treemap('REPERTORI DISCORSIVI')
#list_filter = ['Coinvolgimento', 'Associazioni', 'Reti', 'Bisogni', 'Aggregazione']
#%%
#PROVA SUNBRUST
dict_rd = data.dict_sunbrust(data.filt_df)
df = data.rd_rd(data.filt_df)
plt = Plotter(df)
figure = plt.chart_sunbrust(dict_rd)

#%%
#PROVA GAUGE INDEX
figure = plt.chart_gauge_index(6)

# %%
figure.show()
# %%
#come ritornare le info da un oggetto figure
print(figure.layout.title.text)
print(figure.layout.annotations[0]['text'])
# %%
