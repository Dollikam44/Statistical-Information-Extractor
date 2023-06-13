
import pdfminer.high_level
import pdfminer.layout
import nltk
import os
import re
import csv
from collections import OrderedDict
import tkinter as tk
from tkinter import filedialog
import pandas as pd


#diese Funktion ist für das Löschen von Absatzüberschrifften und ihre Nummernaus dem Textinhalt
def remove_headers(text):
    #Teile Text in lines
    lines = text.split('\n')
    #for schleife geht durch alle Lines und Sucht,ob Anfang jedes Line ein Absatzüberschrifft Nummer existiert, fals Ja lösche die Line
    filtered_lines = [line for line in lines if not line.startswith(('1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ','1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) and not line.isupper()]
    filtered_text = '\n'.join(filtered_lines)
    return filtered_text

#in diese Funktion geht es, um Textinhalt aus PDF zu extrahiren und einem neuen .txt Fiel zu schreiben
def convert_pdf_to_txt():
    #Wähle PDF-Path oder mehr als einem PDF-Path
    pdf_file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
    #Falls kein Problem mit ausgewählten Pathes existieren
    if pdf_file_paths:
        #Wähle Speicherort für die neue .txt Files
        txt_save_directory = filedialog.askdirectory(title="Select directory to save .txt files")
        #Falls es keine Probleme mit Speicheort existiert
        if txt_save_directory:
            #For schleige geht durch alle ausgewählte PDF-Pathes
            for pdf_file_path in pdf_file_paths:
                #öffne PDF-File
                with open(pdf_file_path, 'rb') as file:
                    #Extrahiere Textinhalt aus PDF mithilfe von pdfminer
                    pdf_doc = pdfminer.high_level.extract_text(file)
                #Speichere Extrahierte Text in Filtered_text
                filtered_text = pdf_doc
                #Lösche Extraabstände zwischen Wörter, Zeilen und TextBoxses
                filtered_text = ' '.join(filtered_text.strip().split())
                #Lösche Quellen Liste am Ende de PDFs
                references_pattern = r'References \[1\].*'
                filtered_text = re.sub(references_pattern, 'References [1]', filtered_text, flags=re.DOTALL)
                #Ersetze Quellen Nummern durch Leerzeichen
                filtered_text = re.sub(r'\[[0-9]+\]', '', filtered_text)
                #Lösche Extraabstände Nach dem Löschen von Quellen Nummern zwischen Textinhalt
                filtered_text = ' '.join(filtered_text.strip().split())
                #Speichere neue Filterd Text in pages
                pages = filtered_text.split('\f')
                #Extrahiere PDF-Name, damit diese Name bei Bennenung von .txt File und auch Bennenumg von .csv File später genutzt werden kann
                pdf_file_name = os.path.splitext(os.path.split(pdf_file_path)[-1])[0]
                #Erstelle .txt File, dass das gleicher Name wie PDF hat und Speicher erstellte .txt File in ausgewählte Speicherort
                txt_file_path = os.path.join(txt_save_directory, pdf_file_name + '.txt')
                #Öffne die neute .txt File
                with open(txt_file_path, 'w', encoding='utf-8') as file:
                    #Schreibe extrahiehrt filterde Textinhalt in .txt File
                    for i, page in enumerate(pages):
                        file.write(page)
                #Schreibe in Interface, dass Textinhalt ohne Probleme Extrahiert wurde
                print(f'Text extracted and saved to {txt_file_path} successfully.')
            txt_text.delete(1.0, tk.END)
            txt_text.insert(tk.END, f'Text extracted without removing Headers and saved to {txt_file_path} successfully.')



#in diese Funktion geht es, um Textinhalt aus PDF zu extrahiren,
#unrelevante Ausdruke aus Extrahierte Textinhalt zu löschen
#und Endergebniss von maschinenlesbaren Text in einem neuen .txt Fiel zu schreiben
#diese Funktion funktioniert wie obere Funktion aber hier werden die Absatzüberschriften und Fußzeilen gelöscht
def convert_pdf_to_txt2():
    pdf_file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
    if pdf_file_paths:
        txt_save_directory = filedialog.askdirectory(title="Select directory to save .txt files")
        if txt_save_directory:
            for pdf_file_path in pdf_file_paths:
                with open(pdf_file_path, 'rb') as file:
                    pdf_doc = pdfminer.high_level.extract_text(file)
                filtered_text = remove_headers(pdf_doc)  # Call remove_headers function
                filtered_text = ' '.join(filtered_text.strip().split())
                references_pattern = r'References \[1\].*'
                filtered_text = re.sub(references_pattern, 'References [1]', filtered_text, flags=re.DOTALL)
                filtered_text = re.sub(r'\[[0-9]+\]', '', filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                #filtered_text = re.sub(r'\([0-9]+\)', '', filtered_text)
                #Lösche Ausdrucke wie "in Section" and "Figure 1" usw.
                filtered_text = re.sub(r'[Ss]ection\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = re.sub(r'[Ss]ections\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                filtered_text = re.sub(r'[iI]n [Ss]ection\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = re.sub(r'[Ii]n [Ss]ections\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                filtered_text = re.sub(r'[fF]igure\s*(\d+(?:\.\d+)*)[.,):]?', '', filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                filtered_text = re.sub(r'Eighteenth Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ Eighteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Eighteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Seventeenth Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ Seventeenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Seventeenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Sixteenth Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ Sixteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Sixteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Fifteenth Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ Fifteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Fifteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Fourteenth Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ Fourteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Fourteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Thirteenth Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ Thirteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Thirteenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'2016 Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ 2016 Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'2016 Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'2015 Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ 2015 Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'2015 Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Tenth Symposium on Usable Privacy and Security \d+', '', filtered_text)
                filtered_text = re.sub(r'\d+ Tenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Tenth Symposium on Usable Privacy and Security', '', filtered_text)
                filtered_text = re.sub(r'Train TravelNonePap.Dig.Certificate Type107812241091543296537213402654School/Child CareNonePap.Dig.Certificate Type227338027399921741156013001119Grocery', '', filtered_text)
                filtered_text = re.sub(r'PerspicuityDependabilityStimulationEfficiencyNoveltyAttractiveness−3−2−10123Windows HelloPassword', '', filtered_text)
                filtered_text = re.sub(r'USENIX Association', '',filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                #save filterd Textinhalt in Pages
                pages = filtered_text.split('\f')
                pdf_file_name = os.path.splitext(os.path.split(pdf_file_path)[-1])[0]
                txt_file_path = os.path.join(txt_save_directory, pdf_file_name + '.txt')
                with open(txt_file_path, 'w', encoding='utf-8') as file:
                    for i, page in enumerate(pages):
                        file.write(page)
                print(f'Text extracted and saved to {txt_file_path} successfully.')
            txt_text.delete(1.0, tk.END)
            txt_text.insert(tk.END, f'Text extracted without Headers and saved to {txt_file_path} successfully.')


#lade wichtige nlts (NLP) wichtige Packages
#tokanizieret gegebenen Text in Sätze und Wörter
nltk.download('punkt') #The Punkt tokenizer is a pre-trained unsupervised machine learning model for tokenizing text into sentences and words. It is widely used in natural language processing (NLP) applications.
#damit jede Wort im Text taggiert wird, und das ist wichtig für Sätze Vrestehen, damit die Sätze richtig tokaniesiert werden können
nltk.download('averaged_perceptron_tagger')# POS tagging is the process of labeling each word in a text with its corresponding part of speech (such as noun, verb, adjective, etc.).

#Hier geht es um die Methode von Extraktion der Sätze, die wichtige statistische Werte und Contexte enthalten
def extract_statistical_info(file_path):
    #öffne die ausgewählte .txt File Path
    with open(file_path, 'r', encoding='utf-8') as file:
        #lese Inhalt von .txt File
        text = file.read()
    #Extrahiere der Name von .txt File, damit der Name genutzt in Umbenennung von .csv File kann
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    #tokaniziere den Text in .txt File in Sinvolle Sätze mithilve von nltk Bibliothek
    sentences = nltk.sent_tokenize(text)
    #Erstlle Klassifizierte Pattarns (Taggierte Patterns) mithilfe von re, für die wichtigeste statistische Ergebnisse, Tests, Values, Konzepten usw.
    tags = [
        # p-values
        (r"p\s*(?:[<=>])\s*(0\.(?!\D+)[\d),.;]+|(?!\D+)1(?!\D+)|\.(?!\D+)[\d),.;])\s*", 'p-value'),
        (r"\(?\s*p\s*[:=><]\s*0\.\d+\s*\)?\.?,?", 'p-value'),
        (r"\(?\s*p\s*-?\s*value\s*[:=><]\s*0\.\d+\s*\)?\.?,?", 'p-value'),

        (r"\(?p\s*(?:[<=>])\s*1\.(?!\D+)[\d),.;]\s*", 'p-value'),
        (r'[pP]-?[Vv]alues?.* was .*([Ss]maller|[Bb]igger)\s*.*\s*\d+\.(?!\D+)[\d),.;]+', 'p-value'),
        (r'-*[pP]-?[Vv]alues?.*', 'p-value Context'),
        (r'0\.05\s*p\s*[–-]?\s*[Vv]alue', 'p-value Context'),
        #corrected p-value
        (r"\s*corrected\s*[–-]\s* p[–-]?\s*[vV]?a?l?u?e?s?\s*", 'corrected p-value'),
        #(r"\(?cor\s*[–-]?\s*p\s*(?:[<=>])\s*(0\.(?!\D+)[\d),.;]+|(?!\D+)1(?!\D+)|\.(?!\D+)[\d),.;])\s*", 'corrected p-value'),
        # Bonferroni-Holm
        (r"Bonferroni[–-]?\s*H?o?l?m?", 'Bonferroni-Holm context'),

        # mean
        (r'\(?\s*[mM]ean\s*[=:]\s*([\d.]+)[s%]?\s*\)', 'Mean value'),# entwieder secunde oder prozent oder keiner davon [s%]?
        (r'\(?[Mm]ean\s*[=:]?\s*\b([+-]?\d+(?:\.\d+)?)\b', 'Mean value'),
        (r'([Tt]he\s*|\s*\(?)[mM]ean .*\s*([Ww]as|are) (\d+.(?!\D+)[\d),.;]+[s%]?|([\d.]+)[s%]?|\b([+-]?\d+(?:\.\d+)?)\b)\s*', 'Mean value'),
        (r' \(?[mMµ]\s*[=:]\s*\d+.(?!\D+)[\d),.;]+[s%]?\s*', 'Mean value'),
        (r'\(?\s*[Mm]ean of (\d+\.\d+[s%]?|\d+[s%]?)\)?\.?\,?', 'Mean value'),
        (r'\(?\s*[Mm]ean .* of (\d+\.\d+[s%]?|\d+[s%]?)\)?\.?\,?', 'Mean value'),


        # standard deviation
        (r'[Ss]tan-?dard [Dd]eviation\s*.*\s*(of|was set to)\s*\d+\.\d+', 'Standard Deviation Value'),
        (r'.*\(?([Ss][Tt]?[dD]|σ)\s*[=:]\s*\b(\d+(?:\.\d+)?)\b\)?.*', 'Standard Deviation Value'),
        (r'.*\s*(\(?\s*[Ss]tandard [Dd]eviation\s*\)?| \(?\s*[Ss][Tt][Dd]\s*\)? )\s*', 'Standard Deviation Value'),
        (r'\(?\s*[Ss][Dd]\s*[:=]\s*\b(\d+(?:\.\d+)?)\b\)?\.?\)?', 'Standard Deviation Value'),
        (r'\(?\s*(?:S|s)(?:D|d)\s*[:=]\s*\b(\d+(?:\.\d+)?)\b\)?\.?\)?', 'Standard Deviation Value'),
        (r' \(\s*[Ss][Dd]\s*\)\.?,? ', 'Standard Deviation Context'),
        (r'\(?\s*σ2\s*[:=]\s*[+–-]?\s*\d+\.\d+\s*\)?\.?,?', 'σ^2 Value'),

        # Median
        (r'\(?[mM]edian\s*[:=]?\s*([\d.]+)[s%]?\)', 'Median value'), # entwieder secunde oder prozent oder keiner davon [s%]?
        (r'\(?[Mm]edian\s*[=:]?\s*\b([+-]?\d+(?:\.\d+)?)\b', 'Median value'),
        (r'\(?[Mm][Dd]\)?\s*[=:]?\s*\b([+-]?\d+(?:\.\d+)?)\b', 'Median value'),
        (r'([Tt]he\s*|\s*)[mM]edian .*([Ww]as|of)\s*(\d+.(?!\D+)[\d),.;]+[s%]?|([\d.]+)[s%]?|\b([+-]?\d+(?:\.\d+)?)\b)\s*','Median value'),

        #Max
        (r'\(?[mM]ax\s*[:=]\s*.*', 'Max value'),
        #Min
        (r'\(?[mM]in\s*[:=]\s*.*', 'Min value'),

        #Odds Ratio Value
        (r'.*\s*[oO]dds?\s*[Rr]atio\s*(of |[=:]?\s*0\.(?!\D+)[\d),.;]+|[=:]?\s*(?!\D+)1(?!\D+)|[=:]?\s*\.(?!\D+)[\d),.;])\s*.*','Odds Ratio Value '),
        (r' [Oo][Rr]\s*[:=]\s*','Odds Ratio Value '),
        (r'\(?\s*[Oo][Rr]\s*[:=]\s*(1|[+–-]?0\.(?!\D+)[\d),.;]+|[+–-]?\.(?!\D+)[\d),.;])\s*', 'Odds Ratio Value'), #Problem Lösen
        (r',?\(?\s*[Oo]dds? [Rr]atio\s*[:=]\s*[+–-]?\s*\d+\.\d+\s*\)?,?\.?', 'Odds Ratio Value'),
        #Odds Ratio Context
        (r'\(?\s*[oO]dds [rR]atio\s*\)?,?\.?', 'Odds Ratio Context'),


        # Chi-square test
        (r'[cC]hi[–-]?[Ss]quared? [Tt]ests?', 'Test Name is Chi-square test'),

        #Chi-square test
        (r'\(?.*χ\s*2\s*[–-]?.*\)?', 'Test Name is Chi-square test'),
        # Chi-square test Context
        (r'χ\s*2\s*[–-]?[Ss]cores?', 'Chi-square test Context'),
        # Chi-square Value
        (r'.* \(?χ\s*2\s*(\(.*\)\s*|\s*)[:=]\s*', 'Chi-square Value'),
        (r'.*\(?χ\s*[:=]\s*\)?,?\.?', 'Chi-square Value'),

        #f Value
        (r'.*\(?f\s*[:=]\s*([–-]?\d+\.\d+|[–-]?\.\d+|[–-]?\d+)\s*\)?,?\.?', 'f Value'),

        # t-test
        (r' \(?[Tt][–-]\s*[Tt]ests?\)?\?,?', 'Test name is t-test'),
        (r' \(?[Tt][–-]?\s*[Tt]ests?\)?\?,?', 'Test name is t-test'),
        (' \(?\s*t-test\s*\)?\.?,? ','Test Name is T-test'),
        (' \(?\s*t-\s* .* [Cc]orrelation [Tt]ests?\s*\)?\.?,? ', 'Test Name is T-test'),
        #T-test test statistic Value
        (r'\(?\s*[tT]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*[:=]\s*[–-]?\s*([\d.]+)', 'T-test test statistic Value '),

        #Shapiro-Wilks Test
        (r'\(?[sS]hapiro\s*-?[wW]ilks\s*[tT]ests?', 'Test name is Shapiro-Wilks Test'),


        # ANOVA Test
        (r'.*\s*ANOVA\s*,?\s*.*', 'test name is ANOVA Test'),
        # ANOVA Test
        (r'.*\(?\s*[Ff]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*', 'Test statistic Value'),

        # ANOVA Effect Size Eta-squared Value
        (r',?\(?η\s*2\s*[:=]\s*(0\.(?!\D+)[\d),.;]+|(?!\D+)1(?!\D+)|\.(?!\D+)[\d),.;])', 'Effect Size Eta-squared Value η2'),
        (r',?\(?η\s*p\s*2\s*[:=]\s*0\.\d+\)?\.?,?','Eta-squared Value ηp^2'),
        ('\(?ω\s*2\)?','Effect Size ω^2 context'),
        ('\(?ω\s*2\)?\s*[:=]\s*.*\s*\)?\.?,?', 'Effect Size ω^2 Value'),

        #Beta Value
        ('\(?\s*[\u03B2Ββ]\s*[=:].*','Beta (β) Value'),

        #b Value (Beta)
        ('\(?\s*b\s*[:=<>]\s*−?\s*\d+\.\d+\s*\)?\.?,?', 'b Value (Beta)'),


        # Correlation Context
        (r'[Cc]orrelations?\s*.*\s*between', 'Correlation Context'),
        (r'[Cc]orrelations?\s*ρ', 'Correlation Context'),
        (r'[pP]earson’?\s*s\s*ρ', 'Pearson’s correlation ρ Context'),

        # Pearson Correlation Context
        (r'Pearson’s r', 'Pearson Correlation Context'),
        #Pearson r Value
        (r'\(?\s*r\s*=\s*([+-]?1|[–-]?\s*0\.(?!\D+)[\d),.;]+|[–-]?0\.\.(?!\D+)[\d),.;]+)\s*', ' r Value'),
        (r'\(?\s*r\s*=\s*[+-–]?\.\d+\s*\)?\.?,?', ' r Value'),
        (r'\(?\s*rs\s*=\s*[+-–]?\d+\.\d+\s*\)?\.?,?', ' r Value'),
        (r'\(?\s*rs\s*=\s*[+-–]?\.\d+\s*\)?\.?,?', ' r Value'),
        (r'\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*([+-]?1|[–-]?\s*0\.(?!\D+)[\d),.;]+|[–-]?0\.\.(?!\D+)[\d),.;]+|[–-]?\.(?!\D+)[\d),.;]+)\s*', ' r Value'),
        # Pearson Correlation Coefficient
        (r'[Pp]earson\s*’?\s*s-?r[–-]?\(?r\s*[:=<>]\s*([+-]?1|−\s*0\.(?!\D+)[\d),.;]+|0\.\.(?!\D+)[\d),.;]+)\s*',
         'Pearson Correlation Coefficient Value'),
        (r'\(?ρ\s*[:=><]\s*\s*(0\.(?!\D+)[\d),.;]+|(?!\D+)[+-]?1(?!\D+)|\.(?!\D+)[\d),.;])\s*','Correlation Coefficient Value'),
        (r'\(?ρ\s*[:=><].*','Correlation Coefficient Value'),
        (r'[Cc]orrelation [Cc]oef(ﬁ|fi)-?\s*cients?\s*(.* was\s*|:|\s*=\s*| are\s*| is\s*)', 'Correlation Coefficient Value'),
        #Pearson’s Correlation Coefficient
        (r'[pP]earson’?s? [Cc]orrelations? [Cc]oef(ﬁ|fi)-?\s*cients?','Pearson’s Correlation Coefficient Context'),
        #(r'[pP]earson’?s? ρ', 'Pearson’s Correlation Coefficient Context'),

        #Spearman’s rank
        (r'[sS]pearman’?\s*s? [Rr]ank', 'Spearman’s rank Context'),


        # Wilcoxon signed-rank Test
        (r'.*\s*[wW]ilcoxon [Ss]igned[–-]?\s*[Rr]anks?[–-]?\s*[tT]ests?', 'Test Name is Wilcoxon signed-rank Test'),
        (r'\(?[Ss]igned[–-]?\s*[Rr]anks?[–-]?\s*[wW]ilcoxon\)?\.?,?', 'Test Name is Wilcoxon signed-rank Test'),
        # Wilcoxon signed-rank Test statistic V
        (r'.*\s*[wW]ilcoxon [Ss]igned[–-]?\s*[Rr]ank\s*.*[vV]\s*[:=]\s*.*', 'Test statistic V Value'),
        (r'\s*[Ww]\s*[:=]\s*\b(\d+(?:\.\d+)?)\b', 'Test statistic W Value'),
        # Test statistic Z Value
        (r'\(?[zZ]\s*[:=<>]\s*[–-]?\s*\d+\.\d+\)?\.?,?', 'Test statistic Z Value'),
        # Test statistic V Value
        (r'\(?[Vv]\s*[:=<>]\s*(\d+\.\d+|\d+)\s*\)?\.?,?', 'Test statistic V Value'),

        # Test statistic V Value
        (r'\(?\s*[Ff]\s*\(.*,.*\)\s*[:=]\s*[–-]?\s*\d+\.\d+\)?\.?,?;?', 'Test statistic Value'),

        #Shapiro-Wilk Test
        (r'\(?\s*[sS]hapiro-?\s*[wW]ilks?\)?\.?,?', 'Test Name is Shapiro-Wilk Test'),

        #Agreement Value
        (r'\(?\s*([Ll]evel of [aA]gremment|[aA]greement)\s*(was|rate was|is|were|level was|:|=|<|>)\s*\d+\.\d+\s*\)?\.?,?', 'Agreement Value'),



        # Wilcoxon Rrank-Sum Test
        (r'.*\s*[wW]ilcoxon[–-]?\s*[Rr]ank[–-]?\s*[Ss]um[–-]?\s*[tT]ests?', 'Test Name is Wilcoxon Rrank-Sum Test'),
        (r'.*\s*[wW]?i?l?c?o?x?o?n?[–-]?\s*[mM]ann[–-]?\s*[wW]hitney', 'Test Name is Wilcoxon Rrank-Sum Test'),
        (r'.* [Uu][–-]?\s*[Tt]est', 'Test Name is Wilcoxon Rrank-Sum Test'),
        (r'.*\s*[wW]ilcoxon\s*[rR]ank\s*[Ss]um\s*.*', 'Test Name is Wilcoxon Rrank-Sum Test'),
        (r'\(?\s*[mM]ann\s*-?\s*[Ww]hitney [Tt]est\s*\)?\.?,?', 'Test Name is Wilcoxon Rrank-Sum Test'),
        (r'\(?\s*[Ww]hitney [Tt]est\s*\)?\.?,?', 'Test Name is Wilcoxon Rrank-Sum Test'),
        # Wilcoxon Rrank-Sum Test statistic W Value
        (r'\(?\s*(?!\D+)[Ww]\s*[:=]\s*.*', 'Test statistic W Value'),

        (r'\(?MWU\)?\.?,?', 'Test Name is Wilcoxon Rrank-Sum Test'),
        #p-Value von wilcoxon Rank-Sum Test
        (r'\(?\s*[Mm][Ww]\s*[:=]\s*.*', 'p-Value of wilcoxon Rank-Sum Test MW or mw'),
        #Test statistic U Value
        (r'\(?\s*U\s*[:=<>]\s*\d+\.\d+\)?\.?,?', 'Test statistic U Value'),
        (r'\(?\s*U\s*[:=<>]\s*\d+\)?\.?,?', 'Test statistic U Value'),
        #Test statistic H Value
        (r'\(?H\s*[:=<>]\s*\d+\.\d+\)?\.?,?', 'Test statistic H Value'),


        #Wilcoxon Test
        (r'.*\s*[wW]ilcoxon [Tt]ests?\s*.*', 'Test Name is Wilcoxon Test'),

        #Paired Wilcoxon Test
        (r'\(?Paired [wW]ilcoxon\)?,?\.?', 'Test Name is Pairde Wilcoxon Test'),


        # Post-hoc Test
        (r'.*\s*[pP]ost[–-]?[Hh]oc[–-]?\s*[tT]ests?\s*.*', 'Test Name is Post-hoc Test'),

        #Friedman Test
        (r'[fF]riedman [tT]est', 'Test Name is Friedman Test'),
        # Friedman Analysis Context
        (r'\(?\s*[fF]riedman’?\s*s Analysis\s*', 'Friedman Analysis Context'),

        # Fisher's Exact test
        (r'[fF]isher’?\s*s [Ee]xact [Tt]?e?s?t?s?\s*\)?,?.?', 'Test Name is Fisher’s Exact test'),
        # Fisher’s Exact Test Context
        (r' \(?[fF][Ee][Tt]:? ', 'Fisher’s Exact Test Context'),
        (r'[fF]isher’?\s*s? [Tt]ests?\s*,?.?', 'Test Name is Fisher’s Exact test'),


        #Kruskal-Wallis Test
        (r'-*[kK]ruskal-?\s*[wW]allis\s*.*', 'Test Name is Kruskal-Wallis Test'),

        #Test Statistic H Value
        (r'\(?[Hh]\(\d+\)\s*[:=]\s*\s*\b(\d+(?:\.\d+)?)\b(\.?|,?|\)?)', 'Test Statistic H Value '),

        # Effect Size (Cramer's V)
        (r"Cramer’s [vV]", "Effect Size (Cramer’s V)"),
        (r"(small|low|large|medium|big)\s*.*\s*[Ee]ffect [Ss]ize", "Effect Size Context"),
        # Effect Size Value
        (r".*\s*[Ee]ffect [Ss]ize of", "Effect Size Value"),
        (r".*\s*[Ee]ffect [Ss]izes of", "Effect Size Value"),
        (r".*\s*[Ee]ffect [Ss]ize\s*", "Effect Size Context"),
        (r"\(?\s*[Ee]ffect [Ss]izes?\s*\)?\.?,?", "Effect Size Context"),

        #f^2 Value
        ('\(?f\s*\s*\s*2\s*[=:><]\s*[–-]?(\d+\.\d+|\.\d+)\)?','f^2 Value'),

        #estimate Value
        ('\(?[Ee]stimates?\s*[=:><]\s*[–-]?(\d+\.\d+|\.\d+)\)?,?\.?', 'Estimate Value'),

        #T Value
        ('\.?,?\(?\s*t\(\s*\d+\s*\)\s*[:=]\s*[–-]?\s*\d+\.\d+\)?\.?,?', 't Value'),

        # Cohen’s Kappa
        (r'.*\s*κ\s*[<=>:]\s*(-1|1|−\s*0\.(?!\D+)[\d),.;]+|0\.(?!\D+)[\d),.;]+)', 'Cohen’s Kappa κ Value'),
        (r'.*\s*[Kk]\s*[<=>:]\s*(-1|1|−\s*0\.(?!\D+)[\d),.;]+|0\.(?!\D+)[\d),.;]+)', 'Cohen’s Kappa κ Value'),
        (r',?\(?\s*[cC]ohen’?\s*s?\s*d\s*[<=>:]\s*(-1|1|[–-]\s*0\.(?!\D+)[\d),.;]+|0\.(?!\D+)[\d),.;]+)', 'Cohen’s Kappa d Value'),
        (r'[cC]ohen’?\s*s\s* [kK]appa.*\(?\s*κ\s*\)?.*', 'Cohen’s Kappa Contect'),
        (r'[cC]oef(fi|ﬁ)cient [kK]appa.*', 'Cohen’s Kappa Contect'),
        (r'[cC]ohen’?\s*s\s*[kK]appa .*[cC]oef(fi|ﬁ)cient ([Ww]as|:|=)\s*\d+\.\d+\s*\)?\.?,?', 'Cohen’s Kappa Value'),
        (r'[kK]appa [Vv]alues?', 'Cohen’s Kappa Context'),


        #α Context and value
        (r'\s*\u03B1 ', ' α Context'),
        #(r'\s*\u03B1', ' α Context'),
        (r'.*\s*\u03B1\s*(of |[<=>:]?\s*0\.(?!\D+)[\d),.;]+|[=:]?\s*(?!\D+)1(?!\D+)|[=:]?\s*\.(?!\D+)[\d),.;])\s*.*', ' α Value'),
        (r'.*\s*[cC]ronbach’?[Ss]?\s* [aA]lpha', 'Cronbach’s Alpha Context'),
        (r'.*\s*[aA]lpha .* of .*', 'Alpha Value'),

        # marginal R-squared
        (r'.* R\s*2 .*', 'Marginal R-squared Context'),
        # marginal R-squared
        (r'.* R\s*2\s*[:=]\s*.*', 'Marginal R-squared Value'),
        (r'\(?R\s*2\s*[:=]\s*.*\)?\.?,?', 'Marginal R-squared Value'),

        #(φ) Phi Value
        (r'\(?\s*φ\s*[:=]\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?', '(φ) Phi Value'),

        ('\(?[Ss]igni(fi|ﬁ)cant at 0\.\d+ level\s*\)?;?\.?,?','Significant Level Value'),

        #d Value
        (r',?\(?\s*\b(?<![st])d\b\s*[:=]\s*[–-]?\s*\d+\.\d+\)?\.?,?', 'd Value'),
        (r',?\(?\s*\b(?<![st])d\b\s*[:=]\s*[–-]?\s*\.\d+\)?\.?,?', 'd Value'),

        #Degree of freedom
        (r'.* \(?[dD]\s*[Ff]\s*[=:<>]\s*', 'Degree of freedom'),

        #λ value
        (r'\(?\s*λ\s*[:=]\s*[–-]?\s*\d+\.\d+\)?,?\.?', 'λ value'),

        #Significant level Value
        (r"\(?[Ss]igni(fi|ﬁ)can(ce|t) [Ll]evel\s*(=|:|of|was|were|is)\s*\.?\)?,?", "Significant level Value "),

        # Statistically Difference context
        (r"[sS]tatisticall?y? [Dd]ifferen[tc]e?", "Statistically Difference context"),
        # Statistically significant context
        (r"[sS]tatisticall?y? ([Ss]igni(fi|ﬁ)cant|[Ss]igni(fi|ﬁ)cance)", "Statistically Significant context"),
        (r"[sS]ta-?\s*tisticall?y? ([Ss]igni(fi|ﬁ)cant|[Ss]igni(fi|ﬁ)cance)", "Statistically Significant context"),

        # Statistically Significant Range
        (r"[sS]tatistical ([Ss]igni(fi|ﬁ)cant|[Ss]igni(fi|ﬁ)cance) [Rr]anges?", "Statistically Significant Range"),

        #Significant Difference context
        (r"[sS]igni(fi|ﬁ)cant( | [Mm]ean )[dD]ifferences?", "Significant Difference context"),
        (r"[sS]igni(fi|ﬁ)cantly [dD]ifferents?", "Significant Difference context"),

        # Significant Effect Context
        (r"\(?\s*we found\s*.*\s*[sS]igni(fi|ﬁ)cant [Ee]ffects?", "Significant Effect Context"),

        # logistic Regression
        (r".*([Ll]og [Rr]atio|[lL]ogistic [rR]egression).*", "Logistic Regression Context"),
        (r"\(?\s*[lL]ogistic [rR]egression\)?\.?,?", "Logistic Regression Context"),
        #Regression coefficient Context
        (r".* [rR]egression [Cc]oefficients?.*", "Regression coefficient Context"),
        (r"\(?\.?,?\s*[rR]egression [rR]esults?.*(was|are|were)\s* .*\)?\.?,?", "Regression coefficient Context"),

        #Linear Regression Context
        (r"\(?\s*[lL]inear [rR]egression\s*\)?\.?,?", "Linear Regression Context"),

        #Log Odds Context
        (r"\(?\s*[lL]og [Oo]dds\s*\)?,?\.?", "Log Odds Context"),
        #Log Odds Value
        (r"\(?\s*([lL]og|\s*) [Oo]dds\s*[=:].*", "Log Odds Value"),

        #Odds Value
        #(r" Odds .* of rating .* \d+\.\d+ ", "Odds Value"),


        # Comparing results
        (r".*\s*[rR]esults\s*.*\s*(faster|smaller|bigger|slower)", "Comparing Results "),
        (r".*[oO]n [Aa]verage\s*.*\s*(faster|smaller|bigger|slower)\s*.*than\s*.*", "Comparing Results "),
        (r".*\s*[Cc]omparing .* [Rr]esults?\s*.*", "Comparing Results "),
        (r"[sS]tatistical [Tt]ests? [cC]ompare?i?n?g?", "Statistical Comparing Context"),

        #System Usability score
        (r"(SUS|sus) ([sS]core|[vV]alue)", "context about System Usability score"),
        (r" [sS]ystem [uU]sability [Ss]cores? ", "context about System Usability score"),

        #Mean security Score Value
        (r"\(?\s*[Mm]ean [sS]ecurity [Ss]core\s*[:=]\s*\d+\.\d+\s*\)?,?\.?", "Mean security Score Value"),

        # Total Variation Distance
        (r'([tT]otal [vV]ariation [dD]istances?|\(?TVD\)?)', 'Total Variation Distance Context'),
        # Total Variation Distance Value
        (r'TV\s*Ds?\(.*,.*\)\s*=\s*.*', 'Total Variation Distance Value'),
        (r'TV\s*Ds?\ of ', 'Total Variation Distance Value'),

        #Confidence Interval
        (r'.*[Cc]on(fi|ﬁ)dence [iI]ntervals?', 'Confidence Interval Context'),
        #Confidence Interval Value
        (r'.*[Cc]\.?[Ii]\s*[=:]\s*\[.*,.*\].?', 'Confidence Interval Value'),
        (r'\(?[Cc]\.?[Ii]\s*\[.*,.*\]\)?,?\.?', 'Confidence Interval Value'),
        (r'\(?\s*\d+%\s*[Cc]\.?[Ii]\s*,?.?\)?', 'Confidence Interval Value'),
        (r',?\(?[Cc]\.?[Ii]\s*\d+\s*%?\s*\[.*,.*\]\)?,?\.?', 'Confidence Interval Value'),

        #Bernoulli Trail
        (r'\s*[bB]ernoulli\s*.*', 'Bernoulli Trail Context'),
        # Bernoulli Trail Value
        (r'\(?[bB][:=]\s*((0\.(?!\D+)[\d),.;]+|(?!\D+)1(?!\D+)|\.(?!\D+)[\d),.;])|0|1)\s*.*', 'Bernoulli Trail Value'),

        #acceptance criteria Value
        (r'.*\s*[Aa]cceptance [Cc]riteria (of|was|=|:)\s*', 'acceptance criteria Value'),

        #statistical Power Value
        ('[Ss]tatistical [Pp]ower\s*( [oO]f | was |=\s*|:\s*)','Statistical Power Value '),
        # statistical Power Value
        ('\(?\s*power of 0\.\d+\s*\)?,?\.?', 'Power Value '),

        #Z-Scoure Value
        ('\(?\s*[zZ]\s*[–-]?\s*[Ss]cores?\s*(of|=|:|<|>|is|was|were)\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?', 'Z-Scoure Value'),


    ]
    #Erstelle ein Result_Dictionary.
    results_dict = OrderedDict()
    #Hier Startet die Algorithmus, statistsche Sätze aus .txt File zu Extrahieren.
    #For schleife geht von erste Satz in .txt File bis zum letzten Satz
    for sentence in sentences:
        #Initialisiere leeres Tags Liste, die Später alle gefundene Taggierte Pattern in einem Satz enthät
        tags_found = []
        #For schleife durch alle taggierte Patterns Liste
        for pattern, tag in tags:
            #Falls pattern in einem Satz existiert
            if re.search(pattern, sentence):
                #Überprüfe ob die gefundene Tag nicht vorher existiert, damit wir Verdupplung vermeiden
                if tag not in tags_found:
                    #Addiere Tag in tegs_found List für aktuelle Satz
                    tags_found.append(tag)
        #Schreibe alle Tags in tags_found list durch , getrennt
        if tags_found:
            results_dict[sentence] = ", ".join(tags_found)
    #Hier ist For schleife, dass jede Satz ein Key angibt, und die gefundene Statistische Sätze wie PDF-Ordnung sortiert
    results = [(k, v) for k, v in results_dict.items()]
    #Wähle Speicherort für die neue .csv File
    csv_save_directory = filedialog.askdirectory(title="Select directory to save .csv file")
    #Wenn es kein Problem mit Speicherort Path der .csv File existiert
    if csv_save_directory:
        #Öffne .CSV File
        output_file_path = os.path.join(csv_save_directory, f"{file_name}_results.csv")
        with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
            #Initiealisiere .CSV File für Schreiben un passe HEaders Sentence und Tag in die erste Zeile
            writer = csv.writer(file)
            writer.writerow(['Sentence', 'Tag'])
            #For Schleife für alle gefundene Sätze, die statistische Werte oder Informationen enthalten
            for result in results:
                #Schreibe alle gefundene Sätze in .csv File
                writer.writerow(result)
        print(f'Statistical information extracted and saved to {output_file_path} successfully.')
        return output_file_path

#Hier geht es um Statistische Values aus jede gefundene Statistische Satz in neue Spalte in gleichem .csv File zu extrahieren
def extract_statistical_numbers(sentence):
    #diefiniere ein Pattern für bestimmte Zahlen, die sich auf statistische Werte basieren
    decimal_patterns = [
        r'(\b(?:\w+\W+){0,2})\b([+-]?\d+(?:\.\d+)?)\b',
        r'(\b(?:\w+\W+){0,2})\b([+-]?\d+(?:\.\d+)?)(?:\W+\w+){0,2}',

        #r'(\b(?:\w+\W+){0,2})\b([+-]?\d+(?:\.\d+)?)\b(?:\W+\w+){0,2}',

    ]
    #finde alle Numbers in extrahierte statistische Sentences Liste (Spalte) in .csv File
    extracted_numbers = re.findall(decimal_patterns[0], sentence, re.IGNORECASE)
    #retern allle gefundene Numbers
    return [f"{context.strip()} {number}" for context, number in extracted_numbers]

#Hier wird Panda Bibliothek genutzt, da Panda ist gut .csv Files zu bearbeiten
def process_csv_file(input_file):
    #Lese ausgewählte .csv Inhalt mithilfe von Panda Lib
    df = pd.read_csv(input_file)
    #Extract Numbers mithilfe von vorherige Funktion extract_statistical_numbers(sentence)
    df['Statistical Values'] = df['Sentence'].apply(extract_statistical_numbers)
    #join alle gefundene Nambers (Statistische Values zusammen) und speichere die in Neue Spalte "Statistical Values" in gleiche .csv File
    df['Statistical Values'] = df['Statistical Values'].apply(lambda x: ', '.join(x))
    df.to_csv(input_file, index=False)


#Hier ist die Funktion zum Select .txt File oder mehr als einem .txt File
def browse_file():
    #Wähle ein .txt File oder mehr für statistische Information Extraktion
    txt_file_paths = filedialog.askopenfilenames(title="Select .txt Files", filetypes=[("Text Files", "*.txt")])
    #Wenn es Keine Problem mit ausgewählten File Pathes existieren
    if txt_file_paths:
        #Lösche alle was vorher in Interface existiert
        txt_text.delete(1.0, tk.END)
        results_text.delete(1.0, tk.END)
        all_rows = []
        #Loop durch alle ausgewählte .txt Files
        for file_path in txt_file_paths:
            #hier werden zuerst alle Statistische Sätze Extrahiert und auf Display Window gezeigt
            txt_text.insert(tk.END, f"Processing file: {file_path}\n\n")
            txt_text.update_idletasks()
            results_file_path = extract_statistical_info(file_path)
            txt_text.insert(tk.END, f"Statistical information extracted. Results saved to: {results_file_path}\n\n")
            #Hier werden die .csv File geöffnet und alle statistische Values aus statistische Sätze Extrahiert
            #und unter Neue Spalte gespeichert und dann in Display Window in UserIntrface gezeigt
            txt_text.update_idletasks()
            process_csv_file(results_file_path)
            txt_text.insert(tk.END, f"Statistical Values extracted and saved to the CSV file.\n\n")
            txt_text.update_idletasks()
            with open(results_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                rows = []
                for row in csv_reader:
                    sentence = row['Sentence']
                    tag = row['Tag']
                    combined_value = row['Statistical Values']
                    rows.append(f"Sentence: {sentence}\nTag: {tag}\nStatistical Values: {combined_value}\n\n")
                all_rows.extend(rows)
                results_text.config(state=tk.NORMAL)
                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, "".join(all_rows))
                results_text.config(state=tk.DISABLED)


#Diese Funktion habe ich für mich persönlich gebaut,
#um mehr als .csv File auszwählen und die in Display window zu schreiben
#Das war Hilfreicher Für mich,
#damit ich die Extrahierte Statistische Informationen Results
#mit Markierte Infors aus PDF-Dokumenten zu vergleichen
#das ist einfach ein Zwei Loops
#Zuerst Loop durch alle ausgewählte .csv File
#Dann Loop durch alle Zeilen in aktuelle .csv File und schreibe alle Zeilen in aktuellen .csv File in Display Window
def display_csv_tables():
    csv_file_paths = filedialog.askopenfilenames(title="Select .csv Files", filetypes=[("CSV Files", "*.csv")])
    if csv_file_paths:
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)
        for file_path in csv_file_paths:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                results_text.insert(tk.END, f"CSV File: {file_name}\n")
                headers = rows[0]
                values = rows[1:]
                for row in values:
                    for header, value in zip(headers, row):
                        results_text.insert(tk.END, f"{header}: {value}\n")
                    results_text.insert(tk.END, "\n")
                results_text.insert(tk.END, "\n")
        results_text.config(state=tk.DISABLED)

#Hier ist nur Für Interface Aussehen (Bottuns und Display Windows)
root = tk.Tk()
root.title("PDF to Txt Converter and Statistical Information Extractor")
pdf_to_txt_frame = tk.Frame(root)
pdf_to_txt_frame.pack(side=tk.TOP, padx=10, pady=10)
buttons_frame = tk.Frame(pdf_to_txt_frame)
buttons_frame.pack(pady=10)
pdf_to_txt_button = tk.Button(buttons_frame, text="Convert PDF to Text", command=convert_pdf_to_txt)
pdf_to_txt_button.pack(side=tk.LEFT)
pdf_to_txt_button = tk.Button(buttons_frame, text="Convert PDF to Text and filter Headers", command=convert_pdf_to_txt2)
pdf_to_txt_button.pack(side=tk.LEFT, padx=10)
browse_button = tk.Button(buttons_frame, text="Select .txt File", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=10)
display_csv_button = tk.Button(buttons_frame, text="Display CSV Tables", command=display_csv_tables)
display_csv_button.pack(side=tk.LEFT, padx=10)
txt_frame = tk.Frame(root)
txt_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
txt_label = tk.Label(txt_frame, text="Information about files")
txt_label.pack()
txt_scroll = tk.Scrollbar(txt_frame)
txt_scroll.pack(side=tk.RIGHT, fill=tk.Y)
txt_text = tk.Text(txt_frame, yscrollcommand=txt_scroll.set, height=50, width=30)
txt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
txt_scroll.config(command=txt_text.yview)
results_frame = tk.Frame(root)
results_frame.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.BOTH, expand=True)
results_label = tk.Label(results_frame, text="Extracted Statistical Information")
results_label.pack()
results_text = tk.Text(results_frame, state=tk.DISABLED, height=50, width=105)
results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
results_scroll = tk.Scrollbar(results_frame)
results_scroll.pack(side=tk.RIGHT, fill=tk.Y)
results_text.config(yscrollcommand=results_scroll.set)
results_scroll.config(command=results_text.yview)
root.mainloop()
