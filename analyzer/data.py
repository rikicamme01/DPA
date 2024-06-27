#%%
import pandas as pd
#import plotly as pl
import numpy as np
from useful_data  import COLS_ALLOWED, COLS_CHECKED, COLS_FINALS, RD, REP_GENERATIVI, REP_IBRIDI, REP_MANTENIMENTO

class Data():
    def __init__(self, path) -> None:
        self.filter_dict={}
        try:
            # if path.endswith('.xlsx')
            self.df = pd.read_excel(path)
            self.clean_df()
            #self.filter_dict
            self.filt_df = self.df
        except ValueError as e:
            raise (f"Errore durante il caricamento del file .xlsx: {e}")
        
    
    def replace_nan_with_previous(self, column):
        previous_value = None
        for i in range(len(column)):
            if pd.isna(column[i]):
                column[i] = previous_value
            else:
                previous_value = column[i]
        return column

    def reform_domande(self, list_domande):
        domande_formatted = []
        for domande in list_domande:
            domande_formatted.append(f'Domanda {domande[0]}')  # se si volesse salvare solo il numero della domanda 

        return domande_formatted

    def check_domande(self, list_domande):
        #funzione che scorre la lista passata e verifica che il primo carattere sia un numero
        #print(len(list_domande))
        check = True
        n_error = 0
        for domanda in list_domande:
            if not domanda[0].isdigit():
                check = False
                n_error += 1
        if check == False:
            print(f'Sono stati trovati {n_error} elementi nella colonna \'Domanda\' senza un numero di riferimento')
        else:
            print('Tutti gli elementi della colonna \'Domanda\' sono preceduti da un numero 👍')
        return check

    def update_filter_dict(self, df):
        lenght= 0
        for col in COLS_CHECKED:
            self.filter_dict[col] = df[col].unique().tolist()
        #controllo filter_dict
    def check_spelling_rep(self, filter_dict):
        if set(filter_dict['Repertorio']) <= set(RD):
            print('Tutti i repertori sono scritti correttamente 👍')
            return True
        print('Sono stati trovati repertori non ammessi. Controllare l\'ortografia')
        return False
        
    def count_nan(self, dataframe):
        # controlla valori NaN in colonne 'Stralcio' e 'Repertorio' e 'Ads' -> nel caso raise errore miss
        # aggiorna attrib num stralci
        # confronta num Testo con el non NaN delle colonne filtri (eta, genere, ruolo)
        nan_dict = {}
        for col in dataframe.columns:
            if col in ['Stralcio', 'Repertorio', 'Ads']:
                nan_dict[col] = dataframe[col].isna().sum()
            else:
                nan_dict[col] = dataframe['Testo'].notna().sum() - dataframe[col].notna().sum()
        return nan_dict
    
    def print_req(self, nan_dict):
        if sum(nan_dict.values()) == 0:
            print('Nessuna cella mancante trovata 👍')
            return True
        else:
            for key, value in nan_dict.items():
                if value > 0:
                    print(f'Elementi mancanti nella colonna {key}: {value}')
        return False



    def clean_df(self):
        check = True
        temp_df = self.df.loc[:, ~self.df.columns.str.startswith('Unnamed')]

        temp_df = temp_df.rename(columns=lambda x: x.strip().title())

        if 'Testo' not in temp_df.columns:
            raise ValueError("The column \'Testo\' miss in the passed excel file")
        # -> aggiorna attributo num_risposte con num_risposte = len(df['Testo'].unique())
        elif 'Repertorio' not in temp_df.columns:
            raise ValueError("The column \'Repertorio\' miss in the passed excel file")
        elif 'Ads' not in temp_df.columns:
            raise ValueError("The column \'Ads\' miss in the passed excel file")

        # filter the column (self.list_column)
        list_col=[]
        for col in list(temp_df.columns):
            if col in COLS_ALLOWED:
                list_col.append(col)
        new_df = temp_df.loc[:, list_col]

        # funzione aggiorna attributo dizionario nan (da fare self.nan_dict)
        nan_dict = self.count_nan(new_df)

        #funzione stampa requisiti
        if self.print_req(nan_dict) == False:
            check = False
            # mostra alert: tutti requisiti soddisfatti

        # add column "num_risposta"
        num_risposta = []
        index = 0
        for i in new_df['Testo'].isna():
            if i == False:
                index = index +1
            num_risposta.append(index)
        new_df['num_risposta'] = num_risposta

        # funzione toglie NaN
        #for col in new_df.columns:
        new_df = new_df.ffill()

        #funzione controlla colonna Domande
        if 'Domanda' in list_col:
            list_domande = list(new_df['Domanda'])
            #controllo che
            if all(isinstance(domanda, str) for domanda in list_domande):
                if self.check_domande(list_domande) == False:
                    check = False
                else:
                    #modifico new_df con nuova colonna (funzione che ritorna nuova lista domande con numeri) es: 'Domanda 1'
                    new_df['Domanda'] = self.reform_domande(list_domande)
            else:
                print('La colonna \'Domanda\' contiene almeno un elemento che non è una stringa')

        #funzione aggiorna dizionario con unique + controlli spelling rep e limite massimo opzioni
        self.update_filter_dict(new_df)


        # funzione controlla spelling rep confrontando filter_dict con LISTA_REP
        if self.check_spelling_rep(self.filter_dict) == False:
            check = False
            # mostra alert repertori scritti correttamente

        if check == True:
            # funz stampa riassunto: file caricato rispetta tutti i requisiti. Si può procedere all'analisi dei testi
            self.df = new_df.loc[:,COLS_FINALS]
            #self.splited_df = self.duplica_ads(new_df)
        else:
            # stampa requisiti mancanti
            raise ValueError('Sono stati riscontrati errori nel formato del file caricato')

    def filter_df(self, readed_dict):
        #controllo dizionario passato
        if set(readed_dict.keys()) <= set(self.filter_dict.keys()) :
            query = ' & '.join([f"{col} == {val}" for col, val in readed_dict.items()])
            self.filt_df = self.df.query(query)
        else:
            print("Il dizionario usato per filtrare i dati usa delle chiavi diverse da quelle consentite")


    def df_freq(self, df, column):
        if column in df.columns:
            dict_col = df[column].value_counts().to_dict()
            new_df = pd.DataFrame(list(dict_col.items()), columns=['Classe', 'Num'])
            new_df['Frequenza'] = ((new_df['Num'] / new_df['Num'].sum()) * 100).round(2)
            return new_df
        else:
            raise ValueError (f'The column \'{column}\' is not in {list(df.columns)}')

    def count_rep_group(self, df):
        dict_rep = df['Repertorio'].value_counts().to_dict()
        # Creazione del nuovo dizionario
        dict_group = {'Generativi': 0, 'Ibridi': 0, 'Mantenimento': 0}

        # Iterazione sul dizionario originale
        for key, value in dict_rep.items():
            if key in REP_GENERATIVI:
                dict_group['Generativi'] += value
            elif key in REP_IBRIDI:
                dict_group['Ibridi']+= value
            elif key in REP_MANTENIMENTO:
                dict_group['Mantenimento'] += value
            else:
                raise ValueError(f"There is an unknown rep: '{key}'")

        new_df = pd.DataFrame(list(dict_group.items()), columns=['Classe', 'Num'])
        new_df['Frequenza'] = ((new_df['Num'] / new_df['Num'].sum()) * 100).round(2)
        return new_df

    def df_freq_refe(self, df, column1, column2): # column1 = riferimento , column2 = colonna su cui contare le frequenze
        new_df = pd.DataFrame()
        if column1 in df.columns and column2 in df.columns: # allora ciclo tutti e 24 repertori (poi filtrari solo per plot)
            for i in df[column1].unique():
                # filtro df con repertorio corrente
                #calcolo frequenze colonna 2
                temp_df = self.df_freq(df.loc[df[column1] == i], column2)
                temp_df['Riferimento'] = i
                #aggiungo nuovo df a df 'globale' dato dall'unione di tutti i df creati per repertori
                new_df = pd.concat([new_df, temp_df], ignore_index = True)
            return new_df
        else:
            raise TypeError(f'There is not columns: {column1}, {column2} in this dataframe{list(df.columns)}')

    def rd_rd(self, df):
        new_df = pd.DataFrame()
        for i in df['Repertorio'].unique():
            list_risposte = df.loc[df['Repertorio'] == i]['num_risposta'].unique()
            temp_df = df.loc[df['num_risposta'].isin(list_risposte)]
            frequency_df = self.df_freq(temp_df, 'Repertorio')
            frequency_df['Riferimento'] = i

            frequency_df.loc[frequency_df['Classe'] == i, 'Num'] -= len(list(list_risposte))
            frequency_df['Frequenza'] = ((frequency_df['Num'] / frequency_df['Num'].sum()) * 100).round(2)

            new_df = pd.concat([new_df, frequency_df], ignore_index = True)
        return new_df
    
    def dict_sunbrust(self, df):
        df_values=self.df_freq(df, 'Repertorio')
        freq_dict =dict(zip(df_values['Classe'], df_values['Frequenza']))
        return freq_dict


    def duplica_ads(self, df):
        # Separare le stringhe nella colonna Ads
        df['Ads'] = df['Ads'].str.split(';')

        df_exploded = df.explode('Ads')
        #df_exploded = df_exploded.reset_index(drop=True)

        return df_exploded  
'''## TEST
#%%
path='/Users/riccardo/Desktop/Network_Analysis/Shared_module/Prova_denominazione (6).xlsx'
data = Data(path)
print(data.df)
prova = {'Genere': ['Maschio'], 'Ruolo':['Operativo', 'Gestionale'] }
data.filter_df(prova)
print(data.filt_df)
# %%
'''
