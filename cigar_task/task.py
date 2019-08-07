#!/usr/bin/env python

from map import Map
import pandas as pd
import os


class Task():
    def __init__(self, task_type):
        here = os.path.abspath(os.path.dirname(__file__))
        if task_type in ('main_spec', 'bells_and_whistles', 'tests'):
            self.target_dir = os.path.join(here, f'data/{task_type}')

    def _get_data(self):
        mapping = {
            'delimiter': '\t', 
            'header': None
            }

        df1 = pd.read_csv(
                filepath_or_buffer=f'{self.target_dir}/input_01.tsv',
                names=['tr_name', 'chr_name', 'start_site', 'cigar_str'],
                **mapping
            ).set_index('tr_name')
        df2 = pd.read_csv(
                filepath_or_buffer=f'{self.target_dir}/input_02.tsv',
                names=['tr_name', 'query'],
                **mapping
            ).set_index(['tr_name', 'query'])
        return df2.join(df1, sort=False).reset_index()

    def run(self):
        df = self._get_data()
        df['output']=df.apply(
                lambda row: Map(
                    cigar_str=row['cigar_str'],
                    direction = 'F',
                    start_site=row['start_site'],
                    inverted=False
                    ).align(query=row['query']), 
                axis=1
                )
        df = df[['tr_name', 'query', 'chr_name', 'output']]

        mapping = {
            'sep': '\t',
            'header': False,
            'index': False
            }
        df.to_csv(f'{self.target_dir}/output_file.tsv', **mapping)
        print(f'Output file path: {self.target_dir}/output_file.tsv')
        return print(df.values)

if __name__ == "__main__":
    Task(task_type='main_spec').run()







