
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
    # Teile Text in Zeilen
    lines = text.split('\n')

    # Lösche alle Zeilen die mit Header Nummer anfangen
    filtered_lines = [line for line in lines if not line.startswith(('1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ','1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) and not line.isupper()]
    filtered_text = '\n'.join(filtered_lines)

    return filtered_text


def convert_pdf_to_txt():
    #Wähle ein PDF
    pdf_file_path = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF Files", "*.pdf")])
    #Wenn es Kein Problem mit PDF Path existiert dann
    if pdf_file_path:
        #öffne PDF durch Path
        with open(pdf_file_path, 'rb') as file:
            #Extrahiere Text aus PDF mithilfe von pdfminer high_level.extract_text
            pdf_doc = pdfminer.high_level.extract_text(file)

        #lösche Headers mit hilfe von remove_headers Funktion
        filtered_text = remove_headers(pdf_doc)

        #ordene Extrahierte Texte in Ihre Seite
        pages = filtered_text.split('\f')
        #Extrahiere PDF-Name aus dem PDF Path, weil wir die gleiche Name Später für .txt File und .csv File genutzt wird
        pdf_file_name = os.path.splitext(os.path.split(pdf_file_path)[-1])[0]
        #erstelle .txt File der gleiche name wie PDF hat
        txt_file_name = pdf_file_name + '.txt'
        #öffne die erstellte .txt File
        with open(txt_file_name, 'w', encoding='utf-8') as file:
            #für jede Seite in Liste von PDF Seiten
            for i, page in enumerate(pages):
                #Counter für Page Numbers
                page_num = i + 1
                #Lösche Extra Space zwischen Wörter, Sätze und Textboxen
                page = ' '.join(page.strip().split())
                #schreibe die Ergebniss in .txt File
                file.write(f'Page {page_num}:\n{page}\n\n')
        print(f'Text extracted and saved to {txt_file_name} successfully.')
        #heir ist für display Inhalt von .txt File in User Interface
        with open(txt_file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            #alles was in Display Box vorher geschrieben ist, wird gelöschet und stattdessen die neue TextInhalt von ausgewählte PDF geschrieben wird
            txt_text.delete(1.0, tk.END)
            txt_text.insert(tk.END, text)


#lade wichtige nlts (NLP) wichtige Packages
#tokanizieret gegebenen Text in Sätze und Wörter
nltk.download('punkt') #The Punkt tokenizer is a pre-trained unsupervised machine learning model for tokenizing text into sentences and words. It is widely used in natural language processing (NLP) applications.
#damit jede Wort im Text taggiert wird, und das ist wichtig für Sätze Vrestehen, damit die Sätze richtig tokaniesiert werden können
nltk.download('averaged_perceptron_tagger')# POS tagging is the process of labeling each word in a text with its corresponding part of speech (such as noun, verb, adjective, etc.).


#Ektraktion von statistische Informationen aus maschinenlesbaren Text bzw. aus .txt File
def extract_statistical_info(file_path):#input .txt File
    #öffne .txt File, das wir vor her mit hilfe von def convert_pdf_to_txt() erstellt haben
    with open(file_path, 'r', encoding='utf-8') as file:
        #lese text inhalt aus .txt File
        text = file.read()
    #Extrahiere der Name von .txt File, damit wir die NAme später in .CSV File Name nutzen können
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    #tokaniziere Text aus .txt File in Sätze
    sentences = nltk.sent_tokenize(text)#Sentences ist hier eine Liste an Sätze

    #Inintiealisiere Tags Liste, die wichtige statistische Begriffe (Patterns mit hilfe von Regex) enthält und manuell taggiert

    tags = [
        # Chi-square test
        (r'[cC]hi-?[sS]quare', 'Chi-square test'),
        # [sS] entwieder große S oder kleine s  ### -? enwieder existiert Charakter - oder nicht
        (r'(χ2.*|χ2 test|χ\s*2)', 'Chi-square test'),

        # Wilcoxon-Rank-Sum Test
        (r'([Ww]ilcoxon-?[Rr]ank.*|[wW]ilcoxon [rR]ank [sS]um.*|[Mm]ann\s*-?[wW]hitney.*|[Uu]-[Tt]est.*)',
         'Wilcoxon-Rank-Sum Test'),
        (r'[Ww]ilcoxon-?[Mm]ann.*', 'Wilcoxon-Rank-Sum Test'),
        # p-value for Wilcoxon-Rank-Sum Test
        (r'MW\s*=\s*\d+\.\d+', 'p-value for Wilcoxon-Rank-Sum Test'),

        # Wilcoxon Test
        (r'[Ww]ilcoxon-?.*[Tt]est', 'Wilcoxon Test'),

        # t-test
        (r'[Tt]-[Tt]ests? .*', 't-test'),

        # Fisher’s exact test
        (r'[fF]isher’?s? [Ee]xact.*', 'Fisher’s exact test'),
        (r'\(?\s*?FET\s*:\s*? .*', 'Fisher’s exact test'),

        # Wilcoxon signed-rank test
        (r'([Ww]ilcoxon [Ss]igned-?[Rr]ank|[Ss]igned-?[Rr]ank|[Ww]ilcoxon [Ss]igned.* [Rr]ank) ',
         'Wilcoxon signed-rank test'),

        # ANOVA Test
        (r'[aA][nN][oO][vV][aA].*', 'ANOVA Test'),

        # Pearson Correlation
        (r'([Pp]earson’?s? [Cc]orrelation|[Pp]earson’?s?-?r?.*)', 'Pearson Correlation'),

        # Correlation coefficient
        (r'([cC]orrelation [Cc]oefficient\s*.*r\s*=\s*(\.?\d+|\d+(\.\d+)?).*)', 'Correlation coefficient'),
        (r'[cC]orrelation.* \(\s*r\s*\(\d+(\.\d+)?\)\s*=\s*(\.?\d+|\d+(\.\d+)?).*', 'Correlation coefficient'),
        (r'[cC]orrelation [Cc]oeffi-?\s*cients?\s* .* (\.?\d+|\d+(\.\d+)?).*', 'Correlation coefficient'),

        # Friedman test
        (r'[fF]riedman-?\s*[Tt]est.*', 'Friedman test'),

        # Kruskal Wallis test
        (r'[kK]ruskal-?[wW]allis.*', 'Kruskal Wallis Test'),

        # Shapiro-Wilks test
        (r'[sS]hapiro-?\s*[wW]ilks.*', 'Shapiro-Wilks test'),

        # Cramer's V
        (r'[Cc]ramer’?s [Vv]', 'Cramer’s V'),  # ? bedeutet es kann sein dass ’ existiert oder nicht existiert

        # Effect Size
        (r'((large|low|medium|small|big|signigicant|unsignificant) [eE]ffect [sS]ize|(large|low|medium|small|big|signigicant|unsignificant) [eE]ffect [sS]ize.*r\s*=−?\s*\d+(\.\d+)?)','Effect Size'),  # large or low or medium or small ...Effect size
        (r' [Rr]eporte?d? .* [eE]ffect [sS]ize .* [Cc]ramer’?s [Vv]', 'Effect Size'),
        (r'[eE]ffect [sS]ize of \d+(\.\d+)?', 'Effect Size'),
        (r'[eE]ffect [sS]ize', 'Effect Size'),

        # Regression Model
        (r'regression model.* \(F\(\d+,\d+\)\s*=\s*\d+\.\d+\)', 'Regression Model'),

        # Bernoulli Trial
        (r'(Bernoulli Trial|B\s*=\s*\d+\.\d+)', 'Bernoulli Trial'),

        # statistical different
        (r'[Hh]ad.*[Ss]tatistically [Dd]ifferent.*[Ff]rom', 'statistical different'),
        # .* bedeutet, dass alle mögliche Buchstaben und Wörter zwischen zwei bestimmte Wörter existieren

        # Standard deviation
        (r'[sS]tan-?dard [dD]eviation (of|was set to) \d+(\.\d+)?', 'Standard deviation'),
        # \d+(\.\d+)? bedeutet alle Zahlen Typen
        (r'(.*[Ss][tT]?[dD]\s*[:=]\s*\d+(\.\d+)?|\u03C3\\s*[:=]\s*\d+(\.\d+)?)', 'Standard deviation'),  # alle Zahlen Typen
        (r'([sS]tandard [dD]eviation of |.*SD ?[:=] ?)\d+(\.\d+)? \d+(\.\d+)?|\(?[sS]tandard [dD]eviation.*\)?|σ\s*=\s*\d+(\.\d+)?',
        'Standard deviation'),  # alle Zahlen Typen



        # Total Variation Distance
        (r'([tT]otal [vV]ariation [dD]istance|(TVDs?)|TV\s*D(.*,.*)\s*=\s*.*)', 'Total Variation Distance'),

        # Mean
        (r'.*[Mm]ean\s* .*\s*(was|of|=)\s*\d+(\.\d+)?.*', 'Mean'),

        # Median
        (r'.*\s*[Mm]edian\s*=\s*\d+(\.\d+)?.*', 'Median'),

        # Odd ratio
        (r'.*([Oo]dds? [Rr]atios?|[Oo]dd[Rr]atios*\s*=\s*\d+(\.\d+)?|[Oo]dds [Rr]atios*\s*=\s*\d+(\.\d+)?).*',
         'Odd ratio'),
        #logistic regression
        (r'.*\s*log odds\s*.*','Logistic Regression'),

        # Sample Number
        # (r'\d [pP]articipants?', 'Sample Number'),

        # marginal R-squared
        (r'.* R2 .*', ' marginal R-squared'),

        # Alpha
        (r'\u03b1\s*=\s*\d+(\.\d+)?.*', 'Alpha'),

        # degree of freedom
        (r'.* df .*', ' degree of freedom'),

        # Cohens’ Kappa
        (r'([Aa]greement,? .*|.*) [Cc]ohen’?s? [kK]appa.*', 'Cohens’ Kappa'),
        (r'[Aa]greement .*[of|was] [Kkκ] ?= ?\d+(\.\d+)?', 'Cohens’ Kappa'),
        (r'[Cc]oefficient [kK]appa of', 'Cohens’ Kappa'),
        (r'[Kkκ] ?= ?\d+(\.\d+)?', 'Cohens’ Kappa'),

        # p-value
        (r'.*p [>=<] (\d+(\.\d+)?.*|.\d+.*)', 'p-value'),
        (r'.*p[>=<]\d+(\.\d+)?', 'p-value'),
        (r'[Pp]-?[vV]alue .* (of|was|<|>|=) .* \d+(\.\d+)?', 'p-value'),
        (r'.*p[>=<]\.?\d+', 'p-value'),
        (r'.*p [>=<]\.?\d+.*', 'p-value'),
        (r'.*[Pp]-?[Vv]alues?', 'p-value'),
        (r'.*\s*ρ\s*=\s*\d+(\.\d+)?\s*.*', 'p-value'),

        # Corrected p-value
        (r'([Bb]onferroni[–-]?[Hh]olm.*|[Bb]onferroni.*)', 'Corrected p-value'),
        (r'(cor - p-value|corrected - p-value|cor - p|corrected p=.*)', 'Corrected p-value'),

        #Confidence Interval
        (r'(\d+%\s*.*\s*con[ﬁf]i?dence interval|\d+(?:\.\d+)?%\s*.*\s*con[ﬁf]i?dence interval)', 'Confidence Interval'),


        # statistically signiﬁcant difference.
        (r'(([sS]tatistically | )[Ss]igni(fi|ﬁ)cant [Dd]ifferences?.*|[wWas] [Ss]igni(fi|ﬁ)cantly ([Hh]igher|[Ll]ower|[Bb]igger|[Ss]maller))','significant difference'),
        # statistically signiﬁcant correlation.
        (r'[sS]tatistically [Ss]igni(fi|ﬁ)cant [Cc]orrelations?.*', 'significant corellation'),
        # statistically signiﬁcant.
        (r'[sS]ta-?tistically [Ss]igni(fi|ﬁ)cant.*', 'statistically significant'),

        # Comparing Results
        (
        r'(([Tt]hese|[tT]he) [Rr]esults?|[wW]e [fF]ound) .* [Oo]n [Aa]verage \d+(\.\d+)?% ([fF]aste?r?|[Ss]lowe?r?) [tT]han',
        'Comparing Result'),
        (r'[Rr]atings? .* ([Tt]end|[Tt]end to be) ([Ll]owe?r?|[Hh]ighe?r?) then', 'Comparing Results'),
        (r'[Ww]e [Ff]ound .*m?o?r?e?\s*[sS]ignificant?l?y? more', 'Comparing Results'),

        # Cornbach's alpha
        (r'.*([cC]ronbach’?s? [aA]lpha|[cC]ronbach’?s?).* .*\u03b1\s*=? ', 'Cronbach’s alpha'),

        (r'f\s*\(.*\)\s*<\s*f\s*\(.*\)', '   '),
        # acceptance criteria
        (r'[Aa]cceptance [Cc]riteria of \d+\.\d+', 'acceptance criteria'),

    ]
    #initialisiere ordentliche Dictionary, damit die extrahierte statistische Sätze ordentlich wie PDF ReihenFolge gespeichert wird
    results_dict = OrderedDict()
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
            results_dict[sentence] = ", ".join(tags_found)# join all found Tages together
    #konvertiere die ordentliche Dictionary in eine Liste von (sentence,Tag)
    results = [(k, v) for k, v in results_dict.items()]


    # initialisiere .csv File, das gleiche Name wie .txt bzw .pdf File hat
    output_file_path = os.path.join(os.path.dirname(file_path), f"{file_name}_results.csv")
    #offnie die initialisierte .csv File
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
        #initialiesiere csv File für schreibel
        writer = csv.writer(file)
        writer.writerow(['Sentence', 'Tag'])
        #Schleife, damit alle Sätze die statistische Patterns enthalten, in .csv File geschrieben werden
        for result in results:
            writer.writerow(result)

    return results
#öffne .txt File
def browse_file():
    # öffne .txt File
    file_path = filedialog.askopenfilename()
    #wenn kein Problem mit .txt File existiert
    if file_path:
        #extract statistical Informationen aus ausgewählte .txt File
        results = extract_statistical_info(file_path)
        #lösche was in Extracted statistical Information Window existiret, falls vorher genutzt wurde
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)
        #schreibe all gefundene statistische Results in Extracted statistical Information Window
        for result in results:
            results_text.insert(tk.END, f"{result[0]}\nTag: {result[1]}\n\n")
        results_text.config(state=tk.DISABLED)


#erstelle root window für GUI (Graphical user Interface)
root = tk.Tk()
#Name von Interface PDF to Txt Converter and Statistical Information Extractor
root.title("PDF to Txt Converter and Statistical Information Extractor")

#erstelle Frame für PDF to 
pdf_to_txt_frame = tk.Frame(root)
pdf_to_txt_frame.pack(side=tk.TOP, padx=10, pady=10)

#pdf_to_txt_label = tk.Label(pdf_to_txt_frame, text="PDF to TXT Converter")
#pdf_to_txt_label.pack()

buttons_frame = tk.Frame(pdf_to_txt_frame)
buttons_frame.pack(pady=10)

pdf_to_txt_button = tk.Button(buttons_frame, text="Select PDF", command=convert_pdf_to_txt)
pdf_to_txt_button.pack(side=tk.LEFT)

browse_button = tk.Button(buttons_frame, text="Select .txt File", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=20)

txt_frame = tk.Frame(root)
txt_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

txt_label = tk.Label(txt_frame, text="Extracted Text from PDF")
txt_label.pack()

txt_scroll = tk.Scrollbar(txt_frame)
txt_scroll.pack(side=tk.RIGHT, fill=tk.Y)

txt_text = tk.Text(txt_frame, yscrollcommand=txt_scroll.set, height=50, width=60)
txt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

txt_scroll.config(command=txt_text.yview)

results_frame = tk.Frame(root)
results_frame.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.BOTH, expand=True)

results_label = tk.Label(results_frame, text="Extracted Statistical Information")
results_label.pack()

results_text = tk.Text(results_frame, state=tk.DISABLED, height=50, width=75)
results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

results_scroll = tk.Scrollbar(results_frame)
results_scroll.pack(side=tk.RIGHT, fill=tk.Y)

results_text.config(yscrollcommand=results_scroll.set)
results_scroll.config(command=results_text.yview)

root.mainloop()
