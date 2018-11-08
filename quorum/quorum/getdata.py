import numpy as np
import pandas as pd


#http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterDebitoVereadorJSON?ano=2018&mes=01
#http://freegeoip.net/json/

def getAllDebits(request):
    #import das solicitações de reembolso por mês
    df_2017_01 = pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterDebitoVereadorJSON?ano=2017&mes=01")
    df_2017_02 = pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterDebitoVereadorJSON?ano=2017&mes=02")
    df_2017_03 = pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterDebitoVereadorJSON?ano=2017&mes=03")

    #import dos créditos disponíveis pra cada vereador, mês a mês
    df_credits_2017_01 = pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterCreditoVereadorJSON?ano=2017&mes=01")
    df_credits_2017_02 = pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterCreditoVereadorJSON?ano=2017&mes=02")
    df_credits_2017_03 = pd.read_json("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterCreditoVereadorJSON?ano=2017&mes=03")

    #junção de todos os dataframes dos reembolsos
    frames_debits = [df_2017_01, df_2017_02, df_2017_03]
    df_final = pd.concat(frames_debits)

    return render(request, 'debito/alldebits.html',{'debits':df_final}
