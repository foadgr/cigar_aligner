#!/usr/bin/env python

from map import Map
import pandas as pd
import os


class Task(object):
  """
  Class object for cigar task table and test table data processing.

  Parameters
  ----------
  task_type : str, string-like object.
    Valid arguments: include 'main_spec', 'bells_and_whistles', 'tests'
  query_type : str, string-like object.
    Valid arguments: 'single', 'range'
  """
  def __init__(self, task_type, query_type):
    here = os.path.abspath(os.path.dirname(__file__))
    if query_type in ('single', 'range'):
      self.query_type = query_type
    if task_type in ('main_spec', 'bells_and_whistles'):
      self.task_type = task_type
      self.target_dir = os.path.join(here, f'data/{self.task_type}')

  def _get_data(self):
    """
    Retrieve necessary data from relative path specified by task_type arg
    """
    mapping = {
      'delimiter': '\t',
      'header': None
      }

    df1 = pd.read_csv(
        filepath_or_buffer=f'{self.target_dir}/input_01.tsv',
        names=['tr_name', 'chr_name', 'start_site', 'cigar_str'],
        **mapping
      ).set_index('tr_name')

    if self.task_type == 'bells_and_whistles':
      colnames = ['tr_name', 'query', 'end', 'dir', 'inv']
    if self.task_type == 'main_spec':
      colnames = ['tr_name', 'query']
    df2 = pd.read_csv(
        filepath_or_buffer=f'{self.target_dir}/input_02.tsv',
        names=colnames,
        **mapping
      ).set_index(['tr_name', 'query'])

    return df2.join(df1, sort=False).reset_index()

  def run(self, writefile):
    """
    Apply the query alignment function to a well-formated input table
    """
    df = self._get_data()

    if self.task_type == 'main_spec':
      main_func = lambda row: Map(
        row['cigar_str'],
        'F',
        row['start_site'],
        False
      ).align(row['query'])

    elif self.task_type == 'bells_and_whistles':
      if self.query_type == 'single':
        main_func = lambda row: Map(
          cigar_str=row['cigar_str'],
          direction=row['dir'],
          start_site=row['start_site'],
          inverted=row['inv']
        ).align(query=row['query'])

      elif self.query_type == 'range':
        main_func = lambda row: Map(
          cigar_str=row['cigar_str'],
          direction=row['dir'],
          start_site=row['start_site'],
          inverted=row['inv']
        ).map_ranger(
          start=row['query'],
          end=row['end']
        )

    df['output']=df.apply(main_func, axis=1)

    df = df[['tr_name', 'query', 'chr_name', 'output']]

    if writefile is True:
      mapping = {
        'sep': '\t',
        'header': False,
        'index': False
        }
      fname = f'{self.target_dir}/output_{self.query_type}.tsv'
      df.to_csv(fname, **mapping)
      print(f'Output file path: {fname}')
    return list(df.values)

  @classmethod
  def passing_tasks(self, test_name):
    """A function to pass to `test_task.py`"""
    if test_name == 'main_spec':
      df = Task(
        task_type=f'{test_name}',
        query_type='single').run(writefile=False)[0]

    if test_name == 'bells_and_whistles':
      df =  Task(
        task_type=f'{test_name}',
        query_type='single').run(writefile=False)[0]
    return df

if __name__ == "__main__":
  tasks = ['main_spec', 'bells_and_whistles']
  coords = ['single', 'range']

  print(f'Running {tasks[0]}')
  Task(task_type=tasks[0], query_type=coords[0]).run(writefile=True)

  print(f'Running {tasks[1]}. Return {coords[0]} result.')
  Task(task_type=tasks[1], query_type=coords[0]).run(writefile=True)

  print(f'Running {tasks[1]}. Return {coords[1]} result.')
  Task(task_type=tasks[1], query_type=coords[1]).run(writefile=True)







