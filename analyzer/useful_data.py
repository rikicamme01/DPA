RD = [
                'anticipazione',
                'causa',
                'commento',
                'conferma',
                'considerazione',
                'contrapposizione',
                'deresponsabilizzazione',
                'descrizione',
                'dichiarazione di intenti',
                'generalizzazione',
                'giudizio',
                'giustificazione',
                'implicazione',
                'non risposta',
                'opinione',
                'possibilità',
                'prescrizione',
                'previsione',
                'proposta',
                'ridimensionamento',
                'sancire',
                'specificazione',
                'valutazione',
                'riferimento all\'obiettivo',
        ]

COLS_ALLOWED = ['Domanda', 'Età', 'Genere', 'Ruolo', 'Testo', 'Stralcio', 'Repertorio', 'Ads']
COLS_FINALS = ['Domanda', 'Età', 'Genere', 'Ruolo', 'Repertorio', 'Ads', 'num_risposta']

COLS_CHECKED = ['Domanda', 'Età', 'Genere', 'Ruolo', 'Repertorio', 'Ads']

COLS_ALLOWED_PLOTTER =[
                    'num_risposta',
                    'num_domanda', #-> da ricordarsi quando si creerà file excel con risposte forms
                    'Età','età','Eta','ETÀ',
                    'Genere', 'GENERE', 'genere', 'Sesso', 'sesso', 'SESSO',
                    'Ruolo', 'RUOLO', 'ruolo',
                    'Repertorio','REPERTORIO', 'repertorio',
                    'Arcipelago', 'ARCIPELAGO', 'arcipelago','Ads', 
]
REP_GENERATIVI = ['descrizione','proposta','considerazione','anticipazione','riferimento all\'obiettivo']
REP_IBRIDI = ['possibilità', 'valutazione', 'dichiarazione di intenti', 'specificazione', 'conferma', 'prescrizione', 'ridimensionamento', 'implicazione']
REP_MANTENIMENTO = ['sancire', 'causa', 'previsione', 'giudizio', 'opinione', 'deresponsabilizzazione', 'giustificazione', 'contrapposizione', 'generalizzazione', 'commento', 'non risposta']

dict_RD_color={
           'descrizione': '#5BC69A',
           'proposta': '#5BC69A',
           'considerazione': '#5BC69A',
           'anticipazione':'#5BC69A',
           'riferimento all\'obiettivo': '#5BC69A',
           'conferma': '#F3CB74' ,
           'specificazione':'#F3CB74' ,
           'valutazione':'#F3CB74' ,
           'possibilità':'#F3CB74' ,
           'implicazione':'#F3CB74' ,
           'sancire':'#E85B55' ,
           'causa':'#E85B55',
           'opinione':'#E85B55' ,
           'giustificazione':'#E85B55'
}
dict_RD_group={
        'descrizione': 'Generativi',
        'proposta': 'Generativi',
        'considerazione': 'Generativi',
        'anticipazione':'Generativi',
        #'riferimento all\'obiettivo': 'Generativi',
        'conferma': 'Ibridi' ,
        'specificazione':'Ibridi' ,
        'valutazione':'Ibridi' ,
        'possibilità':'Ibridi' ,
        'implicazione':'Ibridi' ,
        'sancire':'Mantenimento' ,
        'causa':'Mantenimento',
        'opinione':'Mantenimento' ,
        'giustificazione':'Mantenimento'
}
bg_color = '#002C2C'
column_color = '#088F8F'
