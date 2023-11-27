import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib as mpl
import shap
from scipy.stats import chi2_contingency
from pycaret.anomaly import *
import pickle
import matplotlib.font_manager as fm
import hashlib

# -*- coding: utf-8-sig -*-

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

class AnomalyDetection:
    def __init__(self, data, target_column):
        """이상치 탐지 클래스의 생성자입니다."""
        self.data = data
        self.models = ['iforest', 'knn', 'lof', 'pca']
        self.models_dict = {}  # 모델 이름과 모델 객체를 매핑하는 딕셔너리
        self.results = {}
        
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
        num_cols = _self.data.select_dtypes(exclude=['object']).columns.tolist()
        figures = []
        for column in num_cols:
            plt.figure(figsize=(7, 4))
            ax = sns.histplot(_self.data[column], kde=True, bins=30)
            ax.set_title(f'Distribution of {column}')
            plt.tight_layout()
            figures.append(plt.gcf())
            plt.close()
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
    def setup(self, session_id = 786, normalize = True, normalize_method = 'zscore', profile = True):
        """이상치 탐지 모델을 설정합니다."""
        num_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = self.data.select_dtypes(include=['datetime64[ns]']).columns.tolist()
                                
        self.setup_data = setup(data=self.data,
                                categorical_features=cat_cols,
                                numeric_features=num_cols,
                                date_features=date_cols,
                                encoding_method='binary',
                                session_id=session_id,
                                normalize=normalize,
                                normalize_method=normalize_method
                                )
        
        result = pull()
        result = result.iloc[:-5, :]

        return self.setup_data, result

    # 모델 생성
    def create_models(self):
        self.models_dict = {}
        for model_name in self.models:
            model = create_model(model_name)
            self.anomaly_model = model
            assigned_data = assign_model(model)
            self.models_dict[model_name] = model
            self.results[model_name] = assigned_data

    def get_models(self):
        return self.models_dict
    
    def get_results(self):
        return self.results
    
    def save_model(self, selected_model, model_name):
        """모델을 파일에 저장하고 파일 경로를 반환합니다."""
        save_path = f"{model_name}.pkl"
        with open(save_path, 'wb') as f:
            pickle.dump(selected_model, f)  # 모델을 파일에 저장
        return save_path
        
    # 모델 시각화
    def visualize_model(self, model, plot_type):
        """
        선택된 모델의 성능을 시각화합니다.
        plot_type: 'tsne', 'umap'
        """
        plot_result = plot_model(model, plot=plot_type, display_format='streamlit')
        return plot_result   

    @classmethod
    def predict_data(cls, model, data):
        """모델을 사용하여 데이터를 예측합니다."""
        predictions = predict_model(model, data=data)
        return predictions