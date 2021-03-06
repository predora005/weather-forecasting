# coding: utf-8

import os
import pandas as pd
import re
import datetime
from . import name_handle

##################################################
# 指定したディレクトリから
# 指定した拡張子のファイルのリストを取得する
##################################################
def get_file_paths(dir_path, extension=None):
    """ 指定したディレクトリから
        指定した拡張子のファイルのリストを取得する
    
    Args:
        dir_path    (string)            : ディレクトリパス
        extension   (string, optional)  : 拡張子

    Returns:
        list[string] : ファイルパスのリスト
    """
    file_paths = []
    
    # sortedを使用してファイル名の昇順に読み込む
    for filename in sorted(os.listdir(dir_path)):
        
        # ディレクトリの場合はpass
        if os.path.isdir(dir_path + '/' + filename):
            continue
        
        # 拡張子が一致したらリストに追加
        if extension is None:
            # 拡張子の指定無しの場合は無条件に追加
            file_paths.append(dir_path + '/' + filename)
        else:
            base,ext = os.path.splitext(filename)
            if ext == extension:
                file_paths.append(dir_path + '/' + filename)
        
    return file_paths

##################################################
# CSVファイルから地上の気象データを読み込み、
# DataFrameを返す
##################################################
def read_ground(file_path):
    """ CSVファイルから地上の気象データを読み込み、
        DataFrameを返す
    
    Args:
        file_path    (string) : ファイルパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # CSVファイル読み込み
    df = pd.read_csv(file_path, sep=',', skiprows=0, header=[0,1], index_col=0)
    
    # ファイル名から地点名、日付を抽出
    file_name = os.path.basename(file_path)
    elements = name_handle.elements_from_filename_ground(file_name)
    name = elements['name']
    year = elements['year']
    month = elements['month']
    day = elements['day']

    # 日付をDataFrameに追加する
    date = datetime.datetime(year, month, day)
    df[('日付','日付')] = date
    
    # 地点名をDataFrameに追加する
    #df[('地点','地点')] = name
    
    return df

##################################################
# CSVファイルから高層の気象データを読み込み、
# DataFrameを返す
##################################################
def read_highrise(file_path):
    """ CSVファイルから高層の気象データを読み込み、
        DataFrameを返す
    
    Args:
        file_path    (string) : ファイルパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # CSVファイル読み込み
    df = pd.read_csv(file_path, sep=',', skiprows=0, header=[0], index_col=0)
    
    # ファイル名から地点名、日付を抽出
    file_name = os.path.basename(file_path)
    elements = name_handle.elements_from_filename_highrise(file_name)
    name = elements['name']
    year = elements['year']
    month = elements['month']
    day = elements['day']
    hour = elements['hour']

    # 日付をDataFrameに追加する
    date = datetime.datetime(year, month, day)
    df['日付'] = date
    
    # 時刻をDataFrameに追加する
    df['時'] = hour
    
    # 地点名をDataFrameに追加する
    #df['地点'] = name
    
    return df

