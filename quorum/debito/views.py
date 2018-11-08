from django.shortcuts import render
from .models import Debito
import numpy as np
import pandas as pd
import locale
ano = 2018

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


#import das solicitações de reembolso por mês
def_temp_debits = []
for i in range(1,13):
    def_temp_debits.append(
    pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterDebitoVereadorJSON?ano=%d&mes=%d"
     % (ano,i)))

#junção de todos os dataframes dos reembolsos
df_final = pd.concat(def_temp_debits)


#import dos créditos por mês
def_temp_credits = []
for i in range(1,13):
    def_temp_credits.append(pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterCreditoVereadorJSON?ano=%d&mes=%d" % (ano,i)))

#junção de todos os dataframes de créditos
df_credits_final = pd.concat(def_temp_credits)

#lista de todos os vereadores encontrados
council_members_original = df_final["VEREADOR"].unique()

#substitui espaços por _ nos nomes dos vereadores no DF de debitos
df_final["VEREADOR"].replace(to_replace = r'\s+', value = '_', regex=True, inplace=True)


#remoção dos espaços entre os nomes dos vereadores no DF de créditos
df_credits_final["VEREADOR"].replace(to_replace = r'\s+', value = '_', regex=True, inplace=True)


#DF com os nomes em ambos os formatos
council_members_formatted = df_final["VEREADOR"].unique()
council_members_both_formats = pd.DataFrame(council_members_original,council_members_formatted)

#arredonda os valores
df_final["VALOR"] = round(df_final["VALOR"])
df_credits_final["VALOR"] = round(df_credits_final["VALOR"])

total_credits_by_council = df_credits_final.groupby("VEREADOR").sum()
total_credits_by_council = total_credits_by_council["VALOR"]


#gastos por categoria
category_spendings = df_final.groupby(by = ["VEREADOR", "DESPESA"])["VALOR"].sum()

#total de créditos
total_credits = df_credits_final.groupby(by = ["VEREADOR"])["VALOR"].sum()
total_credits_mean = total_credits.mean()

general_spendings = df_final.groupby(by = ["VEREADOR"])["VALOR"].sum()

general_credit = df_credits_final.groupby(by = ["VEREADOR"])["VALOR"].sum()

all_spends_by_month = df_final.pivot_table(index = ["VEREADOR","ANO", "MES"], columns = "DESPESA", values = "VALOR")
all_spends_by_month.fillna(value = 0, inplace = True)

all_spends_by_council = all_spends_by_month.groupby(by = all_spends_by_month.index.get_level_values(0)).sum()
all_spends_by_council.fillna(value=0, inplace = True)




def vereadorPretty(vereador):
    return council_members_both_formats.loc[vereador][0]

def gastos(vereador):
    #general_spendings.sort_values(ascending = False, inplace=True)
    return general_spendings[vereador]
    #print(gastos('ABOU_ANNI'))

def creditos(vereador):
    return total_credits_by_council[vereador]

def usoCota(vereador):
    return gastos(vereador)/creditos(vereador)

def gastosMensais(vereador):
    x={}
    for i in range(12):
        try:
            x[i] = round(df_final.groupby(by = ["ANO","MES","VEREADOR"])["VALOR"].sum()[ano,i+1,vereador])
        except KeyError:
            x[i]=0
    return x.values()

def mediaGastosMensais():
    x={}
    for i in range(12):
        try:
            x[i] =  round(df_final.groupby(by =["ANO","MES"])['VALOR'].sum()[ano,i+1]/len(df_final.groupby(by =["ANO","MES","VEREADOR"])['VALOR'].count()[ano,i+1]))
        except KeyError:
            x[i]=0
    return list(x.values())


def gastosPorCategoria(vereador):
    category_spendings = df_final.groupby(by = ["VEREADOR", "DESPESA"])["VALOR"].sum()
    return category_spendings[vereador]

def mediaGastosPorCategoria(vereador):
    x = round(category_spendings.groupby(by = ["DESPESA"]).mean())[list(category_spendings[vereador].index)]
    return x

def totalDeCategorias(vereador):
    x=len(category_spendings[vereador])
    return x

def mediaGastosGerais():
    return general_spendings.mean()

def mediaCreditosGerais():
    return general_credit.mean()
