
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
        (r"\(?\s*p\s*[<=>≥≤]\s*\.\d+\s*\)?\.?,?;?", 'p-value'),
        (r" \(?\s*p\s*[<=>≥≤]\s*1\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*p\s*[<=>≥≤]\s*0\.\d+\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*p-value\s*\)?\.?,?;?", 'p-value Context'),
        (r" \(?\s*[Pp] [Vv]alue\s*\)?\.?,?;?", 'p-value'),
        (r" \(?\s*\d+\.\d+ [Pp]\s*[–-]\s*[Vv]alue\s*\)?\.?,?;?", 'p-value'),
        (r" \(?\s*\d+\.\d+ [Pp]\s*[Vv]alue\s*\)?\.?,?;?", 'p-value'),
        (r" \(?\s*\.\d+ [Pp]\s*[–-]\s*[Vv]alue\s*\)?\.?,?;?", 'p-value'),
        (r" \(?\s*\.\d+ [Pp]\s*[Vv]alue\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*p-values?\s*[=<>≥≤]\s*\.\d+\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*p-values?\s*[=<>≥≤]\s*\d+\.\d+\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*p-value .* smaller than 0?\.\d+\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*p-values .* are .* 0?\.\d+\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*p-?\s*values? of 0?\.\d+\s*\)?\.?,?;?", 'p-value'),
        (r"\(?\s*cor\s*−\s*p\s*[<=>≥≤]\s*\.\d+\*?\s*\)?\.?,?;?", 'corrected p-value'),
        (r"\(?\s*cor\s*−\s*p\s*[<=>≥≤]\s*\d\.\d+\*?\s*\)?\.?,?;?", 'corrected p-value'),

        #Mann Whitny P-value MW
        (r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        (r" \.?,?;?\(?\s*MW\s*[<=>≥≤]\s*0\.\d+\s*\)?\.?,?;?", 'Mann Whitny P-value (MW)'),
        (r" \.?,?;?\(?MW=\d+×10−\d+\)?", 'Mann Whitny P-value (MW)'),

        #Participants Number
        (r"\(?\s*Participants were \d+\s*\)?\.?,?;?", 'Participants Number'),

        #Mean
        (r"\(?\s*[Mm]ean .*\s*of \d+\.\d+\s*\)?,?\.?;?", 'Mean Value'),
        (r"\(?\s*[Mm]ean .*\s*of \d+\s*\)?,?\.?;?", 'Mean Value'),
        (r"\(?\s*[Mm]ean\s*[:=]?\s*\d+\.\d+\s*\)?,?\.?;?", 'Mean Value'),
        (r"\(?\s*[Mm]ean\s*[:=]?\s*\d+\s*\)?,?\.?;?", 'Mean Value'),
        (r"\(?\s*[Mm]ean .* was \d+\.\d+\s*\)?,?\.?;?", 'Mean Value'),
        (r"\(?\s*[Mm]ean .* was \d+\s*\)?,?\.?;?", 'Mean Value'),
        (r" \.?,?;?\(?\s*[mMµ]\s*[:=]\s*\d+\.\d+\s*\)?,?;?\.?", 'Mean Value'),
        (r" \.?,?;?\(?\s*[mMµ]\s*[:=]\s*\d+\s*\)?,?;?\.?", 'Mean Value'),

        #Median
        (r"\(?\s*[Mm]edian .*\s*of \d+\.\d+\s*\)?,?\.?;?", 'Median Value'),
        (r"\(?\s*[Mm]edian .*\s*of \d+\s*\)?,?\.?;?", 'Median Value'),
        (r"\(?\s*[Mm]edian\s*[:=]?\s*\d+\s*\)?,?\.?;?", 'Median Value'),
        (r"\(?\s*[Mm]edian\s*[:=]?\s*\d+\.\d+\s*\)?,?\.?;?", 'Median Value'),
        (r" \(?\s*[Mm][Dd]\s*[:=]\s*\d+\.\d+\s*\)?,?\.?;?", 'Median Value'),
        (r" \(?\s*[Mm][Dd]\s*[:=]\s*\d+\s*\)?,?\.?;?", 'Median Value'),
        (r"\(?\s*[Mm]edian .*\s*was \d+\.\d+\s*\)?,?\.?;?", 'Median Value'),
        (r"\(?\s*[Mm]edian .*\s*was \d+\s*\)?,?\.?;?", 'Median Value'),

        #Max
        (r"\(?\s*[Mm]ax\s*[=:]\s*\d+\.\d+\s*\)?,?\.?;?", 'Max Value'),
        (r"\(?\s*[Mm]ax\s*[=:]\s*\d+\s*\)?,?\.?;?", 'Max Value'),

        #Min
        (r"\(?\s*[Mm]in\s*[:=]\s*\d+\.\d+\s*\)?,?\.?;?", 'Min Value'),
        (r"\(?\s*[Mm]in\s*[:=]\s*\d+\s*\)?,?\.?;?", 'Min Value'),

        #Range
        (r"\(?\s*[Rr]ange\s*[=:]?o?f?\s*\d+\s*[–-]\s*\d+\s*\)?,?\.?;?", 'Range'),
        (r"\(?\s*[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\s*,\s*\d+\s*\]\s*\)?,?\.?;?", 'Range'),
        (r"\(?\s*[Rr]ange\s*[=:]?o?f?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]\s*\)?,?\.?;?", 'Range'),
        (r"\(?\s*[Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+\)?,?\.?;?", 'range'),
        (r"\(?\s*[Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+\)?,?\.?;?", 'range'),

        #Standard Deviation Value
        (r" \.?,?;?\(?\s*sd\s*[:=]?\s*\d+\.\d+.*\s*\)?,?\.?;?", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*SD\s*[:=]?\s*\d+\.\d+\s*\)?,?\.?;?", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*sd\s*[:=]?\s*\d+.*\s*\)?,?\.?;?", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*SD\s*[:=]?\s*\d+.*\s*\)?,?\.?;?", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*STD\s*\)?\s*[:=]?\s*\d+\.\d+\s*\)?,?\.?;?", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*std\s*\)?\s*[:=]?\s*\d+\.\d+\s*\)?,?\.?;?", 'Standard Deviation Value'),
        (r"\(?\s*[Ss]tandard [Dd]eviation of \d+\.\d+\s*\)?,?\.?;?", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*σ\s*[=]\s*\d+\.\d+\s*\)?,?;?\.?", 'Standard Deviation Value'),
        (r" \.?,?;?\(?\s*σ\s*[=]\s*\d+\%\s*\)?,?;?\.?", 'Standard Deviation Value'),
        (r"\(?\s*[sS]tandard [dD]eviations?\s*\)?,?;?\.?", 'Standard Deviation Context'),

        #Test statistic V
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+\.\d+\s*\)?\.?,?;?", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*\d+\s*\)?\.?,?;?", 'Test statistic V'),
        (r" \.?,?;?\(?\s*V\s*[=:]\s*0\s*\)?\.?,?;?", 'Test statistic V'),
        #test statistic W Value
        (r" \.?,?;?\(?\s*(?<![Mm])W\s*[=:]\s*\d+\.\d+\s*\)?\.?,?;?", 'Test statistic W'),
        (r" \.?,?;?\(?\s*(?<![Mm])W\s*[=:]\s*\d+\s*\)?\.?,?;?", 'Test statistic W'),
        (r" \.?,?;?\(?\s*(?<![Mm])W\s*[=:]\s*0\s*\)?\.?,?;?", 'Test statistic W'),
        # test statistic U Value
        (r" \.?,?;?\(?\s*(?<![MW])U\s*[=:]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Test statistic U'),
        (r" \.?,?;?\(?\s*(?<![MW])U\s*[=:]\s*[–-−]?\s*\d+\s*\)?\.?,?;?", 'Test statistic U'),
        #test statistic H Value
        (r" \.?,?;?\(?\s*H\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'H Value'),
        (r" \.?,?;?\(?\s*H\s*\(\s*\d+\s*\)\s*=\s*\d+\s*\)?\.?,?;?", 'H Value'),
        (r" \.?,?;?\(?\s*H\s*=\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'H Value'),

        #Z Value
        (r" \.?,?;?\(?\s*Z\s*[=:]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Z Value'),
        (r" \.?,?;?\(?\s*Z\s*[=:]\s*[–-−]?\s*\d+\s*\)?\.?,?;?", 'Z Value'),

        (r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+\.\d+\s*\)?\.?,?;?", 'Z Value'),
        (r" \.?,?;?\(?\s*z =\s*[–-−]?-?\s*\d+\s*\)?\.?,?;?", 'Z Value'),

        #b Value
        (r" \.?,?;?\(?\s*b\s*[=:]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'b Value'),

        #F Value
        (r"\(?\s*[Ff]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'F Value'),

        #T Value
        (r"\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r"\(?\s*[Tt]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'T Value'),
        (r" \(?\s*[tT]\s*-?\s*[Vv]alues?\s*\)?\.?,?;?", 'T Value Context'),

        #Singnificantly different
        (r"\(?\s*signiﬁcantly different\s*\)?,?\.?;?", 'Singnificantly different Context'),
        (r"\(?\s*significantly different\s*\)?,?\.?;?", 'Singnificantly different Context'),
        (r"\(?\s*signiﬁcant differences?\s*\)?,?\.?;?", 'Singnificantly different Context'),# significant difference
        (r"\(?\s*significant differences?\s*\)?,?\.?;?", 'Singnificantly different Context'),
        (r"\(?\s*significantly different\s*\)?,?\.?;?", 'Singnificantly different Context'),
        (r"\(?\s*statistically different\s*\)?,?\.?;?", 'statistically different'),
        (r"\(?\s*statistical differences?\s*\)?,?\.?;?", 'statistically different'),
        (r"\(?\s*[Ss]tatistical [Ss]ignificance\s*\)?,?\.?;?", 'statistical significance'),
        (r"\(?\s*[Ss]tatistical [Ss]igniﬁcance\s*\)?,?\.?;?", 'statistical significance'),
        (r"\(?\s*[Ss]tatistically [Ss]igniﬁcant\s*\)?,?\.?;?", 'statistical significance'),
        (r"\(?\s*[Ss]tatistically [Ss]ignificant\s*\)?,?\.?;?", 'statistical significance'),

        #Chi-square test
        (r"\(?\s*[Cc]hi-[sS]quared?\s*[Tt]?e?s?t?s?\s*\)?\.?,?;?", 'Chi-square test'),

        #ANOVA test
        (r"\(?\s*ANOVA\s*\)?\.?,?;?", 'ANOVA test'),

        #post-Hoc
        (r"\(?\s*[Pp]ost-?\s*[Hh]oc\s*\)?\.?,?;?", 'post-Hoc Test'),
        (r"\(?\s*[Pp]ost-?\s*[Hh]oc [Tt]ests?\s*\)?\.?,?;?", 'post-Hoc Test'),

        #Fisher’s exact test
        (r"\(?\s*[fF]isher’?s? [Ee]xact [Tt]?e?s?t?s?\s*\)?\.?,?;?", 'Fisher’s exact test'),
        (r"\(?\s*[fF]isher’?s? [Tt]ests?\s*\)?\.?,?;?", 'Fisher’s exact test'),
        (r" \(?\s*FET\s*:?\s*\)?\.?,?;? ", 'Fisher’s exact test'),

        #Wilcoxon signed-rank test
        (r"\(?\s*[Ww]ilcoxon [Ss]igned[–-]?\s*[Rr]anks? [Tt]?e?s?t?s?\s*\)?\.?,?;?", 'Wilcoxon signed-rank test'),
        (r"\(?\s*[Ss]igne?d?\s*[–-]?\s*[Rr]anks? [Ww]ilcoxon [Tt]?e?s?t?s?\s*\)?\.?,?;?", 'Wilcoxon signed-rank test'),

        #Wilcoxon test
        (r"\(?\s*[Ww]ilcoxon\s*t?e?s?t?s?\s*\)?\.?,?;?", 'Wilcoxon test'),

        #Wilcoxon-Rank-Sum Tests
        (r"\(?\s*[Ww]ilcoxon[–-]?\s*[rR]ank[–-]?\s*\s*[sS]um\s* [Tt]?e?s?t?s?\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r"\(?\s*[wW]ilcoxon [rR]ank [Ss]um\s*:?\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r"\(?\s*[wW]ilcoxon-?\s*[Rr]ank-?\s*[sS]um\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r"\(?\s*[Ww]ilcoxon[–-]?\s*[Mm]ann[–-]?\s*[Ww]hitney\s*[Tt]?e?s?t?s?\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r"\(?\s*[mM]ann-?\s*[wW]hitney\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r"\(?\s*Mann–Whitney\s*\)?\.?,?;?", 'Wilcoxon-Rank-Sum Test'),
        (r" \(?\s*[Uu]-?\s*[Tt]ests?\s*\)?\.?,?;? ", 'Wilcoxon-Rank-Sum Test'),
        (r" \(?\s*Mann-Whitney U test\s*\)?\.?,?;? ", 'Wilcoxon-Rank-Sum Test'),
        (r" \(?\s*MWU-?\s*[Tt]ests?\s*\)?\.?,?;? ", 'Wilcoxon-Rank-Sum Test'),
        (r" \(?\s*MWU\s*\)?\.?,?;? ", 'Wilcoxon-Rank-Sum Test'),

        #t-test
        (r" \(?\s*t-tests?\s*\)?\.?,?;?: ", 't-test'),
        (r" \(?\s*t tests?\s*\)?\.?,?;?:? ", 't-test'),

        # t-test
        (r" \(?\s*H-tests?\s*\)?\.?,?;?: ", 'H-test'),
        (r" \(?\s*H tests?\s*\)?\.?,?;?:? ", 'H-test'),

        #Mood’s median test
        (r"\(?\s*[mM]ood[s’]?\s*[s’]?[–-−]?\s*[Mm]edian [Tt]ests?\s*\)?\.?,?;?:?", 'Mood’s median test'),

        #Friedman test
        (r"\(?\s*[fF]riedman\s*[Tt]?e?s?t?s?\s*\)?\.?,?;?:?", 'Friedman test'),
        #Friedman Analysis
        (r"\(?\s*[fF]riedman[s’]?\s*[s’]?\s*[Aa]nalysis\s*\)?\.?,?;?", 'Friedman test'),

        #Kruskal-Wallace
        (r"\(?\s*[Kk]ruskal-?\s*[wW]allace\s*\)?\.?,?;?:?", 'Kruskal-Wallace'),

        #Paired Wilcoxon
        (r"\(?\s*[pP]aired [wW]ilcoxon\s*[Tt]?e?s?t?s?\s*\)?\.?,?;?:?", 'Paired Wilcoxon'),

        #Shapiro-Wilk Test
        (r"\(?\s*[sS]hapiro[–-]?\s*[wW]ilks?\s*[Tt]?e?s?t?s?\s*\)?\.?,?;?:?", 'Shapiro-Wilk Test'),

        #Kruskal-Wallis Test Kruskal- Wallis
        (r"\(?\s*[kK]ruskal-?\s*[wW]allis\s*:?\s*\)?\.?,?;?:?", 'Kruskal-Wallis'),
        (r"\(?\s*[kK]ruskal-?\s*[wW]allis [Tt]ests?\s*\)?\.?,?;?:?", 'Kruskal-Wallis'),

        #statistical tests comparing
        (r"\(?\s*[Ss]tatistical [tT]ests? [Cc]omparing\s*\)?\.?,?;? ", 'statistical tests comparing'),
        (r"\(?\s*[Ss]tatistical [Cc]omparing [tT]ests?\s*\)?\.?,?;? ", 'statistical tests comparing'),

        #Effect Size
        (r"\(?\s*[Ee]ffect [Ss]izes?\s*\)?\.?,?;?", 'Effect Size Context'),
        (r"\(?\s*[Ee]ffect [Ss]izes? of \d+\.\d+\s*\)?\.?,?;?", 'Effect Size Value'),
        (r"\(?\s*\d+\.\d+ [Ee]ffect [Ss]izes?\s*\)?\.?,?;?", 'Effect Size Value'),
        (r"\(?\s* \.\d+ [Ee]ffect [Ss]izes?\s*\)?\.?,?;?", 'Effect Size Value'),
        (r"\(?\s*[Ss]mall [Ee]ffect [Ss]izes?\s*\)?\.?,?;?", 'Effect Size Value'),
        (r"\(?\s*[Ll]arge [Ee]ffect [Ss]izes?\s*\)?\.?,?;?", 'Effect Size Value'),
        (r"\(?\s*[Mm]edium [Ee]ffect [Ss]izes?\s*\)?\.?,?;?", 'Effect Size Value'),
        (r"\(?\s*[Ll]imited [Ee]ffect [Ss]izes?\s*\)?\.?,?;?", 'Effect Size Context'),
        (r"\(?\s*[Ee]ffect [Ss]izes?\s*\(?\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]\s*\)?\s*\)?\.?,?;?", 'Effect Size Value'),

        #Cramer’s V
        (r"\(?\s*Cramer’s V?\s*\)?\.?,?;?", 'Cramer’s V'),
        (r"\(?\s*Cramer’s V\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'Cramer’s V'),
        (r"\(?\s*Cramer’s V\s*=\s*\.\d+\s*\)?\.?,?;?", 'Cramer’s V'),

        #Log Ratio
        (r"\(?\s*[lL]og [rR]atio\s*\)?\.?,?;?", 'Log Ratio Context'),
        (r"\(?\s*[Ll]ogistic [Rr]egression\s*\)?\.?,?;?", 'Logistic Regression Context'),

        #Log Odds
        (r"\(?\s*[lL]og [Oo]dds?\s*\)?\.?,?;?", 'Log Odds Context'),
        (r"\(?\s*[lL]og [Oo]dds?\s*[=:]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Logistic Odds Value'),
        (r"\(?\s*[lL]og [Oo]dds? .*of\s*.*\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Logistic Odds Value'),
        (r"\(?\s*[Nn]egative [lL]og [Oo]dds?\s*\)?\.?,?;?", 'Negative Log Odds Context'),
        (r"\(?\s*[Pp]ositive [lL]og [Oo]dds?\s*\)?\.?,?;?", 'Positive Log Odds Context'),

        #Regression coefficients
        (r"\(?\s*[rR]egression [Cc]oefficients?\s*\)?\.?,?;?", 'Regression coefficients Context'),
        #linear regression
        (r"\(?\s*[Ll]inear [Rr]egressions?\s*\)?\.?,?;?", 'linear regression Context'),

        #coefﬁcient Kappa
        (r"\(?\s*[Cc]oefﬁcient [kK]appa\s*\)?\.?,?;?", 'coefﬁcient Kappa Context'),
        (r"\(?\s*coefficient [kK]appa\s*\)?\.?,?;?", 'coefﬁcient Kappa Context'),
        (r"\(?[cC]ohen’?s?\s*[Kk]appa coefﬁcient was \d+\.\d+\s*\)?\.?,?;?", 'Cohen’s Kappa coefﬁcient Value'),
        (r"\(?[cC]ohen’?s?\s*[Kk]appa coefficient was \d+\.\d+\s*\)?\.?,?;?", 'Cohen’s Kappa coefﬁcient Value'),
        (r"\(?[cC]ohen’?s?\s*[Kk]appa coefﬁcient was \.\d+\s*\)?\.?,?;?", 'Cohen’s Kappa coefﬁcient Value'),
        (r"\(?[cC]ohen’?s?\s*[Kk]appa coefficient was \.\d+\s*\)?\.?,?;?", 'Cohen’s Kappa coefﬁcient Value'),
        (r"\(?[cC]ohen[s’]?\s*[s’]?\s* [cC]onﬁdence [Ii]nterval r?\s*\)?\.?,?;?", 'Cohen’s Conﬁdence Interval Context'),
        (r"\(?[cC]ohen[s’]?\s*[s’]?\s* [cC]offidence [Ii]nterval r?\s*\)?\.?,?;?", 'Cohen’s Conﬁdence Interval Context'),

        #coefﬁcient
        (r"\(?\s*[Cc]oefﬁcient\s*\(?\s*\d+\.\d+s*\)?\s*\)?\.?,?;?", 'coefﬁcient Value'),
        (r"\(?\s*[Cc]oefficient\s*\(?\s*\.\d+s*\)?\s*\)?\.?,?;?", 'coefﬁcient Value'),

        #Bernoulli Trial
        (r"\(?\s*[Bb]ernoulli\s*[Tt]?r?i?a?l?s?\s*\)?\.?,?;?", 'Bernoulli Trial Context'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\.\d+\s*\)?\.?,?;?", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\d+\.\d+\s*\)?\.?,?;?", 'B Value'),
        (r" \.?,?;?\(?\s*[Bb]\s*=\s*\d+\.\d+×10−\d+\s*\)?\.?,?;?", 'B Value'),

        #Cohens’ Kappa
        (r"\(?\s*[cC]ohen[s’]?\s*[s’]? [kK]appa\s*\)?\.?,?;?", 'Cohens’ Kappa Context'),
        (r"\(?\s*κ of \d+\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*\(κ\) of \d+\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*Cohen[s’]?\s*[s’]? Kappa .*\s*of .*\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Kappa Value'),
        (r"\(?\s*Cohen[s’]?\s*[s’]?\s*κ\s*\)?\.?,?;?", 'Cohens’ Kappa κ Context'),
        (r"\(?\s*Cohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oefﬁcient\s*\)?\.?,?;?", 'Cohens’ Kappa coefﬁcient Context'),
        (r"\(?\s*Cohen[s’]?\s*[s’]?\s*[Kk]appa\s*[Cc]oefficient\s*\)?\.?,?;?", 'Cohens’ Kappa coefﬁcient Context'),
        (r"\(?\s*Cohen[s’]?\s*[s’]?\s*κ\s*=\s*\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*κ\s*[>=<]\s*\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*[Kk]\s*[>=<]\s*\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*κ\s*[>=<]\s*\d+\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*κ\s*.*\s*was\s*\d+\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*κ\s*[Oo]ver\s*\d+\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*κ\s*[Bb]elow\s*\d+\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*[Kk]\s*[>=<≥≤]\s*\d+\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),
        (r"\(?\s*Cohen[s’]?\s*[s’]?\s*κ\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'Cohens’ Kappa κ Value'),
        (r"\(?\s*Cohen[s’]?\s*[s’]?\s*κ values? between \.\d+ and \.\d+\s*\)?\.?,?;?", 'Cohens’ Kappa κ Value'),
        (r"\(?\s*Cohen[s’]?\s*[s’]?\s*κ values? between \d+\.\d+ and \d+\.\d+\s*\)?\.?,?;?", 'Cohens’ Kappa κ Value'),

        # Cohens’ d
        (r"\(?\s*Cohen[s’]?\s*[’s]? d\s*=\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Cohens’ d Value'),
        (r"\(?\s*Cohen[s’]?\s*[’s]? d\s*=\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Cohens’ d Value'),
        (r"\(?\s*Cohen[s’]?\s*[’s]? d\s*\)?\.?,?;?", 'Cohens’ d Context'),

        #d Value
        (r"\(?\s*d\s*=\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'd Value'),
        (r"\(?\s*d\s*=\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'd Value'),
        (r"\(?\s*[cC]ohen[s’]?\s*[’s]? [Ee]ffect [Ss]ize\s*[Vv]?a?l?u?e?s?\s*\)?\.?,?;?", 'Cohen’s effect size Context'),

        #Pearson’s r # Pearson’s correlation coefﬁcient
        (r"\(?\s*[pP]earson’?s?\s*r\s*\)?\.?,?;?", 'Pearson’s r Context'),

        #Pearson’s correlation coefﬁcient
        (r"\(?\s*[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?ﬁ?c?i?e?n?t?\s*\)?\.?,?;?", 'Pearson’s correlation coefﬁcient Context'),
        (r"\(?\s*[Pp]earson[’s]?\s*[’s]?\s* [Cc]orrelation\s*[Cc]?o?e?f?f?i?c?i?e?n?t?\s*\)?\.?,?;?",'Pearson’s correlation coefﬁcient Context'),
        (r"\(?\s*[Cc]orrelation\s*[Cc]oefficient\s*\)?\.?,?;?",'correlation coefﬁcient Context'),
        (r"\(?\s*[Cc]orrelation\s*[Cc]oefﬁcient\s*\)?\.?,?;?", 'correlation coefﬁcient Context'),

        # Pearson’s ρ
        (r"\(?\s*[pP]earson’?s?\s*ρ\s*\)?\.?,?;?", 'Pearson’s  ρ Context'),

        #Agreement Value
        (r"\(?\s*[Aa]greement was \d+\.\d+\%?\s*\)?\.?,?;?", 'Agreement Value'),
        (r"\(?\s*[Aa]greement was \.\d+\s*\)?\.?,?;?", 'Agreement Value'),
        (r"\(?\s*[Aa]greement .*\s*of \d+\.\d+\s*\)?\.?,?;?", 'Agreement Value'),

        #χ2
        (r"\(?\s*χ\s*2\s*-?[Dd]ifference [Tt]?e?s?t?s?\s*\)?\.?,?;?", 'χ2 Context'),
        (r"\(?\s*χ\s*2\s*-?[Ss]cores?\s*\)?\.?,?;?", 'χ2 Context'),
        (r"\(?\s*χ\s*2\s*\)?\.?,?;?", 'χ2 Context'),
        (r"\(?\s*χ\s*2\s*[–-]?\s*[tT]ests?\s*\)?\.?,?;?", 'χ2 Test'),
        (r"\(?\s*χ\s*2\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'χ2 Value'),
        (r"\(?\s*χ\s*2\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'χ2 Value'),
        (r"\(?\s*χ\s*2\(.*,.*\)\s*=\s*\d+\s*\)?\.?,?;?", 'χ2 Vlaue'),
        (r"\(?\s*χ\s*2\(.*,.*\)\s*=\s*\d+\.?,?\d+\s*\)?\.?,?;?", 'χ2 Vlaue'),
        #χ
        (r"\(?\s*χ\s*\(\s*\d+\s*\)\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'χ Value'),
        (r"\(?\s*χ\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'χ Value'),
        (r"\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+\s*\)?\.?,?;?", 'χ Vlaue'),
        (r"\(?\s*χ\s*\(.*,.*\)\s*=\s*\d+\.?,?\d+\s*\)?\.?,?;?", 'χ Vlaue'),

        #Odds Ratio
        (r"\(?\s*[oO]dds? [rR]atios?\s*\)?\.?,?;?", 'Odds Ratio Context'),
        (r" \(?\s*O\.R\s*\)?\.?,?;? ", 'Odds Ratio Context'),
        (r" \(\s*OR\s*\)\s*\.?,?;? ", 'Odds Ratio Context'),
        (r"\(?\s*OR\s*=\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Odds Ratio Value'),
        (r"\(?\s*OR\s*=\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Odds Ratio Value'),
        (r"\(?\s*O\.R\s*=\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Odds Ratio Value'),
        (r"\(?\s*O\.R\s*=\s*[–-]?\s*\.\d+\s*\)?\.?,?;? ", 'Odds Ratio Value'),
        (r"\(?\s*[Oo]dds?\s*[Rr]atio\s*[:=]\s*\.\d+\s*\)?\.?,?;?", 'Odds Ratio Value'),
        (r"\(?\s*[Oo]dds?\s*[Rr]atio\s*[:=]\s*1\s*\)?\.?,?;?", 'Odds Ratio Value'),
        (r"\(?\s*[Oo]dds?\s*[Rr]atio\s*[:=]\s*\d+\.\d+\s*\)?\.?,?;?", 'Odds Ratio Value'),
        (r"\(?\s*[Oo]dds?\s*[Rr]atio\s*[:=]\s*[–-]\s*\d+\.\d+\s*\)?\.?,?;? ", 'Odds Ratio Value'),

        #confidence interval
        (r"\(?\s*[Cc]onfidence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Context'),
        (r"\(?\s*[Cc]onﬁdence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Context'),
        (r"\(?\s*\d+\s*\%\s*[Cc]onﬁdence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        (r"\(?\s*\d+\s*\%\s*[Cc]onfidence [Ii]ntervals?\s*\)?\.?,?;?", 'confidence interval Value'),
        (r"\(?\s*C\.I\s*\)?\.?,?;?", 'confidence interval Context'),
        (r"\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]\s*\)?\.?,?;?", 'confidence interval Value'),
        (r"\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\s*\]\s*\)?\.?,?;?", 'confidence interval Value'),
        (r"\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\]\s*\)?\.?,?;?", 'confidence interval Value'),
        (r"\(?\s*C\.?\s*I\s*=\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]\s*\)?\.?,?;?", 'confidence interval Value'),
        (r"\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\.\d+\s*\]\s*\)?,?\.?;?", 'confidence interval Value'),
        (r"\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\.\d+\s*\]\s*\)?,?\.?;?", 'confidence interval Value'),
        (r"\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\.\d+\s*,\s*\d+\s*\]\s*\)?,?\.?;?", 'confidence interval Value'),
        (r"\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]\s*\)?,?\.?;?", 'confidence interval Value'),
        (r"\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\[\s*\d+\s*,\s*\d+\s*\]\s*\)?,?\.?;?", 'confidence interval Value'),
        (r"\(?\s*\d+\s*\%\s*C\s*\.?\s*I\s*\)?,?\.?;?", 'confidence interval Value'),

        #Kappa   [–-]?
        (r"\(?\s*κ\s*\)?\.?,?;?", 'Kappa κ Context'),
        (r"\(?\s*κ\s*[=:><≥≤]\s*\d+?\.\d+\s*\)?\.?,?;?", 'Kappa κ Value'),

        (r"\(?\s*[Kk]appa [Vv]alues?\s*\)?\.?,?;?", 'Kappa κ Context'),

        #β Value
        (r"\(?\s*β\s*=\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'β Value'),
        (r"\(?\s*β\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'β Value'),

        #z-Score
        (r"\(?\s*[Zz]-[Ss]core\s*\)?\.?,?;?", 'z-score'),

        #correlation coefficients
        (r"\(?\s*ρ\s*=\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'ρ Value'),
        (r"\(?\s*ρ\s*=\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'ρ Value'),
        (r"\(?\s*[pP]earson’?s?\s*[cC]orrelations?\s*ρ\s*\)?\.?,?;?", 'Pearson’s Correlation ρ Context'),
        #correlation coefficients
        (r"\(?\s*[Cc]orrelation [Cc]oefﬁ-?\s*\s*cients? .*\s*\d+\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\d+\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oefﬁ-?\s*\s*cients? .*\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oeffi-?\s*\s*cients? .*\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficients Value'),
        (r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oefﬁ-?\s*\s*cients?\s*:?\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oeffi-?\s*\s*cients?\s*:?\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        (r"\(?\s*[Cc]oefﬁ-?\s*\s*cients?\s*:?\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Coefficient Vlaue'),
        #correlation coefficients
        (r"\(?\s*[Cc]orrelation [Cc]oefﬁcient .* was .*\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oefficient .* was .*\s*\d+[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oefficient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),
        (r"\(?\s*[Cc]orrelation [Cc]oefﬁcient .* was .*\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'Correlation Coefficient Value'),
        #Spearman’s rank correlation
        (r"\(?\s*[sS]pearman’?s?\s*[Rr]ank[–-]?\s*[cC]?o?r?r?e?l?a?t?i?o?n?s?\s*\)?\.?,?;?", 'Spearman’s rank correlation Context'),

        #Spearman − ρ
        (r"\(?\s*Spearman\s*[–-−]?\s*ρ\s*\)?\.?,?;?",'Spearman − ρ'),
        (r"\(?\s*Spearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\d+\.\d+\s*\)?\.?,?;?", 'Spearman − ρ Value'),
        (r"\(?\s*Spearman\s*[–-−]?\s*ρ\s*=\s*[–-−]?\.\d+\s*\)?\.?,?;?", 'Spearman − ρ Value'),

        #Degree of freedom
        (r" \(?\s*d\s*f\s*\)?\.?,?;? ", 'Degree of freedom Context'),
        (r" \(?\s*d\s*f\s*=\s*\d+\s*\)?\.?,?;? ", 'Degree of freedom Value'),
        (r" \(?\s*d\s*f\s*=\s*\d+\.\d+\s*\)?\.?,?;? ", 'Degree of freedom Value'),

        #Total Variation Distance
        (r" \(?\s*TVDs?\s*\)?\.?,?;? ", 'Total Variation Distance Context'),
        (r" \(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\d+\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r" \(?\s*TVDs?\s*\(?.*\)?\s*=\s*.*\s*\.\d+\s*\)?\.?,?;? ", 'Total Variation Distance Value'),
        (r"\(?\s*[tT]otal [vV]ariation [dD]istances?\s*\)?\.?,?;?", 'Total Variation Distance Context'),

        #R^2
        (r" \(?\s*R\s*2\s*\)?\.?,?;? ", 'R^2 Context'),
        (r"\(?\s*R\s*2\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'R^2 Vlaue'),
        (r"\(?\s*R\s*2\s*a\s*d\s*j\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'R^2 Value'),
        (r"\(?\s*a\s*d\s*j\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'R^2 Value'),

        #f^2 Value
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'f^2 Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*2\s*[<=>]\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'f^2 Value'),

        # f Value
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\d+\.\d+\s*\)?\.?,?;?", 'f Value'),
        (r" \.?,?;?:?\(?\s*[fF]\s*[<=>]\s*[–-−]?\s*\.\d+\s*\)?\.?,?;?", 'f Value'),

        #η^2
        (r"\(?\s*η\s*2\s*=\s*\.\d+\s*\)?\.?,?;?", 'Eta square η^2 Value'),
        (r"\(?\s*η\s*2\s*=\s*\d+\.\d+\s*\)?\.?,?;?", 'Eta square η^2 Value'),

        #Statistical Power
        (r"\(?\s*[Ss]tatistical [pP]ower of \d+\.\d+\s*\)?\.?,?;?", 'Statistical Power Value'),
        (r"\(?\s*[Ss]tatistical [pP]ower of \.\d+\s*\)?\.?,?;?", 'Statistical Power Value'),

        #Alpha
        (r"\(?\s*\u03B1\s*[<=>≥≤]\s*\.\d+\s*\)?,?\.?;?", 'Alpha α Value'),
        (r" \(?\s*\u03B1\s*[<=>≥≤]\s*\d+\.\d+\s*\)?,?\.?;?", 'Alpha α Value'),
        (r"\(?\s*\u03B1\s*of\s*\.\d+\s*\)?,?\.?;?", 'Alpha α Value'),
        (r"\(?\s*\u03B1\s*of\s*\d+\.\d+\s*\)?,?\.?;?", 'Alpha α Vlaue'),
        (r"\(?\s*\u03B1\s*of\s*\.\d+\s*\)?,?\.?;?", 'Alpha α Value'),
        (r"\(?\s*\d+\s*≤\s*\u03B1\s*≤\s*\d+\s*\)?,?\.?;?", 'Alpha α Values Range'),
        (r"\(?\s*\d+\.\d+\s*≤\s*\u03B1\s*≤\s*\d+\.\d+\s*\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*\u03B1\s*[<=>≥≤]\s*d+\.\d+\s*\)?,?\.?;?", 'Alpha α Value'),
        (r"\(?\s*[aA]lpha [Ll]evels? of\s*d+\.\d+\s*\)?,?\.?;?", 'Alpha Levels Value'),
        (r"\(?\s*[aA]lpha [Ll]evels? of\s*\.\d+\s*\)?,?\.?;?", 'Alpha Levels Value'),
        (r"\(?\s*[aA]lpha [Ll]evels? was\s*\.\d+\s*\)?,?\.?;?", 'Alpha Levels Value'),
        (r"\(?\s*[aA]lpha [Ll]evels? was\s*\d+\.\d+\s*\)?,?\.?;?", 'Alpha Levels Value'),
        (r"\(?\s*[aA]lpha [Ll]evels? .*\s*\d+\.\d+\s*\)?,?\.?;?", 'Alpha Levels Value'),
        (r"\(?\s*[aA]lpha [Ll]evels? .*\s*\.\d+\s*\)?,?\.?;?", 'Alpha Levels Value'),
        (r"\(?\s*[aA]lpha from \.\d+ to \.\d+\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*\u03B1 from \.\d+ to \.\d+\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*[aA]lpha [Rr]ang[ei]?n?g? from \.\d+ to \.\d+\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \.\d+ to \.\d+\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*[aA]lpha from \d+\.\d+ to \d+\.\d+\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*\u03B1 from \d+\.\d+ to \d+\.\d+\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*[aA]lpha [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+\)?,?\.?;?", 'Alpha α Range Values'),
        (r"\(?\s*\u03B1 [Rr]ang[ei]?n?g? from \d+\.\d+ to \d+\.\d+\)?,?\.?;?", 'Alpha α Range Values'),

        #Significant Level
        (r"\(?\s*[Ss]ignifican[tc]e? [Ll]evel of \d+\.\d+\s*\)?,?\.?;?", 'Significant Level Value'),
        (r"\(?\s*[Ss]ignifican[tc]e? [Ll]evel of \.\d+\s*\)?,?\.?;?", 'Significant Level Value'),
        (r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \d+\.\d+\s*\)?,?\.?;?", 'Significant Level Value'),
        (r"\(?\s*[Ss]igniﬁcan[tc]e? [Ll]evel of \.\d+\s*\)?,?\.?;?", 'Significant Level Value'),

        #Krippendorff’s alpha
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*\)?,?\.?;?", 'Krippendorff’s alpha Context'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \d+\.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha of \.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \d+\.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha was \.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1\s*\)?,?\.?;?", 'Krippendorff’s alpha Context'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \d+\.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 of \.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \d+\.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1 was \.\d+\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*[Aa]lpha\s*[<>=]?\s*\(?\s*\.\d+\s*\)?\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*\u03B1\s*[<>=]\s*\(?\s*\d+\.\d+\s*\)?\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),
        (r"\(?\s*[kK]rippendorff?[s’]?\s*[s’]?\s*\s*\u03B1\s*[<>=]?\s*\(?\s*\.\d+\s*\)?\s*\)?,?\.?;?", 'Krippendorff’s alpha Value'),

        #Cronbach’s α
        (r"\(?\s*Cronbach’?s? \u03B1\s*\)?,?\.?;?", 'Cronbach’s α Context'),
        (r"\(?\s*Cronbach’?s? \u03B1 of \d+\.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),
        (r"\(?\s*Cronbach’?s? \u03B1 of \.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),
        (r"\(?\s*Cronbach’?s? \u03B1 .*\s*\d+\.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),
        (r"\(?\s*Cronbach’?s? \u03B1 .*\s*\.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),
        (r"\(?\s*Cronbach’?s? [Aa]lpha .*\s*\d+\.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),
        (r"\(?\s*Cronbach’?s? [Aa]lpha .*\s*\.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),
        (r"\(?\s*Cronbach’?s? \u03B1\s*=\s*\.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),
        (r"\(?\s*Cronbach’?s? \u03B1\s*=\s*\d+\.?\d+\s*\)?,?\.?;?", 'Cronbach’s αValue'),
        (r"\(?\s*Cronbach’?s? \u03B1\s*\(?\s*\d+\.\d+\s*[–-−]?\s*\d+\.\d+\s*\)?,?\.?;?", 'Cronbach’s α Value'),

        #r Value
        (r"\(?\s*r\s*=\s*−0\.\d+\s*\)?\.?,?;?", 'r Value'),
        (r"\(?\s*r\s*=\s*-\s*\d+\.\d+\s*\)?\.?,?;?", 'r Value'),
        (r"\(?\s*r\s*=\s*0\.\d+\s*\)?\.?,?;?", 'r Value'),
        (r"\(?\s*r\s*=\s*−\.\d+\s*\)?\.?,?;?", 'r Value'),
        (r"\(?\s*r\s*=\s*\.\d+\s*\)?\.?,?;?", 'r Value'),
        (r"\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\.\d+\s*\)?\.?,?;?", 'r Value'),
        (r"\(?\s*r\s*\(\s*\d+\s*\)\s*=\s*[–-]?\s*\d+\.\d+\s*\)?\.?,?;?", 'r Value'),

        #acceptance criteria
        (r"\(?\s*[aA]cceptance [Cc]riteria of \d+\.\d+\s*\)?\.?,?;?", 'acceptance criteria Value'),

        #Bonferroni–Holm
        (r"\(?\s*[bB]onferroni[–-]?\s*[hH]?o?l?m?\s*\)?\.?,?;?", 'Bonferroni–Holm Context'),
        (r"\(?\s*[bB]onferroni [Cc]orrect[ie][od]n?\s*\)?\.?,?;?", 'Bonferroni–Holm Context'),
        (r"\(?\s*[bB]onferroni[–-]?\s*[Cc]orrect[ie][od]n?\s*\)?\.?,?;?", 'Bonferroni–Holm Context'),
        (r"\(?\s*[bB]onferoni[–-]?\s*[Cc]orrect[ie][od]n?\s*\)?\.?,?;?", 'Bonferroni–Holm Context'),

        #Comparing Results
        (r"\.?\(?\s*results .* faster than .*\s*\)?\.?,?;?", 'Comparing Results Context and Values'),
        (r"\.?\(?\s*found .* on average .* faster than .*\s*\)?\.?,?;?", 'Comparing Results Context and Values'),
        (r"\.?\(?\s*[Cc]omparing .* to .*\s*\)?\.?,?;?", 'Comparing Results Context and Values'),
        (r" \.?,?;?\(?\s*[Ff]\s*\(.*\)\s*[<>]\s*[Ff]\s*\(.*\)\s*\)?\.?,?;?", 'Comparing Results Values'),
        (r" \.?,?;?\(?\s*\d+\.\d+\s*[<>]\s*\d+\.\d+\s*\)?\.?,?;?", 'Comparing Results Values'),

        #Correlation between
        (r"\(?\s*[Cc]orrelations? between\)?,?\.?;?", 'Correlation Context'),
        #Positive and Negative Correlation
        (r"\(?\s*[pP]ositive [Cc]orrelate?d?i?o?n?\)?,?\.?;?", 'Positive Correlation Context'),
        (r"\(?\s*[Nn]egative [Cc]orrelate?d?i?o?n?\)?,?\.?;?", 'Negative Correlation Context'),
    ]
    results_dict = OrderedDict()

    for sentence in sentences:
        tags_found = []
        matches_found = []
        #numbers_found = []

        for pattern, tag in tags:
            matches = re.findall(pattern, sentence)

            if matches:
                #tags_found.extend(f'"{match}"' for match in matches)
                #matches_found.append(f'"{tag}"')

                #tags_found.extend(matches)  #richtig
                #matches_found.append(tag)   #richtig

                #tags_found.extend(matches)
                #matches_found.extend([tag] * len(matches))

                tags_found.extend([f'{tag}: ({"  ,  ".join(matches)})'])
                #tags_found.extend([f'{tag}: {match}' for match in matches])
                matches_found.extend([tag] * len(matches))

        # Find numbers in sentence that do not exist in matches_found
        #numbers = re.findall(r'\d+', sentence)
        #unique_numbers = [number for number in numbers if number not in matches_found]
        #numbers_found.extend(unique_numbers)

        #if tags_found or numbers_found:
        if tags_found:
            #results_dict[sentence] = (", ".join(tags_found), ", ".join(matches_found))

            results_dict[sentence] = (", ".join(matches_found), ", ".join(tags_found))   #richtig
            #results_dict[sentence] = (", ".join(tags_found), ", ".join(matches_found), ", ".join(numbers_found))#For other not tagged Values extraction

            #results_dict[sentence] = (", ".join(map(lambda match: f'"{match}"', matches_found)),", ".join(map(lambda tag: f'"{tag}"', tags_found)))

            #Hier I only tried to Order the Founed Tagged Match as same as they exist in the sentenc but that is not Working
            #ordered_tags_found = [tag_found for _, tag_found in sorted(zip(matches_found, tags_found))] #Falsch
            #results_dict[sentence] = (", ".join(matches_found), ", ".join(f'"{match}"' for match in ordered_tags_found)) #Falsch
            #ordered_matches_found = [match for _, match in sorted(zip(tags_found, matches_found))]
            #results_dict[sentence] = (", ".join(tags_found), ", ".join(f'"{match}"' for match in ordered_matches_found))


    results = [(k, v[0], v[1]) for k, v in results_dict.items()] #richtig
    #results = [(k, v[0], v[1], v[2]) for k, v in results_dict.items()]

    csv_save_directory = filedialog.askdirectory(title="Select directory to save .csv file")
    if csv_save_directory:
        output_file_path = os.path.join(csv_save_directory, f"{file_name}_results.csv")
        with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sentence', 'Tag', 'Wert(Match)', 'Numbers'])
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
                    tag = row['Tag']
                    Matches = row['Wert(Match)']
                    #Numbers = row['Numbers']
                    #rows.append(f"Sentence: {sentence}\n Tag: {tag}\n Match: {Matches}\n Other Numbers: {Numbers}\n*******************************************************\n\n")
                    rows.append(f"Sentence: {sentence}\n\n Tag: {tag}\n\n Match: {Matches}\n\n\n*******************************************************\n\n\n")
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
root.title("PDF to Txt Converter and Statistical Information Extractor")
pdf_to_txt_frame = tk.Frame(root)
pdf_to_txt_frame.pack(side=tk.TOP, padx=10, pady=10)
buttons_frame = tk.Frame(pdf_to_txt_frame)
buttons_frame.pack(pady=10)
pdf_to_txt_button = tk.Button(buttons_frame, text="Convert PDF to Text", command=convert_pdf_to_txt)
pdf_to_txt_button.pack(side=tk.LEFT)
pdf_to_txt_button = tk.Button(buttons_frame, text="Convert PDF to Text and filter Headers", command=convert_pdf_to_txt2)
pdf_to_txt_button.pack(side=tk.LEFT, padx=10)
browse_button = tk.Button(buttons_frame, text="Extract Statistical Sentences and Matches from .txt File", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=10)
join_button = tk.Button(buttons_frame, text="Join .txt Files", command=join_txt_files)
join_button.pack(side=tk.LEFT, padx=10)
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
