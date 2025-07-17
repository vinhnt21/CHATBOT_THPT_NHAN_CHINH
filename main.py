import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Chatbot THCS Nhân Chính",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Giao diện người dùng (Sử dụng 100% thành phần gốc của Streamlit) ---

# 1. Tiêu đề
st.title("🏫 Chatbot THCS Nhân Chính")
st.write("Chào mừng đến với hệ thống AI hỗ trợ học sinh, giáo viên và phụ huynh.")

st.divider()

# 2. Các chức năng chính
st.header("⚙️ Chức năng chính")

col1, col2 = st.columns(2)

with col1:
    # Container cho chức năng Chat
    with st.container(border=True):
        st.markdown("### 💬 Chat với AI")
        st.markdown("Hỏi đáp tức thì về thông tin trường học, quy chế và các hoạt động.")
        if st.button("Bắt đầu Chat", use_container_width=True, type="primary"):
            st.switch_page("pages/1_💬_Chat_Bot.py")

with col2:
    # Container cho chức năng Tải tài liệu
    with st.container(border=True):
        st.markdown("### 📚 Tải tài liệu")
        st.markdown("Bổ sung kiến thức cho hệ thống bằng cách tải lên các tài liệu mới.")
        if st.button("Tải tài liệu", use_container_width=True):
            st.switch_page("pages/2_📚_Document_Upload.py")

st.divider()

# 3. Phần thông tin và hướng dẫn
st.header("💡 Thông tin & Hướng dẫn")

with st.container(border=True):
    st.subheader("🎯 Cách sử dụng")
    st.markdown("""
    - **Chat với AI:** Đặt câu hỏi trực tiếp để nhận câu trả lời tự động.
    - **Tải tài liệu:** Cung cấp thêm tài liệu (PDF, Word,...) để làm giàu kiến thức cho AI.
    """)

with st.container(border=True):
    st.subheader("📋 Thông tin hỗ trợ")
    st.markdown("""
    - **Chủ đề chính:** Thông tin về trường THCS Nhân Chính.
    - **File hỗ trợ:** PDF, DOCX, TXT, MD (tối đa 10MB).
    - **Ngôn ngữ:** Tiếng Việt.
    """)

# 4. Chân trang (Footer)
st.divider()
st.caption("Trường THCS Nhân Chính | Powered by AI | Version 1.0")