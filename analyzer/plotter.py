#%%
import pandas as pd
import plotly.graph_objects as go
import plotly as pl
import numpy as np
from useful_data import COLS_ALLOWED_PLOTTER
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

#%%
path ='/Users/riccardo/Desktop/Network_Analysis/Shared_module/Prova_denominazione (6).xlsx'
data = Data(path)
dup_filt_df = data.duplica_ads(data.filt_df)
df_freq_rep = data.df_freq(data.filt_df, 'Repertorio')
df_freq_ads = data.df_freq(dup_filt_df, 'Ads')
print(data.df)
print(df_freq_rep)
print(df_freq_ads)

# %%
plot_freq = Plotter(df_freq_rep)
figure = plot_freq.table('REPERTORI')

# %%
figure.show()
# %%
