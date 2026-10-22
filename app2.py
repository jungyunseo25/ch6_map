import streamlit as st
import pandas as pd
import folium
import math

# 1. 앱 제목 설정
st.title("🚌 부산 지하철 역별 이용객 수 지도 분석 앱")

# 호선별 색상 사전 정의 (1호선: 주황, 2호선: 초록, 3호선: 갈색, 4호선: 파랑, 기타: 회색)
COLOR_DICT = {
    "1호선": "orange",
    "2호선": "green",
    "3호선": "brown",
    "4호선": "blue"
}

# 2. CSV 파일 업로드
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 3. 데이터 읽기
    df = pd.read_csv(uploaded_file)

    # [호선 필터] multiselect로 표시할 호선 선택
    line_list = df['호선'].unique().tolist()
    selected_lines = st.multiselect("보려 하는 호선을 선택하세요", line_list, default=line_list)

    # 선택된 호선의 데이터만 필터링
    filtered_df = df[df['호선'].isin(selected_lines)]

    # 4. 전체 데이터 표 출력
    st.subheader("📊 전체 데이터 목록")
    st.dataframe(filtered_df)

    # [표] 이용객 상위 5개 역 추출 및 표시
    st.subheader("🏆 이용객 상위 5개 역")
    top5_df = filtered_df.sort_values(by="이용객수", ascending=False).head(5)
    st.dataframe(top5_df[['호선', '역명', '이용객수']])

    # 5. 지도 생성 (부산 중심 좌표)
    m = folium.Map(location=[35.1795543, 129.0756416], zoom_start=11)

    # 6. 필터링된 역 위치에 CircleMarker 추가
    for index, row in filtered_df.iterrows():
        # 원의 면적이 이용객수에 비례하도록 반지름을 제곱근으로 계산
        radius_value = math.sqrt(row['이용객수']) * 0.05

        # [색상] 호선별 색상 설정 (기본값은 gray)
        line_color = COLOR_DICT.get(row['호선'], 'gray')

        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=radius_value,
            color=line_color,
            fill=True,
            fill_color=line_color,
            fill_opacity=0.6,
            tooltip=f"{row['호선']} {row['역명']}",  # 마우스 올렸을 때: 역명
            popup=f"이용객수: {row['이용객수']:,}명"  # 클릭했을 때: 이용객 수
        ).add_to(m)

    # 7. Streamlit에 지도 출력
    st.subheader("🗺️ 역별 이용객 수 지도")
    st.components.v1.html(m._repr_html_(), height=500)

else:
    st.info("시각화를 시작하려면 CSV 파일을 먼저 업로드해주세요.")