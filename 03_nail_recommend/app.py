import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

FASTAPI_URL = "ngrok으로 FastAPI 외부주소"

st.set_page_config(page_title="Nail AI", page_icon="💅")
st.title("💅 Nail Design AI Recommender")

uploaded = st.file_uploader("손 이미지 업로드", type=["jpg", "png", "jpeg"])

def decode_base64_to_image(base64_str):
    return Image.open(BytesIO(base64.b64decode(base64_str)))

if uploaded:
    st.image(uploaded, caption="업로드한 이미지", width=300)

    if st.button("분석 시작"):
        with st.spinner("AI 분석 중입니다... (약 20~40초)"):
            files = {
                "file": (
                    uploaded.name,
                    uploaded.getvalue(),
                    uploaded.type
                )
            }

            try:
                res = requests.post(FASTAPI_URL, files=files, timeout=300)
            except Exception as e:
                st.error("❌ 서버 연결 실패!")
                st.write(e)
                st.stop()

        if res.status_code != 200:
            st.error("❌ 서버 오류 발생")
            st.write(res.text)
            st.stop()

        data = res.json()

        st.success("🎉 분석 완료!")

        # -------------------------------------------------------
        # 📌 손톱 타입 표시
        # -------------------------------------------------------
        st.subheader(f"📌 손톱 타입: **{data['nail_type']}**")
        st.caption(f"그룹 ID: {data['group_id']}")

        # -------------------------------------------------------
        # 📌 YOLO 탐지 결과 이미지 표시
        # -------------------------------------------------------
        st.subheader("📸 YOLO 탐지 결과")
        yolo_img = decode_base64_to_image(data["yolo_image"])
        st.image(yolo_img, width=350)

        # -------------------------------------------------------
        # 📌 SAM 마스크 이미지 표시
        # -------------------------------------------------------
        st.subheader("🩵 SAM 마스크 결과")
        mask_img = decode_base64_to_image(data["mask_image"])
        st.image(mask_img, width=350)

        # -------------------------------------------------------
        # 📌 추천 디자인 Top3
        # -------------------------------------------------------
        st.subheader("✨ Top 3 추천 네일 디자인")

        top3 = data["recommendations"]

        cols = st.columns(3)
        for i, reco in enumerate(top3):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        padding:15px; 
                        border-radius:12px; 
                        background:#ffe6f2;
                        text-align:center;">
                        <h4>{reco['shape']}</h4>
                        <p style="font-size:18px;">💅 {reco['design']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
