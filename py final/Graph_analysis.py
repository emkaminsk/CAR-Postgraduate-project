# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 14:36:46 2017

@author: 125385
Analiza grafu - budowa podgrafow.
"""

#from pathlib import Path
import networkx as nx

def analiza_p(node):
    for elem in g.predecessors_iter(node):
        if not elem in nbun:
            nbun.append(elem)    
            dummy = analiza_p(elem)

def analiza_s(node):
    for elem in g.successors_iter(node):
        if not elem in nbun:
            for u,v,d in g.in_edges_iter(nbunch=[elem], data=True):
                if u == node and v == elem and d['sql'] != 'In':
                     nbun.append(elem)    
                     dummy = analiza_s(elem)

def sg_create(car_part):
    nb = []
    for u,v,d in g.in_edges_iter(nbunch=car_part, data=True):
        if d['sql'] in ['From','Sel_Cond','Out_Sel_Cond','Group_By','Having','Qualify']:
            nb.append(u)
        if d['sql'] == 'In':
            nb.append(u)
            for u1,v1,d1 in g.in_edges_iter(nbunch=u, data=True):
                if d1['sql'] == 'Transform':            
                    nb.append(u1)    
    return nb

def Load_elems_from_graph(object_type, project_path, obj_name_part, filename='car'):
    g = nx.DiGraph() 
    g=nx.read_graphml(project_path + filename + ".graphml")
    temp = []
    if object_type == 'Pole':
        for elem, sql_type in g.nodes_iter(data=True):        
            if sql_type['sql'] == 'Field' and elem.count(obj_name_part) > 0:
                temp.append(elem)
    elif object_type == 'Tabela':
        for elem, sql_type in g.nodes_iter(data=True):        
            if sql_type['sql'] in ['Source','CAR_part','CAR'] and elem.count(obj_name_part) > 0:
                temp.append(elem)
    return sorted(temp)
                
#if __name__  == '__main__':     
def Graph_analysis(project_path, user_kontekst = 'CREDIT', kierunek ='z', filename = 'car'):    
    global g, nbun
    n = g = nx.DiGraph() 
    g=nx.read_graphml(project_path + filename + ".graphml")

    # czy podany wierzcholek jest w grafie?
    node = None
    for elem, sql_type in g.nodes_iter(data=True):
        if elem == user_kontekst:
            node = elem            
            node_sql = sql_type['sql']
            print('Jest!')
            break
    if node == None:    
        for elem, sql_type in g.nodes_iter(data=True):
            if elem.count(user_kontekst) > 0:
                node = elem            
                node_sql = sql_type['sql']
                print('Jest przybyliżony!')
                break
        else:
            print('Brak elementu w grafie...')
            exit
    
    nbun = []
    nbun.append(node)               
    
    # zbudowanie kolekcji wierzchołkow na podstawie nbunch dla kontekstu
    if kierunek == 'p':
        dummy = analiza_p(node)  
        
    elif kierunek == 's' or kierunek == 'n':
        dummy = analiza_s(node)  
    
    elif kierunek == 'a':
        dummy = analiza_p(node)  
        dummy = analiza_s(node)  
    
    elif kierunek == 'z':
        if node_sql == 'CAR':            
            for u,v,d in g.in_edges_iter(nbunch=node, data=True):
                if d['sql'] == 'Merge':
                    nbun.append(u)
                    nbun = nbun + sg_create(u)
        elif node_sql == 'CAR_part':
            for u,v,d in g.out_edges_iter(nbunch=node, data=True):
                if d['sql'] == 'Merge':
                    nbun.append(v)
            nbun = nbun + sg_create(node)
        elif node_sql == 'Field': # do dookreslenia co tu chcielibysmy zobaczyc
            for u,v,d in g.out_edges_iter(nbunch=node, data=True):
                if d['sql'] in ['In', 'From','Sel_Cond','Out_Sel_Cond','Group_By','Having','Qualify','Transform']:
                    nbun.append(v)
            for u,v,d in g.in_edges_iter(nbunch=node, data=True):
                if d['sql'] in ['In', 'From','Sel_Cond','Out_Sel_Cond','Group_By','Having','Qualify','Transform']:
                    nbun.append(u)
                if d['sql'] == 'In':
                    nbun.append(u)
                    for u1,v1,d1 in g.in_edges_iter(nbunch=u, data=True):
                        if d1['sql'] == 'Transform':            
                            nbun.append(u1)
    else:
        print('Blad kierunku!')
        exit
    
    print('Analiza zrobiona!')
    # utworzenie podgrafu na bazie g
    n = nx.subgraph(g, nbun)      
    
    nx.write_graphml(n,project_path + node + '_' + kierunek + ".graphml")
    return 'Plik ' + node + '_' + kierunek + '.graphml zapisany!'