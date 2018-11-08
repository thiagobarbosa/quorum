from django.shortcuts import render, redirect
import debito.views
ano = 2018
def home(request):

    gastosTotais = gastoGeralTotal()
    gastosTotaisFormatado = "{:,.2f}".format(gastosTotais)
    creditosTotais = creditoGeralTotal()
    creditosTotaisFormatado = "{:,.2f}".format(creditosTotais)
    totalEconomizado = creditosTotais - gastosTotais
    percentualGeralUsado = round(100*(1-((creditosTotais-gastosTotais)/creditosTotais)))
    percentualGeralDisponivel = round(100-percentualGeralUsado)
    topCategoriasHome = topCategorias(10)
    topVereadoresHome = topVereadores(50)
    topVereadoresMenoresGastosHome = topVereadoresMenoresGastos(50)
    mediaGastosMensaisGeral = debito.views.mediaGastosMensais()
    totalGastosMensaisHome = totalGastosMensais()


    return render(request, 'home.html', {'gastosTotais':gastosTotais,'creditosTotais':creditosTotais,
    'percentualGeralUsado':percentualGeralUsado,'percentualGeralDisponivel':percentualGeralDisponivel,'totalEconomizado':totalEconomizado,
    'gastosTotaisFormatado':gastosTotaisFormatado,'creditosTotaisFormatado':creditosTotaisFormatado,
    'topCategoriasHomeValues':topCategoriasHome.values,'topCategoriasHome':topCategoriasHome.index,
    'topVereadoresHome':topVereadoresHome, 'topVereadoresMenoresGastosHome':topVereadoresMenoresGastosHome,
    'totalGastosMensaisHome':totalGastosMensaisHome})


def gastoGeralTotal():
    return debito.views.general_spendings.sum()

def creditoGeralTotal():
    return debito.views.df_credits_final["VALOR"].sum()

def topCategorias(num):
    x = {}
    x = round(debito.views.category_spendings.groupby(by = ["DESPESA"]).sum()).sort_values(ascending=False).head(num)
    return x

def topVereadores(num):
    total_spends_by_council = debito.views.all_spends_by_council.sum(1)
    total_spends_by_council.sort_values(ascending = False, inplace = True)
    #total_spends_by_council.index = total_spends_by_council.index.str.replace(pat='_', repl=' ')
    return round(total_spends_by_council.head(num)).map('R$ {:,.2f}'.format)

def topVereadoresMenoresGastos(num):
    total_spends_by_council = debito.views.all_spends_by_council.sum(1)
    total_spends_by_council.sort_values(ascending = True, inplace = True)
    #total_spends_by_council.index = total_spends_by_council.index.str.replace(pat='_', repl=' ')
    return round(total_spends_by_council.head(num)).map('R$ {:,.2f}'.format)

#def topVereadoresMenoresGastosPercentual(num):
#    percentual_usage = debito.views.all_spends_by_council.sum(1)/debito.views.total_credits_by_council.sum(1)
#    percentual_usage.sort_values(ascending = True, inplace = True)
#    return round(percentual_usage.head(num)).map('R$ {:,.2f}'.format)

def totalGastosMensais():
    x={}
    for i in range(12):
        try:
            x[i] = round(debito.views.df_final.groupby(by = ["ANO","MES"])['VALOR'].sum()[ano,i+1])
        except KeyError:
            x[i]=0
    return list(x.values())
