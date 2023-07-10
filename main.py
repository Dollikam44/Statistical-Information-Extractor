
import pdfminer.high_level
import pdfminer.layout
import nltk
import os
import re
import csv
from collections import OrderedDict
import tkinter as tk
from tkinter import filedialog

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
                filtered_text = re.sub(r'[Ss]ection\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = re.sub(r'[Ss]ections\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                filtered_text = re.sub(r'[iI]n [Ss]ection\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = re.sub(r'[Ii]n [Ss]ections\s*(\d+(?:\.\d+)*)[.,)]?', '', filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                filtered_text = re.sub(r'[fF]igure\s*(\d+(?:\.\d+)*)[.,):]?', '', filtered_text)
                filtered_text = ' '.join(filtered_text.strip().split())
                # Lösche FußZeilen
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
                filtered_text = re.sub(r'Train TravelNonePap.Dig.Certificate Type107812241091543296537213402654School/Child CareNonePap.Dig.Certificate Type227338027399921741156013001119Grocery','', filtered_text)
                filtered_text = re.sub(r'PerspicuityDependabilityStimulationEfficiencyNoveltyAttractiveness−3−2−10123Windows HelloPassword','', filtered_text)
                filtered_text = re.sub(r'USENIX Association', '', filtered_text)
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
                #Lösche FußZeilen
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


    tags = [#[–-]?    #(?!\D+)

        # p-values
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*\.\d+\s*\)?\s*\.?,?;?", 'p-value'),
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*1\s*\)?\s*\.?,?;?", 'p-value'),
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*0\.\d+\s*\)?\s*\.?,?;?", 'p-value'),
        (r" \(?p\s*=\s*\d+\.\d+e", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?", 'p-value Context'),
        (r" \.?,?;?\(?0?\.\d+ [Pp]\s*[–-]?\s*[Vv]alues?\s*\)? \.?,?;? ", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?\s*[=<>≥≤]\s*\.\d+", 'p-value'),
        (r"[Pp]\s*\(.*\)\s*[=<>≥≤]\s*\.\d+", 'p-value'),
        (r"[Pp]\s*\(.*\)\s*[=<>≥≤]\s*0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?\s*[=<>≥≤]\s*\d+\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*smaller than \.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*smaller than 0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*bigger than \.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*bigger than 0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alue less than \d+\.\d+", 'p-value Value'),
        (r"[Pp][–-]?[Vv]alue less than \.\d+", 'p-value Value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*are .*\s*0\.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*are .*\s*.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? of 0\.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? of .\d+\s*", 'p-value'),
        (r"[Pp][–-]?\s*[Vv]alues? range?i?n?g .*\s*0\.\d+ to 0\.\d+", 'p-value Range'),
        (r"[Pp][–-]?\s*[Vv]alues? range?i?n?g .*\s*\.\d+ to \.\d+", 'p-value Range'),
        (r"corr?[–-]?\s*p\s*[<=>≥≤]\s*\.\d+", 'corrected p-value'),
        (r"corr?[–-]?\s*p\s*[<=>≥≤]\s*0\.\d+", 'corrected p-value'),
        (r"corrected [Pp][–-]?[Vv]alues?", 'corrected p-value'),


        # Mann Whitny P-value MW
        # (r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        # (r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*0\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        # (r" \.?,?;?\(?MW=\d+×10−\d+\)?", 'Mann Whitny P-value (MW)'),

        (r"MW\s*[<=>≥≤]\s*\.\d+", 'Mann Whitny P-value (MW)'),
        (r"MW\s*[<=>≥≤]\s*0\.\d+", 'Mann Whitny P-value (MW)'),
        (r"MW=\d+×10−\d+", 'Mann Whitny P-value (MW)'),

        # Participants Number
        (r"Participants were \d+", 'Participants Number'),

        # Mean
        (r"[Mm]ean .*\s*of \d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .*\s*of \.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .*\s*of \d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean\s*[:=]?\s*\d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean\s*[:=]?\s*\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .* was \d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .* was \d+\s*\%?[Ss]?", 'Mean Value'),
        (r" \.?,?;?\(?\s*[mMµ]\s*[:=]\s*\d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r" [mMµ]\s*[:=]\s*\d+\s*\%?[Ss]?", 'Mean Value'),

        # Median
        (r"[Mm]edian .*\s*of \d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*of \.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*of \d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian\s*[:=]?\s*\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian\s*[:=]?\s*\d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r" \.?,?;?\(?[Mm][Dd]\s*[:=]\s*\d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r" \.?,?;?\(?[Mm][Dd]\s*[:=]\s*\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*was \d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*was \d+\s*\%?[Ss]?", 'Median Value'),

        # Max
        (r"[Mm]ax\s*[=:]\s*\d+\.\d+", 'Max Value'),
        (r"[Mm]ax\s*[=:]\s*\d+", 'Max Value'),

        # Min
        (r"[Mm]in\s*[:=]\s*\d+\.\d+", 'Min Value'),
        (r"[Mm]in\s*[:=]\s*\d+", 'Min Value'),

        # Range
        (r"[Rr]ange\s*[=:]?o?f?\s*\d+\s*[–-]\s*\d+", 'Range'),
        (r"[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\s*,\s*\d+\s*\]", 'Range'),
        (r"[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'Range'),
        (r"[Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'range'),

        # Standard Deviation Value
        (r" \.?,?;?\(?\s*[Ss][Dd]\s*[:=]?\s*\d+\.\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*[Ss][Dd]\s*[:=]?\s*\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*[sS][tT][dD]\s*\)?\s*[:=]?\s*\(?\s*\d+\.\d+\s*\)?", 'Standard Deviation Value'),
        (r"[Ss]tandard [Dd]eviation of \d+\.\d+", 'Standard Deviation Value'),
        (r" ,?\(?\s*[sS][Dd]\s*\d+\.\d+", 'Standard Deviation Value'),
        (r"[Ss]tandard [Dd]eviation of \d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?σ\s*[=:]\s*\d+\.\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?σ\s*[=:]\s*\d+", 'Standard Deviation Value'),
        (r"[sS]tandard [dD]eviations?", 'Standard Deviation Context'),
        (r" \(?\s*[sS][tT][Dd]\s*\)? ", 'Standard Deviation Context'),
        (r" \(?\s*[sS][Dd]\s*\)? ", 'Standard Deviation Context'),


        # Test statistic V
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+\.\d+", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*0", 'Test statistic V'),
        # test statistic W Value
        (r" \.?,?;?\(?\s*W\s*[=:]\s*\d+\.\d+", 'Test statistic W'),
        (r" \.?,?;?\(?\s*W\s*[=:]\s*\d+", 'Test statistic W'),
        (r" \.?,?;?\(?\s*W\s*[=:]\s*0", 'Test statistic W'),
        # test statistic U Value
        (r" \.?,?;?\(?\s*U\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Test statistic U'),
        (r" \.?,?;?\(?\s*U\s*[=:]\s*[–-−]?\s*\d+", 'Test statistic U'),
        # test statistic H Value
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+\.\d+", 'H Value'),
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\.\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+\.\d+", 'H Value'),
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+", 'H Value'),
        (r" \.?,?;?\(?\s*H\s*[:=]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'H Value'),

        # Z Value
        (r" \.?,?;?\(?\s*[zZ]\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Z Value'),
        (r" \.?,?;?\(?\s*[zZ]\s*[=:]\s*[–-−]?\s*\d+", 'Z Value'),

        # (r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+\.\d+", 'Z Value'),
        # (r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+", 'Z Value'),

        # b Value
        (r" \.?,?;?\(?\s*b\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'b Value'),

        # F Value
        (r" \.?,?;?\(?\s*[Ff]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*[:=]\s*\d+\.\d+", 'F Value'),
        (r" \.?,?;?\(?\s*[Ff]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*[:=]\s*\d+\.\d+", 'F Value'),

        # T Value
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'T Value'),


        (r" [tT]\s*-?\s*[Vv]alues? ", 'T Value Context'),

        # Singnificantly different
        (r"[Ss]igni[ﬁf]i?cantly [Dd]ifferents?", 'Singnificantly different Context'),
        # (r"[Ss]ignificantly different", 'Singnificantly different Context'),
        (r"[Ss]igni[fﬁ]i?cant [Dd]ifferences?", 'Singnificantly different Context'),  # significant difference
        # (r"\(?\s*significant [Dd]ifferences?\s*\)?,?\.?;?", 'Singnificantly different Context'),
        (r"[Ss]igni[fﬁ]i?cantly [Dd]ifferents?", 'Singnificantly different Context'),
        (r"[Ss]tatistically [Dd]ifferent", 'statistically different'),
        (r"[Ss]tatistical differences?", 'statistically different'),
        (r"[Ss]tatistical [Ss]igni[fﬁ]i?cance", 'statistical significance'),
        # (r"\(?\s*[Ss]tatistical [Ss]igniﬁcance\s*\)?,?\.?;?", 'statistical significance'),
        (r"[Ss]tatistically [Ss]igni[fﬁ]i?cant\s*\)?,?\.?;?", 'statistical significance'),
        # (r"\(?\s*[Ss]tatistically [Ss]ignificant\s*\)?,?\.?;?", 'statistical significance'),

        # Chi-square test
        (r"[Cc]hi-?\s*[sS]quared?\s*[Tt]?e?s?t?s?", 'Chi-square test'),
        (r"[Cc]hi-?\s*[sS]quare", 'Chi-square test'),

        #McNemar’s test
        (r"[mM][Cc]\s*[nN]emar’?s [Tt]est", 'McNemar’s test'),

        # ANOVA test
        (r" \.?,?;?\(?\s*ANOVA", 'ANOVA test'),
        (r" \.?,?;?\(?\s*ANOVAs", 'ANOVA test'),

        # post-Hoc
        # (r"\(?\s*[Pp]ost-?\s*[Hh]oc\s*\)?\.?,?;?", 'post-Hoc Test'),
        (r"[Pp]ost-?\s*[Hh]oc-??\s*[Tt]?e?s?t?s?", 'post-Hoc Test'),

        # Fisher’s exact test
        (r"[fF]isher’?s? [Ee]xact [Tt]?e?s?t?s?", 'Fisher’s exact test'),
        (r"[fF]isher’?s? [Tt]?e?s?t?s?", 'Fisher’s exact test'),
        (r" \.?,?;?\(?\s*FET\s*:?", 'Fisher’s exact test'),

        # Wilcoxon signed-rank test
        (r"[Ww]ilcoxon-?\s*[Ss]igned-??\s*[Rr]anks?", 'Wilcoxon signed-rank test'),
        (r"[Ss]igne?d?-?\s*[Rr]anks?-?\s*[Ww]ilcoxon", 'Wilcoxon signed-rank test'),

        # Wilcoxon test
        (r"[Ww]ilcoxon\s*t?e?s?t?s?", 'Wilcoxon test'),

        # Wilcoxon-Rank-Sum Tests
        (r"[Ww]ilcoxon-?\s*[rR]ank-?\s*[sS]um", 'Wilcoxon-Rank-Sum Test'),
        # (r"[wW]ilcoxon\s*[–-−]?\s*[rR]ank\s*[–-−]?\s*[Ss]um\s*:?", 'Wilcoxon-Rank-Sum Test'),
        # (r"[wW]ilcoxon-?\s*[Rr]ank-?\s*[sS]um", 'Wilcoxon-Rank-Sum Test'),
        (r"[Ww]ilcoxon-?\s*[Mm]ann-?\s*[Ww]hitney", 'Wilcoxon-Rank-Sum Test'),
        (r"[mM]ann-?\s*[wW]hitney\s*[Uu]?", 'Wilcoxon-Rank-Sum Test'),
        (r" \.?,?;?\(?\s*[Uu]-?\s*[Tt]ests?\s*\)?\.?,?;? ", 'Wilcoxon-Rank-Sum Test'),
        # (r"Mann\s*[–-−]?\s*Whitney\s*[Uu]", 'Wilcoxon-Rank-Sum Test'),
        (r"\.?,?;?\(?\s*MWU-?\s*[Tt]ests?\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r" \(?\s*MWU\s*\)?\.?,?:? ", 'Wilcoxon-Rank-Sum Test'),

        # t-test
        (r" \.?,?;?\(?\s*[Tt]-?\s*[Tt]ests?\s*\)?\.?,?;? ", 't-test'),
        # (r" \(?\s*t tests?\s*\)?\.?,?;?:? ", 't-test'),

        # t-test
        (r" \.?,?;?\(?\s*H-?\s*[Tt]ests?\s*\)?\.?,?;?: ", 'H-test'),
        # (r" \(?\s*H tests?\s*\)?\.?,?;?:? ", 'H-test'),

        #Mauchly’s test
        (r"[mM]auchly’?s? [Tt]ests?", 'Mauchly’s test'),

        # Mood’s median test
        (r"[mM]ood[s’]?\s*[s’]?-?\s*[Mm]edian [Tt]ests?", 'Mood’s median test'),

        # Friedman test
        (r"[fF]riedman [Tt]ests?\s*\)?\.?,?;?:?", 'Friedman test'),
        # Friedman Analysis
        (r"[fF]riedman[s’]?\s*[s’]?\s*[Aa]nalysis", 'Friedman test'),

        # Kruskal-Wallace
        (r"[Kk]ruskal-?\s*[wW]allace", 'Kruskal-Wallace'),
        (r"[Kk]ruskall-?\s*[wW]all[ai][cs]e?", 'Kruskal-Wallace'),

        # Paired Wilcoxon
        (r"[pP]aired [wW]ilcoxon", 'Paired Wilcoxon'),

        # Shapiro-Wilk Test
        (r"[sS]hapiro-?\s*[wW]ilks?", 'Shapiro-Wilk Test'),

        # Kruskal-Wallis Test Kruskal- Wallis
        (r"[kK]ruskal-?\s*[wW]allis", 'Kruskal-Wallis'),
        # (r"\(?\s*[kK]ruskal-?\s*[wW]allis [Tt]ests?\s*\)?\.?,?;?:?", 'Kruskal-Wallis'),

        # statistical tests comparing
        (r"[Ss]tatistical [tT]ests? [Cc]omparing", 'statistical tests comparing'),
        (r"[Ss]tatistical [Cc]omparing [tT]ests?", 'statistical tests comparing'),

        # Effect Size
        (r"[Ee]ffect [Ss]izes?", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes? of \d+\.\d+", 'Effect Size Value'),
        (r"\d+\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        # (r"d+\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ss]mall [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? was small", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? is small", 'Effect Size Value'),
        (r"[Ll]arge [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? was large", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? is large", 'Effect Size Value'),
        (r"[Mm]edium [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? was medium", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? is medium", 'Effect Size Value'),
        (r"[Ll]imited [Ee]ffect [Ss]izes?", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes? was limited", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes? is limited", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes?\s*\(?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]\s*\)?", 'Effect Size Value'),

        # Cramer’s V
        (r" \.?,?;?\(?\s*Cramer’s V?", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer’s V\s*=\s*\d+\.\d+", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer’s V\s*=\s*\.\d+", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer\s*\(cid:31\)\s*sV\s*=\s*\d+\.\d+", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*\s*Cramer\s*\(cid:31\)\s*sV\s*=\s*\.\d+", 'Cramer’s V'),

        # Log Ratio
        (r" \.?,?;?\(?\s*[lL]og [rR]atio\s*\)?,?:?;?\.?", 'Log Ratio Context'),
        (r"[Ll]ogistic [Rr]egressions?", 'Logistic Regression Context'),

        # Log Odds
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds?", 'Log Odds Context'),
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds?\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Logistic Odds Value'),
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds? .*of.*\s*[–-−]?\s*\d+\.\d+", 'Logistic Odds Value'),
        (r"[Nn]egative [lL]og [Oo]dds?", 'Negative Log Odds Context'),
        (r"[Pp]ositive [lL]og [Oo]dds?", 'Positive Log Odds Context'),

        # Regression coefficients
        (r"[rR]egression [Cc]oefficients?", 'Regression coefficients Context'),
        # linear regression
        (r"[Ll]inear [Rr]egressions?", 'linear regression Context'),

        # coefﬁcient Kappa
        (r"[Cc]oef[ﬁf]i?cient [kK]appa", 'coefﬁcient Kappa Context'),
        # (r"\(?\s*coefficient [kK]appa\s*\)?\.?,?;?", 'coefﬁcient Kappa Context'),
        (r"[cC]ohen’?s?\s*[Kk]appa coef[fﬁ]i?cient was \d+\.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        # (r"[cC]ohen’?s?\s*[Kk]appa coefficient was \d+\.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        (r"[cC]ohen’?s?\s*[Kk]appa coef[fﬁ]i?cient was \.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        # (r"[cC]ohen’?s?\s*[Kk]appa coefficient was \.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s* [cC]on[fﬁ]idence [Ii]nterval r?", 'Cohen’s Conﬁdence Interval Context'),
        # (r"\(?[cC]ohen[s’]?\s*[s’]?\s* [cC]offidence [Ii]nterval r?\s*\)?\.?,?;?", 'Cohen’s Conﬁdence Interval Context'),

        # coefﬁcient
        (r"[Cc]oef[ﬁf]i?cient\s*\(?\s*\d+\.\d+s*\)?", 'coefﬁcient Value'),
        # (r"\(?\s*[Cc]oefficient\s*\(?\s*\.\d+s*\)?\s*\)?\.?,?;?", 'coefﬁcient Value'),

        # Bernoulli Trial
        (r" [Bb]ernoulli [Tt]?r?i?a?l?s?", 'Bernoulli Trial Context'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\.\d+", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\d+\.\d+", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\s*\d+\.\d+×10−\d+", 'B Value'),

        # Cohens’ Kappa
        (r"[cC]ohen[s’]?\s*[s’]? [kK]appa", 'Cohens’ Kappa Context'),
        (r" \.?,?;?\(?\s*κ of \d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*\(\s*κ\s*\) of \d+\.\d+", 'Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]? [kK]appa .*\s*of .*\s*[–-−]?\s*\d+\.\d+", 'Kappa Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ", 'Cohens’ Kappa κ Context'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oef[fﬁ]i?cients?", 'Cohens’ Kappa coefﬁcient Context'),
        # (r"\(?\s*Cohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oefficient\s*\)?\.?,?;?", 'Cohens’ Kappa coefﬁcient Context'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ\s*[=:]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[>=<]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*[Kk]\s*[>=<]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[>=<]\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*.*\s*was\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[Oo]ver\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[Bb]elow\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*[Kk]\s*[>=<≥≤]\s*\d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue of \d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue of \d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue is \d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue is \d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue was \d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue was \d+", 'Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ\s*=\s*\d+\.\d+", 'Cohens’ Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ values? between \.\d+ and \.\d+", 'Cohens’ Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ values? between \d+\.\d+ and \d+\.\d+", 'Cohens’ Kappa κ Value'),

        # Cohens’ d
        (r"[cC]ohen[s’]?\s*[’s]? d\s*[:=]\s*[–-]?\s*\d+\.\d+", 'Cohens’ d Value'),
        (r"[cC]ohen[s’]?\s*[’s]? d\s*=\s*[–-]?\s*\.\d+", 'Cohens’ d Value'),
        (r"[cC]ohen[s’]?\s*[’s]? d\s*\)?\.?,?;? ", 'Cohens’ d Context'),

        # d Value
        (r" \.?,?;?\(?\s*d\s*=\s*[–-]?\s*\d+\.\d+", 'd Value'),
        (r" \.?,?;?\(?\s*d\s*=\s*[–-]?\s*\.\d+", 'd Value'),
        (r"[cC]ohen[s’]?\s*[’s]? [Ee]ffect [Ss]izes?\s*[Vv]?a?l?u?e?s?\s*\)?\.?,?;?", 'Cohen’s effect size Context'),

        # Pearson’s r # Pearson’s correlation coefﬁcient
        (r"[pP]earson[s’]?\s*[’s]?\s*r\s*\)?\.?,?;? ", 'Pearson’s r Context'),

        # Pearson’s correlation coefﬁcient
        (r"[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?[ﬁf]?i?c?i?e?n?t?",
         'Pearson’s correlation coefﬁcient Context'),
        # (r"\(?\s*[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?f?i?c?i?e?n?t?\s*\)?\.?,?;?",'Pearson’s correlation coefﬁcient Context'),
        # (r"\(?\s*[Cc]orrelation\s*[Cc]oefficient\s*\)?\.?,?;?",'correlation coefﬁcient Context'),
        (r"[Cc]orrelation\s*[Cc]oef[ﬁf]i?cient", 'correlation coefﬁcient Context'),

        # Pearson’s ρ
        (r"[pP]earson’?s?\s*ρ\s*\)?\.?,?;? ", 'Pearson’s  ρ Context'),

        # Agreement Value
        (r"[Aa]greement was \d+\.\d+\%?", 'Agreement Value'),
        (r"[Aa]greement was \.\d+\s*", 'Agreement Value'),
        (r"[Aa]greement .*\s*of \d+\.\d+", 'Agreement Value'),

        # χ2
        (r" \.?,?;?\(?\s*χ\s*2\s*-?[Dd]ifference [Tt]?e?s?t?s?", 'χ2 Context'),
        (r" \.?,?;?\(?\s*χ\s*2\s*-?[Ss]cores?", 'χ2 Context'),
        (r" \.?,?;?\(?\s*χ\s*2\s*\)?\.?,?;? ", 'χ2 Context'),
        (r"χ\s*2\s*[–-]?\s*[tT]ests?", 'χ2 Test'),
        (r"χ\s*2\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+", 'χ2 Value'),
        (r"χ\s*2\s*=\s*\d+\.\d+", 'χ2 Value'),
        (r"χ\s*2\(.*,.*\)\s*=\s*\d+\s*", 'χ2 Vlaue'),
        (r"χ\s*2\(.*,.*\)\s*=\s*\d+\.?,?\d+", 'χ2 Vlaue'),
        (r"χ\s*2\[.*,.*\]\s*=\s*\d+\s*", 'χ2 Vlaue'),
        (r"χ\s*2\[.*,.*\]\s*=\s*\d+\.?,?\d+", 'χ2 Vlaue'),

        # χ
        (r" \.?,?;?\(?\s*χ\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+", 'χ Value'),
        (r" \.?,?;?\(?\s*χ\s*=\s*\d+\.\d+", 'χ Value'),
        (r" \.?,?;?\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+", 'χ Vlaue'),
        (r" \.?,?;?\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+\.?,?\d+", 'χ Vlaue'),
        (r" \.?,?;?\(?\s*χ\s*\[.*,.*\]\s*=\s*\d+", 'χ Vlaue'),
        (r" \.?,?;?\(?\s*χ\s*\[.*,.*\]\s*=\s*\d+\.?,?\d+", 'χ Vlaue'),

        # Odds Ratio
        (r"[oO]dds? [rR]atios?", 'Odds Ratio Context'),
        (r" \.?,?;?\(?\s*O\.R\s*\)?\.?,?;? ", 'Odds Ratio Context'),
        (r" \.?,?;?\(\s*OR\s*\)\s*\.?,?;? ", 'Odds Ratio Context'),
        (r" \.?,?;?\(?\s*OR\s*=\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*OR\s*=\s*[–-]?\s*\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*O\.R\s*=\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*O\.R\s*=\s*[–-]?\s*\.\d+ ", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*of\s*[–-]?\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*of\s*[–-]?\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*of\s*[–-]?\d+\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*1", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*\d+\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),

        # confidence interval
        (r"[Cc]on[fﬁ]i?dence [Ii]ntervals?", 'confidence interval Context'),
        (r" \(?\s*C\.I\.?\s*\)?\.?,?;?:? ", 'confidence interval Context'),
        # (r"\(?\s*[Cc]onﬁdence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Context'),
        (r"\(?\s*\d+\s*\%\s*[Cc]on[ﬁf]i?dence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        # (r"\(?\s*\d+\s*\%\s*[Cc]onfidence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.I\s*\)?\.?,?;?:? ", 'confidence interval Context'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\] ", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\)?,?\.?;? ", 'confidence interval Value'),
        (r"C\.?\s*I\s*\d+\s*\%\s*\[[–-−]?\s*\d+\.\d+\s*,\s*[–-−]?\s*\s*\d+\s*\]", 'confidence interval Value'),
        (r"\d+\s*\%\s*\s*,?\s*C\.?I\s*±\s*\d+\.\d+\s*", 'confidence interval Value'),
        (r"C\.?I\s*±\s*\d+\.\d+", 'confidence interval Value'),

        # Kappa   [–-]?
        (r" \.?,?;?\(?\s*κ\s*\)?\.?,?;? ", 'Kappa κ Context'),
        (r" \.?,?;?\(?\s*κ\s*[=:><≥≤]\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[=:><≥≤]\s*\.\d+", 'Kappa κ Value'),
        (r"[Kk]appa [Vv]alues?", 'Kappa κ Context'),

        # β Value
        (r" \.?,?;?\(?\s*β\s*=\s*[–-−]?\s*\d+\.\d+", 'β Value'),
        (r" \.?,?;?\(?\s*β\s*=\s*[–-−]?\s*\.\d+", 'β Value'),

        # z-Score
        (r" \.?,?;?\(?\s*[Zz]-[Ss]cores?", 'z-score'),
        (r"[Zz]-[Ss]core of -?\s*\d+\.\d+", 'z-score Value'),
        (r"[Zz]-[Ss]core is -?\s*\d+\.\d+", 'z-score Value'),
        (r"[Zz]-[Ss]core was -?\s*\d+\.\d+", 'z-score Value'),

        # correlation coefficients
        (r"  \.?,?;?\(?\s*ρ\s*=\s*[–-−]?\s*\.\d+", 'ρ Value'),
        (r" \.?,?;?\(?\s*ρ\s*=\s*[–-−]?\s*\d+\.\d+", 'ρ Value'),
        (r"[pP]earson’?s?\s*[cC]orrelations?\s*ρ", 'Pearson’s Correlation ρ Context'),
        # correlation coefficients
        (r"[Cc]orrelation [Cc]oef[ﬁf]-?\s*\s*i?cients? .*\s*\d+\.\d+", 'Correlation Coefficients Value'),
        # (r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\d+\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oef[fﬁ]-?\s*\s*i?cients? .*\s*\.\d+", 'Correlation Coefficients Value'),
        # (r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        # (r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oef[fﬁ]-?\s*\s*i?cients?\s*:?\s*[–-]?\s*\d+\.\d+", 'Coefficient Vlaue'),
        # (r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oef[fﬁ]-?\s*\s*i?cients?\s*:?\s*[–-]?\s*\.\d+", 'Coefficient Vlaue'),
        # correlation coefficients
        (r"[Cc]orrelation [Cc]oef[fﬁ]i?cient .* was .*\s*[–-]?\s*\d+\.\d+", 'Correlation Coefficient Value'),
        # (r"[Cc]orrelation [Cc]oefficient .* was .*\s*\d+[–-]?\s*\.\d+", 'Correlation Coefficient Value'),
        # (r"\(?\s*[Cc]orrelation [Cc]oefficient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oef[fﬁ]i?cient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?",
         'Correlation Coefficient Value'),

        # Spearman’s rank correlation
        (r"[sS]pearman’?s?\s*[Rr]ank[–-]?\s*[cC]?o?r?r?e?l?a?t?i?o?n?s?", 'Spearman’s rank correlation Context'),

        # Spearman − ρ
        (r"[sS]pearman\s*[–-−]?\s*ρ", 'Spearman − ρ Context'),
        (r"[sS]pearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\d+\.\d+", 'Spearman − ρ Value'),
        (r"[sS]pearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\.\d+", 'Spearman − ρ Value'),

        # Degree of freedom
        (r" \(?\s*d\s*f\s*\)?\.?,?;? ", 'Degree of freedom Context'),
        (r" \(?\s*d\s*f\s*=\s*\d+", 'Degree of freedom Value'),
        (r" \(?\s*d\s*f\s*=\s*\d+\.\d+", 'Degree of freedom Value'),

        # Total Variation Distance
        (r" \.?,?;?\(?\s*TVDs?\s*\)?\.?,?;? ", 'Total Variation Distance Context'),
        (r" \.?,?;?\(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\d+\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r" \.?,?;?\(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r"[tT]otal [vV]ariation [dD]istances?", 'Total Variation Distance Context'),

        # R^2
        (r" \.?,?;?\(?\s*R\s*2\s*\)?\.?,?;? ", 'R^2 Context'),
        (r" \.?,?;?\(?\s*R\s*2\s*=\s*\d+\.\d+", 'R^2 Vlaue'),
        (r" \.?,?;?\(?\s*R\s*2\s*=\s*\.\d+", 'R^2 Vlaue'),
        (r"\.?,?;?\(?\s*R\s*2\s*=\s*\d+\.\d+", 'R^2 Vlaue'),
        (r"\.?,?;?\(?\s*R\s*2\s*=\s*0\.\d+", 'R^2 Context'),
        (r" \.?,?;?\(?\s*R\s*2\s*a\s*d\s*j\s*=\s*\d+\.\d+", 'R^2 Value'),
        (r" \.?,?;?\(?\s*a\s*d\s*j\s*=\s*\d+\.\d+", 'R^2 Value'),

        # f^2 Value
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f^2 Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\.\d+", 'f^2 Value'),

        # f Value
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\s*,\s*d+\s*\)\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\s*,\s*d+\s*\)\s*[<=>]\s*[–-−]?\s*\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\.\d+\s*,\s*d+\.\d+\s*\)\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\.\d+\s*,\s*d+\.\d+\s*\)\s*[<=>]\s*[–-−]?\s*\.\d+", 'f Value'),



        # η^2
        (r" \.?,?;?\(?\s*η\s*2\s*=\s*\.\d+", 'Eta square η^2 Value'),
        (r" \.?,?;?\(?\s*η\s*2\s*=\s*\d+\.\d+", 'Eta square η^2 Value'),
        (r" \.?,?;?\(?\s*η\s*[pP]\s*2\s*=\s*\d+\.\d+", 'Eta square η^2 Value'),
        (r" \.?,?;?\(?\s*η\s*[pP]\s*2\s*=\s*\.\d+", 'Eta square η^2 Value'),
        (r"[eE]ta-?\s*[sS]quared?\s*=\s*\.\d+", 'Eta square η^2 Value'),
        (r"[eE]ta-?\s*[sS]quared?\s*=\s*d+\.\d+", 'Eta square η^2 Value'),
        (r"η\s*2-?\s*[Vv]alue", 'Eta square η^2 Context'),
        (r"[eE]ta-?\s*[sS]quared?", 'Eta square η^2 Context'),

        # Statistical Power
        (r"[Ss]tatistical [pP]ower of \d+\.\d+", 'Statistical Power Value'),
        (r"[Ss]tatistical [pP]ower of \.\d+", 'Statistical Power Value'),

        # Alpha
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*\d+\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\d+\.\d+", 'Alpha α Vlaue'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\.\d+", 'Alpha α Value'),
        (r"\d+\s*≤\s*\u03B1\s*≤\s*\d+", 'Alpha α Values Range'),
        (r"\d+\.\d+\s*≤\s*\u03B1\s*≤\s*\d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*d+\.\d+", 'Alpha α Value'),
        (r"[aA]lpha [Ll]evels? of\s*d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? of\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? was\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? was\s*\d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? .*\s*\d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? .*\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha [Rr]ang[ei]?n?g? from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),

        #################Significant Level
        (r"[Ss]igni[fﬁ]i?can[tc]e? [Ll]evel of \d+\.\d+", 'Significant Level Value'),
        (r"[Ss]igni[fﬁ]i?can[tc]e? [Ll]evel of \.\d+", 'Significant Level Value'),
        # (r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \d+\.\d+\s*\)?,?\.?;?", 'Significant Level Value'),
        # (r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \.\d+\s*\)?,?\.?;?", 'Significant Level Value'),

        # Krippendorff’s alpha
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha", 'Krippendorff’s alpha Context'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1", 'Krippendorff’s alpha Context'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]?\s*\(?\s*\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\s*\u03B1\s*[<>=]?\s*\(?\s*\.\d+\s*\)?", 'Krippendorff’s alpha Value'),

        # Cronbach’s α
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1", 'Cronbach’s α Context'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 of \d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 of \.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 .*\s*\d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 .*\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? [Aa]lpha .*\s*\d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? [Aa]lpha .*\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*=\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*=\s*\d+\.\d+", 'Cronbach’s αValue'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*\(?\s*\d+\.\d+\s*[–-−]?\s*\d+\.\d+\s*\)?", 'Cronbach’s α Value'),

        # r Value
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?0\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?0\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),

        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?0\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?\s*\d+\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?0\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r_s Value'),

        # acceptance criteria
        (r"[aA]cceptance [Cc]riteria of \d+\.\d+", 'acceptance criteria Value'),

        # Bonferroni–Holm
        (r"[bB]onferroni[–-]?\s*[hH]?o?l?m?", 'Bonferroni–Holm Context'),
        (r"[bB]onferroni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),
        # (r"[bB]onferroni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),
        (r"[bB]onferoni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),

        # Comparing Results
        (r"[Rr]esults? .* faster than .*", 'Comparing Results Context and Values'),
        (r"[Ff]ound .* on average .* faster than .*", 'Comparing Results Context and Values'),
        (r"[Cc]omparing .* to .*", 'Comparing Results Context and Values'),
        (r" \.?,?;?\(?\s*[Ff]\s*\(.*\)\s*[<>]\s*[Ff]\s*\(.*\)\s*\)?\.?,?;? ", 'Comparing Results Values'),
        (r" \.?,?;?\(?\s*\d+\.\d+\s*[<>]\s*\d+\.\d+\s*\)?\.?,?;? ", 'Comparing Results Values'),

        # Correlation between
        (r"[Cc]orrelations? between", 'Correlation Context'),
        # Positive and Negative Correlation
        (r"[pP]ositive [Cc]orrelate?d?i?o?n?", 'Positive Correlation Context'),
        (r"[Nn]egative [Cc]orrelate?d?i?o?n?", 'Negative Correlation Context'),


        #λ Value
        (r"λ\s*=\s*\d+\.\d+", 'λ Value'),
        (r"λ\s*=\s*\.\d+", 'λ Value'),

        #ω OMega suared Value
        (r"ω\s*2\s*=[–-]?\s*\d+\.\d+", 'ω Omega suared Value'),
        (r"ω\s*2\s*=[–-]?\s*\.\d+", 'ω Omega suared Value'),
        (r"\(?\s*ω\s*2\s*\)?", 'ω Omega suared Value'),

        #Power Value
        (r"[Pp]ower of \d+\.\d+", 'Power Value'),
        (r"[Pp]ower of \.\d+", 'Power Value'),

        #Kendall’s τ correlation coefficients
        (r"Kendall’s τ correlation coef[fﬁ]i?cients?", 'Kendall’s τ context'),
        (r"Kendall’s τ", 'Kendall’s τ context'),
        (r"τ\s*=[–-]?\s*\d+", 'Kendall’s τ Value'),
        (r"τ\s*=[–-]?\s*\d+\.\d+", 'Kendall’s τ Value'),

        # rank Value
        (r"[Rr]ank of \d+\.\d+", 'rank Value'),
        (r"[Rr]ank is \d+\.\d+", 'rank Value'),
        (r"[Rr]ank was \d+\.\d+", 'rank Value'),

        #σ^2 Value
        (r"σ\s*2\s*=[–-]?\s*\d+\.\d+", 'σ^2 Value'),

        # Phi (φ) Value
        (r"φ\s*=\s*[–-]?\d+\.\d+", 'Phi (φ) Value'),
        (r"φ\s*=\s*[–-]?\.\d+", 'Phi (φ) Value'),

    ]

    results_dict = OrderedDict()

    for sentence in sentences:
        tags_found = []
        matches_found = []
        numbers_not_matched = []

        for pattern, tag in tags:
            matches = re.findall(pattern, sentence)
            if matches:
                tags_found.append(f'{tag}: ({", ".join(matches)})')
                matches_found.extend(matches)

        if tags_found:
            numbers = re.findall(r'(\w+\s+\w+)\s+(\d+(?:\.\d+)?)', sentence)
            for match in numbers:
                words = match[0]
                number = match[1]
                if number not in matches_found:
                    numbers_not_matched.append((number, words))

            results_dict[sentence] = (", ".join(tags_found), ", ".join(matches_found), numbers_not_matched)

    results = [(k, v[0], v[1], ", ".join([f"{num[1]} {num[0]}" for num in v[2]])) for k, v in results_dict.items()]

    csv_save_directory = filedialog.askdirectory(title="Select directory to save .csv file")
    if csv_save_directory:
        output_file_path = os.path.join(csv_save_directory, f"{file_name}_results.csv")
        with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sentence', 'Tagged Matches', 'Matches', 'Other not tagged Values'])
            for result in results:
                writer.writerow(result)
        print(f'Statistical information extracted and saved to {output_file_path} successfully.')
        return output_file_path



#not tagged number aber nicht mit die zwei Vorwörter
def extract_statistical_info_with_not_tagged_numbers(file_path):
    #öffne die ausgewählte .txt File Path
    with open(file_path, 'r', encoding='utf-8') as file:
        #lese Inhalt von .txt File
        text = file.read()
    #Extrahiere der Name von .txt File, damit der Name genutzt in Umbenennung von .csv File kann
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    #tokaniziere den Text in .txt File in Sinvolle Sätze mithilve von nltk Bibliothek
    sentences = nltk.sent_tokenize(text)
    #Erstlle Klassifizierte Pattarns (Taggierte Patterns) mithilfe von re, für die wichtigeste statistische Ergebnisse, Tests, Values, Konzepten usw.


    tags = [#[–-]?    #(?!\D+)
        # p-values
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*\.\d+\s*\)?\s*\.?,?;?", 'p-value'),
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*1\s*\)?\s*\.?,?;?", 'p-value'),
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*0\.\d+\s*\)?\s*\.?,?;?", 'p-value'),
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*d+\.\d+\s*e\s*\)?\s*\.?,?;?", 'p-value'),
        (r" \(?p\s*=\s*\d+\.\d+e", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?", 'p-value Context'),
        (r" \.?,?;?\(?0?\.\d+ [Pp]\s*[–-]?\s*[Vv]alues?\s*\)? \.?,?;? ", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?\s*[=<>≥≤]\s*\.\d+", 'p-value'),
        (r"[Pp]\s*\(.*\)\s*[=<>≥≤]\s*\.\d+", 'p-value'),
        (r"[Pp]\s*\(.*\)\s*[=<>≥≤]\s*0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?\s*[=<>≥≤]\s*\d+\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*smaller than \.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*smaller than 0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*bigger than \.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*bigger than 0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alue less than \d+\.\d+", 'p-value Value'),
        (r"[Pp][–-]?[Vv]alue less than \.\d+", 'p-value Value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*are .*\s*0\.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*are .*\s*.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? of 0\.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? of .\d+\s*", 'p-value'),
        (r"[Pp][–-]?\s*[Vv]alues? range?i?n?g .*\s*0\.\d+ to 0\.\d+", 'p-value Range'),
        (r"[Pp][–-]?\s*[Vv]alues? range?i?n?g .*\s*\.\d+ to \.\d+", 'p-value Range'),
        (r"corr?[–-]?\s*p\s*[<=>≥≤]\s*\.\d+", 'corrected p-value'),
        (r"corr?[–-]?\s*p\s*[<=>≥≤]\s*0\.\d+", 'corrected p-value'),
        (r"corrected [Pp][–-]?[Vv]alues?", 'corrected p-value'),

        # Mann Whitny P-value MW
        # (r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        # (r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*0\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        # (r" \.?,?;?\(?MW=\d+×10−\d+\)?", 'Mann Whitny P-value (MW)'),

        (r"MW\s*[<=>≥≤]\s*\.\d+", 'Mann Whitny P-value (MW)'),
        (r"MW\s*[<=>≥≤]\s*0\.\d+", 'Mann Whitny P-value (MW)'),
        (r"MW=\d+×10−\d+", 'Mann Whitny P-value (MW)'),

        # Participants Number
        (r"Participants were \d+", 'Participants Number'),

        # Mean
        (r"[Mm]ean .*\s*of \d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .*\s*of \.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .*\s*of \d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean\s*[:=]?\s*\d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean\s*[:=]?\s*\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .* was \d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .* was \d+\s*\%?[Ss]?", 'Mean Value'),
        (r" \.?,?;?\(?\s*[mMµ]\s*[:=]\s*\d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r" [mMµ]\s*[:=]\s*\d+\s*\%?[Ss]?", 'Mean Value'),

        # Median
        (r"[Mm]edian .*\s*of \d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*of \.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*of \d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian\s*[:=]?\s*\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian\s*[:=]?\s*\d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r" \.?,?;?\(?[Mm][Dd]\s*[:=]\s*\d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r" \.?,?;?\(?[Mm][Dd]\s*[:=]\s*\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*was \d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*was \d+\s*\%?[Ss]?", 'Median Value'),

        # Max
        (r"[Mm]ax\s*[=:]\s*\d+\.\d+", 'Max Value'),
        (r"[Mm]ax\s*[=:]\s*\d+", 'Max Value'),

        # Min
        (r"[Mm]in\s*[:=]\s*\d+\.\d+", 'Min Value'),
        (r"[Mm]in\s*[:=]\s*\d+", 'Min Value'),

        # Range
        (r"[Rr]ange\s*[=:]?o?f?\s*\d+\s*[–-]\s*\d+", 'Range'),
        (r"[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\s*,\s*\d+\s*\]", 'Range'),
        (r"[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'Range'),
        (r"[Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'range'),

        # Standard Deviation Value
        (r" \.?,?;?\(?\s*[Ss][Dd]\s*[:=]?\s*\d+\.\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*[Ss][Dd]\s*[:=]?\s*\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*[sS][tT][dD]\s*\)?\s*[:=]?\s*\(?\s*\d+\.\d+\s*\)?", 'Standard Deviation Value'),
        (r" ,?\(?\s*[sS][Dd]\s*\d+\.\d+", 'Standard Deviation Value'),
        (r"[Ss]tandard [Dd]eviation of \d+\.\d+", 'Standard Deviation Value'),
        (r"[Ss]tandard [Dd]eviation of \d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?σ\s*[=:]\s*\d+\.\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?σ\s*[=:]\s*\d+", 'Standard Deviation Value'),
        (r"[sS]tandard [dD]eviations?", 'Standard Deviation Context'),
        (r" \(?\s*[sS][tT][Dd]\s*\)? ", 'Standard Deviation Context'),
        (r" \(?\s*[sS][Dd]\s*\)? ", 'Standard Deviation Context'),

        # Test statistic V
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+\.\d+", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*0", 'Test statistic V'),
        # test statistic W Value
        (r" \.?,?;?\(?\s*W\s*[=:]\s*\d+\.\d+", 'Test statistic W'),
        (r" \.?,?;?\(?\s*W\s*[=:]\s*\d+", 'Test statistic W'),
        (r" \.?,?;?\(?\s*W\s*[=:]\s*0", 'Test statistic W'),
        # test statistic U Value
        (r" \.?,?;?\(?\s*U\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Test statistic U'),
        (r" \.?,?;?\(?\s*U\s*[=:]\s*[–-−]?\s*\d+", 'Test statistic U'),
        # test statistic H Value
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+\.\d+", 'H Value'),
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\.\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+\.\d+", 'H Value'),
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+", 'H Value'),
        (r" \.?,?;?\(?\s*H\s*[:=]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'H Value'),

        # Z Value
        (r" \.?,?;?\(?\s*[zZ]\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Z Value'),
        (r" \.?,?;?\(?\s*[zZ]\s*[=:]\s*[–-−]?\s*\d+", 'Z Value'),

        # (r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+\.\d+", 'Z Value'),
        # (r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+", 'Z Value'),

        # b Value
        (r" \.?,?;?\(?\s*b\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'b Value'),

        # F Value
        (r" \.?,?;?\(?\s*[Ff]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*[:=]\s*\d+\.\d+", 'F Value'),
        (r" \.?,?;?\(?\s*[Ff]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*[:=]\s*\d+\.\d+", 'F Value'),

        # T Value
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'T Value'),

        (r" [tT]\s*-?\s*[Vv]alues? ", 'T Value Context'),

        # Singnificantly different
        (r"[Ss]igni[ﬁf]i?cantly [Dd]ifferents?", 'Singnificantly different Context'),
        # (r"[Ss]ignificantly different", 'Singnificantly different Context'),
        (r"[Ss]igni[fﬁ]i?cant [Dd]ifferences?", 'Singnificantly different Context'),  # significant difference
        # (r"\(?\s*significant [Dd]ifferences?\s*\)?,?\.?;?", 'Singnificantly different Context'),
        (r"[Ss]igni[fﬁ]i?cantly [Dd]ifferents?", 'Singnificantly different Context'),
        (r"[Ss]tatistically [Dd]ifferent", 'statistically different'),
        (r"[Ss]tatistical differences?", 'statistically different'),
        (r"[Ss]tatistical [Ss]igni[fﬁ]i?cance", 'statistical significance'),
        # (r"\(?\s*[Ss]tatistical [Ss]igniﬁcance\s*\)?,?\.?;?", 'statistical significance'),
        (r"[Ss]tatistically [Ss]igni[fﬁ]i?cant\s*\)?,?\.?;?", 'statistical significance'),
        # (r"\(?\s*[Ss]tatistically [Ss]ignificant\s*\)?,?\.?;?", 'statistical significance'),

        # Chi-square test
        (r"[Cc]hi-?\s*[sS]quared?\s*[Tt]?e?s?t?s?", 'Chi-square test'),

        # ANOVA test
        (r" \.?,?;?\(?\s*ANOVA", 'ANOVA test'),
        (r" \.?,?;?\(?\s*ANOVAs", 'ANOVA test'),

        # post-Hoc
        # (r"\(?\s*[Pp]ost-?\s*[Hh]oc\s*\)?\.?,?;?", 'post-Hoc Test'),
        (r"[Pp]ost-?\s*[Hh]oc-??\s*[Tt]?e?s?t?s?", 'post-Hoc Test'),

        # Fisher’s exact test
        (r"[fF]isher’?s? [Ee]xact [Tt]?e?s?t?s?", 'Fisher’s exact test'),
        (r"[fF]isher’?s? [Tt]?e?s?t?s?", 'Fisher’s exact test'),
        (r" \.?,?;?\(?\s*FET\s*:?", 'Fisher’s exact test'),

        # Wilcoxon signed-rank test
        (r"[Ww]ilcoxon-?\s*[Ss]igned-??\s*[Rr]anks?", 'Wilcoxon signed-rank test'),
        (r"[Ss]igne?d?-?\s*[Rr]anks?-?\s*[Ww]ilcoxon", 'Wilcoxon signed-rank test'),

        # Wilcoxon test
        (r"[Ww]ilcoxon\s*t?e?s?t?s?", 'Wilcoxon test'),

        # Wilcoxon-Rank-Sum Tests
        (r"[Ww]ilcoxon-?\s*[rR]ank-?\s*[sS]um", 'Wilcoxon-Rank-Sum Test'),
        # (r"[wW]ilcoxon\s*[–-−]?\s*[rR]ank\s*[–-−]?\s*[Ss]um\s*:?", 'Wilcoxon-Rank-Sum Test'),
        # (r"[wW]ilcoxon-?\s*[Rr]ank-?\s*[sS]um", 'Wilcoxon-Rank-Sum Test'),
        (r"[Ww]ilcoxon-?\s*[Mm]ann-?\s*[Ww]hitney", 'Wilcoxon-Rank-Sum Test'),
        (r"[mM]ann-?\s*[wW]hitney\s*[Uu]?", 'Wilcoxon-Rank-Sum Test'),
        (r" \.?,?;?\(?\s*[Uu]-?\s*[Tt]ests?\s*\)?\.?,?;? ", 'Wilcoxon-Rank-Sum Test'),
        # (r"Mann\s*[–-−]?\s*Whitney\s*[Uu]", 'Wilcoxon-Rank-Sum Test'),
        (r"\.?,?;?\(?\s*MWU-?\s*[Tt]ests?\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r" \(?\s*MWU\s*\)?\.?,?:? ", 'Wilcoxon-Rank-Sum Test'),

        # t-test
        (r" \.?,?;?\(?\s*[Tt]-?\s*[Tt]ests?\s*\)?\.?,?;? ", 't-test'),
        # (r" \(?\s*t tests?\s*\)?\.?,?;?:? ", 't-test'),

        # t-test
        (r" \.?,?;?\(?\s*H-?\s*[Tt]ests?\s*\)?\.?,?;?: ", 'H-test'),
        # (r" \(?\s*H tests?\s*\)?\.?,?;?:? ", 'H-test'),

        # Mauchly’s test
        (r"[mM]auchly’?s? [Tt]ests?", 'Mauchly’s test'),

        # Mood’s median test
        (r"[mM]ood[s’]?\s*[s’]?-?\s*[Mm]edian [Tt]ests?", 'Mood’s median test'),

        # Friedman test
        (r"[fF]riedman [Tt]ests?\s*\)?\.?,?;?:?", 'Friedman test'),
        # Friedman Analysis
        (r"[fF]riedman[s’]?\s*[s’]?\s*[Aa]nalysis", 'Friedman test'),

        # Kruskal-Wallace
        (r"[Kk]ruskal-?\s*[wW]allace", 'Kruskal-Wallace'),
        (r"[Kk]ruskall-?\s*[wW]all[ai][cs]e?", 'Kruskal-Wallace'),

        # Paired Wilcoxon
        (r"[pP]aired [wW]ilcoxon", 'Paired Wilcoxon'),

        # Shapiro-Wilk Test
        (r"[sS]hapiro-?\s*[wW]ilks?", 'Shapiro-Wilk Test'),

        # Kruskal-Wallis Test Kruskal- Wallis
        (r"[kK]ruskal-?\s*[wW]allis", 'Kruskal-Wallis'),
        # (r"\(?\s*[kK]ruskal-?\s*[wW]allis [Tt]ests?\s*\)?\.?,?;?:?", 'Kruskal-Wallis'),

        # statistical tests comparing
        (r"[Ss]tatistical [tT]ests? [Cc]omparing", 'statistical tests comparing'),
        (r"[Ss]tatistical [Cc]omparing [tT]ests?", 'statistical tests comparing'),

        # Effect Size
        (r"[Ee]ffect [Ss]izes?", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes? of \d+\.\d+", 'Effect Size Value'),
        (r"\d+\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        # (r"d+\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ss]mall [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? was small", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? is small", 'Effect Size Value'),
        (r"[Ll]arge [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? was large", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? is large", 'Effect Size Value'),
        (r"[Mm]edium [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? was medium", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? is medium", 'Effect Size Value'),
        (r"[Ll]imited [Ee]ffect [Ss]izes?", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes? was limited", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes? is limited", 'Effect Size Value'),
        (r"[Ee]ffect [Ss]izes?\s*\(?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]\s*\)?", 'Effect Size Value'),

        # Cramer’s V
        (r" \.?,?;?\(?\s*Cramer’s V?", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer’s V\s*=\s*\d+\.\d+", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer’s V\s*=\s*\.\d+", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer\s*\(cid:31\)\s*sV\s*=\s*\d+\.\d+", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*\s*Cramer\s*\(cid:31\)\s*sV\s*=\s*\.\d+", 'Cramer’s V'),

        # Log Ratio
        (r" \.?,?;?\(?\s*[lL]og [rR]atio\s*\)?,?:?;?\.?", 'Log Ratio Context'),
        (r"[Ll]ogistic [Rr]egressions?", 'Logistic Regression Context'),

        # Log Odds
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds?", 'Log Odds Context'),
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds?\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Logistic Odds Value'),
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds? .*of.*\s*[–-−]?\s*\d+\.\d+", 'Logistic Odds Value'),
        (r"[Nn]egative [lL]og [Oo]dds?", 'Negative Log Odds Context'),
        (r"[Pp]ositive [lL]og [Oo]dds?", 'Positive Log Odds Context'),

        # Regression coefficients
        (r"[rR]egression [Cc]oefficients?", 'Regression coefficients Context'),
        # linear regression
        (r"[Ll]inear [Rr]egressions?", 'linear regression Context'),

        # coefﬁcient Kappa
        (r"[Cc]oef[ﬁf]i?cient [kK]appa", 'coefﬁcient Kappa Context'),
        # (r"\(?\s*coefficient [kK]appa\s*\)?\.?,?;?", 'coefﬁcient Kappa Context'),
        (r"[cC]ohen’?s?\s*[Kk]appa coef[fﬁ]i?cient was \d+\.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        # (r"[cC]ohen’?s?\s*[Kk]appa coefficient was \d+\.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        (r"[cC]ohen’?s?\s*[Kk]appa coef[fﬁ]i?cient was \.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        # (r"[cC]ohen’?s?\s*[Kk]appa coefficient was \.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s* [cC]on[fﬁ]idence [Ii]nterval r?", 'Cohen’s Conﬁdence Interval Context'),
        # (r"\(?[cC]ohen[s’]?\s*[s’]?\s* [cC]offidence [Ii]nterval r?\s*\)?\.?,?;?", 'Cohen’s Conﬁdence Interval Context'),

        # coefﬁcient
        (r"[Cc]oef[ﬁf]i?cient\s*\(?\s*\d+\.\d+s*\)?", 'coefﬁcient Value'),
        # (r"\(?\s*[Cc]oefficient\s*\(?\s*\.\d+s*\)?\s*\)?\.?,?;?", 'coefﬁcient Value'),

        # Bernoulli Trial
        (r" [Bb]ernoulli [Tt]?r?i?a?l?s?", 'Bernoulli Trial Context'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\.\d+", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\d+\.\d+", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\s*\d+\.\d+×10−\d+", 'B Value'),

        # Cohens’ Kappa
        (r"[cC]ohen[s’]?\s*[s’]? [kK]appa", 'Cohens’ Kappa Context'),
        (r" \.?,?;?\(?\s*κ of \d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*\(\s*κ\s*\) of \d+\.\d+", 'Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]? [kK]appa .*\s*of .*\s*[–-−]?\s*\d+\.\d+", 'Kappa Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ", 'Cohens’ Kappa κ Context'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oef[fﬁ]i?cients?", 'Cohens’ Kappa coefﬁcient Context'),
        # (r"\(?\s*Cohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oefficient\s*\)?\.?,?;?", 'Cohens’ Kappa coefﬁcient Context'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ\s*[=:]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[>=<]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*[Kk]\s*[>=<]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[>=<]\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*.*\s*was\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[Oo]ver\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[Bb]elow\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*[Kk]\s*[>=<≥≤]\s*\d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue of \d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue of \d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue is \d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue is \d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue was \d+\.\d+", 'Kappa κ Value'),
        (r"[kK]appa [vV]alue was \d+", 'Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ\s*=\s*\d+\.\d+", 'Cohens’ Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ values? between \.\d+ and \.\d+", 'Cohens’ Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ values? between \d+\.\d+ and \d+\.\d+", 'Cohens’ Kappa κ Value'),

        # Cohens’ d
        (r"[cC]ohen[s’]?\s*[’s]? d\s*[:=]\s*[–-]?\s*\d+\.\d+", 'Cohens’ d Value'),
        (r"[cC]ohen[s’]?\s*[’s]? d\s*=\s*[–-]?\s*\.\d+", 'Cohens’ d Value'),
        (r"[cC]ohen[s’]?\s*[’s]? d\s*\)?\.?,?;? ", 'Cohens’ d Context'),

        # d Value
        (r" \.?,?;?\(?\s*d\s*=\s*[–-]?\s*\d+\.\d+", 'd Value'),
        (r" \.?,?;?\(?\s*d\s*=\s*[–-]?\s*\.\d+", 'd Value'),
        (r"[cC]ohen[s’]?\s*[’s]? [Ee]ffect [Ss]izes?\s*[Vv]?a?l?u?e?s?\s*\)?\.?,?;?", 'Cohen’s effect size Context'),

        # Pearson’s r # Pearson’s correlation coefﬁcient
        (r"[pP]earson[s’]?\s*[’s]?\s*r\s*\)?\.?,?;? ", 'Pearson’s r Context'),

        # Pearson’s correlation coefﬁcient
        (r"[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?[ﬁf]?i?c?i?e?n?t?",
         'Pearson’s correlation coefﬁcient Context'),
        # (r"\(?\s*[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?f?i?c?i?e?n?t?\s*\)?\.?,?;?",'Pearson’s correlation coefﬁcient Context'),
        # (r"\(?\s*[Cc]orrelation\s*[Cc]oefficient\s*\)?\.?,?;?",'correlation coefﬁcient Context'),
        (r"[Cc]orrelation\s*[Cc]oef[ﬁf]i?cient", 'correlation coefﬁcient Context'),

        # Pearson’s ρ
        (r"[pP]earson’?s?\s*ρ\s*\)?\.?,?;? ", 'Pearson’s  ρ Context'),

        # Agreement Value
        (r"[Aa]greement was \d+\.\d+\%?", 'Agreement Value'),
        (r"[Aa]greement was \.\d+\s*", 'Agreement Value'),
        (r"[Aa]greement .*\s*of \d+\.\d+", 'Agreement Value'),

        # χ2
        (r" \.?,?;?\(?\s*χ\s*2\s*-?[Dd]ifference [Tt]?e?s?t?s?", 'χ2 Context'),
        (r" \.?,?;?\(?\s*χ\s*2\s*-?[Ss]cores?", 'χ2 Context'),
        (r" \.?,?;?\(?\s*χ\s*2\s*\)?\.?,?;? ", 'χ2 Context'),
        (r"χ\s*2\s*[–-]?\s*[tT]ests?", 'χ2 Test'),
        (r"χ\s*2\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+", 'χ2 Value'),
        (r"χ\s*2\s*=\s*\d+\.\d+", 'χ2 Value'),
        (r"χ\s*2\(.*,.*\)\s*=\s*\d+\s*", 'χ2 Vlaue'),
        (r"χ\s*2\(.*,.*\)\s*=\s*\d+\.?,?\d+", 'χ2 Vlaue'),
        (r"χ\s*2\[.*,.*\]\s*=\s*\d+\s*", 'χ2 Vlaue'),
        (r"χ\s*2\[.*,.*\]\s*=\s*\d+\.?,?\d+", 'χ2 Vlaue'),

        # χ
        (r" \.?,?;?\(?\s*χ\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+", 'χ Value'),
        (r" \.?,?;?\(?\s*χ\s*=\s*\d+\.\d+", 'χ Value'),
        (r" \.?,?;?\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+", 'χ Vlaue'),
        (r" \.?,?;?\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+\.?,?\d+", 'χ Vlaue'),
        (r" \.?,?;?\(?\s*χ\s*\[.*,.*\]\s*=\s*\d+", 'χ Vlaue'),
        (r" \.?,?;?\(?\s*χ\s*\[.*,.*\]\s*=\s*\d+\.?,?\d+", 'χ Vlaue'),

        # Odds Ratio
        (r"[oO]dds? [rR]atios?", 'Odds Ratio Context'),
        (r" \.?,?;?\(?\s*O\.R\s*\)?\.?,?;? ", 'Odds Ratio Context'),
        (r" \.?,?;?\(\s*OR\s*\)\s*\.?,?;? ", 'Odds Ratio Context'),
        (r" \.?,?;?\(?\s*OR\s*=\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*OR\s*=\s*[–-]?\s*\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*O\.R\s*=\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*O\.R\s*=\s*[–-]?\s*\.\d+ ", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*of\s*[–-]?\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*of\s*[–-]?\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*of\s*[–-]?\d+\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*1", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*\d+\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),

        # confidence interval
        (r"[Cc]on[fﬁ]i?dence [Ii]ntervals?", 'confidence interval Context'),
        (r" \(?\s*C\.I\.?\s*\)?\.?,?;?:? ", 'confidence interval Context'),
        # (r"\(?\s*[Cc]onﬁdence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Context'),
        (r"\(?\s*\d+\s*\%\s*[Cc]on[ﬁf]i?dence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        # (r"\(?\s*\d+\s*\%\s*[Cc]onfidence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.I\s*\)?\.?,?;?:? ", 'confidence interval Context'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\] ", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\)?,?\.?;? ", 'confidence interval Value'),
        (r"C\.?\s*I\s*\d+\s*\%\s*\[\s*-?\s*\d+\.\d+\s*,\s*-?\s*\s*\d+\s*\]", 'confidence interval Value'),
        (r"\d+\s*\%\s*\s*,?\s*C\.?I\s*±\s*\d+\.\d+\s*", 'confidence interval Value'),
        (r"C\.?I\s*±\s*\d+\.\d+", 'confidence interval Value'),

        # Kappa   [–-]?
        (r" \.?,?;?\(?\s*κ\s*\)?\.?,?;? ", 'Kappa κ Context'),
        (r" \.?,?;?\(?\s*κ\s*[=:><≥≤]\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[=:><≥≤]\s*\.\d+", 'Kappa κ Value'),
        (r"[Kk]appa [Vv]alues?", 'Kappa κ Context'),

        # β Value
        (r" \.?,?;?\(?\s*β\s*=\s*[–-−]?\s*\d+\.\d+", 'β Value'),
        (r" \.?,?;?\(?\s*β\s*=\s*[–-−]?\s*\.\d+", 'β Value'),

        # z-Score
        (r" \.?,?;?\(?\s*[Zz]-[Ss]cores?", 'z-score Context'),
        (r"[Zz]-[Ss]core of -?\s*\d+\.\d+", 'z-score Value'),
        (r"[Zz]-[Ss]core is -?\s*\d+\.\d+", 'z-score Value'),
        (r"[Zz]-[Ss]core was -?\s*\d+\.\d+", 'z-score Value'),


        # correlation coefficients
        (r"  \.?,?;?\(?\s*ρ\s*=\s*[–-−]?\s*\.\d+", 'ρ Value'),
        (r" \.?,?;?\(?\s*ρ\s*=\s*[–-−]?\s*\d+\.\d+", 'ρ Value'),
        (r"[pP]earson’?s?\s*[cC]orrelations?\s*ρ", 'Pearson’s Correlation ρ Context'),
        # correlation coefficients
        (r"[Cc]orrelation [Cc]oef[ﬁf]-?\s*\s*i?cients? .*\s*\d+\.\d+", 'Correlation Coefficients Value'),
        # (r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\d+\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oef[fﬁ]-?\s*\s*i?cients? .*\s*\.\d+", 'Correlation Coefficients Value'),
        # (r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        # (r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oef[fﬁ]-?\s*\s*i?cients?\s*:?\s*[–-]?\s*\d+\.\d+", 'Coefficient Vlaue'),
        # (r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oef[fﬁ]-?\s*\s*i?cients?\s*:?\s*[–-]?\s*\.\d+", 'Coefficient Vlaue'),
        # correlation coefficients
        (r"[Cc]orrelation [Cc]oef[fﬁ]i?cient .* was .*\s*[–-]?\s*\d+\.\d+", 'Correlation Coefficient Value'),
        # (r"[Cc]orrelation [Cc]oefficient .* was .*\s*\d+[–-]?\s*\.\d+", 'Correlation Coefficient Value'),
        # (r"\(?\s*[Cc]orrelation [Cc]oefficient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oef[fﬁ]i?cient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?",
         'Correlation Coefficient Value'),

        # Spearman’s rank correlation
        (r"[sS]pearman’?s?\s*[Rr]ank[–-]?\s*[cC]?o?r?r?e?l?a?t?i?o?n?s?", 'Spearman’s rank correlation Context'),

        # Spearman − ρ
        (r"[sS]pearman\s*[–-−]?\s*ρ", 'Spearman − ρ Context'),
        (r"[sS]pearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\d+\.\d+", 'Spearman − ρ Value'),
        (r"[sS]pearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\.\d+", 'Spearman − ρ Value'),

        # Degree of freedom
        (r" \(?\s*d\s*f\s*\)?\.?,?;? ", 'Degree of freedom Context'),
        (r" \(?\s*d\s*f\s*=\s*\d+", 'Degree of freedom Value'),
        (r" \(?\s*d\s*f\s*=\s*\d+\.\d+", 'Degree of freedom Value'),

        # Total Variation Distance
        (r" \.?,?;?\(?\s*TVDs?\s*\)?\.?,?;? ", 'Total Variation Distance Context'),
        (r" \.?,?;?\(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\d+\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r" \.?,?;?\(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r"[tT]otal [vV]ariation [dD]istances?", 'Total Variation Distance Context'),

        # R^2
        (r" \.?,?;?\(?\s*R\s*2\s*\)?\.?,?;? ", 'R^2 Context'),
        (r" \.?,?;?\(?\s*R\s*2\s*=\s*\d+\.\d+", 'R^2 Vlaue'),
        (r"\.?,?;?\(?\s*R\s*2\s*=\s*0\.\d+", 'R^2 Context'),
        (r" \.?,?;?\(?\s*R\s*2\s*a\s*d\s*j\s*=\s*\d+\.\d+", 'R^2 Value'),
        (r" \.?,?;?\(?\s*a\s*d\s*j\s*=\s*\d+\.\d+", 'R^2 Value'),

        # f^2 Value
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f^2 Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\.\d+", 'f^2 Value'),

        # f Value
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\s*,\s*d+\s*\)\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\s*,\s*d+\s*\)\s*[<=>]\s*[–-−]?\s*\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\.\d+\s*,\s*d+\.\d+\s*\)\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*\(\s*d+\.\d+\s*,\s*d+\.\d+\s*\)\s*[<=>]\s*[–-−]?\s*\.\d+", 'f Value'),

        # η^2
        (r" \.?,?;?\(?\s*η\s*2\s*=\s*\.\d+", 'Eta square η^2 Value'),
        (r" \.?,?;?\(?\s*η\s*2\s*=\s*\d+\.\d+", 'Eta square η^2 Value'),
        (r" \.?,?;?\(?\s*η\s*[pP]\s*2\s*=\s*\d+\.\d+", 'Eta square η^2 Value'),
        (r" \.?,?;?\(?\s*η\s*[pP]\s*2\s*=\s*\.\d+", 'Eta square η^2 Value'),
        (r"[eE]ta-?\s*[sS]quared?\s*=\s*\.\d+", 'Eta square η^2 Value'),
        (r"[eE]ta-?\s*[sS]quared?\s*=\s*d+\.\d+", 'Eta square η^2 Value'),
        (r"η\s*2-?\s*[Vv]alue", 'Eta square η^2 Context'),
        (r"[eE]ta-?\s*[sS]quared?", 'Eta square η^2 Context'),

        # Statistical Power
        (r"[Ss]tatistical [pP]ower of \d+\.\d+", 'Statistical Power Value'),
        (r"[Ss]tatistical [pP]ower of \.\d+", 'Statistical Power Value'),

        # Alpha
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*\d+\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\d+\.\d+", 'Alpha α Vlaue'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\.\d+", 'Alpha α Value'),
        (r"\d+\s*≤\s*\u03B1\s*≤\s*\d+", 'Alpha α Values Range'),
        (r"\d+\.\d+\s*≤\s*\u03B1\s*≤\s*\d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*d+\.\d+", 'Alpha α Value'),
        (r"[aA]lpha [Ll]evels? of\s*d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? of\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? was\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? was\s*\d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? .*\s*\d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? .*\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha [Rr]ang[ei]?n?g? from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),

        #################Significant Level
        (r"[Ss]igni[fﬁ]i?can[tc]e? [Ll]evel of \d+\.\d+", 'Significant Level Value'),
        (r"[Ss]igni[fﬁ]i?can[tc]e? [Ll]evel of \.\d+", 'Significant Level Value'),
        # (r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \d+\.\d+\s*\)?,?\.?;?", 'Significant Level Value'),
        # (r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \.\d+\s*\)?,?\.?;?", 'Significant Level Value'),

        # Krippendorff’s alpha
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha", 'Krippendorff’s alpha Context'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1", 'Krippendorff’s alpha Context'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]?\s*\(?\s*\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\s*\u03B1\s*[<>=]?\s*\(?\s*\.\d+\s*\)?", 'Krippendorff’s alpha Value'),

        # Cronbach’s α
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1", 'Cronbach’s α Context'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 of \d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 of \.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 .*\s*\d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 .*\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? [Aa]lpha .*\s*\d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? [Aa]lpha .*\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*=\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*=\s*\d+\.\d+", 'Cronbach’s αValue'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*\(?\s*\d+\.\d+\s*[–-−]?\s*\d+\.\d+\s*\)?", 'Cronbach’s α Value'),

        # r Value
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?0\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?0\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),
        #r_s Value
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?0\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?\s*\d+\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?0\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*=\s*[–-]?\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r_s Value'),
        (r" \.?,?;?\(?\s*r\s*s\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r_s Value'),

        # acceptance criteria
        (r"[aA]cceptance [Cc]riteria of \d+\.\d+", 'acceptance criteria Value'),

        # Bonferroni–Holm
        (r"[bB]onferroni[–-]?\s*[hH]?o?l?m?", 'Bonferroni–Holm Context'),
        (r"[bB]onferroni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),
        # (r"[bB]onferroni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),
        (r"[bB]onferoni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),

        # Comparing Results
        (r"[Rr]esults? .* faster than .*", 'Comparing Results Context and Values'),
        (r"[Ff]ound .* on average .* faster than .*", 'Comparing Results Context and Values'),
        (r"[Cc]omparing .* to .*", 'Comparing Results Context and Values'),
        (r" \.?,?;?\(?\s*[Ff]\s*\(.*\)\s*[<>]\s*[Ff]\s*\(.*\)\s*\)?\.?,?;? ", 'Comparing Results Values'),
        (r" \.?,?;?\(?\s*\d+\.\d+\s*[<>]\s*\d+\.\d+\s*\)?\.?,?;? ", 'Comparing Results Values'),

        # Correlation between
        (r"[Cc]orrelations? between", 'Correlation Context'),
        # Positive and Negative Correlation
        (r"[pP]ositive [Cc]orrelate?d?i?o?n?", 'Positive Correlation Context'),
        (r"[Nn]egative [Cc]orrelate?d?i?o?n?", 'Negative Correlation Context'),

        # λ Value
        (r"λ\s*=\s*\d+\.\d+", 'Negative Correlation Context'),
        (r"λ\s*=\s*\.\d+", 'Negative Correlation Context'),

        # ω Omega suared Value
        (r"ω\s*2\s*=[–-]?\s*\d+\.\d+", 'ω Omega suared Value'),
        (r"ω\s*2\s*=[–-]?\s*\.\d+", 'ω Omega suared Value'),
        (r"\(?\s*ω\s*2\s*\)?", 'ω Omega suared Value'),

        # Power Value
        (r"[Pp]ower of \d+\.\d+", 'Power Value'),
        (r"[Pp]ower of \.\d+", 'Power Value'),

        # Kendall’s τ correlation coefficients
        (r"[kK]endall’s τ [Cc]orrelation [Cc]oef[fﬁ]i?cients?", 'Kendall’s τ context'),
        (r"[kK]endall’s τ", 'Kendall’s τ context'),
        (r"τ\s*=[–-]?\s*\d+", 'Kendall’s τ Value'),
        (r"τ\s*=[–-]?\s*\d+\.\d+", 'Kendall’s τ Value'),

        #rank Value
        (r"[Rr]ank of \d+\.\d+", 'rank Value'),
        (r"[Rr]ank is \d+\.\d+", 'rank Value'),
        (r"[Rr]ank was \d+\.\d+", 'rank Value'),

        # σ^2 Value
        (r"σ\s*2\s*=[–-]?\s*\d+\.\d+", 'σ^2 Value'),

        # Phi (φ) Value
        (r"φ\s*=\s*[–-]?\d+\.\d+", 'Phi (φ) Value'),
        (r"φ\s*=\s*[–-]?\.\d+", 'Phi (φ) Value'),


    ]

    results_dict = OrderedDict()

    for sentence in sentences:
        tags_found = []
        matches_found = []
        numbers_found = []
        numbers_not_matched = []

        for pattern, tag in tags:
            matches = re.findall(pattern, sentence)
            if matches:
                tags_found.extend([f'{tag}: ({" ,  ".join(matches)})'])
                matches_found.extend(matches)
        if tags_found:
            numbers = re.findall(r'\d+(?:\.\d+)?', sentence)  # \d+\.\d+   #\b(\w+)\s+(\w+)\s+(\d+\.\d+)\b
            for number in numbers:
                if not any(number in match for match in matches_found):
                    numbers_not_matched.append(number)
            if numbers_not_matched:
                numbers_found = numbers_not_matched
            else:
                numbers_found = []
            results_dict[sentence] = (", ".join(tags_found), ", ".join(matches_found), ", ".join(numbers_found))

    results = [(k, v[0], v[1], v[2]) for k, v in results_dict.items()]

    csv_save_directory = filedialog.askdirectory(title="Select directory to save .csv file")
    if csv_save_directory:
        output_file_path = os.path.join(csv_save_directory, f"{file_name}_results.csv")
        with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sentence', 'Tagged Matches', 'Matches', 'Other not tagged Values'])
            for result in results:
                writer.writerow(result)
        print(f'Statistical information extracted and saved to {output_file_path} successfully.')
        return output_file_path


def browse_file():
    txt_file_paths = filedialog.askopenfilenames(title="Select .txt Files", filetypes=[("Text Files", "*.txt")])
    if txt_file_paths:
        txt_text.delete(1.0, tk.END)
        results_text.delete(1.0, tk.END)
        all_rows = []
        for file_path in txt_file_paths:
            txt_text.insert(tk.END, f"Processing file: {file_path}\n\n")
            txt_text.update_idletasks()
            results_file_path = extract_statistical_info(file_path)
            txt_text.insert(tk.END, f"Statistical information extracted. Results saved to: {results_file_path}\n\n")
            txt_text.update_idletasks()
            with open(results_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                rows = []
                for row in csv_reader:
                    sentence = row['Sentence']
                    tag = row['Tagged Matches']
                    Matches = row['Matches']
                    Numbers = row['Other not tagged Values']
                    rows.append(f"Sentence: {sentence}\n Tagged Matches: {tag}\n Matches: {Matches}\n Other not tagged Values: {Numbers}\n*******************************************************\n\n")
                    #rows.append(f"Sentence: {sentence}\n\n Tag: {tag}\n\n Match: {Matches}\n\n\n*******************************************************\n\n\n")
                all_rows.extend(rows)
                results_text.config(state=tk.NORMAL)
                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, "".join(all_rows))
                results_text.config(state=tk.DISABLED)

def browse_file2():
    txt_file_paths = filedialog.askopenfilenames(title="Select .txt Files", filetypes=[("Text Files", "*.txt")])
    if txt_file_paths:
        txt_text.delete(1.0, tk.END)
        results_text.delete(1.0, tk.END)
        all_rows = []
        for file_path in txt_file_paths:
            txt_text.insert(tk.END, f"Processing file: {file_path}\n\n")
            txt_text.update_idletasks()
            results_file_path = extract_statistical_info_with_not_tagged_numbers(file_path)
            txt_text.insert(tk.END, f"Statistical information extracted. Results saved to: {results_file_path}\n\n")
            txt_text.update_idletasks()
            with open(results_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                rows = []
                for row in csv_reader:
                    sentence = row['Sentence']
                    tag = row['Tagged Matches']
                    Matches = row['Matches']
                    Numbers = row['Other not tagged Values']
                    rows.append(f"Sentence: {sentence}\n Tagged Matches: {tag}\n Matches: {Matches}\n Other not tagged Values: {Numbers}\n*******************************************************\n\n")
                    #rows.append(f"Sentence: {sentence}\n\n Tag: {tag}\n\n Match: {Matches}\n\n\n*******************************************************\n\n\n")
                all_rows.extend(rows)
                results_text.config(state=tk.NORMAL)
                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, "".join(all_rows))
                results_text.config(state=tk.DISABLED)



def join_txt_files():
    txt_file_paths = filedialog.askopenfilenames(title="Select .txt Files", filetypes=[("Text Files", "*.txt")])
    if txt_file_paths:
        txt_save_directory = filedialog.askdirectory(title="Select directory to save joined .txt file")
        if txt_save_directory:
            joined_file_path = os.path.join(txt_save_directory, "joined_file.txt")
            with open(joined_file_path, 'w', encoding='utf-8') as joined_file:
                for file_path in txt_file_paths:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        joined_file.write(content)
                        joined_file.write('\n')
            print(f'Txt files joined and saved to {joined_file_path} successfully.')

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

root = tk.Tk()
root.title("PDF in .Txt-File Converter and Statistical Information Extractor")
pdf_to_txt_frame = tk.Frame(root)
pdf_to_txt_frame.pack(side=tk.TOP, padx=10, pady=10)
buttons_frame = tk.Frame(pdf_to_txt_frame)
buttons_frame.pack(pady=10)
pdf_to_txt_button = tk.Button(buttons_frame, text="Convert PDF to Text", command=convert_pdf_to_txt)
pdf_to_txt_button.pack(side=tk.LEFT)
pdf_to_txt_button = tk.Button(buttons_frame, text="Convert PDF to Text and filter Headers", command=convert_pdf_to_txt2)
pdf_to_txt_button.pack(side=tk.LEFT, padx=10)
join_button = tk.Button(buttons_frame, text="Join more than .txt File", command=join_txt_files)
join_button.pack(side=tk.LEFT, padx=10)
browse_button = tk.Button(buttons_frame, text="Method1 Extract Statistical Information from .txt File", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=10)
browse_button = tk.Button(buttons_frame, text="Method2 Extract Statistical Information from .txt File", command=browse_file2)
browse_button.pack(side=tk.LEFT, padx=10)
join_button = tk.Button(buttons_frame, text="Display .csv File", command=display_csv_tables)
join_button.pack(side=tk.LEFT, padx=10)
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



#####Regex Patterns
'''
        # p-values
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*\.\d+\s*\)?\s*\.?,?;? ", 'p-value'),
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*1\s*\)?\s*\.?,?;? ", 'p-value'),
        (r" \.?,?;?\(?\s*p\s*[<=>≥≤]\s*0\.\d+\s*\)?\s*\.?,?;? ", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?", 'p-value Context'),
        (r" \.?,?;?\(?0?\.\d+ [Pp]\s*[–-]?\s*[Vv]alues?\s*\)? \.?,?;? ", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?\s*[=<>≥≤]\s*\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues?\s*[=<>≥≤]\s*\d+\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*smaller than \.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*smaller than 0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*bigger than \.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*bigger than 0\.\d+", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*are .*\s*0\.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? .*\s*are .*\s*.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? of 0\.\d+\s*", 'p-value'),
        (r"[Pp][–-]?[Vv]alues? of .\d+\s*", 'p-value'),
        (r"corr?[–-]?\s*p\s*[<=>≥≤]\s*\.\d+", 'corrected p-value'),
        (r"corr?[–-]?\s*p\s*[<=>≥≤]\s*0\.\d+", 'corrected p-value'),
        (r"corrected [Pp][–-]?[Vv]alues?", 'corrected p-value'),

        #Mann Whitny P-value MW
        #(r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        #(r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*0\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        #(r" \.?,?;?\(?MW=\d+×10−\d+\)?", 'Mann Whitny P-value (MW)'),

        (r"MW\s*[<=>≥≤]\s*\.\d+", 'Mann Whitny P-value (MW)'),
        (r"MW\s*[<=>≥≤]\s*0\.\d+", 'Mann Whitny P-value (MW)'),
        (r"MW=\d+×10−\d+", 'Mann Whitny P-value (MW)'),

        #Participants Number
        (r"Participants were \d+", 'Participants Number'),

        #Mean
        (r"[Mm]ean .*\s*of \d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .*\s*of \d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean\s*[:=]?\s*\d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean\s*[:=]?\s*\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .* was \d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r"[Mm]ean .* was \d+\s*\%?[Ss]?", 'Mean Value'),
        (r" \.?,?;?\(?\s*[mMµ]\s*[:=]\s*\d+\.\d+\s*\%?[Ss]?", 'Mean Value'),
        (r" [mMµ]\s*[:=]\s*\d+\s*\%?[Ss]?", 'Mean Value'),

        #Median
        (r"[Mm]edian .*\s*of \d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*of \d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian\s*[:=]?\s*\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian\s*[:=]?\s*\d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r" \.?,?;?\(?[Mm][Dd]\s*[:=]\s*\d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r" \.?,?;?\(?[Mm][Dd]\s*[:=]\s*\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*was \d+\.\d+\s*\%?[Ss]?", 'Median Value'),
        (r"[Mm]edian .*\s*was \d+\s*\%?[Ss]?", 'Median Value'),

        #Max
        (r"[Mm]ax\s*[=:]\s*\d+\.\d+", 'Max Value'),
        (r"[Mm]ax\s*[=:]\s*\d+", 'Max Value'),

        #Min
        (r"[Mm]in\s*[:=]\s*\d+\.\d+", 'Min Value'),
        (r"[Mm]in\s*[:=]\s*\d+", 'Min Value'),

        #Range
        (r"[Rr]ange\s*[=:]?o?f?\s*\d+\s*[–-]\s*\d+", 'Range'),
        (r"[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\s*,\s*\d+\s*\]", 'Range'),
        (r"[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'Range'),
        (r"[Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'range'),

        #Standard Deviation Value
        (r" \.?,?;?\(?\s*[Ss][Dd]\s*[:=]?\s*\d+\.\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*[Ss][Dd]\s*[:=]?\s*\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*[sS][tT][dD]\s*\)?\s*[:=]?\s*\(?\s*\d+\.\d+\s*\)?", 'Standard Deviation Value'),
        (r"[Ss]tandard [Dd]eviation of \d+\.\d+", 'Standard Deviation Value'),
        (r"[Ss]tandard [Dd]eviation of \d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?σ\s*[=:]\s*\d+\.\d+", 'Standard Deviation Value'),
        (r" \.?,?;?\(?σ\s*[=:]\s*\d+", 'Standard Deviation Value'),
        (r"[sS]tandard [dD]eviations?", 'Standard Deviation Context'),
        (r" \(?\s*[sS][tT][Dd]\s*\)? ", 'Standard Deviation Context'),

        #Test statistic V
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+\.\d+", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*0", 'Test statistic V'),
        #test statistic W Value
        (r" \.?,?;?\(?\s*W\s*[=:]\s*\d+\.\d+", 'Test statistic W'),
        (r" \.?,?;?\(?\s*W\s*[=:]\s*\d+", 'Test statistic W'),
        (r" \.?,?;?\(?\s*W\s*[=:]\s*0", 'Test statistic W'),
        # test statistic U Value
        (r" \.?,?;?\(?\s*U\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Test statistic U'),
        (r" \.?,?;?\(?\s*U\s*[=:]\s*[–-−]?\s*\d+", 'Test statistic U'),
        ##test statistic H Value
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+\.\d+", 'H Value'),
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\.\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+\.\d+", 'H Value'),
        (r" \.?,?;?\(?\s*[hH]\s*\(\s*\d+\s*\)\s*[:=]\s*[–-−]?\s*\d+", 'H Value'),
        (r" \.?,?;?\(?\s*H\s*[:=]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'H Value'),

        #Z Value
        (r" \.?,?;?\(?\s*[zZ]\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Z Value'),
        (r" \.?,?;?\(?\s*[zZ]\s*[=:]\s*[–-−]?\s*\d+", 'Z Value'),

        #(r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+\.\d+", 'Z Value'),
        #(r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+", 'Z Value'),

        #b Value
        (r" \.?,?;?\(?\s*b\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'b Value'),

        #F Value
        (r" \.?,?;?\(?\s*[Ff]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*[:=]\s*\d+\.\d+", 'F Value'),
        (r" \.?,?;?\(?\s*[Ff]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*[:=]\s*\d+\.\d+", 'F Value'),

        #T Value
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\d+\.\d+\s*", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r" \.?,?;?\(?\s*[Tt]\s*\(\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\)\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r" [tT]\s*-?\s*[Vv]alues? ", 'T Value Context'),

        #Singnificantly different
        (r"[Ss]igni[ﬁf]i?cantly [Dd]ifferents?", 'Singnificantly different Context'),
        #(r"[Ss]ignificantly different", 'Singnificantly different Context'),
        (r"[Ss]igni[fﬁ]i?cant [Dd]ifferences?", 'Singnificantly different Context'),# significant difference
        #(r"\(?\s*significant [Dd]ifferences?\s*\)?,?\.?;?", 'Singnificantly different Context'),
        (r"[Ss]igni[fﬁ]i?cantly [Dd]ifferents?", 'Singnificantly different Context'),
        (r"[Ss]tatistically [Dd]ifferent", 'statistically different'),
        (r"[Ss]tatistical differences?", 'statistically different'),
        (r"[Ss]tatistical [Ss]igni[fﬁ]i?cance", 'statistical significance'),
        #(r"\(?\s*[Ss]tatistical [Ss]igniﬁcance\s*\)?,?\.?;?", 'statistical significance'),
        (r"[Ss]tatistically [Ss]igni[fﬁ]i?cant\s*\)?,?\.?;?", 'statistical significance'),
        #(r"\(?\s*[Ss]tatistically [Ss]ignificant\s*\)?,?\.?;?", 'statistical significance'),

        #Chi-square test
        (r"[Cc]hi-?\s*[sS]quared?\s*[Tt]?e?s?t?s?", 'Chi-square test'),

        #ANOVA test
        (r" \.?,?;?\(?\s*ANOVA", 'ANOVA test'),

        #post-Hoc
        #(r"\(?\s*[Pp]ost-?\s*[Hh]oc\s*\)?\.?,?;?", 'post-Hoc Test'),
        (r"[Pp]ost-?\s*[Hh]oc-??\s*[Tt]?e?s?t?s?", 'post-Hoc Test'),

        #Fisher’s exact test
        (r"[fF]isher’?s? [Ee]xact [Tt]?e?s?t?s?", 'Fisher’s exact test'),
        (r"[fF]isher’?s? [Tt]?e?s?t?s?", 'Fisher’s exact test'),
        (r" \.?,?;?\(?\s*FET\s*:?", 'Fisher’s exact test'),

        #Wilcoxon signed-rank test
        (r"[Ww]ilcoxon-?\s*[Ss]igned-??\s*[Rr]anks?", 'Wilcoxon signed-rank test'),
        (r"[Ss]igne?d?-?\s*[Rr]anks?-?\s*[Ww]ilcoxon", 'Wilcoxon signed-rank test'),

        #Wilcoxon test
        (r"[Ww]ilcoxon\s*t?e?s?t?s?", 'Wilcoxon test'),

        #Wilcoxon-Rank-Sum Tests
        (r"[Ww]ilcoxon-?\s*[rR]ank-?\s*[sS]um", 'Wilcoxon-Rank-Sum Test'),
        #(r"[wW]ilcoxon\s*[–-−]?\s*[rR]ank\s*[–-−]?\s*[Ss]um\s*:?", 'Wilcoxon-Rank-Sum Test'),
        #(r"[wW]ilcoxon-?\s*[Rr]ank-?\s*[sS]um", 'Wilcoxon-Rank-Sum Test'),
        (r"[Ww]ilcoxon-?\s*[Mm]ann-?\s*[Ww]hitney", 'Wilcoxon-Rank-Sum Test'),
        (r"[mM]ann-?\s*[wW]hitney\s*[Uu]?", 'Wilcoxon-Rank-Sum Test'),
        (r" \.?,?;?\(?\s*[Uu]-?\s*[Tt]ests?\s*\)?\.?,?;? ", 'Wilcoxon-Rank-Sum Test'),
        #(r"Mann\s*[–-−]?\s*Whitney\s*[Uu]", 'Wilcoxon-Rank-Sum Test'),
        (r"\.?,?;?\(?\s*MWU-?\s*[Tt]ests?\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r" MWU ", 'Wilcoxon-Rank-Sum Test'),

        #t-test
        (r" \.?,?;?\(?\s*[Tt]-?\s*[Tt]ests?\s*\)?\.?,?;? ", 't-test'),
        #(r" \(?\s*t tests?\s*\)?\.?,?;?:? ", 't-test'),

        # t-test
        (r" \.?,?;?\(?\s*H-?\s*[Tt]ests?\s*\)?\.?,?;?: ", 'H-test'),
        #(r" \(?\s*H tests?\s*\)?\.?,?;?:? ", 'H-test'),

        #Mood’s median test
        (r"[mM]ood[s’]?\s*[s’]?-?\s*[Mm]edian [Tt]ests?", 'Mood’s median test'),

        #Friedman test
        (r"[fF]riedman [Tt]ests?\s*\)?\.?,?;?:?", 'Friedman test'),
        #Friedman Analysis
        (r"[fF]riedman[s’]?\s*[s’]?\s*[Aa]nalysis", 'Friedman test'),

        #Kruskal-Wallace
        (r"[Kk]ruskal-?\s*[wW]allace", 'Kruskal-Wallace'),

        #Paired Wilcoxon
        (r"[pP]aired [wW]ilcoxon", 'Paired Wilcoxon'),

        #Shapiro-Wilk Test
        (r"[sS]hapiro-?\s*[wW]ilks?", 'Shapiro-Wilk Test'),

        #Kruskal-Wallis Test Kruskal- Wallis
        (r"[kK]ruskal-?\s*[wW]allis", 'Kruskal-Wallis'),
        #(r"\(?\s*[kK]ruskal-?\s*[wW]allis [Tt]ests?\s*\)?\.?,?;?:?", 'Kruskal-Wallis'),

        #statistical tests comparing
        (r"[Ss]tatistical [tT]ests? [Cc]omparing", 'statistical tests comparing'),
        (r"[Ss]tatistical [Cc]omparing [tT]ests?", 'statistical tests comparing'),

        #Effect Size
        (r"[Ee]ffect [Ss]izes?", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes? of \d+\.\d+", 'Effect Size Value'),
        (r"\d+\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        #(r"d+\.\d+ [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ss]mall [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ll]arge [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Mm]edium [Ee]ffect [Ss]izes?", 'Effect Size Value'),
        (r"[Ll]imited [Ee]ffect [Ss]izes?", 'Effect Size Context'),
        (r"[Ee]ffect [Ss]izes?\s*\(?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]\s*\)?", 'Effect Size Value'),

        #Cramer’s V
        (r" \.?,?;?\(?\s*Cramer’s V?", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer’s V\s*=\s*\d+\.\d+", 'Cramer’s V'),
        (r" \.?,?;?\(?\s*Cramer’s V\s*=\s*\.\d+", 'Cramer’s V'),

        #Log Ratio
        (r" \.?,?;?\(?\s*[lL]og [rR]atio\s*\)?,?:?;?\.?", 'Log Ratio Context'),
        (r"[Ll]ogistic [Rr]egressions?", 'Logistic Regression Context'),

        #Log Odds
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds?", 'Log Odds Context'),
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds?\s*[=:]\s*[–-−]?\s*\d+\.\d+", 'Logistic Odds Value'),
        (r" \.?,?;?\(?\s*[lL]og [Oo]dds? .*of.*\s*[–-−]?\s*\d+\.\d+", 'Logistic Odds Value'),
        (r"[Nn]egative [lL]og [Oo]dds?", 'Negative Log Odds Context'),
        (r"[Pp]ositive [lL]og [Oo]dds?", 'Positive Log Odds Context'),

        #Regression coefficients
        (r"[rR]egression [Cc]oefficients?", 'Regression coefficients Context'),
        #linear regression
        (r"[Ll]inear [Rr]egressions?", 'linear regression Context'),

        #coefﬁcient Kappa
        (r"[Cc]oef[ﬁf]i?cient [kK]appa", 'coefﬁcient Kappa Context'),
        #(r"\(?\s*coefficient [kK]appa\s*\)?\.?,?;?", 'coefﬁcient Kappa Context'),
        (r"[cC]ohen’?s?\s*[Kk]appa coef[fﬁ]i?cient was \d+\.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        #(r"[cC]ohen’?s?\s*[Kk]appa coefficient was \d+\.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        (r"[cC]ohen’?s?\s*[Kk]appa coef[fﬁ]i?cient was \.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        #(r"[cC]ohen’?s?\s*[Kk]appa coefficient was \.\d+", 'Cohen’s Kappa coefﬁcient Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s* [cC]on[fﬁ]idence [Ii]nterval r?", 'Cohen’s Conﬁdence Interval Context'),
        #(r"\(?[cC]ohen[s’]?\s*[s’]?\s* [cC]offidence [Ii]nterval r?\s*\)?\.?,?;?", 'Cohen’s Conﬁdence Interval Context'),

        #coefﬁcient
        (r"[Cc]oef[ﬁf]i?cient\s*\(?\s*\d+\.\d+s*\)?", 'coefﬁcient Value'),
        #(r"\(?\s*[Cc]oefficient\s*\(?\s*\.\d+s*\)?\s*\)?\.?,?;?", 'coefﬁcient Value'),

        #Bernoulli Trial
        (r" [Bb]ernoulli [Tt]?r?i?a?l?s?", 'Bernoulli Trial Context'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\.\d+", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\d+\.\d+", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\s*\d+\.\d+×10−\d+", 'B Value'),

        #Cohens’ Kappa
        (r"[cC]ohen[s’]?\s*[s’]? [kK]appa", 'Cohens’ Kappa Context'),
        (r" \.?,?;?\(?\s*κ of \d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*\(\s*κ\s*\) of \d+\.\d+", 'Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]? [kK]appa .*\s*of .*\s*[–-−]?\s*\d+\.\d+", 'Kappa Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ", 'Cohens’ Kappa κ Context'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oef[fﬁ]i?cients?", 'Cohens’ Kappa coefﬁcient Context'),
        #(r"\(?\s*Cohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oefficient\s*\)?\.?,?;?", 'Cohens’ Kappa coefﬁcient Context'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ\s*[=:]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[>=<]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*[Kk]\s*[>=<]\s*\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[>=<]\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*.*\s*was\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[Oo]ver\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[Bb]elow\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*[Kk]\s*[>=<≥≤]\s*\d+\.\d+", 'Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ\s*=\s*\d+\.\d+", 'Cohens’ Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ values? between \.\d+ and \.\d+", 'Cohens’ Kappa κ Value'),
        (r"[cC]ohen[s’]?\s*[s’]?\s*κ values? between \d+\.\d+ and \d+\.\d+", 'Cohens’ Kappa κ Value'),

        # Cohens’ d
        (r"[cC]ohen[s’]?\s*[’s]? d\s*[:=]\s*[–-]?\s*\d+\.\d+", 'Cohens’ d Value'),
        (r"[cC]ohen[s’]?\s*[’s]? d\s*=\s*[–-]?\s*\.\d+", 'Cohens’ d Value'),
        (r"[cC]ohen[s’]?\s*[’s]? d\s*\)?\.?,?;? ", 'Cohens’ d Context'),

        #d Value
        (r" \.?,?;?\(?\s*d\s*=\s*[–-]?\s*\d+\.\d+", 'd Value'),
        (r" \.?,?;?\(?\s*d\s*=\s*[–-]?\s*\.\d+", 'd Value'),
        (r"[cC]ohen[s’]?\s*[’s]? [Ee]ffect [Ss]izes?\s*[Vv]?a?l?u?e?s?\s*\)?\.?,?;?", 'Cohen’s effect size Context'),

        #Pearson’s r # Pearson’s correlation coefﬁcient
        (r"[pP]earson[s’]?\s*[’s]?\s*r\s*\)?\.?,?;? ", 'Pearson’s r Context'),

        #Pearson’s correlation coefﬁcient
        (r"[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?[ﬁf]?i?c?i?e?n?t?", 'Pearson’s correlation coefﬁcient Context'),
        #(r"\(?\s*[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?f?i?c?i?e?n?t?\s*\)?\.?,?;?",'Pearson’s correlation coefﬁcient Context'),
        #(r"\(?\s*[Cc]orrelation\s*[Cc]oefficient\s*\)?\.?,?;?",'correlation coefﬁcient Context'),
        (r"[Cc]orrelation\s*[Cc]oef[ﬁf]i?cient", 'correlation coefﬁcient Context'),

        # Pearson’s ρ
        (r"[pP]earson’?s?\s*ρ\s*\)?\.?,?;? ", 'Pearson’s  ρ Context'),

        #Agreement Value
        (r"[Aa]greement was \d+\.\d+\%?", 'Agreement Value'),
        (r"[Aa]greement was \.\d+\s*", 'Agreement Value'),
        (r"[Aa]greement .*\s*of \d+\.\d+", 'Agreement Value'),

        #χ2
        (r" \.?,?;?\(?\s*χ\s*2\s*-?[Dd]ifference [Tt]?e?s?t?s?", 'χ2 Context'),
        (r" \.?,?;?\(?\s*χ\s*2\s*-?[Ss]cores?", 'χ2 Context'),
        (r" \.?,?;?\(?\s*χ\s*2\s*\)?\.?,?;? ", 'χ2 Context'),
        (r"χ\s*2\s*[–-]?\s*[tT]ests?", 'χ2 Test'),
        (r"χ\s*2\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+", 'χ2 Value'),
        (r"χ\s*2\s*=\s*\d+\.\d+", 'χ2 Value'),
        (r"χ\s*2\(.*,.*\)\s*=\s*\d+\s*", 'χ2 Vlaue'),
        (r"χ\s*2\(.*,.*\)\s*=\s*\d+\.?,?\d+", 'χ2 Vlaue'),

        #χ
        (r" \.?,?;?\(?\s*χ\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+", 'χ Value'),
        (r" \.?,?;?\(?\s*χ\s*=\s*\d+\.\d+", 'χ Value'),
        (r" \.?,?;?\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+", 'χ Vlaue'),
        (r" \.?,?;?\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+\.?,?\d+", 'χ Vlaue'),

        #Odds Ratio
        (r"[oO]dds? [rR]atios?", 'Odds Ratio Context'),
        (r" \.?,?;?\(?\s*O\.R\s*\)?\.?,?;? ", 'Odds Ratio Context'),
        (r" \.?,?;?\(\s*OR\s*\)\s*\.?,?;? ", 'Odds Ratio Context'),
        (r" \.?,?;?\(?\s*OR\s*=\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*OR\s*=\s*[–-]?\s*\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*O\.R\s*=\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),
        (r" \.?,?;?\(?\s*O\.R\s*=\s*[–-]?\s*\.\d+ ", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*1", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*\d+\.\d+", 'Odds Ratio Value'),
        (r"[Oo]dds?\s*[Rr]atio\s*[:=]\s*[–-]?\s*\d+\.\d+", 'Odds Ratio Value'),

        #confidence interval
        (r"[Cc]on[fﬁ]i?dence [Ii]ntervals?", 'confidence interval Context'),
        #(r"\(?\s*[Cc]onﬁdence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Context'),
        (r"\(?\s*\d+\s*\%\s*[Cc]on[ﬁf]i?dence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        #(r"\(?\s*\d+\s*\%\s*[Cc]onfidence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.I\s*\)?\.?,?;?:? ", 'confidence interval Context'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\] ", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]", 'confidence interval Value'),
        (r" \.?,?;?\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\)?,?\.?;? ", 'confidence interval Value'),

        #Kappa   [–-]?
        (r" \.?,?;?\(?\s*κ\s*\)?\.?,?;? ", 'Kappa κ Context'),
        (r" \.?,?;?\(?\s*κ\s*[=:><≥≤]\s*\d+\.\d+", 'Kappa κ Value'),
        (r" \.?,?;?\(?\s*κ\s*[=:><≥≤]\s*\.\d+", 'Kappa κ Value'),
        (r"[Kk]appa [Vv]alues?", 'Kappa κ Context'),

        #β Value
        (r" \.?,?;?\(?\s*β\s*=\s*[–-−]?\s*\d+\.\d+", 'β Value'),
        (r" \.?,?;?\(?\s*β\s*=\s*[–-−]?\s*\.\d+", 'β Value'),

        #z-Score
        (r" \.?,?;?\(?\s*[Zz]-[Ss]cores?", 'z-score'),

        #correlation coefficients
        (r"  \.?,?;?\(?\s*ρ\s*=\s*[–-−]?\s*\.\d+", 'ρ Value'),
        (r" \.?,?;?\(?\s*ρ\s*=\s*[–-−]?\s*\d+\.\d+", 'ρ Value'),
        (r"[pP]earson’?s?\s*[cC]orrelations?\s*ρ", 'Pearson’s Correlation ρ Context'),
        #correlation coefficients
        (r"[Cc]orrelation [Cc]oef[ﬁf]-?\s*\s*i?cients? .*\s*\d+\.\d+", 'Correlation Coefficients Value'),
        #(r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\d+\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oef[fﬁ]-?\s*\s*i?cients? .*\s*\.\d+", 'Correlation Coefficients Value'),
        #(r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        #(r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oef[fﬁ]-?\s*\s*i?cients?\s*:?\s*[–-]?\s*\d+\.\d+", 'Coefficient Vlaue'),
        #(r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oef[fﬁ]-?\s*\s*i?cients?\s*:?\s*[–-]?\s*\.\d+", 'Coefficient Vlaue'),
        #correlation coefficients
        (r"[Cc]orrelation [Cc]oef[fﬁ]i?cient .* was .*\s*[–-]?\s*\d+\.\d+", 'Correlation Coefficient Value'),
        #(r"[Cc]orrelation [Cc]oefficient .* was .*\s*\d+[–-]?\s*\.\d+", 'Correlation Coefficient Value'),
        #(r"\(?\s*[Cc]orrelation [Cc]oefficient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oef[fﬁ]i?cient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),



        #Spearman’s rank correlation
        (r"[sS]pearman’?s?\s*[Rr]ank[–-]?\s*[cC]?o?r?r?e?l?a?t?i?o?n?s?", 'Spearman’s rank correlation Context'),

        #Spearman − ρ
        (r"[sS]pearman\s*[–-−]?\s*ρ",'Spearman − ρ Context'),
        (r"[sS]pearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\d+\.\d+", 'Spearman − ρ Value'),
        (r"[sS]pearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\.\d+", 'Spearman − ρ Value'),

        #Degree of freedom
        (r" \(?\s*d\s*f\s*\)?\.?,?;? ", 'Degree of freedom Context'),
        (r" \(?\s*d\s*f\s*=\s*\d+\s*\)?\.?,?;? ", 'Degree of freedom Value'),
        (r" \(?\s*d\s*f\s*=\s*\d+\.\d+\s*\)?\.?,?;? ", 'Degree of freedom Value'),

        #Total Variation Distance
        (r" \.?,?;?\(?\s*TVDs?\s*\)?\.?,?;? ", 'Total Variation Distance Context'),
        (r" \.?,?;?\(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\d+\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r" \.?,?;?\(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r"[tT]otal [vV]ariation [dD]istances?", 'Total Variation Distance Context'),

        #R^2
        (r" \.?,?;?\(?\s*R\s*2\s*\)?\.?,?;?\s*", 'R^2 Context'),
        (r" \.?,?;?\(?\s*R\s*2\s*=\s*\d+\.\d+", 'R^2 Vlaue'),
         #R2 = 0.08.
        (r" \.?,?;?\(?\s*R\s*2\s*a\s*d\s*j\s*=\s*\d+\.\d+", 'R^2 Value'),
        (r" \.?,?;?\(?\s*a\s*d\s*j\s*=\s*\d+\.\d+", 'R^2 Value'),

        #f^2 Value
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f^2 Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\.\d+", 'f^2 Value'),

        # f Value
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\d+\.\d+", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\.\d+", 'f Value'),

        #η^2
        (r" \.?,?;?\(?\s*η\s*2\s*=\s*\.\d+", 'Eta square η^2 Value'),
        (r" \.?,?;?\(?\s*η\s*2\s*=\s*\d+\.\d+", 'Eta square η^2 Value'),

        #Statistical Power
        (r"[Ss]tatistical [pP]ower of \d+\.\d+", 'Statistical Power Value'),
        (r"[Ss]tatistical [pP]ower of \.\d+", 'Statistical Power Value'),

        #Alpha
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*\d+\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\.\d+", 'Alpha α Value'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\d+\.\d+", 'Alpha α Vlaue'),
        (r" \.?,?;?\(?\s*\u03B1\s*of\s*\.\d+", 'Alpha α Value'),
        (r"\d+\s*≤\s*\u03B1\s*≤\s*\d+", 'Alpha α Values Range'),
        (r"\d+\.\d+\s*≤\s*\u03B1\s*≤\s*\d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1\s*[<=>≥≤]\s*d+\.\d+", 'Alpha α Value'),
        (r"[aA]lpha [Ll]evels? of\s*d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? of\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? was\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? was\s*\d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? .*\s*\d+\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha [Ll]evels? .*\s*\.\d+", 'Alpha Levels Value'),
        (r"[aA]lpha from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha [Rr]ang[ei]?n?g? from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \.\d+ to \.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r"[aA]lpha [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),
        (r" \.?,?;?\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+", 'Alpha α Range Values'),

        #################Significant Level
        (r"[Ss]igni[fﬁ]i?can[tc]e? [Ll]evel of \d+\.\d+", 'Significant Level Value'),
        (r"[Ss]igni[fﬁ]i?can[tc]e? [Ll]evel of \.\d+", 'Significant Level Value'),
        #(r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \d+\.\d+\s*\)?,?\.?;?", 'Significant Level Value'),
        #(r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \.\d+\s*\)?,?\.?;?", 'Significant Level Value'),

        #Krippendorff’s alpha
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha", 'Krippendorff’s alpha Context'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1", 'Krippendorff’s alpha Context'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \d+\.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \.\d+", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]?\s*\(?\s*\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?", 'Krippendorff’s alpha Value'),
        (r"[kK]rippendorff?[s’]?\s*[s’]?\s*\s*\u03B1\s*[<>=]?\s*\(?\s*\.\d+\s*\)?", 'Krippendorff’s alpha Value'),

        #Cronbach’s α
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1", 'Cronbach’s α Context'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 of \d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 of \.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 .*\s*\d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1 .*\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? [Aa]lpha .*\s*\d+\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? [Aa]lpha .*\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*=\s*\.\d+", 'Cronbach’s α Value'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*=\s*\d+\.\d+", 'Cronbach’s αValue'),
        (r"[cC]ronbach[s’]?\s*[s’]? \u03B1\s*\(?\s*\d+\.\d+\s*[–-−]?\s*\d+\.\d+\s*\)?", 'Cronbach’s α Value'),

        #r Value
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?0\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?0\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*=\s*[–-]?\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\.\d+", 'r Value'),
        (r" \.?,?;?\(?\s*r\s*\(\s*\d+\.\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+", 'r Value'),

        #acceptance criteria
        (r"[aA]cceptance [Cc]riteria of \d+\.\d+", 'acceptance criteria Value'),

        #Bonferroni–Holm
        (r"[bB]onferroni[–-]?\s*[hH]?o?l?m?", 'Bonferroni–Holm Context'),
        (r"[bB]onferroni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),
        #(r"[bB]onferroni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),
        (r"[bB]onferoni[–-]?\s*[Cc]orrect[ie][od]n?", 'Bonferroni–Holm Context'),

        #Comparing Results
        (r"[Rr]esults? .* faster than .*", 'Comparing Results Context and Values'),
        (r"[Ff]ound .* on average .* faster than .*", 'Comparing Results Context and Values'),
        (r"[Cc]omparing .* to .*", 'Comparing Results Context and Values'),
        (r" \.?,?;?\(?\s*[Ff]\s*\(.*\)\s*[<>]\s*[Ff]\s*\(.*\)\s*\)?\.?,?;? ", 'Comparing Results Values'),
        (r" \.?,?;?\(?\s*\d+\.\d+\s*[<>]\s*\d+\.\d+\s*\)?\.?,?;? ", 'Comparing Results Values'),

        #Correlation between
        (r"[Cc]orrelations? between", 'Correlation Context'),
        #Positive and Negative Correlation
        (r"[pP]ositive [Cc]orrelate?d?i?o?n?", 'Positive Correlation Context'),
        (r"[Nn]egative [Cc]orrelate?d?i?o?n?", 'Negative Correlation Context'),
'''####