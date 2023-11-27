import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib as mpl
import shap
from scipy.stats import chi2_contingency
from pycaret.classification import *
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
import hashlib

# 한글 폰트 경로 설정
font_path = './fonts/NanumBarunGothic.ttf'
fm.fontManager.addfont('./fonts/NanumBarunGothic.ttf')
fm.FontProperties(fname=font_path).get_name()
font_name = fm.FontProperties(fname=font_path).get_name()

# Matplotlib의 rcParams를 사용하여 폰트를 설정
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False  # 한글 사용 시 마이너스 기호 문제 방지

# Seaborn 스타일 설정 (최신 버전의 Seaborn을 사용하는 경우)
sns.set_theme(style="whitegrid", palette="pastel", font=font_name)

def cramers_v(x, y):
    """Cramér's V를 계산합니다."""
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

class Classification:
    def __init__(self, data_path, target_col):
        import pycaret.classification as clf_module
        self.clf_module = clf_module
        self.data_path = data_path
        self.data = None
        self.target_col = target_col
        self.setup_data = None
        self.tuned_models = []
        self.best_models = []
        self.best_model = None
        self.blended_model = None
        self.best_final_model = None
        self.models_dict = {}  # 모델 이름과 모델 객체를 매핑하는 딕셔너리
        
        # self.optimization_completed = False  # 상태 추적 변수 추가

    # 데이터 불러오기
    def load_data(self):
        """데이터를 불러옵니다."""
        if self.data_path.endswith('.csv'):
            self.data = pd.read_csv(self.data_path, encoding='utf-8-sig')
        elif self.data_path.endswith('.xlsx'):
            self.data = pd.read_excel(self.data_path)
        elif self.data_path.endswith(('.pkl', '.pickle')):
            with open(self.data_path, 'rb') as file:
                self.data = pickle.load(file)
        # 추가적인 데이터 형식에 대한 처리 (예: .xlsx)는 필요에 따라 확장 가능

    def load_data(self, dataframe=None):
        """데이터를 불러옵니다. 파일 경로 또는 데이터프레임을 사용합니다."""
        if dataframe is not None:
            self.data = dataframe
        elif self.data_path.endswith('.csv'):
            self.data = pd.read_csv(self.data_path, encoding='utf-8-sig')
        elif self.data_path.endswith('.xlsx'):
            self.data = pd.read_excel(self.data_path)
        elif self.data_path.endswith(('.pkl', '.pickle')):
            with open(self.data_path, 'rb') as file:
                self.data = pickle.load(file)

    def load_uploaded_file(uploaded_file):
        if uploaded_file.name.endswith('.csv', encoding='utf-8-sig'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(('.pkl', '.pickle')):
            return pickle.load(uploaded_file)

    def hash_data(self):
        return hashlib.sha256(pd.util.hash_pandas_object(self.data, index=True).values).hexdigest()

    @st.cache_data
    def explore_data(_self, data_hash):
        """데이터의 형태와 컬럼을 확인합니다."""
        data_description = _self.data.describe()
        return data_description

    @st.cache_data
    def feature_type(_self, data_hash):
        """데이터의 변수 타입을 구분합니다."""
        categorical_features = _self.data.select_dtypes(include=['object']).columns.tolist()
        numerical_features = _self.data.select_dtypes(exclude=['object']).columns.tolist()
        return categorical_features, numerical_features

    @st.cache_data
    def visualize_numerical_distribution(_self, data_hash):
        """수치형 변수의 분포를 시각화합니다. 각 변수별로 별도의 그래프를 생성합니다."""

        # 수치형 변수 추출
        num_cols = _self.data.select_dtypes(exclude=['object']).columns.tolist()

        # 각 변수별로 그래프 생성
        figures = []
        for column in num_cols:
            plt.figure(figsize=(7, 4))
            ax = sns.histplot(_self.data[column], kde=True, bins=30)
            ax.set_title(f'Distribution of {column}')
            plt.tight_layout()

            # 현재 그래프 저장
            figures.append(plt.gcf())
            plt.close()  # 현재 그래프를 닫음 (출력 방지)

        return figures

    @st.cache_data
    def visualize_categorical_distribution(_self, data_hash):
        cat_cols = _self.data.select_dtypes(include=['object']).columns.tolist()
        if not cat_cols:
            print('범주형 변수가 없습니다.')
            return None
        figs = []
        for column in cat_cols:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.countplot(y=_self.data[column], ax=ax, palette=sns.color_palette("pastel"), order=_self.data[column].value_counts().index)
            ax.set_title(f'Distribution of {column}')
            ax.set_xlabel('Count')
            figs.append(fig)
        plt.tight_layout()
        return figs
    
    # 결측치 시각화
    @st.cache_data
    def visualize_missing_distribution(_self, data_hash):
        """결측치 분포를 시각화합니다."""
        
        # 결측치 비율 계산
        missing_ratio = _self.data.isnull().mean() * 100
        missing_count = _self.data.isnull().sum()

        # 결측치 건수 및 비율에 대한 데이터프레임
        missing_df = pd.DataFrame({'Missing Count': missing_count, 'Missing Ratio (%)': missing_ratio})

        # 결측치 비율을 시각화
        plt.figure(figsize=(16, 8))
        sns.barplot(x=missing_ratio.index, y=missing_ratio, palette=sns.color_palette("pastel"))
        plt.axhline(30, color='red', linestyle='--')  # 30% 초과를 나타내는 빨간색 점선 추가
        plt.xticks(rotation=45)
        plt.title('Percentage of Missing Values by Columns')
        plt.ylabel('Missing Value Percentage (%)')
        plt.tight_layout()

        # plt.show()
        return missing_df, plt.gcf()

    # 결측치 처리
    @st.cache_data
    def handle_and_visualize_missing(_self, data_hash, threshold=30):
        """결측치 처리 후 데이터를 확인하고 시각화합니다."""
        
        # 1. 결측치 비율 계산
        missing_ratio = _self.data.isnull().mean() * 100
        
        # 2. 결측치 비율이 threshold(기본값: 30%)가 넘는 변수들 추출
        columns_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()

        # 3. 해당 변수들 제거
        _self.data.drop(columns=columns_to_drop, inplace=True)

        # 4. 결측치 비율 재확인
        missing_ratio_cleaned = _self.data.isnull().mean() * 100
        missing_count_cleaned = _self.data.isnull().sum()

        # 결측치 건수 및 비율에 대한 데이터프레임
        missing_df_cleaned = pd.DataFrame({'Missing Count': missing_count_cleaned, 'Missing Ratio (%)': missing_ratio_cleaned})

        # 시각화 그래프
        plt.figure(figsize=(16, 8))
        sns.barplot(x=missing_ratio_cleaned.index, y=missing_ratio_cleaned, palette=sns.color_palette("pastel"))
        plt.ylim(0, 100) # y축의 범위를 0부터 100까지로 설정
        plt.xticks(rotation=45)
        plt.title('Percentage of Missing Values by Columns (After Cleaning)')
        plt.ylabel('Missing Value Percentage (%)')
        plt.tight_layout()

        # plt.show()
        return missing_df_cleaned, plt.gcf()

    @st.cache_data
    def numerical_correlation(_self, data_hash):
        corr_matrix = _self.data.corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        plt.figure(figsize=(20, 12))
        sns.heatmap(corr_matrix, 
                    annot=True, 
                    fmt=".2f", 
                    cmap=cmap, 
                    mask=mask,
                    linewidths=0.5,
                    cbar_kws={"shrink": .8})
        plt.title("Numerical Features Correlation Matrix", fontsize=16)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        return plt.gcf()

    @st.cache_data
    def categorical_correlation(_self, data_hash):
        try:
            columns = _self.data.select_dtypes(include=['object', 'category']).columns
            corr_matrix = pd.DataFrame(index=columns, columns=columns)
            for i in columns:
                for j in columns:
                    corr_matrix.loc[i, j] = cramers_v(_self.data[i], _self.data[j])
            corr_matrix = corr_matrix.astype(float)

            cmap = sns.diverging_palette(230, 20, as_cmap=True)
            plt.figure(figsize=(20, 12))
            sns.heatmap(corr_matrix, 
                        annot=True, 
                        fmt=".2f", 
                        cmap=cmap)
            plt.title("Categorical Features Correlation Matrix", fontsize=16)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
        except: 
            print('범주형 변수가 없습니다.')

        return plt.gcf()
        
    # 옵션 설정
    def setup(_self, fix_imbalance=False, fix_imbalance_method='SMOTE', remove_outliers=False, remove_multicollinearity=True,
                    multicollinearity_threshold=0.9, train_size=0.7, fold_strategy='stratifiedkfold',
                    fold=3, profile=True, session_id=786, verbose=False):
        """옵션을 설정하고 데이터를 준비합니다."""
        # from pycaret.classification import setup
        _self.setup_data = setup(data=_self.data, target=_self.target_col,
                                fix_imbalance=fix_imbalance,
                                fix_imbalance_method=fix_imbalance_method,
                                remove_outliers=remove_outliers,
                                remove_multicollinearity=remove_multicollinearity,
                                multicollinearity_threshold=multicollinearity_threshold,
                                train_size=train_size,
                                fold_strategy=fold_strategy,
                                fold=fold,
                                profile=profile,
                                session_id=session_id, 
                                # silent=silent, 
                                verbose=verbose)
        
        result = pull()
        result = result.iloc[:-5, :]

        _self.feature_names = _self.data.columns.drop(_self.target_col) # 타겟 열을 제외한 모든 열 이름 저장

        return _self.setup_data, result

    # 모델 비교 및 생성/최적화
    def compare_and_optimize_models(_self, n_select=3, n_iter=50):
        best = compare_models(n_select=n_select,
                              include=['lr','knn', 'dt', 'rf', 'ada', 'gbc', 'et', 'xgboost', 'lightgbm', 'catboost'])
        best_df = pull()

        _self.best_models = []
        _self.tuned_models = []
        optimization_results = []  # 결과를 저장할 리스트

        for i in range(n_select):
            best_model_name = str(best_df.index[i])
            model = create_model(best_model_name)
            tuned_model = tune_model(model, n_iter=n_iter)
            
            _self.best_models.append(model)
            _self.tuned_models.append(tuned_model)
            _self.models_dict[f"모델 {i+1}"] = tuned_model  # 각 단계의 결과를 딕셔너리에 추가
            # self.models_dict[f"모델 {i+1}"] = {"model": tuned_model, "features": self.feature_names}

            # 각 단계의 결과를 리스트에 추가
            result_df = pull()  # 각 모델의 최적화 결과를 가져옵니다.
            optimization_results.append(result_df)

        # self.optimization_completed = True  # 최적화가 완료되었음을 상태 추적 변수에 저장

        return _self.models_dict, _self.tuned_models, best_df, optimization_results
    
    def create_ensemble_model(self, optimize='Recall'):
        """최적화된 모델들을 사용하여 앙상블 모델을 생성합니다."""

        if not self.tuned_models:
            raise AttributeError("최적화된 모델이 정의되지 않았습니다. 먼저 모델 비교 및 최적화 설정 단계를 실행하세요.")
        
        self.blended_model = blend_models(estimator_list=self.tuned_models, optimize=optimize)
        result_df = pull()

        result_df = pull()

        return self.blended_model, result_df

    def select_best_model(self, optimize='F1'):
        """최고 성능의 모델을 선정합니다."""
        self.best_final_model = automl(optimize=optimize)
        self.models_dict["최고 성능 모델"] = self.best_final_model 
        print(self.best_final_model)
        return self.best_final_model
    
    def save_model(self, model_name):
        """모델을 파일에 저장하고 파일 경로를 반환합니다."""
        save_path = f"{model_name}.pkl"
        with open(save_path, 'wb') as f:
            pickle.dump(self.best_final_model, f)  # 모델을 파일에 저장
        return save_path
        
    # 모델 시각화
    def visualize_model(self, model, plot_type):
        """
        선택된 모델의 성능을 시각화합니다.
        plot_type: ‘auc’, ‘threshold’, ‘pr’, ‘error’, ‘class_report’,
        ‘boundary’, ‘rfe’, ‘learning’, ‘manifold’, ‘calibration’, ‘vc’,
        ‘dimension’, ‘feature’, ‘feature_all’, ‘parameter’, ‘lift’, ‘gain’,
        ‘tree’, ‘ks’, ‘confusion_matrix’
        """
        plot_result = plot_model(model, plot=plot_type, display_format='streamlit', plot_kwargs={"fontsize":40})
        return plot_result
        
        
    # 모델 해석
    def interpret_model(self, model, plot, **kwargs):
        """모델을 해석하고 SHAP 값을 시각화합니다."""
        interpret_result = interpret_model(model, plot=plot, **kwargs)
        return interpret_result

    @classmethod
    def predict_data(cls, model, data):
        """모델을 사용하여 데이터를 예측합니다."""
        predictions = predict_model(model, data=data, raw_score = True)
        return predictions