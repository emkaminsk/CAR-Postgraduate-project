# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 23:22:56 2017

@author: 125385
"""

import sys
from PyQt5 import QtWidgets, uic
import importlib
import CAR_table_ranking as Ctr
import CMT_parser_Graph_constructor as CMTp
import Graph_analysis as Ga

importlib.reload(Ctr)
importlib.reload(CMTp)
importlib.reload(Ga)
 
qtCreatorFile = "parser_app_v2.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class CMT_Widget(QtWidgets.QTabWidget, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.project_path = self.CMT_project_path_textbox.text()        
        self.CMT_parse_button.clicked.connect(self.CMT_Parse)
        self.object_type_list.addItems(['Pole','Tabela'])
        self.object_type_list.currentItemChanged.connect(self.Load_List)
        self.name_lineedit.textChanged.connect(self.Load_List)
        self.range_list.addItems(['Wszystkie','Poprzedniki','Nastepniki','Zakładka'])              
        self.generate_subgraph_button.clicked.connect(self.Graph_analysis)
        self.From = []
        self.Where = []
        self.Gb = []
        self.Clear_From_pb.clicked.connect(self.Clear)
        self.Clear_Where_pb.clicked.connect(self.Clear)
        self.Clear_Gb_pb.clicked.connect(self.Clear)
        self.Del_From_pb.clicked.connect(self.Delete)
        self.Del_Where_pb.clicked.connect(self.Delete)
        self.Del_Gb_pb.clicked.connect(self.Delete)
        self.nazwa_TRT_lineedit.returnPressed.connect(self.TRT_Add_object_from_line)
        self.zaczytaj_obiekt_pb.clicked.connect(self.TRT_Add_object_from_analyse_tab)
        self.wylicz_ranking_pb.clicked.connect(self.CAR_table_ranking)
          
    def CMT_Parse(self):
        self.Parse_result_status.setText('Uruchomione!')
        self.completed = 0
        wynik = CMTp.CMT_parser(self.parse_progress_Bar, self.project_path, self.CMT_directory_textbox.text(), self.result_filename_textBox.text())
        self.Parse_result_status.setText(wynik)
 
    def Load_List(self):
        #self.Parse_result_status.setText(self.object_type_list.currentItem().text())
        self.object_list.clear()        
        wybor = self.object_type_list.currentItem().text()
        plik = self.result_filename_textBox.text()
        fragment_nazwy = self.name_lineedit.text()
        wynik = Ga.Load_elems_from_graph(wybor, self.project_path, fragment_nazwy, plik)
        self.object_list.addItems(wynik)
                        
    def Graph_analysis(self):
        self.subgraph_status.setText('Gotowy! Wybierz obiekt i kierunek powyżej.')
        zaznaczony_obiekt = self.object_list.currentItem().text()
        if zaznaczony_obiekt != '':
            self.subgraph_status.setText('Obiekt zaznaczony! Wybierz kierunek analizy.')
        if self.range_list.currentItem().text() == 'Wszystkie':
            kierunek_analizy = 'a'
        elif self.range_list.currentItem().text() == 'Poprzedniki':
            kierunek_analizy = 'p'
        elif self.range_list.currentItem().text() == 'Nastepniki':
            kierunek_analizy = 'n'
        elif self.range_list.currentItem().text() == 'Zakładka':
            kierunek_analizy = 'z'
        if kierunek_analizy in ['a','p','n','z']:
            self.subgraph_status.setText('Kierunek wybrany! Wybierz obiekt do analizy.')
        plik_z_baza_car = self.result_filename_textBox.text()
#        print(self.project_path, zaznaczony_obiekt, kierunek_analizy, plik_z_baza_car)        
        if kierunek_analizy in ['a','p','n','z'] and zaznaczony_obiekt != '':
            wynik = Ga.Graph_analysis(self.project_path, zaznaczony_obiekt, kierunek_analizy, plik_z_baza_car)
            self.subgraph_status.setText(wynik)
        else:
            #print(zaznaczony_obiekt)
            self.subgraph_status.setText('Cos jest nie tak! Wybierz obiekt i kierunek powyżej.')

    def Clear(self):               
        button = self.sender()
        if button.objectName() == 'Clear_From_pb':
            self.From = []
            self.Lista_obiektow_From.setText('')
        elif button.objectName() == 'Clear_Where_pb':
            self.Where = []
            self.Lista_obiektow_Where.setText('')
        elif button.objectName() == 'Clear_Gb_pb':
            self.Gb = []
            self.Lista_obiektow_Gb.setText('')
            
    def Delete(self):
        sender = self.sender()
        if sender.objectName() == 'Del_From_pb':
            junk = self.From.pop()
            self.Lista_obiektow_From.setText(str(self.From))
        elif sender.objectName() == 'Del_Where_pb':
            junk = self.Where.pop()
            self.Lista_obiektow_Where.setText(str(self.Where))
        elif sender.objectName() == 'Del_Gb_pb':
            junk = self.Gb.pop()
            self.Lista_obiektow_Gb.setText(str(self.Gb))
            
    def TRT_Add_object_from_line(self):
        if self.From_rb.isChecked():
            self.From.append(self.nazwa_TRT_lineedit.text())
            self.Lista_obiektow_From.setText(str(self.From))
        elif self.Where_rb.isChecked():
            self.Where.append(self.nazwa_TRT_lineedit.text())
            self.Lista_obiektow_Where.setText(str(self.Where))    
        elif self.Gb_rb.isChecked():
            self.Gb.append(self.nazwa_TRT_lineedit.text())
            self.Lista_obiektow_Gb.setText(str(self.Gb))           
        if self.From_rb.isChecked() or self.Where_rb.isChecked() or self.Gb_rb.isChecked():  
            self.nazwa_TRT_lineedit.setText('')    
            self.wyniki_TRT_text.setText('')            
        if not (self.From_rb.isChecked() or self.Where_rb.isChecked() or self.Gb_rb.isChecked()):
            self.wyniki_TRT_text.setText('Wybierz rodzaj obiektu!')                    
    
    def TRT_Add_object_from_analyse_tab(self):
        if self.From_rb.isChecked():
            if self.object_type_list.currentItem().text() == 'Pole':
                self.wyniki_TRT_text.setText('Niepoprawny rodzaj obiektu!')
            else:
                self.From.append(self.object_list.currentItem().text())
                self.Lista_obiektow_From.setText(str(self.From))
        elif self.Where_rb.isChecked():
            if self.object_type_list.currentItem().text() == 'Tabela':
                self.wyniki_TRT_text.setText('Niepoprawny rodzaj obiektu!')
            else:            
                self.Where.append(self.object_list.currentItem().text())
                self.Lista_obiektow_Where.setText(str(self.Where))        
        elif self.Gb_rb.isChecked():
            if self.object_type_list.currentItem().text() == 'Tabela':
                self.wyniki_TRT_text.setText('Niepoprawny rodzaj obiektu!')
            else:            
                self.Gb.append(self.object_list.currentItem().text())
                self.Lista_obiektow_Gb.setText(str(self.Gb))        
        else:
            self.wyniki_TRT_text.setText('Wybierz rodzaj obiektu!')

    def CAR_table_ranking(self):
        text_do_prezentacji = ''
        wyniki, final_results = Ctr.table_ranking(self.project_path, self.result_filename_textBox.text(), self.From, self.Gb, self.Where)
        for x in range(min(len(final_results),5)):
            p = '' if x == 0  else '\n'
            text_do_prezentacji = text_do_prezentacji + p + str(x) + ':  ' + str(final_results[x]) + '   ' + str(wyniki[final_results[x]])
        self.wyniki_TRT_text.setText('Zakończone!\n' + text_do_prezentacji)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    window = CMT_Widget()
    window.show()
    sys.exit(app.exec_())