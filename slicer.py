import pandas as pd


def get_dictionary(df_dino):
    first_letter = df_dino['dinosaur'].str[:1]

    first_letterlist = []
    first_letterlist = first_letter.unique()

    slicer_dictionary = {}
    keys = range(len(first_letterlist))

    for i in keys:
        slicer_dictionary[i] = first_letterlist[i]
    
    return slicer_dictionary

def show_genoms(selected_letter, df_dino):
    return [dinoname for dinoname in df_dino['dinosaur'] if dinoname[:1] == selected_letter]

    
#genom_picked = genom_list[0]



def mapping_genome_to_dino(genom_picked):
    df_fossil = pd.read_json(r'Dataset/fossils.json')
    
    
    return df_fossil.loc[df_fossil['name'].str.startswith(genom_picked.capitalize())]

 
#mapping_genome_to_dino(genom_picked)