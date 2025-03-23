
#%%
# 
import bibtexparser
bibtex_file = open("bibtest.bib")
bib = bibtexparser.load(bibtex_file)
# %%

keys = list(bib.entries_dict.keys())

entry = bib.entries_dict[keys[0]]
# %%
entry.author
# %%
