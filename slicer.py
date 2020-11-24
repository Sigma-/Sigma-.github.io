import pandas as pd
df_fossil = pd.read_json(r'Dataset/fossils.json')
df_dino = pd.read_csv(r'Dataset/dinosaurs.csv')

# print(df_fossil.head())
# print(df_dino.head())
# print(df_dino.columns)
# print(df_fossil.columns)

df_dino['first_letter'] = df_dino['dinosaur'].str[:1]

first_letterlist = []
first_letterlist = df_dino['first_letter'].unique()
#first_letterlist_ordered = first_letterlist.sort()

#print(first_letterlist_ordered)
print(first_letterlist)

# # print(first_letterlist_ordered)
# print(first_letterlist)
# # print(df['first_letter'])


# picked_letter = 'a'
# capitalized_letter = picked_letter.upper()
# print(capitalized_letter)
# genom = df_dino.loc[df_dino['first_letter'] == picked_letter]
# genom_list = genom['dinosaur'].unique()

# print(genom_list)
# genom_picked = genom_list[0]
# print("genom_picked")

# def mapping_genome_to_dino(genom_picked):

#     for i in range(0,len(df_fossil)):
#         fossil_entire_name = df_fossil['name'][i]
#         fossil_first_name = df_fossil['name'][i].split()[0].lower()
#         if genom_picked == fossil_first_name:
#             print(fossil_entire_name)


 
# mapping_genome_to_dino(genom_picked)



    # if== df_fossil.loc[df_fossil['name']]
