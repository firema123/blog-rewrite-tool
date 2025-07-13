import streamlit as st
import openai
import textwrap

st.set_page_config(page_title="블로그 자동 리라이팅", layout="wide")
st.title("📝 블로그 자동 리라이팅 툴")

# ✨ 사용자에게 API 키 입력받도록 하는 부분
api_key = st.sidebar.text_input("▶ OpenAI API 키 입력", type="password")
model = st.sidebar.selectbox("모델 선택", ["gpt-4", "gpt-3.5-turbo"], index=0)

def split_text(text, max_chars=2000):
    return textwrap.wrap(text, max_chars, break_long_words=False, replace_whitespace=False)

def rewrite_chunk(chunk):
    openai.api_key = api_key
    prompt = f"""
너는 블로그 글을 유사문서로 분류되지 않게 자연스럽게 재작성하는 도우미야.
- 의미는 유지하되 새로운 표현으로 바꿔.
- ( ) 안, 사진명, (내용), (링크 넣기), H2/H3/H4 등은 절대 변경 금지.
- 문장을 줄이거나 요약하지 말고, 길이와 구조를 유지해.
- 너무 꾸미지 말고, 깔끔하고 자연스럽게 써.

원문:
{chunk}
"""
    res = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return res.choices[0].message.content.strip()

uploaded = st.file_uploader("🗂️ 블로그 원고 업로드 (.txt)", type="txt")
if uploaded:
    raw = uploaded.read().decode("utf-8")
    parts = split_text(raw)
    st.success(f"{len(parts)}개 블록으로 분할됨")

    if st.button("🚀 리라이팅 시작"):
        if not api_key:
            st.error("🔑 API 키를 먼저 입력하세요.")
        else:
            rewritten = []
            progress = st.progress(0)
            for i, chunk in enumerate(parts):
                rewritten.append(rewrite_chunk(chunk))
                progress.progress((i+1)/len(parts))
            final = "\n\n".join(rewritten)
            st.text_area("✅ 결과", final, height=400)
            st.download_button("⬇️ 다운로드 (.txt)", final, file_name="rephrased_blog.txt")
