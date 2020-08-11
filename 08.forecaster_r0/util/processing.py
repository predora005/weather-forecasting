# coding: utf-8

import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

##################################################
# Max-Minスケール化(0〜1の範囲に収まるように標準化)
##################################################
def max_min_scale(train_data, test_data=None):
    
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_data)
    
    if test_data is not None:
        test_scaled  = scaler.transform(test_data)
    else:
        test_scaled = None
    
    return scaler, train_scaled, test_scaled
    
##################################################
# 標準化(平均0, 分散1になるように変換)
##################################################
def standardize(train_data, test_data=None):
    
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_data)
    
    if test_data is not None:
        test_scaled  = scaler.transform(test_data)
    else:
        test_scaled = None
    
    return scaler, train_scaled, test_scaled
    
##################################################
# NaNを平均値で置換する
##################################################
def fill_na_avg(df, inplace=True):
    """ NaNを平均値で置換する

    Args:
        df(DataFrame) : 変換対象のDataFrame
        inplace(bool) : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 変換する列と値のディクショナリを作成する
    fillna_dict = {}
    has_nan_columns = new_df.isnull().any()
    for col in has_nan_columns.index:
        
        # NaNが含まれる列のみ変換対象とする
        has_nan = has_nan_columns[col]
        if has_nan:
            
            typ = new_df[col].dtype
            if (typ == np.float32) or (typ == np.float64) :
                # データ型がfloatの場合は平均値で変換する
                avg = new_df[col].mean()
                fillna_dict[col] = avg
            elif (typ == np.int32) or (typ ==  np.int64) :
                # データ型がintの場合は平均値に最も近い整数値で変換する
                avg = new_df[col].mean()
                fillna_dict[col] = int(np.around(avg))
            
    # NaNを置換する
    new_df = new_df.fillna(fillna_dict)
    
    return new_df
    
##################################################
# 浮動小数点を32ビットに変更する
##################################################
def type_to_float32(df, inplace=True):
    """ 浮動小数点を32ビットに変更する

    Args:
        df(DataFrame) : 変換対象のDataFrame
        inplace(bool) : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 変換する列と型のディクショナリを作成する
    astype_dict = {}
    for col in new_df.columns:
        typ = new_df[col].dtype
        if typ == object:
            # object -> np.float32
            astype_dict[col] = np.float32
        elif typ == np.float64:
            # np.float64 -> np.float32
            astype_dict[col] = np.float32
    
    # データ型を変換する
    new_df = new_df.astype(astype_dict, copy=False)
    
    return new_df
    
##################################################
# 時間変化量をDataFrameに追加する
##################################################
def add_time_variation(df, exclude_columns=['時', '日付'], inplace=True):
    """ 時間変化量をDataFrameに追加する

    Args:
        df(DataFrame)           : 変換対象のDataFrame
        exclude_columns(list)   : 変換対象から除外する列
        inplace(bool)           : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 列名のリストを取得する。
    columns = new_df.columns
    
    for column in columns:
        
        # 指定した列は対象外とする
        if column in exclude_columns:
            continue
        
        # 新しい列名を作成する
        new_column = '{0:s}_d1'.format(column)
        
        # 時間変化量の列を作成
        new_df[new_column] = new_df[column].diff()
        
    return new_df
    
##################################################
# 月平均との差分をDataFrameに追加する
##################################################
def add_difference_monthly_mean(df, columns, inplace=True):
    """ 月平均との差分をDataFrameに追加する

    Args:
        df(DataFrame)   : 変換対象のDataFrame
        columns(list)   : 変換対象の列
        inplace(bool)   : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 変換対象の列をリストに格納する
    base_columns = []
    for base_col in columns:
        base_cols = [col for col in df.columns if(base_col in col)]
        base_columns.extend(base_cols)
    
    # 月の列を追加する
    new_df['月'] = new_df['日付'].dt.month
    
    # 月ごとの平均値を算出する
    mean = new_df.groupby(['月']).mean()
    
    # 1列ずつ月平均値との差分列を追加する
    for column in base_columns:
        
        # 新しい列を追加する
        new_column = '{0:s}_diff_month'.format(column)
        new_df[new_column] = new_df[column]
        
        # 月数分ループ。月単位で平均値との差分を代入する。
        for index, row in mean.iterrows():
            
            month = index
            new_df[new_column] = new_df[new_column].mask(new_df['月']==month, new_df[column] - row[column])
    
    # 不要な列を削除する    
    new_df = new_df.drop(columns=['月'])
    #new_df = new_df.drop(columns=base_columns)
    
    return new_df
    
##################################################
# 月平均をDataFrameに追加する
##################################################
def add_monthly_mean(df, columns, inplace=True):
    """ 月平均をDataFrameに追加する

    Args:
        df(DataFrame)   : 変換対象のDataFrame
        columns(list)   : 変換対象の列
        inplace(bool)   : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 変換対象の列をリストに格納する
    add_columns = []
    for add_col in columns:
        add_cols = [col for col in df.columns if(add_col in col)]
        add_columns.extend(add_cols)
    
    # 月の列を追加する
    new_df['月'] = new_df['日付'].dt.month
    
    # 月ごとの平均値を算出する
    mean = new_df.groupby(['月']).mean()
    
    # 1列ずつ月の平均値を追加する
    for column in add_columns:
        
        # 新しい列を追加する
        new_column = '{0:s}_month_mean'.format(column)
        new_df[new_column] = new_df[column]
        
        # 月数分ループ。月単位で平均値との差分を代入する。
        for index, row in mean.iterrows():
            
            month = index
            new_df[new_column] = new_df[new_column].mask(new_df['月']==month, row[column])
    
    # 不要な列を削除する    
    new_df = new_df.drop(columns=['月'])
    
    return new_df
    
