import pandas as pd
import numpy as np
import os
import re


class TMUADataLoader:

    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.years = self.df['Year'].unique()
        self.papers = self.df['P'].unique()
        self.categories = np.unique(
            np.concatenate([
                self.df.Category.unique(),
                self.df["Sub-Category"].dropna().unique()
            ]))
        self.approaches = self.df['Approach'].dropna().unique()
        self.types = self.df['Type'].dropna().unique()

        # add a column for the "key"
        self.df['key'] = self.df.Year.astype(
            str) + self.df.P + "Q" + self.df.Q.astype(str)
        self.process_df_for_lists()
        self.lists_files = self.df['in_list'].apply(
            lambda x: x if len(x) > 0 else None).dropna().explode().unique()

    def get_filter_options(self):
        return {
            'Years': self.years,
            # 'Papers': self.papers,
            'Categories': self.categories,
            "Lists": self.lists_files,
            'Types': self.types,
            'Approaches': self.approaches,
        }

    def get_all_questions(self):
        return self.df

    def get_filtered_questions(self, filters):
        df = self.df
        paper_mask = df['P'].isin(
            filters['Paper']) if filters['Paper'] else True
        years_mask = df['Year'].isin(
            filters['Years']) if filters['Years'] else True
        categories_mask = (df['Category'].isin(filters['Categories'])
                           | df['Sub-Category'].isin(filters['Categories'])
                           ) if filters['Categories'] else True
        approaches_mask = df['Approach'].isin(
            filters['Approaches']) if filters['Approaches'] else True
        types_mask = df['Type'].isin(
            filters['Types']) if filters['Types'] else True
        lists_mask = df['in_list'].apply(
            lambda x: any([list in x for list in filters['Lists']]
                          )) if filters['Lists'] else True
        mask = paper_mask & years_mask & categories_mask & approaches_mask & types_mask & lists_mask
        if type(mask) != pd.Series:
            return df

        filtered_df = df[mask]

        if len(filters['Lists']) == 1:  # sort by list
            filtered_df['key'] = pd.Categorical(
                filtered_df['key'],
                categories=self.lists[filters['Lists'][0]],
                ordered=True)
            filtered_df = filtered_df.sort_values('key')
            print(filtered_df[['key', 'Year', 'P', 'Q', 'in_list']])
            print(self.lists[filters['Lists'][0]])

        return filtered_df

    def process_df_for_lists(self):
        LIST_PATH = './Lists/'
        list_files = [
            f for f in os.listdir(LIST_PATH)
            if os.path.isfile(os.path.join(LIST_PATH, f))
        ]

        self.lists = {}
        # parse the list files
        for list_file in list_files:
            with open(LIST_PATH + list_file, 'r') as f:
                list_file = list_file.replace(".txt", "")
                self.lists[list_file] = []
                for line in f:
                    if not line.strip():
                        continue
                    string = line.strip().replace(" ", "").replace("\n", "")
                    year, paper, question = parse_question(string)
                    year = year.replace("spec", "specimen")
                    self.lists[list_file].append(year + "P" + paper + "Q" +
                                                 question)

        # process the df
        print(self.lists)
        self.df['in_list'] = [[] for _ in range(len(self.df))]

        for list_name, list in self.lists.items():
            mask = self.df['key'].isin(list)
            self.df.loc[mask, 'in_list'] = self.df.loc[mask, 'in_list'].apply(
                lambda x: x + [list_name])


def parse_question(string):
    pattern = r'(\w+)P(\d+)Q(\d+)'
    match = re.search(pattern, string)

    if match:
        year = match.group(1)
        p = match.group(2)
        q = match.group(3)

        return year, p, q
    else:
        # error
        print(f"Error parsing question {string}")
        return None, None, None
