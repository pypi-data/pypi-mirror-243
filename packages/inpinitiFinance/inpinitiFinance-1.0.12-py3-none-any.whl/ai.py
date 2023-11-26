from sklearn.model_selection import train_test_split

# 딥러닝을 위해서
from keras.models import Sequential
from keras.layers import Dense

# 성능 평가를 위해서
from sklearn.metrics import mean_squared_error

# 의사결정트리를 위해서
from sklearn.tree import DecisionTreeRegressor

# 선형 회귀 모델을 위해서
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

# 랜덤 포레스트를 위해서
from sklearn.ensemble import RandomForestRegressor

class ai:
    @staticmethod
    def deep_learning(df, drop_columns=[]):
        # 전처리
        X_train, X_test, y_train, y_test = ai.clean_and_remove_missing_data(df, drop_columns)

        # 모델 구성
        model = Sequential()

        # 2개의 Dense 레이어 추가하고, 64개의 뉴런을 사용
        model.add(Dense(64, activation='relu', input_dim=X_train.shape[1]))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(1))

        # 모델 컴파일
        model.compile(optimizer='adam', loss='mean_squared_error')

        # 모델 학습
        model.fit(X_train, y_train, epochs=10, batch_size=32)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'Deep Learning MSE: {mse:.4f}')

        return model
    
    @staticmethod
    def regressor(df, drop_columns=['year', 'month', 'isu_abbrv', 'isu_srt_cd', 'mkt_nm']):
        # 전처리
        X_train, X_test, y_train, y_test = ai.clean_and_remove_missing_data(df, drop_columns)

        # 선형 회귀 모델 생성
        model = LinearRegression()

        # 모델 학습
        model.fit(X_train, y_train)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'Linear Regression MSE: {mse:.4f}')

        return df
    
    @staticmethod
    def ridge(df, drop_columns=['year', 'month', 'isu_abbrv', 'isu_srt_cd', 'mkt_nm']):
        # 전처리
        X_train, X_test, y_train, y_test = ai.clean_and_remove_missing_data(df, drop_columns)

        # 선형 회귀 모델 생성
        model = Ridge()

        # 모델 학습
        model.fit(X_train, y_train)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'Ridge Regression MSE: {mse:.4f}')

        return df
    
    @staticmethod
    def lasso(df, drop_columns=['year', 'month', 'isu_abbrv', 'isu_srt_cd', 'mkt_nm']):
        # 전처리
        X_train, X_test, y_train, y_test = ai.clean_and_remove_missing_data(df, drop_columns)

        # 선형 회귀 모델 생성
        model = Lasso()

        # 모델 학습
        model.fit(X_train, y_train)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'Lasso Regression MSE: {mse:.4f}')

        return df
    
    @staticmethod
    def elastic_net(df, drop_columns=['year', 'month', 'isu_abbrv', 'isu_srt_cd', 'mkt_nm']):
        # 전처리
        X_train, X_test, y_train, y_test = ai.clean_and_remove_missing_data(df, drop_columns)

        # 선형 회귀 모델 생성
        model = ElasticNet()

        # 모델 학습
        model.fit(X_train, y_train)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'Elastic Net Regression MSE: {mse:.4f}')

        return df
    
    @staticmethod
    def decision_tree(df, drop_columns=['year', 'month', 'isu_abbrv', 'isu_srt_cd', 'mkt_nm']):
        # 전처리
        X_train, X_test, y_train, y_test = ai.clean_and_remove_missing_data(df, drop_columns)

        # 선형 회귀 모델 생성
        model = DecisionTreeRegressor()

        # 모델 학습
        model.fit(X_train, y_train)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'Decision Tree Regression MSE: {mse:.4f}')

        return df
    
    @staticmethod
    def random_forest(df, drop_columns=['year', 'month', 'isu_abbrv', 'isu_srt_cd', 'mkt_nm']):
        # 전처리
        X_train, X_test, y_train, y_test = ai.clean_and_remove_missing_data(df, drop_columns)

        # 선형 회귀 모델 생성
        model = RandomForestRegressor()

        # 모델 학습
        model.fit(X_train, y_train)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'Random Forest Regression MSE: {mse:.4f}')

        return df
    
    @staticmethod
    def clean_and_remove_missing_data(df, drop_columns=['year', 'month', 'isu_abbrv', 'isu_srt_cd', 'mkt_nm']):
        # 제거 isu_abbrv isu_srt_cd mkt_nm
        df = df.drop(drop_columns, axis=1)

        # next_mmend_clsprc_change 이 급격하게 변하는 데이터는 제거
        df = df[(df['mmend_clsprc_change_3'] >= -50) & (df['mmend_clsprc_change_3'] <= 50)]
        df = df[(df['mmend_clsprc_change_6'] >= -50) & (df['mmend_clsprc_change_6'] <= 50)]
        df = df[(df['mmend_clsprc_change_9'] >= -50) & (df['mmend_clsprc_change_9'] <= 50)]
        df = df[(df['mmend_clsprc_change_12'] >= -50) & (df['mmend_clsprc_change_12'] <= 50)]
        df = df[(df['next_mmend_clsprc_change'] >= -50) & (df['next_mmend_clsprc_change'] <= 50)]

        # NaN 값을 포함하는 행을 삭제
        df = df.dropna()

        # 데이터 전처리
        X = df.drop('next_mmend_clsprc_change', axis=1)
        y = df['next_mmend_clsprc_change']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

        # float 타입으로 변환
        X_train = X_train.astype('float32')
        y_train = y_train.astype('float32')
        X_test = X_test.astype('float32')
        y_test = y_test.astype('float32')

        return X_train, X_test, y_train, y_test