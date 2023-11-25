import OpenDartReader
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
from ai import ai

### 0. 객체 생성 ###
# 객체 생성 (API KEY 지정)
api_key = 'your_api_key_here'

def set_api_key(key):
    global api_key
    api_key = key

def mm(reprt_code):
    if reprt_code == '11013':
        return '03'
    elif reprt_code == '11012':
        return '06'
    elif reprt_code == '11014':
        return '09'
    elif reprt_code == '11011':
        return '12'

# ex) get_financial_dataframe('005930')

# year month sales operating_profit net_profit
# sales_change_3 sales_change_6 sales_change_9 sales_change_12
# operating_profit_change_3 operating_profit_change_6 operating_profit_change_9 operating_profit_change_12
# net_profit_change_3 net_profit_change_6 net_profit_change_9 net_profit_change_12
def get_financial_dataframe(corp):
    dart = OpenDartReader(api_key) 

    # 보고서 코드 리스트 (1분기, 반기, 3분기, 사업보고서)
    reprt_codes = ['11013', '11012', '11014', '11011']

    # 각 보고서 코드별 데이터 저장
    data = {}

    # 빈 DataFrame 생성
    df = pd.DataFrame()

    # 현재 년도
    current_year = datetime.now().year

    # 2015년부터 2023년까지의 연도를 순회
    for year in range(2015, current_year + 1):
        for reprt_code in reprt_codes:
            try:
                # 재무제표 데이터 가져오기
                fs = dart.finstate(corp=corp, bsns_year=year, reprt_code=reprt_code)

                # 연결재무제표 데이터만 가져오기
                fs = fs.loc[fs['fs_nm'] == '연결재무제표']
                # 당기순이익, 영업이익, 매출액 추출
                fs = fs.loc[fs['account_nm'].isin(['당기순이익', '영업이익', '매출액'])]
                
                # 열 필터링
                fs = fs.loc[:, ['account_nm', 'thstrm_dt', 'thstrm_amount']]
                
                # 문자열에서 쉼표 제거 후 숫자로 변환 후 억단위로 변환
                fs['thstrm_amount'] = pd.to_numeric(fs['thstrm_amount'].str.replace(',', '')) / 1e8

                # 데이터 저장
                data[reprt_code] = fs

                if(reprt_code == '11011'):
                    # 12월 데이터에서 3월, 6월, 9월 데이터 빼기
                    data['11011']['thstrm_amount'] = data['11011']['thstrm_amount'] - data['11013']['thstrm_amount'] - data['11012']['thstrm_amount'] - data['11014']['thstrm_amount']

                # 년도와 월 추출
                fs['year'] = year
                fs['month'] = mm(reprt_code)

                # 매출액, 영업이익, 당기순이익 분리
                sales = fs[fs['account_nm'] == '매출액'].rename(columns={'thstrm_amount': 'sales'})
                operating_profit = fs[fs['account_nm'] == '영업이익'].rename(columns={'thstrm_amount': 'operating_profit'})
                net_profit = fs[fs['account_nm'] == '당기순이익'].rename(columns={'thstrm_amount': 'net_profit'})

                # 데이터프레임 병합
                result = pd.merge(sales, operating_profit, on=['year', 'month'], how='outer')
                result = pd.merge(result, net_profit, on=['year', 'month'], how='outer')

                # 필드 이름 변경
                result = result[['year', 'month', 'sales', 'operating_profit', 'net_profit']]

                # 결과를 df에 추가
                df = pd.concat([df, result], ignore_index=True)
                
            except Exception as e:
                continue

    # 이전 분기의 매출액 가져오기
    df['prev_sales'] = df['sales'].shift(1)
    df['prev2_sales'] = df['sales'].shift(2)
    df['prev3_sales'] = df['sales'].shift(3)
    df['prev4_sales'] = df['sales'].shift(4)

    df['prev_operating_profit'] = df['operating_profit'].shift(1)
    df['prev_operating_profit2'] = df['operating_profit'].shift(2)
    df['prev_operating_profit3'] = df['operating_profit'].shift(3)
    df['prev_operating_profit4'] = df['operating_profit'].shift(4)

    df['prev_net_profit'] = df['net_profit'].shift(1)
    df['prev_net_profit2'] = df['net_profit'].shift(2)
    df['prev_net_profit3'] = df['net_profit'].shift(3)
    df['prev_net_profit4'] = df['net_profit'].shift(4)

    # 변화량 계산
    df['sales_change_3'] = (df['sales'] - df['prev_sales']) / df['prev_sales'] * 100
    df['sales_change_6'] = (df['sales'] - df['prev2_sales']) / df['prev2_sales'] * 100
    df['sales_change_9'] = (df['sales'] - df['prev3_sales']) / df['prev3_sales'] * 100
    df['sales_change_12'] = (df['sales'] - df['prev4_sales']) / df['prev4_sales'] * 100

    df['operating_profit_change_3'] = (df['operating_profit'] - df['prev_operating_profit']) / df['prev_operating_profit'] * 100
    df['operating_profit_change_6'] = (df['operating_profit'] - df['prev_operating_profit2']) / df['prev_operating_profit2'] * 100
    df['operating_profit_change_9'] = (df['operating_profit'] - df['prev_operating_profit3']) / df['prev_operating_profit3'] * 100
    df['operating_profit_change_12'] = (df['operating_profit'] - df['prev_operating_profit4']) / df['prev_operating_profit4'] * 100

    df['net_profit_change_3'] = (df['net_profit'] - df['prev_net_profit']) / df['prev_net_profit'] * 100
    df['net_profit_change_6'] = (df['net_profit'] - df['prev_net_profit2']) / df['prev_net_profit2'] * 100
    df['net_profit_change_9'] = (df['net_profit'] - df['prev_net_profit3']) / df['prev_net_profit3'] * 100
    df['net_profit_change_12'] = (df['net_profit'] - df['prev_net_profit4']) / df['prev_net_profit4'] * 100

    # 이전 분기의 매출액 필드 삭제
    df = df.drop(['prev_sales', 'prev2_sales', 'prev3_sales', 'prev4_sales', 
                'prev_operating_profit', 'prev_net_profit', 
                'prev_operating_profit2', 'prev_net_profit2', 
                'prev_operating_profit3', 'prev_net_profit3', 
                'prev_operating_profit4', 'prev_net_profit4'], axis=1)

    # 결과 출력
    return df

def get_sector_dataframe():
    response = requests.get(
        'https://finance.daum.net/api/sector/wics/masters', 
        headers={
            'Referer': 'https://finance.daum.net/domestic/sectors',
            'User-Agent': 'PostmanRuntime/7.32.3'
        }
    )
    return pd.DataFrame(response.json())

def get_stock_dataframe(sector):
    # Query Params
    page = '1'
    perPage = '100'
    fieldName = 'changeRate'
    order = 'desc'
    pagination = 'true'

    daum_url = '/api/sector/wics/' + sector + '/stocks'

    query_params = {
        'symbolCode' : sector,
        'page' : page,
        'perPage' : perPage,
        'fieldName' : fieldName,
        'order' : order,
        'pagination' : pagination
    }

    url = (
        'https://finance.daum.net' + 
        daum_url
    )

    headers = {
        'Referer': 'https://finance.daum.net/domestic/sectors',
        'User-Agent': 'PostmanRuntime/7.32.3'
    }

    response = requests.get(url, json=query_params, headers=headers)
    
    # 첫 번째 페이지 데이터 추출
    data = response.json()['data']
    
    # 전체 페이지 수 추출
    total_pages = response.json()['totalPages']

    # 전체 페이지 수가 1 이상인 경우, 추가 데이터 추출
    if total_pages > 1:
        for _page in range(2, total_pages+1):
            query_params = {
                'symbolCode' : sector,
                'page' : _page,
                'perPage' : perPage,
                'fieldName' : fieldName,
                'order' : order,
                'pagination' : pagination
            }
            response = requests.get(url, json=query_params, headers=headers)
            data += response.json()['data']
    
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    json_result = json.loads(json_str)
    
    return pd.DataFrame(json_result)

# 월별 시세 데이터를 가져옵니다.
def get_monthly_stock_dataframe(isuCd):

    # 현재 날짜
    now = datetime.now()

    # 다음 달
    next_month = now + timedelta(days=30)

    # 다음 달의 년월을 yyyymm 형식으로 변환
    endYymm = next_month.year * 100 + next_month.month

    strtYymm = 201501

    url = (
        'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd' + 
        f"?bld=dbms/MDC/STAT/standard/MDCSTAT01802" +
        f"&isuCd={isuCd}" +
        f"&strtYymm={strtYymm}" +
        f"&endYymm={endYymm}"
    )

    print('krx 크롤링 중...')

    response = requests.get(url)

    df = pd.DataFrame(response.json()['OutBlock_1'])

    print('크롤링 완료')

    selected_fields = ["TRD_DD", "ISU_ABBRV", "ISU_SRT_CD", "MKT_NM", "MMEND_CLSPRC"]
    df_selected = df[selected_fields]

    # 필드명을 소문자로 변경
    df_selected.columns = df_selected.columns.str.lower()
    df = df_selected

    # 문자열에서 쉼표 제거 후 숫자로 변환
    df['mmend_clsprc'] = pd.to_numeric(df['mmend_clsprc'].str.replace(',', ''))

    # 'trd_dd' 컬럼을 '/' 기준으로 분리
    df[['year', 'month']] = df['trd_dd'].str.split('/', expand=True)

    # 'trd_dd' 컬럼을 제거
    df = df.drop('trd_dd', axis=1)

    # 'month' 컬럼의 값이 1, 2, 4, 5, 7, 8, 10, 11인 행을 제거
    # 'month' 컬럼의 값이 1, 3, 4, 6, 7, 9, 10, 12인 행을 제거
    #                    2     5     8      11
    months_to_remove = ['01', '03', '04', '06', '07', '09', '10', '12']
    df = df[~df['month'].isin(months_to_remove)]

    # month 값을 1씩 증가 한 다음 문자열로 변환
    df['month'] = (df['month'].astype(int) + 1).apply(lambda x: '{:02}'.format(x))

    # 이전 분기의 종가 가져오기
    df['prev1_mmend_clsprc'] = df['mmend_clsprc'].shift(1)
    df['prev2_mmend_clsprc'] = df['mmend_clsprc'].shift(2)
    df['prev3_mmend_clsprc'] = df['mmend_clsprc'].shift(3)
    df['prev4_mmend_clsprc'] = df['mmend_clsprc'].shift(4)

    # 다음 분기의 종가 가져오기
    df['next1_mmend_clsprc'] = df['mmend_clsprc'].shift(-1)

    # 변화량 계산
    df['mmend_clsprc_change_3'] = (df['mmend_clsprc'] - df['prev1_mmend_clsprc']) / df['prev1_mmend_clsprc'] * 100
    df['mmend_clsprc_change_6'] = (df['mmend_clsprc'] - df['prev2_mmend_clsprc']) / df['prev2_mmend_clsprc'] * 100
    df['mmend_clsprc_change_9'] = (df['mmend_clsprc'] - df['prev3_mmend_clsprc']) / df['prev3_mmend_clsprc'] * 100
    df['mmend_clsprc_change_12'] = (df['mmend_clsprc'] - df['prev4_mmend_clsprc']) / df['prev4_mmend_clsprc'] * 100

    df['next_mmend_clsprc_change'] = (df['next1_mmend_clsprc'] - df['mmend_clsprc']) / df['mmend_clsprc'] * 100

    # 이전 분기의 종가 필드 삭제
    df = df.drop(['prev1_mmend_clsprc', 'prev2_mmend_clsprc', 'prev3_mmend_clsprc', 'prev4_mmend_clsprc', 'next1_mmend_clsprc'], axis=1)

    return df

# financial_monthly_stock
def merge_financial_and_monthly_stock_dataframe(fDf, pDf):
    fDf['year'] = fDf['year'].astype(str)
    pDf['year'] = pDf['year'].astype(str)

    # 두 dataframe 에서 year, month 확인하여 같은 것 끼리 merge
    merged_df = fDf.merge(pDf, on=['year', 'month'])

    return merged_df