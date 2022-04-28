from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
import urllib
from urllib.request import urlopen
import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup

#sprawdzamy połączenie z internetem
try:
    if requests.get('https://google.com').ok:
        X = 1
except:
        X = 0


class exchange:

    def __init__(self):

        #gdy mamy połączenie z internetem, sczytujemy plik xml ze strony i zapisujemy go
        if X == 1:
            self.response = urllib.request.urlopen("https://www.nbp.pl/kursy/xml/LastA.xml")
            self.tree = etree.parse(self.response)
            self.root = self.tree.getroot()
            self.tree.write("tabela.xml")
            
        #gdy nie mamy internetu, sczytujemy ostatnio zapisany plik
        elif X == 0:
            self.tree = etree.parse("tabela.xml")
            self.root = self.tree.getroot()
            
        #tworzymy listę z walutami i dodajemy PLN
        choice = []
        for i in range(2,36):
            choice.append(self.root[i][2].text)
        choice.append('PLN')

        #ustawiamy parametry aplikacji
        self.window = Tk()
        self.window.title(u'Walutomat')
        self.window.geometry('545x250')


        #ustawiamy napis i pierwszą rozsuwaną listę z walutami
        self.choiceIn = tk.StringVar()
        self.currencyInLabel = tk.Label(self.window, text = "Waluta źródłowa:")
        self.currencyInLabel.grid(column = 0, row = 0)

        self.choosingIn = ttk.Combobox(self.window, textvariable = self.choiceIn)
        self.choosingIn['values'] = choice
        self.choosingIn.grid(column = 1, row = 0, sticky = E)


        #ustawiamy napis i drugą rozsuwaną listę z walutami
        self.choiceOut = tk.StringVar()
        self.currencyOutLabel = tk.Label(self.window, text = "Waluta docelowa:")
        self.currencyOutLabel.grid(column = 2, row = 0, sticky = E)

        self.choosingOut = ttk.Combobox(self.window, textvariable = self.choiceOut)
        self.choosingOut['values'] = choice
        self.choosingOut.grid(column = 3, row = 0)


        #ustawiamy napis i pole do wprowadzenia kwoty
        self.value = tk.StringVar()
        self.valueLabel = tk.Label(self.window, text = "Podaj kwotę:")
        self.valueLabel.grid(column = 1, row = 1, pady = 20, sticky = E)

        self.entryValue = tk.Entry(self.window, width = 20, textvariable = self.value)
        self.entryValue.grid(column = 2, row = 1)


        #ustawaimy przycisk oblicz, który urochomi funkcje calculate
        self.resultButton = tk.Button(self.window, text = "Oblicz", command = self.calculate)
        self.resultButton.grid(column = 1, row = 2, columnspan = 2)


        #ustawiamy miejsce na wynik
        self.outcomeLabel = tk.Label(self.window, text = "Kwota w walucie docelowej:")
        self.outcomeLabel.grid(column = 1, row = 3,pady = 20)                         


        self.displayOutcome = tk.Label(self.window, text = "", relief = SUNKEN, width = 20)
        self.displayOutcome.grid(column = 2, row = 3,pady = 20)


        #dodajemy przycisk koniec
        self.end = tk.Button(self.window, text = "Koniec", command = quit)
        self.end.grid(column = 1, row = 4, columnspan = 2, pady = 20)


        #sprawdzamy jakie waluty zostały wybrane
        self.choosingIn.bind("<<ComboboxSelected>>", self.choiceOfFirstCurrency)
        self.choosingOut.bind("<<ComboboxSelected>>", self.choiceOfSecondCurrency)
        

        self.window.mainloop()

    #zapisujemy walute źródłową
    def choiceOfFirstCurrency(self, event):
        self.firstCurrency = str(self.choiceIn.get())
    

    #zapisujemy walutę docelową
    def choiceOfSecondCurrency(self, event):
        self.secondCurrency = str(self.choiceOut.get())
        
        
    def calculate(self):
        #nasza podana kwota
        self.newValue = float(self.value.get())

        #każda waluta ma przypisaną wartość
        #Teraz sprawdzamy która waluta w kolejności została wybrana z listy
        #i dopasowujemy do niej odpowiednią kwotę. Jako,że dodaliśmy walutę PLN,
        #która jest poza oryginalną listą to dla niej dajemy przelicznik 1 w osobnym przypadku
        inIndex = 2
        while inIndex < 37 and self.firstCurrency != self.root[inIndex][2].text:
            inIndex += 1
        if inIndex < 37:
            self.rateIn = self.root[inIndex][3].text
            self.rateIn = self.rateIn.replace(',','.')
        else:
            self.rateIn = 1

        outIndex = 2
        while outIndex < 37 and self.secondCurrency != self.root[outIndex][2].text:
            outIndex += 1
        if outIndex < 37:
            self.rateOut = self.root[outIndex][3].text
            self.rateOut = self.rateOut.replace(',','.')
        else:
            self.rateOut = 1

        #mechanizm przeliczania walut daje wynik
        y = self.newValue * float(self.rateIn)
        self.outcome = round(y/float(self.rateOut), ndigits = 2)

        #nasze miejsce na wynik nadpisujemy nową etykietą
        self.displayOutcome = tk.Label(self.window, text = "%s"%(self.outcome),relief = SUNKEN, width = 20)
        self.displayOutcome.grid(column = 2, row = 3, pady = 20)


exchange()

