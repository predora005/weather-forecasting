# coding: utf-8

from model import ModelRandomForest
from runner import Runner
from sklearn.model_selection import StratifiedKFold

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    run_name = 'Random Forest'
    
    # モデル生成
    model = ModelRandomForest(run_name, None)
        
    # Runner生成
    runner = Runner(run_name, model, None)
    
    # クロスバリデーション実行
    runner.run_train_cv()
    
    # 学習実行
    runner.run_train_all()
    
    # 特徴量の重要度を可視化する
    runner.show_importance_of_feature()
    
    # テストデータで予測を行う
    runner.run_predict_all()
    
    # 正解率を表示する
    #runner.print_accuracy()
    
    #dot_data = export_graphviz(
    #    model.estimators_[0], 
    #    feature_names=train_x.columns,
    #    class_names=['Sunny', 'Cloud', 'Rain', 'Other'],  
    #    filled=True, 
    #    rounded=True)
    #graph = pydotplus.graph_from_dot_data( dot_data )
    #graph.write_png('tree_graphviz.png')
    
    #fig = plt.figure(figsize=(100, 50))
    #ax = fig.add_subplot()
    #plot_tree(
    #    model.estimators_[0], 
    #    feature_names=train_x.columns,
    #    ax=ax, 
    #    class_names=['Sunny', 'Cloud', 'Rain', 'Other'],
    #    filled=True
    #)
    #plt.savefig('tree_plt.png', bbox_inches='tight')
    
