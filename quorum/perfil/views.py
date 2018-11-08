from django.shortcuts import render
import debito.views

def perfil(request, vereador):
    vereadorPretty = debito.views.vereadorPretty(vereador)

    gastosVereador = debito.views.gastos(vereador)
    creditosVereador = debito.views.creditos(vereador)

    usoCotaVereador = round(100*(1-((creditosVereador - gastosVereador)/creditosVereador)))
    cotaDisponivel = round(100-usoCotaVereador)



    gastosMensaisVereador = debito.views.gastosMensais(vereador)
    gastosPorCategoriaVereador = debito.views.gastosPorCategoria(vereador)
    mediaGastosPorCategoria = debito.views.mediaGastosPorCategoria(vereador)
    lenGastosPorCategoriaVereador = len(gastosPorCategoriaVereador)

    mediaGastosMensaisGeral = debito.views.mediaGastosMensais()
    totalDeCategoriasVereador = debito.views.totalDeCategorias(vereador)
    keyTotalDeCategoriasVereador = 1620/totalDeCategoriasVereador

    mediaGastos = debito.views.mediaGastosGerais()
    mediaCreditos = debito.views.mediaCreditosGerais()

    usoCotaGeral = 100*(1-((mediaCreditos - mediaGastos)/mediaCreditos))
    cotaDisponivelGeral = 100-usoCotaGeral




    return render(request, 'perfil/perfil.html',{'vereadorPretty':vereadorPretty,'vereador':vereador,
    'gastosVereador':gastosVereador,'creditosVereador':creditosVereador,'usoCotaVereador':usoCotaVereador,'cotaDisponivel':cotaDisponivel,
    'gastosMensaisVereador':list(gastosMensaisVereador),
    'gastosPorCategoriaVereador':gastosPorCategoriaVereador,'lenGastosPorCategoriaVereador':range(lenGastosPorCategoriaVereador),
    'mediaGastosMensaisGeral':mediaGastosMensaisGeral, 'mediaGastosPorCategoria':mediaGastosPorCategoria,
    'keyTotalDeCategoriasVereador':keyTotalDeCategoriasVereador,'usoCotaGeral':usoCotaGeral,'cotaDisponivelGeral':cotaDisponivelGeral})
