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
filePath2 = r"sentences_base/sentences_base.csv"

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
            # Fill gaps with empty entries if needed
            for _ in range(oldI, idx - 1):
                sentenceLang.append("")
                sentences.append("")
            sentenceLang.append(ls[1])
            sentences.append(ls[2])
            oldI = idx
print("done sentences.csv")

# --- Read sentences_base.csv ---
oldI = 0
with open(filePath2, 'r', encoding='utf-8') as tempfile:
    for line in tempfile:
        ls = line.strip().split("\t")
        if len(ls) == 2:
            idx = int(ls[0])
            # Fill gaps with 0
            for _ in range(oldI, idx - 1):
                sentenceBases.append(0)
            # Store blank as "" to distinguish from 0
            if ls[1].startswith("\\"):
                sentenceBases.append("")
            else:
                sentenceBases.append(int(ls[1]))  # Keep original value, shift later
            oldI = idx
print("done sentences_base.csv")

# --- Generate pair files ---
for a in langAbbrev2:
    for b in langAbbrev2:
        if a != b:
            a2 = langAbbrev[langAbbrev2.index(a)]
            b2 = langAbbrev[langAbbrev2.index(b)]
            out_file = fr"Tatoeba/{a2}-{b2}.tsv"
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                for i, base in enumerate(sentenceBases):
                    if base == "" or base <= 0:
                        continue  # skip blanks or invalid entries
                    base_index = base - 1  # shift to 0-based here
                    if 0 <= base_index < len(sentenceLang):
                        try:
                            if sentenceLang[base_index] == a and sentenceLang[i] == b:
                                f.write(f"{base_index}\t{sentences[base_index]}\t{i}\t{sentences[i]}\n")
                        except:
                            print(f"i:{i}")
                            print(f"sL:{len(sentenceLang)}")
            print(f"Completed {a}-{b}.txt")
