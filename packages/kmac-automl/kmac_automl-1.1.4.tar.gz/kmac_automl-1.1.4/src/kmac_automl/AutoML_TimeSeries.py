import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib as mpl
import shap
from scipy.stats import chi2_contingency
from pycaret.time_series import *
import pickle
import matplotlib.font_manager as fm
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

class TimeSeries: ############################################################################################
    def __init__(self, data_path, target_col):
        import pycaret.time_series as ts_module
        self.ts_module = ts_module
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
        if uploaded_file.name.endswith('.csv'):
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
        """범주형 변수의 분포를 시각화합니다."""
        
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
    def setup(self, fold_strategy='expanding', enforce_exogenous=False, fold=3, fh=12, hyperparameter_split='all', session_id=786, seasonal_period=None, scale_target=None, scale_exogenous=None, 
              numeric_imputation_target='drift', numeric_imputation_exogenous='drift', ignore_seasonality_test=False, seasonality_type ='auto'):
        """시계열 모델을 설정합니다."""
        self.setup_data = setup(data=self.data, target=self.target_col,
                                fold_strategy=fold_strategy,
                                fold=fold,
                                fh=fh,
                                enforce_exogenous=enforce_exogenous,
                                hyperparameter_split=hyperparameter_split,
                                session_id=session_id,
                                seasonal_period=seasonal_period,
                                numeric_imputation_target=numeric_imputation_target,
                                numeric_imputation_exogenous=numeric_imputation_exogenous,
                                scale_target=scale_target,
                                scale_exogenous=scale_exogenous,
                                ignore_seasonality_test=ignore_seasonality_test,
                                seasonality_type=seasonality_type
                                )

        result = pull()
        result = result.iloc[:-5, :]

        self.feature_names = self.data.columns.drop(self.target_col) # 타겟 열을 제외한 모든 열 이름 저장

        return self.setup_data, result

    def compare_and_optimize_models(self, n_select=3, n_iter=50, sort='mase'):
        """모델을 비교하고 최적화합니다."""
        best = compare_models(n_select=n_select, sort=sort, 
                              include=['arima','lr_cds_dt','en_cds_dt','knn_cds_dt','dt_cds_dt','rf_cds_dt','et_cds_dt','gbr_cds_dt'])
        best_df = pull()

        self.best_models = []
        self.tuned_models = []
        optimization_results = []  # 결과를 저장할 리스트

        for i in range(n_select):
            best_model_name = str(best_df.index[i])
            model = create_model(best_model_name)
            tuned_model = tune_model(model, n_iter=n_iter)
            
            self.best_models.append(model)
            self.tuned_models.append(tuned_model)
            self.models_dict[f"모델 {i+1}"] = tuned_model  # 각 단계의 결과를 딕셔너리에 추가

            # 각 단계의 결과를 리스트에 추가
            result_df = pull()  # 각 모델의 최적화 결과를 가져옵니다.
            optimization_results.append(result_df)

        return self.models_dict, self.tuned_models, best_df, optimization_results

    # def create_ensemble_model(self, optimize='MASE'):
    #     """최적화된 모델들을 사용하여 앙상블 모델을 생성합니다."""
    #     if not self.tuned_models:
    #         raise AttributeError("최적화된 모델이 정의되지 않았습니다. 먼저 모델 비교 및 최적화 설정 단계를 실행하세요.")
        
    #     self.blended_model = blend_models(estimator_list=self.tuned_models, optimize=optimize)
    #     result_df = pull()

    #     return self.blended_model, result_df

    # def select_best_model(self, optimize='MASE'):
    #     """앙상블 모델을 생성합니다."""
    #     self.compare_and_optimize_models(n_select=3, n_iter=50)
    #     # 최적화된 모델들을 사용하여 앙상블 모델을 생성합니다.
    #     self.best_final_model, _ = self.create_ensemble_model(optimize=optimize)
    #     self.models_dict["앙상블 모델"] = self.best_final_model
    #     print(self.best_final_model)
    #     return self.best_final_model

    def save_model(self, model_name, selected_model):
        """모델을 파일에 저장하고 파일 경로를 반환합니다."""
        save_path = f"{model_name}.pkl"
        with open(save_path, 'wb') as f:
            pickle.dump(selected_model, f)  # 모델을 파일에 저장
        return save_path

    def plot_model(self, model):
        plt.figure()
        plot_result = plot_model(model, display_format='streamlit')
        
        return plot_result

    def visualize_model(self, model, plot_type):
        """
        선택된 모델의 성능을 시각화합니다.
        plot_type: 'ts', 'train_test_split', 'cv', 'acf', 'pacf', 'decomp', 'decomp_stl', 'diagnostics',
                   'diff', 'periodogram', 'fft', 'ccf', 'forecast', 'insample', 'residuals'
        """
        plt.figure()
        plot_result = plot_model(model, plot=plot_type, display_format='streamlit')
        
        return plot_result
    
    def finalize_model(self, model):
        final_model = finalize_model(model)
        return final_model

    @classmethod
    def predict_model(self, model, X=None, fh=12, round=0):
        predictions = predict_model(model, X=X, fh=fh, round=round)
        return predictions