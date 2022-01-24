# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 18:11:46 2017

@author: 125385

- zbudowanie słownika zawierającego dla każdego sql_part subgraf CARa zbudowany metodą 'z'
- (do napisania pozniej) wyciaganie parametrow kwerendy z sqla SELECT
- pozyskanie od użytkownika parametrow kwerendy do analizy
- modul porownywania (rankingu) kwerend z subgrafami ze slownika
    - dla kazdego sql_part porownywanie podanych parametrow, czy pasuja
    - wyliczenie rankingu sql_parta wg algorytmu: sg (subgraph) vs nq (new query)
        -jesli tabele nie pasuja: punktacja 0 i koniec algorytmu
        -jesli tabele pasuja ale warunki groupby sa inne, punktacja 1 i koniec algorytmu
        -jesli tabele pasuja czesciowo i da sie to pogodzic, punkt 2 i idziemy dalej
        -jesli warunki where sa takie same punkt 3
- petla powrotu do punktu 2/3

"""

#from pathlib import Path
import networkx as nx
import re
#import matplotlib.pyplot as plt

def load_graph(project_path, filename):
    g = nx.DiGraph() 
    g=nx.read_graphml(project_path + filename + ".graphml")
    lcp = {} #slownik ktorego elementami będą nazwy car_part a wartosciami subgrafy opisujące dany car_part (from, in, sel_cond itp)
    for car_part in g.nodes_iter(data=True):
        if car_part[1]['sql'] != 'CAR_part':
            continue
        else:        
            sg = sg_create(g, car_part[0])            
            lcp[clean_name(car_part[0])] = sg.copy()
    return g, lcp

def get_new_query_parts(sql=''):
    # pozyskanie parametrow do analizy: From, Sel_Cond oraz Group_by
    if sql == '':
        u_from = input("Podaj tabele z klauzuli From:")
        l_from = list(map(str.upper, map(str.strip, u_from.split(','))))
        u_where = input("Podaj pola z klauzuli Where:")
        l_where = list(map(str.upper, map(str.strip, u_where.split(','))))
        u_group_by = input("Podaj pola z klauzuli Group by:")
        l_group_by = list(map(str.upper, map(str.strip, u_group_by.split(','))))
    else: 
        l_from, l_where, l_group_by = parse_sql(sql)
    return l_from, l_where, l_group_by

def parse_sql(sql): # pozyskanie z kwerendy sql parametrow do analizy: From, Sel_Cond oraz Group_by
    l_from = []
    l_where= [] 
    l_group_by= []
    return l_from, l_where, l_group_by

def sg_create(graph, car_part): #funkcja tworzy subgraf dla danego car_part z całego załadowanego grafu
    nb = [car_part]
    for u,v,d in graph.in_edges_iter(nbunch=car_part, data=True):
        if d['sql'] in ['From','Sel_Cond','Out_Sel_Cond','Group_By','Having','Qualify']:
            nb.append(u)
        if d['sql'] == 'In':
            nb.append(u)
            for u1,v1,d1 in graph.in_edges_iter(nbunch=u, data=True):
                if d1['sql'] == 'Transform':            
                    nb.append(u1)   
    sg = nx.subgraph(graph, nb) #subgraf                
    return sg

def clean_name(str): #odrzucenie zbednej czesci ${CAR} czy ${CAR_TEMP}
    return str.split('.')[1]

def sg_lists(sg, cp): #funkcja zwraca potrzebne listy z sg dla zadanego car_part (cp)
    sg_tables_list = [] #sg_tables_list - lista tablic z sg
    sg_fields_gb_list = [] #sg_fields_gb_list - lista pol group_by z sg
    sg_fields_where_list = []#sg_fields_where_list - liste pol where z sg
    temp = {}   
    for elem, d in sg.nodes_iter(sg):
        if d['sql'] in ['Source','CAR_part','CAR']:
            dict=sg_edge_attr(sg, elem, cp)
            if dict == {}:
                continue
            elif dict['sql'] == 'From':
                temp[elem] = dict['From_id']
        elif d['sql'] == 'Field':
            dict=sg_edge_attr(sg, elem, cp)
            if dict == {}:
                continue
            elif dict['sql'] == 'Group_By':                
                sg_fields_gb_list.append(elem)
            elif dict['sql'] in ['Sel_Cond', 'Out_Sel_Cond']:
                sg_fields_where_list.append(elem)    
    sg_tables_list = sorted(temp, key=temp.get) 
    #[temp[k] for k in sorted(temp)]
    return sg_tables_list, sg_fields_gb_list, sg_fields_where_list
                                
def sg_edge_attr(sg, psor, ssor): #funkcja do zwracania atrybutow krawedzi dla dwoch wierzcholkow w grafie sg
    for u,v,d in sg.edges_iter(data=True):
        if fits_re(psor,u) and fits_re(ssor,v):
            return d
            break
    else:
        return {}

def score_calc(l_from, sg_from,l_group_by, sg_gb,l_where, sg_where): # funkcja do wyliczenia skoringu 
    if from_not_fit(l_from, sg_from) == True:
        return -1
    score = score_from(l_from, sg_from)
    if score == -1:
        return score
    score += score_gb(l_group_by, sg_gb)    
    score += score_where(l_where, sg_where)
    return score
    
def from_not_fit(n_tables, sg_tables): #funkcja do sprawdzenia, czy w ogole cokolwiek pasuje
    #sg_tables - lista tabel z sg w kolejnosci rosnacego From_id
    #n_tables - lista tabel z nowej kwerendy w kolejnosci rosnacego from_id
    #funkcja zwraca True, jesli zaden element n_tables nie znajduje sie w sg_tables    
    for nt in n_tables:
        for st in sg_tables:
            if fits_re(nt, st):
                return False
    return True

def score_from(n_tables, sg_tables): #czy zbior tabel jest w tej samej kolejnosci?
    #funkcja zwraca -1, jesli porownanie dwoch list pokazuje odmienna kolejnosc wezlow 
    #w przeciwnym wypadku zwracana jest liczba pasujacych tabel
    temp = -1
    score = 0
    for x in range(len(n_tables)):
        for y in range(len(sg_tables)):
            if fits_re(n_tables[x], sg_tables[y]):
                if y > temp:
                    temp = y
                    score += 1
                else:
                    return -1
    return score                

def score_gb(n_gb_fields, sg_gb_fields): #funkcja do punktowania subgrafu wg group by
    if len(n_gb_fields) == len(sg_gb_fields) == 0:
        return 1
    if len(n_gb_fields) != len(sg_gb_fields):
        return 0
    for n_elem in n_gb_fields:
        flaga = False
        for sg_elem in sg_gb_fields:
            if fits_re(n_elem,sg_elem):
                flaga = True
        if flaga == False:
            return 0
    return 1

def score_where(n_where_fields, sg_where_fields): #funkcja do punktowania subgrafu wg kolejnosci w where
    for n_elem in n_where_fields:
        flaga = False
        for sg_elem in sg_where_fields:
            if fits_re(n_elem,sg_elem):
                flaga = True
        if flaga == False:
            return 0
    return 1
  
def fits_re(check_str, graph_str):
    if bool(re.search(r'(^|\.)' + re.escape(check_str) + '$',graph_str)):
        return True
    else:
        return False        
    
#if __name__  == '__main__':     
def table_ranking(project_path, filename ='car', l_from=[], l_group_by=[], l_where=[]):
    print('OK')
    g, lcp = load_graph(project_path, filename)
    if l_from == [] and l_group_by == [] and l_where == []:
        return ['Brak obiektow do analizy!'], None
        #l_from, l_group_by, l_where = get_new_query_parts()   
    wyniki = {}
    for nazwa, subgraph in lcp.items():   #wyliczanie scoringu/rankingu dla kolejnych car_part        
        sg_from, sg_gb, sg_where = sg_lists(subgraph, nazwa) #wyciaganie list obiektow z subgrafow
        score = score_calc(l_from, sg_from,l_group_by, sg_gb,l_where, sg_where)
        if score == -1:
            continue
        wyniki[nazwa] = score 
    # sortowanie wynikow i ich prezentacja
    final_results = sorted(wyniki, key=wyniki.get, reverse = True)  
    return wyniki, final_results
    
"""    
weryfikacja zgodnosci
1) czy tabele pasuja? From
2) czy groupby pasuje? 
    
uniwersalne pytania:
- czy w grafie jest node z okreslonym sql? - funkcja sg_node_sql
- jesli w grafie jest node z danym sql, to jakie ma id? - funkcja sg_node_id
    
stopnie poszczegolnych wierzcholkow
print(nx.degree(lcp['${CAR}.CMT_CIF_PROD_16'])) 
    
density = [(k, nx.density(w)) for (k,w) in lcp.items()]
print(density)

sortowanie
from operator import itemgetter
print(density.sort(key=itemgetter[1]))

przeglad wszystkich subgrafow
for k,w in lcp.items():
    print(k + '\n')
    nx.draw_random(w)
    plt.show()  

Funkcje na zapas:
    
def sg_edge_check(sg, psor, ssor, type): #funkcja do sprawdzania, czy w sg jest krawedz type laczaca psor i ssor
    for u,v,d in nx.edges_iter(nbunch=sg, data=True):
        if fits(u,psor) and fits(v,ssor) and d['sql']==type: #zmienilem kolejnosc u i v
            return True
            break
        else:
            return False
            
def sg_node_check(sg, node, sql_type): #funkcja do sprawdzenia, czy w grafie jest node z okreslonym sql
    for elem,d in sg.nodes_iter(data=True):
        if fits(elem, node) and d['sql'] == sql_type:
            return True
            break
    else:
        return False

def sg_node_id(sg, node, sql_type):  #funkcja do sprawdzenia, jesli w grafie jest node z danym sql_type, to jakie ma id?   
    for elem,d in sg.nodes_iter(data=True):
        if fits(elem, node) and d['sql'] == sql_type:
            return int(d['From_id'])
            break
    else:
        return -1

def fits(check_str, graph_str): #funkcja do sprawdzenia, czy string check_str pasuje do graph_str
    if graph_str.count(check_str) > 0:
        return True
    else:
        return False            
"""
#print([(k, id(w)) for (k,w) in lcp.items()])