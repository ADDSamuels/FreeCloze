import os
import sys

# Set working directory to script location
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# Language lists
langAbbrev = ["en", "fr", "de", "it", "es", "pt", "ru", "da", 
              "el", "eo", "fi", "hu", "ko", "lt", "mk", "nl", 
              "pl", "ro", "sr", "sv", "tl", "tr", "uk"]
langAbbrev2 = ["eng", "fra", "deu", "ita", "spa", "por", "rus", "dan",
               "ell", "epo", "fin", "hun", "kor", "lit", "mkd", "nld",
               "pol", "ron", "srp", "swe", "tgl", "tur", "ukr"]

# File paths
filePath = r"sentences/sentences.csv"
filePath2 = r"links/links.csv"

# Storage lists
sentences = []
sentenceLang = []
sentenceBases = []

# --- Read sentences.csv ---
oldI = 0
with open(filePath, 'r', encoding='utf-8') as tempfile:
    for line in tempfile:
        ls = line.strip().split("\t")
        if len(ls) == 3 and ls[1] in langAbbrev2:
            idx = int(ls[0])
            for _ in range(oldI, idx - 1):
                sentenceLang.append("")
                sentences.append("")
                sentenceBases.append([])  # Ensure alignment
            sentenceLang.append(ls[1])
            sentences.append(ls[2])
            sentenceBases.append([])  # initialize empty list for bases
            oldI = idx

print("done sentences.csv")

# --- Read sentences_base.csv (multiple lines per sentence) ---
with open(filePath2, 'r', encoding='utf-8') as tempfile:
    for line in tempfile:
        ls = line.strip().split("\t")
        if len(ls) == 2:
            idx = int(ls[0]) - 1  # convert to 0-based
            base = int(ls[1])
            # Extend list if needed
            while idx >= len(sentenceBases):
                sentenceBases.append([])
            sentenceBases[idx].append(base)
        else:
            print("Malformed line:", ls)

print("done sentences_base.csv")

# --- Generate pair files ---
lang_map = dict(zip(langAbbrev2, langAbbrev))

for a in langAbbrev2:
    for b in langAbbrev2:
        if a != b:  
            out_file = fr"Tatoeba/{lang_map[a]}-{lang_map[b]}.tsv"
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                for i, base_list in enumerate(sentenceBases):
                    for base_index in base_list:
                        base_index -= 1  # shift to 0-based
                        if 0 <= base_index < len(sentenceLang):
                            try:
                                if sentenceLang[base_index] == a and sentenceLang[i] == b:
                                    f.write(f"{base_index}\t{sentences[base_index]}\t{i}\t{sentences[i]}\n")
                            except:
                                print(base_index)
            print(f"Completed {lang_map[a]}-{lang_map[b]}.tsv")
