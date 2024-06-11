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
COLS_FINALS = ['Domanda', 'Età', 'Genere', 'Ruolo', 'Repertorio', 'Ads']

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
REP_IBRIDI = ['possibilità', 'valutazione', 'dichiarazione di intenti', 'specificazione', 'conferma', 'prescrizione', 'ridimensionamento', 'implicazioni']
REP_MANTENIMENTO = ['sancire', 'causa', 'previsione', 'giudizio', 'opinione', 'deresponsabilizzazione', 'giustificazione', 'contrapposizione', 'generalizzazione', 'commento', 'non risposta']
