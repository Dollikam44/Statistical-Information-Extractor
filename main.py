import pdfminer.high_level
import pdfminer.layout

import nltk

import os
import re
import csv
from collections import OrderedDict

import tkinter as tk
from tkinter import filedialog



def remove_headers(text):
    # Teile Text von PDF in Zeilen
    lines = text.split('\n')

    # Lösche alle Zeilen die mit Header Nummer anfangen
    filtered_lines = [line for line in lines if not line.startswith(('1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ','1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) and not line.isupper()]
    filtered_text = '\n'.join(filtered_lines)

    return filtered_text


def convert_pdf_to_txt():
    # Wähle ein PDF
    pdf_file_path = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF Files", "*.pdf")])
    # Wenn es Kein Problem mit PDF Path existiert dann
    if pdf_file_path:
        #Wähle Speicherort aus
        txt_save_directory = filedialog.askdirectory(title="Select directory to save .txt file")
        #wenn es kein Problem mit Spicherort un File existiert
        if txt_save_directory:
            #öffne PDF durch ausgewählte Path
            with open(pdf_file_path, 'rb') as file:
                #Extrahiere Text aus PDF mithilfe von pdfminer.high_level Funktion
                pdf_doc = pdfminer.high_level.extract_text(file)

            # lösche Headers mit hilfe von remove_headers Funktion
            # filtered_text = remove_headers(pdf_doc)
            filtered_text = pdf_doc
            #Lösche Extra Abstand zwischen Wörte, Sätze oder Textboxes
            filtered_text = ' '.join(filtered_text.strip().split())
            #Lösche alle Quellen am Ende
            references_pattern = r'References \[1\].*'
            filtered_text = re.sub(references_pattern, 'References [1]', filtered_text, flags=re.DOTALL)
            #lösche alle Nummer von Quellen zwischen Text inhalt alles was so aussieht [1] ..[7] .. [17] usw..
            filtered_text = re.sub(r'\[[0-9]+\]', '', filtered_text)  # Remove numbers between square brackets
            pages = filtered_text.split('\f') # lösche Extra Abstände Nach löschen von Quellen Nummer zwischen Textinhalt

            #Extrahiere die Name von PDF damit wir der selbe Name für .txt File und .csv File später genutzt werden kann
            pdf_file_name = os.path.splitext(os.path.split(pdf_file_path)[-1])[0]
            #erstelle .txt File der selbe Name wie PDF hat
            txt_file_path = os.path.join(txt_save_directory, pdf_file_name + '.txt')
            #öffne .txt File
            with open(txt_file_path, 'w', encoding='utf-8') as file:
                #für jede text in einem PDF Seite
                for i, page in enumerate(pages):
                    #schreibe Inhat von jede PDF Seite in .txt File
                    file.write(page)
            #falls es kein Problem mit PDF in .txt File Konvertierung existiet, schreibe Successfull message
            print(f'Text extracted and saved to {txt_file_path} successfully.')

            #dies With Loop ist für schreiben des Textinhalts von PDF aber Ich nutze das Momentan nicht und das Ergebniss erhalten wir in .txt File
            with open(txt_file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                txt_text.delete(1.0, tk.END)
                #Es wird auf disply Interface geschrieben, ob PDF Problemlos konvertiert ist
                txt_text.insert(tk.END, f'Text extracted and saved to {txt_file_path} successfully.')
                

#die folgende Funktion ist das gleiche wie oben, aber hier werde ich versuchen, mehr als ein PDF für Konvertierung in .txt File auszuwählen
'''
def convert_pdf_to_txt():
    pdf_file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
    if pdf_file_paths:
        # Choose the directory to save the .txt files
        txt_save_directory = filedialog.askdirectory(title="Select directory to save .txt files")
        if txt_save_directory:
            for pdf_file_path in pdf_file_paths:
                with open(pdf_file_path, 'rb') as file:
                    pdf_doc = pdfminer.high_level.extract_text(file)

                filtered_text = pdf_doc
                filtered_text = ' '.join(filtered_text.strip().split())
                references_pattern = r'References \[1\].*'
                filtered_text = re.sub(references_pattern, 'References [1]', filtered_text, flags=re.DOTALL)
                filtered_text = re.sub(r'\[[0-9]+\]', '', filtered_text)  # Remove numbers between square brackets
                pages = filtered_text.split('\f')

                pdf_file_name = os.path.splitext(os.path.split(pdf_file_path)[-1])[0]
                txt_file_path = os.path.join(txt_save_directory, pdf_file_name + '.txt')
                with open(txt_file_path, 'w', encoding='utf-8') as file:
                    for i, page in enumerate(pages):
                        file.write(page)

                print(f'Text extracted and saved to {txt_file_path} successfully.')

            print("All PDF files converted to .txt successfully.")
'''

#lade wichtige nlts (NLP) wichtige Packages
#tokanizieret gegebenen Text in Sätze und Wörter
nltk.download('punkt') #The Punkt tokenizer is a pre-trained unsupervised machine learning model for tokenizing text into sentences and words. It is widely used in natural language processing (NLP) applications.
#damit jede Wort im Text taggiert wird, und das ist wichtig für Sätze Vrestehen, damit die Sätze richtig tokaniesiert werden können
nltk.download('averaged_perceptron_tagger')# POS tagging is the process of labeling each word in a text with its corresponding part of speech (such as noun, verb, adjective, etc.).


#Ektraktion von statistische Informationen aus maschinenlesbaren Text bzw. aus .txt File
def extract_statistical_info(file_path):
    #öffne .txt File, das wir vor her mit hilfe von def convert_pdf_to_txt() erstellt haben
    with open(file_path, 'r', encoding='utf-8') as file:
        #lese text inhalt aus .txt File
        text = file.read()
    #Extrahiere der Name von .txt File, damit wir die NAme später in .CSV File Name nutzen können
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    #tokaniziere Text aus .txt File in Sätze
    sentences = nltk.sent_tokenize(text)#Sentences ist hier eine Liste an Sätze

    # Inintiealisiere Tags Liste, die wichtige statistische Begriffe (Patterns mithilfe von Regex) enthält und klassifiziere diese Patterns unter bestimmten Tags
    #Ich bin noch nicht fertig mit Patterns Ich brache zu mindest 10 Tage
    tags = [
        # p-values
        (r"p\s*(?:[<=>])\s*(0\.(?!\D+)[\d),.;]+|(?!\D+)1(?!\D+)|\.(?!\D+)[\d),.;])\s*", 'p-value'),
        (r'[pP]-?[Vv]alues?.* was .*([Ss]maller|[Bb]igger)\s*.*\s*\d+\.(?!\D+)[\d),.;]+', 'p-value'),
        (r'-*[pP]-?[Vv]alues?.*', 'p-value Context'),
        #corrected p-value
        (r"\s*corr?e?c?t?e?d?\s*\s*[–-]\s* p[–-]?\s*\s*[vV]?a?l?u?e?s?\s*.*", 'corrected p-value'),
        (r"\s*\(?\s*cor\s*-\s*p\s*\)?\s*.*", 'corrected p-value Context'),
        # Bonferroni-Holm
        (r"Bonferroni[–-]?\s*H?o?l?m?", 'Bonferroni-Holm context'),

        # mean
        (r'\(?\s*[mM]ean\s*[=:]\s*([\d.]+)[s%]?\s*\)', 'Mean value'),# entwieder secunde oder prozent oder keiner davon [s%]?
        (r'\(?[Mm]ean\s*[=:]?\s*\b([+-]?\d+(?:\.\d+)?)\b', 'Mean value'),
        (r'([Tt]he\s*|\s*)[mM]ean .* ([Ww]as|of) .*', 'Mean value'),
        (r'\(?[mMµ]\s*[=:]\s*\d+.(?!\D+)[\d),.;]+[s%]?\s*', 'Mean value'),

        # standard deviation
        (r'[Ss]tandard [Dd]eviation\s*.*\s*(of|was set to)', 'Standard Deviation Value'),
        (r'.*([Ss][Tt]?[dD]|σ)\s*[=:]\s*\b(\d+(?:\.\d+)?)\b.*', 'Standard Deviation Value'),
        # (r'[Ss]tandard [Dd]eviation', 'Standard Deviation'),

        # Median
        (r'\(?[mM]edian\s*[:=]?\s*([\d.]+)[s%]?\)', 'Median value'), # entwieder secunde oder prozent oder keiner davon [s%]?
        (r'\(?[Mm]edian\s*[=:]?\s*\b([+-]?\d+(?:\.\d+)?)\b', 'Median value'),

        #Max
        (r'\(?[mM]ax\s*[:=]\s*.*', 'Max value'),
        #Min
        (r'\(?[mM]in\s*[:=]\s*.*', 'Min value'),

        #Odds Ratio Value
        (r'.*\s*[oO]dds?\s*[Rr]atio\s*(of |[=:]?\s*0\.(?!\D+)[\d),.;]+|[=:]?\s*(?!\D+)1(?!\D+)|[=:]?\s*\.(?!\D+)[\d),.;])\s*.*','Odds Ratio Value '),
        (r' [Oo][Rr]\s*[:=]\s*','Odds Ratio Value '),


        # Chi-square test
        (r'Chi[–-]?square [Tt]ests?', 'test name is Chi-square'),

        #Chi-square test
        (r'\(?.*χ\s*2\s*[–-]?.*\)?', 'Test Name is Chi-square test'),
        # Chi-square test Context
        (r'χ\s*2\s*[–-]?[Ss]cores?', 'Chi-square test Context'),
        # Chi-square Value
        (r'.* \(?χ\s*2\s*(\(.*\)\s*|\s*)[:=]\s*', 'Chi-square Value'),

        # t-test
        (r'[Tt]-[Tt]ests?', 'test name is t-test'),


        # ANOVA Test
        (r'.*\s*ANOVA\s*,?\s*.*', 'test name is ANOVA Test'),
        # ANOVA Test
        (r'.*\(?\s*[Ff]\s*\(\s*\d+\s*,\s*\d+\s*\)\s*=\s*', 'Test statistic Value'),

        # Correlation Context
        (r'[Cc]orrelation\s*.*\s*between', 'Correlation Context'),

        # Pearson Correlation Context
        (r'Pearson’s r', 'Pearson Correlation Context'),
        #Pearson r Value
        (r'\(?\s*r\s*=\s*([+-]?1|[–-]?\s*0\.(?!\D+)[\d),.;]+|[–-]?0\.\.(?!\D+)[\d),.;]+)\s*', 'Pearson r Value'),
        # Pearson Correlation Coefficient
        (r'[Pp]?e?a?r?s?o?n?’?s?-?r?—?\(?r\s*[:=<>]\s*([+-]?1|−\s*0\.(?!\D+)[\d),.;]+|0\.\.(?!\D+)[\d),.;]+)\s*',
         'Pearson Correlation Coefficient Value'),
        (r'\(?ρ\s*[:=><]\s*\s*(0\.(?!\D+)[\d),.;]+|(?!\D+)[+-]?1(?!\D+)|\.(?!\D+)[\d),.;])\s*',
         'Correlation Coefficient Value'),

        # Wilcoxon signed-rank Test
        (r'.*\s*[wW]ilcoxon [Ss]igned[–-]?\s*[Rr]ank[–-]?\s*[tT]ests?', 'Test Name is Wilcoxon signed-rank Test'),
        # Wilcoxon signed-rank Test statistic V
        (r'.*\s*[wW]ilcoxon [Ss]igned[–-]?\s*[Rr]ank\s*.*[vV]\s*[:=]\s*.*', 'Test statistic V Value'),

        # Wilcoxon Rrank-Sum Test
        (r'.*\s*[wW]ilcoxon[–-]?\s*[Rr]ank[–-]?\s*[Ss]um[–-]?\s*[tT]ests?', 'Test Name is Wilcoxon Rrank-Sum Test'),
        (r'.*\s*[wW]ilcoxon[–-]?\s*[mM]ann[–-]?\s*[wW]hitney', 'Test Name is Wilcoxon Rrank-Sum Test'),
        (r'.*\s*[wW]ilcoxon\s*[rR]ank\s*[Ss]um\s*.*', 'Test Name is Wilcoxon Rrank-Sum Test'),
        # Wilcoxon Rrank-Sum Test statistic W Value
        (r'[Ww]\s*[:=]\s*.*', 'Test statistic W Value'),

        #Wilcoxon Test
        (r'.*\s*[wW]ilcoxon [Tt]ests?\s*.*', 'Test Name is Wilcoxon Test'),


        # Post-hoc Test
        (r'.*\s*[pP]ost[–-]?[Hh]oc[–-]?\s*[tT]ests?\s*.*', 'Post-hoc Test'),

        # Fisher's Exact test
        (r'[fF]isher’?\s*s [Ee]xact [Tt]ests?\s*,?.?', 'Test Name is Fisher’s Exact test'),
        # Fisher’s Exact Test Context
        (r' \(?[fF][Ee][Tt]:? ', 'Fisher’s Exact Test Context'),

        #Kruskal-Wallis Test
        (r'-*[kK]ruskal-?\s*[wW]allis\s*.*', 'Test Name is Kruskal-Wallis Test'),

        # Effect Size (Cramer's V)
        (r"Cramer’s [vV]", "Effect Size (Cramer’s V)"),
        # Effect Size
        (r"(small|low|large|medium|big)\s*.*\s*[Ee]ffect [Ss]ize", "Effect Size Value"),
        (r".*\s*[Ee]ffect [Ss]ize of", "Effect Size Value"),
        (r".*\s*[Ee]ffect [Ss]ize\s*", "Effect Size Context"),

        # Cohen’s Kappa
        (r'.*\s*κ\s*[<=>:]\s*(-1|1|−\s*0\.(?!\D+)[\d),.;]+|0\.(?!\D+)[\d),.;]+)', 'Cohen’s Kappa Value'),
        (r'[cC]ohen’?\s*s\s* [kK]appa.*\(?\s*κ\s*\)?.*', 'Cohen’s Kappa Contect'),


        #α Context and value
        (r'\s*\u03B1', ' α Context'),
        (r'.*\s*\u03B1\s*(of |[<=>:]?\s*0\.(?!\D+)[\d),.;]+|[=:]?\s*(?!\D+)1(?!\D+)|[=:]?\s*\.(?!\D+)[\d),.;])\s*.*', ' α Value'),
        (r'.*\s*[cC]ronbach’?[Ss]?\s* [aA]lpha', 'Cronbach’s Alpha Context'),
        (r'.*\s*[aA]lpha\s*.* of .*', 'Alpha Value'),

        # marginal R-squared
        (r'.* R\s*2 .*', ' marginal R-squared'),
        # marginal R-squared
        (r'.* R\s*2\s*[:=]\s*.*', ' marginal R-squared Value'),

        #Number of Participants
        #(r'.*[nN]\s*[=:<>]\s*', 'Number of Participants'),

        #Degree of freedom
        (r'.* \(?[dD]\s*[Ff]\s*[=:<>]\s*', 'Degree of freedom'),

        # Statistically Difference context
        (r"[sS]tatisticall?y? [Dd]ifferen[tc]e?", "Statistically Difference context"),
        # Statistically significant context
        (r"[sS]tatisticall?y? ([Ss]igni(fi|ﬁ)cant|[Ss]igni(fi|ﬁ)cance)", "Statistically Significant context"),

        #Significant Difference context
        (r"[sS]igni(fi|ﬁ)cant [dD]ifference", "Significant Difference context"),

        # logistic Regression
        (r".*([Ll]og [Rr]atio|Logistic Regression).*", "Logistic Regression Context"),
        #Regression coefficient Context
        (r".* [rR]egression [Cc]oefficients?.*", "Regression coefficient Context"),


        # Comparing results
        (r".*\s*[rR]esults\s*.*\s*(faster|smaller|bigger|slower)", "Comparing Results "),
        (r".*[oO]n [Aa]verage\s*.*\s*(faster|smaller|bigger|slower)\s*.*than\s*.*", "Comparing Results "),
        (r".*\s*[Cc]omparing .* [Rr]esults?\s*.*", "Comparing Results "),

        #System Usability score
        (r"(SUS|sus) [sS]core", "context about System Usability score"),

        # Total Variation Distance
        (r'([tT]otal [vV]ariation [dD]istances?|\(?TVD\)?)', 'Total Variation Distance Context'),
        # Total Variation Distance Value
        (r'TV\s*Ds?\(.*,.*\)\s*=\s*.*', 'Total Variation Distance Value'),
        (r'TV\s*Ds?\ of ', 'Total Variation Distance Value'),

        #Confidence Interval
        (r'.*[Cc]on(fi|ﬁ)dence [iI]ntervals?', 'Confidence Interval Context'),
        #Confidence Interval Value
        (r'.*[Cc]\.?[Ii]\s*=\s*\[.*,.*\].?', 'Confidence Interval Value'),


    ]

    # initialisiere ordentliche Dictionary, damit die extrahierte statistische Sätze ordentlich wie PDF ReihenFolge gespeichert wird
    results_dict = OrderedDict()
    #Hier startet die Algo von Extraktion
    #für erste Satz bis letzte Satz in Sätzeliste
    for sentence in sentences:
        #initialisiere Liste für gefundene Patterns in einem Satz, weil es sein könnte, dass in einem Satz mehr als einem Pattren existiert
        tags_found = []
        #schleife durch alle taggierte patterns (bzw. taggierte statistische wichtige Begriffe), die in Tags Liste sind
        for pattern, tag in tags:
            #wenn ein Pattern in einem Satz existiert
            if re.search(pattern, sentence):
                #addiere gefundene Pattern ind Tags_found liste für diese Satz
                tags_found.append(tag)
        #wenn in einem Satz ein oder mehr als ein patterb existiert
        if tags_found:
            #gebe in result von Tag liste alle gefundene Pattern in diese Satz durch (,) gespltitet sind
            results_dict[sentence] = ", ".join(tags_found)
    #konvertiere die ordentliche Dictionary in eine Liste von (sentence,Tag)
    results = [(k, v) for k, v in results_dict.items()]

    #Suche Nach Speicherort für die .csv Tabelle
    csv_save_directory = filedialog.askdirectory(title="Select directory to save .csv file")
    #wenn es kein Problem mit Speicherort existiert
    if csv_save_directory:
        #Initialisiere .csv File, das gleiche Name wie .txt bzw .pdf File hat
        output_file_path = os.path.join(csv_save_directory, f"{file_name}_results.csv")
        #öffne .csv File
        with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
            #Initialiesiere .csv File für schreiben
            writer = csv.writer(file)
            writer.writerow(['Sentence', 'Tag'])
            # Schleife, damit alle Sätze die statistische Patterns enthalten, in .csv File geschrieben werden
            for result in results:
                writer.writerow(result)
        #wenn es keine Probleme geben, dann schreibe Successfull message
        print(f'Statistical information extracted and saved to {output_file_path} successfully.')
        return output_file_path


#In diesem Part geht es um Statistical Values Extraktion
#Das Idee ist hier, dass wie die Values (Zahlen) aus vorherige extrahierte Sätze extrahieren werden, die die meisten Zahlen (mehr als 90% aus Zahlen) statistische Values besitzen


#Input ist hier eine Zeile  in .csv (Satz) und Patterns Liste
def extract_decimal_numbers_with_context(sentence, patterns):
    #Initialisiere eine Liste für die Statistical Values
    decimal_numbers_with_context = []
    #Schleife für jede Pattern in Liste von Patterns
    for pattern in patterns:
        #suche ob es ein Match zwischen Paterrn und santance extstiert
        matches = re.findall(pattern, sentence, re.IGNORECASE)
        #diese For schleife für jede Match in Matches Liste (Match ist hier, die Extrahierte Value aus einem Satz)
        for match in matches:
            #für contxt vor oder Nach dem Match (Zahl oder Value) und Strip ist hier für Löschen von Extra Abstand, Falls ein Extra Abstand noch existiert
            context = match[0].strip()
            #die Zahl bzw. Statistische Value
            number = match[1]
            #Combiniere Context und Number zusammen
            combined = f"{context} {number}"  # Combine context and number
            #füge die gefundene Match (Context und Number) in  decimal_numbers_with_context Liste
            decimal_numbers_with_context.append(combined)
    #Ausgebe
    return decimal_numbers_with_context


def process_csv_file(input_file):
    #Initialisiere Patterns Liste für Extraktion der Zahlen in Statistische Sätze in .csv File
    decimal_patterns = [
        #r'(\b(?:\w+\W+){0,4})\b(\d+\.\d+)\b',
        #r'(\b(?:\w+\W+){0,3})\b([+-]?\d+(?:\.\d+)?)\b',
        r'(\b(?:\w+\W+){0,3})\b([+-]?\d+(?:\.\d+)?)\b',

        #r'\.\d{2,}\b',
        #r"p\s*(?:[<=>])\s*(0\.(?!\D+)[\d),.;]+|(?!\D+)1(?!\D+)|\.(?!\D+)[\d),.;])\s*",
        #r"(?:\b\w+\b\s+){2}([+-]?\d+(?:\.\d+)?|\.\d+)(?:\b|e[+-]?\d+)",

    ]
    #öffne .csv File und Initialisiere die Zeilen der .CSV Tablle als Liste von Sätze
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    header = rows[0]
    #Adiere neue Spalte (Statistical Values in Zeile 0 Spalte 3)
    #header.append('Combined Context and Decimal')
    header.append('Statistical Values')

    #For schleife geht durch alle Zeilen bzw geht durch alle Sätze in Sentences Spalte
    for row in rows[1:]:
        sentence = row[0]
        #Rufe extracted_decimal_numbers Function für jede Zeiel bzw für jede Satz in .csv File und Suche, ob es Match oder mehr als eines Match in einem Satz esistiert und füge alle gefundene Matches in Liste
        extracted_decimal_numbers = extract_decimal_numbers_with_context(sentence, decimal_patterns)
        #Wenn es keine Probleme beim Patterns und gefundene Matches existieren
        if extracted_decimal_numbers:
            #füge alle gefundene Values unter statistical Values und die sind durch , getreent
            combined_values = ', '.join(extracted_decimal_numbers)  # Join multiple values with comma separator
            row.append(combined_values)
        else:
            #sonst füge leerzeichen
            row.append('')
    #öffne .csv file und mache Update bzw füge die neue statistical Values Spalte
    with open(input_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)



def browse_file():
    #wähle .txt File für statistical Inforamtio Extraktion
    file_path = filedialog.askopenfilename()
    #Wenn es Keine Probleme beim Path geben
    if file_path:
        #lösche alle alte Informationen in Display Window falls was existiert
        txt_text.delete(1.0, tk.END)
        results_text.delete(1.0, tk.END)
        txt_text.insert(tk.END, f"Processing file: {file_path}\n\n")
        txt_text.update_idletasks()

        # Extract statistical information (Statischtische Sätze) from .txt file
        results_file_path = extract_statistical_info(file_path)
        txt_text.insert(tk.END, f"Statistical information extracted. Results saved to: {results_file_path}\n\n")
        txt_text.update_idletasks()

        #für Extraktion an statistical Values mit context aus statistical Sätze
        process_csv_file(results_file_path)
        txt_text.insert(tk.END, f"Statistical Values extracted and saved to the CSV file.\n\n")
        txt_text.update_idletasks()

        #lese alle extrahierte statistical Sentences und Values aus bearbeitete .csv File und schreibe das in Display Window
        with open(results_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            rows = []
            for row in csv_reader:
                sentence = row['Sentence']
                tag = row['Tag']
                combined_value = row['Statistical Values']

                rows.append(f"Sentence: {sentence}\nTag: {tag}\nStatistical Values: {combined_value}\n\n")

            results_text.config(state=tk.NORMAL)
            results_text.delete(1.0, tk.END)
            #in Display Window wurde alle Extrahierte Infos Horizontal geschrieben
            results_text.insert(tk.END, "".join(rows))
            results_text.config(state=tk.DISABLED)

#UI
root = tk.Tk()
root.title("PDF to Txt Converter and Statistical Information Extractor")
pdf_to_txt_frame = tk.Frame(root)
pdf_to_txt_frame.pack(side=tk.TOP, padx=10, pady=10)
buttons_frame = tk.Frame(pdf_to_txt_frame)
buttons_frame.pack(pady=10)
pdf_to_txt_button = tk.Button(buttons_frame, text="Select PDF", command=convert_pdf_to_txt)
pdf_to_txt_button.pack(side=tk.LEFT)
browse_button = tk.Button(buttons_frame, text="Select .txt File", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=20)
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
results_frame.pack(side=tk.RIGHT, padx=20,pady=10, fill=tk.BOTH, expand=True)
results_label = tk.Label(results_frame, text="Extracted Statistical Information")
results_label.pack()
results_text = tk.Text(results_frame, state=tk.DISABLED, height=50, width=105)
results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
results_scroll = tk.Scrollbar(results_frame)
results_scroll.pack(side=tk.RIGHT, fill=tk.Y)
results_text.config(yscrollcommand=results_scroll.set)
results_scroll.config(command=results_text.yview)
root.mainloop()
