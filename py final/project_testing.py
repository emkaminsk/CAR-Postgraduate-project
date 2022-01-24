# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 15:49:25 2017

@author: 125385

Plik do testowania.
"""

import importlib
import CAR_table_ranking as Ctr
import CMT_parser_Graph_constructor as CMTp
import Graph_analysis as Ga

importlib.reload(Ctr)
importlib.reload(CMTp)
importlib.reload(Ga)

def fits_testy():    
    fits_testy_case('a','a')
    fits_testy_case('as','asasas')
    fits_testy_case('a','asdfgh')
    fits_testy_case('a','b')

def fits_testy_case(par1, par2):
    print(par1, par2, Ctr.fits(par1,par2))

def fits_re_testy():    
    fits_re_testy_case('a','a')
    fits_re_testy_case('a','b.a')
    fits_re_testy_case('a','{b}.a')
    fits_re_testy_case('a','${b}.a')
    fits_re_testy_case('as','asasas')
    fits_re_testy_case('a','asdfgh')
    fits_re_testy_case('a','b')
    fits_re_testy_case('asdf_qaws','SUB_asdf_qaws')
    fits_re_testy_case('asdf_qaws','X.SUB_asdf_qaws')
    fits_re_testy_case('asdf_qaws','asdf_qaws_1')
    fits_re_testy_case('asdf_qaws','X.asdf_qaws_1')
    fits_re_testy_case('asdf_qaws_1','X.asdf_qaws_1')
    fits_re_testy_case('asdf_qaws_1','asdf_qaws_1')
    fits_re_testy_case('${CAR}.ACCOUNTS','${CAR}.ACCOUNTS')    
    fits_re_testy_case('${CAR}.ACCOUNTS','${CAR}.ACCOUNTS_1')    
    fits_re_testy_case('${CAR}.ACCOUNTS_1','${CAR}.ACCOUNTS')    
    fits_re_testy_case('${CAR}.ACCOUNTS','${CAR}.SUB_ACCOUNTS')  
    fits_re_testy_case('${CAR}.SUB_ACCOUNTS','${CAR}.ACCOUNTS')  
    fits_re_testy_case('${CAR}.ACCOUNTS','ACCOUNTS')    
    fits_re_testy_case('${CAR}.ACCOUNTS','SUB_ACCOUNTS') 
    fits_re_testy_case('${CAR}.ACCOUNTS_1','ACCOUNTS_1') 
    fits_re_testy_case('ACCOUNTS','${CAR}.ACCOUNTS')
    fits_re_testy_case('ACCOUNTS','${CAR}.ACCOUNTS_1')
    fits_re_testy_case('ACCOUNTS','${CAR}.SUB_ACCOUNTS')
    
def fits_re_testy_case(par1, par2):
    print(par1, par2, Ctr.fits_re(par1,par2))
    
def score_where_testy():
    score_where_testy_case([],[])
    score_where_testy_case(['a'],['a'])
    score_where_testy_case(['a'],['b'])
    score_where_testy_case(['a','b'],['a','b'])
    score_where_testy_case(['a','b'],['a','c'])
    score_where_testy_case(['a','b','c'],['a','c'])
    score_where_testy_case(['a','b','d'],['a','d'])
    score_where_testy_case(['a','b','d'],['a','c'])
    
def score_where_testy_case(par1, par2):
    print(par1, par2, Ctr.score_where(par1,par2))
    
def score_gb_testy():
    score_gb_testy_case([],[])
    score_gb_testy_case(['a'],['a'])
    score_gb_testy_case(['a'],['b'])
    score_gb_testy_case(['a','b'],['a','b'])
    score_gb_testy_case(['a','b'],['a','c'])
    score_gb_testy_case(['a','b','c'],['a','c'])
    score_gb_testy_case(['a','b','d'],['a','d'])
    score_gb_testy_case(['a','b','d'],['a','c'])
    
def score_gb_testy_case(par1, par2):
    print(par1, par2, Ctr.score_gb(par1,par2))   

def score_from_testy():
    score_from_testy_case(['a'],['a'])
    score_from_testy_case(['a'],['b'])
    score_from_testy_case(['a','b'],['a','b'])
    score_from_testy_case(['a','b'],['a','c'])
    score_from_testy_case(['a','b','c'],['a','c'])
    score_from_testy_case(['a','b','d'],['a','d'])
    score_from_testy_case(['a','b','d'],['a','c'])
    score_from_testy_case(['a','b','d'],['a','d','b'])
    
def score_from_testy_case(par1, par2):
    print(par1, par2, Ctr.from_not_fit(par1,par2),  Ctr.score_from(par1,par2))    
    
def score_calc_testy():
    score_calc_testy_case((['a'],['a'],[],[],['a'],['a']))
    score_calc_testy_case((['a'],['b'],[],[],['a'],['a']))
    score_calc_testy_case((['a','b'],['a','b'],[],[],['a'],['a']))
    score_calc_testy_case((['a','b','d'],['a','d','b'],[],[],['a'],['a']))
    
def score_calc_testy_case(par1):    
    print(par1, Ctr.score_calc(*par1))    
    
def sg_create_testy(g, lcp):
    sg_create_testy_case(g, lcp, 'CMT_CUST_PROD_6', 'ACCOUNTS')
    sg_create_testy_case(g,lcp, 'CMT_CIF_PROD_7','CMT_CIF_PROD_6')
    sg_create_testy_case(g,lcp, 'CMT_REL_CIF_2_PARTNER_1','CUST_PORTFOLIO_REL')
    sg_create_testy_case(g,lcp, 'CMT_CEKE_4','CMT_CEKE_0')
    sg_create_testy_case(g,lcp, 'CMT_CREDIT_4','CARD_ACCOUNT_REL')
    sg_create_testy_case(g,lcp, 'CMT_CREDIT_4','TR_DR_POS_LAST_21D_AMT') # nie powinno byc - Field
    sg_create_testy_case(g,lcp, 'CMT_CREDIT_4','CREDIT') #nie powinno byc - relacja Merge
    sg_create_testy_case(g,lcp, 'SUB_CMT_ACCOUNTS_CUST_2','CREDIT')
    
def sg_create_testy_case(g, lcp, par1, par2):
    print('Przypadek testowy: ', par1, par2, len(lcp[par1]))
    print('Wezly: ', str(list(lcp[par1])))
    print('\n' + 'Opis krawedzi miedzy par1 i par2:')
    d = Ctr.sg_edge_attr(lcp[par1],par2, par1)
    for k,v in d.items():
        print(k,v)
    print('\n' + 'Listy obiektow do analizy:')
    print(Ctr.sg_lists(lcp[par1], par1))
    print('\n')

def table_ranking_testy():
    table_ranking_testy_case(['CMT_ACCOUNTS_CUST_1','TREASURY_RATES','CREDIT,REL_CIF_2_PROD','REL_PROD_2_PROD','ACCOUNT_DETAIL_PERIODIC'], ['START_DT', 'WH_ACC_NO'],['WH_ACC_NO','WH_ACC_NO'])
    table_ranking_testy_case(['CMT_CREDIT_1', 'TRANSACTION_CARD_DETAIL_BZWBK', 'CARD_ACCOUNT_REL'], ['TRANSACTION_CARD_DETAIL_BZWBK.POSTED_DTE', 'CARD_ACCOUNT_REL.END_DTE'], [])
    table_ranking_testy_case(['CRM_PORTFOLIO', 'CUST_PORTFOLIO_REL'], ['CUST_PORTFOLIO_REL.END_DTE', 'CUST_PORTFOLIO_REL.WH_CUST_NO', 'CUST_PORTFOLIO_REL.STAFF_ROLE_CDE', 'CRM_PORTFOLIO.STAFF_SKP_NO', 'BASE_CUST_MAP.WH_CUST_NO', 'CRM_PORTFOLIO.STAFF_ROLE_CDE', 'CUST_PORTFOLIO_REL.STAFF_SKP_NO'], [])
    table_ranking_testy_case(['ACCOUNT_DETAIL_PERIODIC', 'CUSTOMER_ACCOUNT_REL'],['WH_ACC_NO','WH_ACC_NO','REL_TYP_CDE'],[])
            
def table_ranking_testy_case(par1, par2, par3):    #from, where, groupby
    wyniki, final_results = Ctr.table_ranking('d:\\projekty\\zajęcia na uczelni\\!tpd\\', 'car', par1, par2, par3)
    print('Najblizsze dopasowania dla:', par1, par2, par3)
    for x in range(min(len(final_results),5)):
        print(final_results[x], wyniki[final_results[x]])

    
"""
print('Funkcja fits' )    
fits_testy()
print('Funkcja fits_re' )    
fits_re_testy()

print('\n' + 'score where')
score_where_testy()
print('\n' + 'score group by')
score_gb_testy()
print('\n' + 'score from')
score_from_testy()
print('\n' + 'score calc')
score_calc_testy()
  
g, lcp = Ctr.load_graph()
#for k in lcp.keys():
#    print(k)
sg_create_testy(g, lcp)

"""
table_ranking_testy()
"""
CMTp.CMT_parser()
"""
