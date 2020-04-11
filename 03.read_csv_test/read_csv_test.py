# coding: utf-8

import os
import pandas as pd
import wfile

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # カレントディレクトリを取得する
    cwd = os.getcwd()

    # 地上気象データを取得する
    ground_dir = os.path.join(cwd, 'ground_weather')
    ground_df = wfile.get_ground_weather(ground_dir)
    ground_df.to_csv('ground.csv')
    
    # 高層気象データを取得する
    #highrise_dir = os.path.join(cwd, 'highrise_weather')
    #highrise_df = wfile.get_highrise_weather(highrise_dir)
