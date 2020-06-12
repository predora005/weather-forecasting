# coding: utf-8

from .abs_model import AbsModel
from sklearn.ensemble import RandomForestClassifier

##################################################
# ランダムフォレスト
##################################################
class ModelRandomForest(AbsModel):
    """ランダムフォレスト
        
    Attributes:
        run_fold_name (string)  : ランとfoldを組み合わせた名称
        params (dict)           : パラメータ
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_fold_name, params):
        """ コンストラクタ
        
        Args:
            run_fold_name(string)   : ランとfoldを組み合わせた名称
            params(dict)            : パラメータ
        """
        
        # 抽象クラスのコンストラクタ
        super().__init__(run_fold_name, params)
        
        # ランダムフォレストの学習モデルを生成する
        self._model = RandomForestClassifier(n_estimators=2000, max_depth=30, random_state=1)
        
    ##################################################
    # 学習
    ##################################################
    def train(self, train_x, train_y, validate_x=None, validate_y=None):
        """ 学習
        
        Args:
            train_x(DataFrame)  : 学習データ(入力)
            train_y(DataFrame)  : 学習データ(出力)
        """
        self._model.fit(train_x, train_y)
        #pred_y = self.predict(validate_x)
        
    ##################################################
    # 予測
    ##################################################
    def predict(self, test_x):
        """ 予測
        
        Args:
            test_x(DataFrame)   : テストデータ(入力)

        Returns:
            DataFrame : テストデータ(出力)
        """
        pred_y = self._model.predict(test_x)
        return pred_y
        
    ##################################################
    # モデルをファイルに保存する
    ##################################################
    def save_model(self):
        """ モデルをファイルに保存する
        """
        raise NotImplementedError()
        
    ##################################################
    # モデルをファイルからロードする
    ##################################################
    def load_model(self):
        """ モデルをファイルからロードする
        """
        raise NotImplementedError()
        
    ##################################################
    # 特徴量の重要度を返す
    ##################################################
    def get_feature_importances(self):
        return self._model.feature_importances_
        
    ##################################################
    # 推定器を返す
    ##################################################
    def get_estimators(self):
        return self._model.estimators_
        
        