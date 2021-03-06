# coding: utf-8

import pydotplus
import sklearn
#from sklearn.tree import export_graphviz, plot_tree

##################################################
# Graphvizのグラフをファイルに出力する
##################################################
def export_graphviz(file_path, estimators, feature_names, class_names):
    """ Graphvizのグラフをファイルに出力する
    
    Args:
        file_path(string)                   : 出力先ファイルパス
        estimators(DecisionTreeClassifier)  : 推定器
        feature_names(list of string)       : 特徴量の名称リスト
        class_names(list of string)         : クラス名のリスト
    """
    dot_data = sklearn.tree.export_graphviz(
        estimators, 
        feature_names=feature_names,
        class_names=class_names,  
        filled=True, 
        rounded=True)
    graph = pydotplus.graph_from_dot_data( dot_data )
    graph.write_png(file_path)
    
