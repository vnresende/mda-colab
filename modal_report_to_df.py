import pandas as pd

class ModalReport():


    def __init__(self, file_name, dataframe):
        self.name = str(file_name)
        self.df = dataframe
        self.units = []
        self.call_functions()
    
    def call_functions(self):
        self.enumerate_columns()                            # Renomeia as coluna a partir do 0
        self.repetir_mesclados(6, 19)                       # Repetir 'PRE', 'MID', 'POS' e 'DIL'
        self.repetir_mesclados(7, 5)                        # Repetir Concentração, gramas e gramas/dist
        self.labels_and_units()                             # Linha 0 recebe labels, linha 1 recebe unidades
        self.df.drop(range(2,16), inplace = True)           # Elimina as linhas desnecessárias
        self.df.dropna(axis = 1, inplace = True)            # Remove colunas com 'Not a Number' (NaN)
        self.df.drop_duplicates(9, inplace = True)          # Remove linhas que contem duplicadas na coluna tempo
        self.move_column_to(9, 0)                           # Translada a coluna de 'tempo' para a 1ª pos
        self.set_labels_and_units()                         # Renomeia as colunas e obtem as unidades
        self.df = self.df.loc[:,~self.df.columns.duplicated()] # Elimina colunas repitidas
        self.df.drop(range(0,2), inplace = True)            # Elimina as linhas 0 e 1 do DF
        self.df.reset_index(drop = True, inplace = True)    # Reset de index

    def enumerate_columns(self):
        """ Enumera as colunas a partir de 0 até a último coluna """

        column_list = []
        for column in range(self.df.shape[1]):
            column_list.append(column)
        self.df.columns = column_list


    def move_column_to(self, current_pos, final_pos):
        """ Move uma coluna para determinada posição, o nome das colunas deve ser em número """

        column = self.df.pop(current_pos)
        self.df.insert(final_pos, current_pos, column)
    

    def repetir_mesclados(self, row, repeat):
        """ Repete o valor da primeira observação encontrada nas demais colunas.
        row é a linha 
        repeat é a quantidade de vezes a ser repetida """

        column = 0
        while column < self.df.shape[1]:
            cell = self.df.loc[row, column]
            i = 0
            if cell == 'HIOKI CHANNEL 1':
                cell == ''
            if isinstance(cell, str):
                for i in range(repeat):
                    self.df.loc[row, column + i ] = cell
                else:
                    cell == ''
            column = column + i + 1


    def labels_and_units(self):
        """ Define as linhas 1 e 2 como label e unidade """

        row = 7
        labels = []
        unit = []
        for column in range(self.df.shape[1]):
            if isinstance(self.df.loc[row-1, column], str):
                str1 = self.df.loc[row-1, column].strip() + '_'
            else:
                str1 = ''
            if isinstance(self.df.loc[row, column], str):
                str2 = self.df.loc[row, column].strip()
            else:
                str2 = ''
            if isinstance(self.df.loc[row+1, column], str):
                str3 = '_' + self.df.loc[row+1, column].strip()
            else:
                str3 = ''
            if isinstance(self.df.loc[row+2, column], str):
                str4 = ' (' + self.df.loc[row+2, column].strip('[]') + ')'
                str5 = self.df.loc[row+2, column].strip('[]')
            else:
                str4 = ''
                str5 = '-'
            string = str1 + str2 + str3 + str4
            labels.append(string)
            unit.append(str5)

        for i in range(len(labels)):
            labels[i] = labels[i].lstrip('_')
        self.df.loc[0, :] = labels
        self.df.loc[1, :] = unit


    def set_labels_and_units(self):
        """ Muda o nome das colunas conforme está na linha 0.
            Armazena a linha 1 em self.units """
        columns = list(self.df.loc[0,:])
        columns[0] = 'time'
        i = 0
        for i in range(len(columns)):
            if columns[i] == '':
                columns[i] = f"Col{i + 1}"
        self.df.columns = columns
        self.units = list(self.df.loc[1,:])
