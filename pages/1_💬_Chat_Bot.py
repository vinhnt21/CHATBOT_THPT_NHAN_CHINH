import streamlit as st
import uuid
from datetime import datetime

# Import từ hệ thống RAG của bạn
try:
    from src.rag.generate_response import generate_response
    from src.configs.settings import pinecone_config
except ImportError as e:
    st.error(f"Lỗi import: {e}")
    st.warning("Vui lòng đảm bảo rằng cấu trúc file và các thư viện cần thiết đã được cài đặt chính xác.")
    st.stop()

# Cấu hình trang
st.set_page_config(page_title="Chatbot THPT Nhân Chính", page_icon="💬", layout="centered")

# Tiêu đề ứng dụng
st.title("🤖 Chatbot THPT Nhân Chính")
st.caption("Trợ lý AI sẵn sàng trả lời các câu hỏi về thông tin trường học.")

# --- Khởi tạo Session State ---
# Khởi tạo session ID duy nhất cho mỗi phiên làm việc
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Khởi tạo chủ đề chat mặc định
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = pinecone_config.NAME_SPACE.THONG_TIN_TRUONG.value

# Khởi tạo lịch sử chat với tin nhắn chào mừng
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào! Tôi có thể giúp gì cho bạn về trường THPT Nhân Chính?"
        }
    ]

# --- Giao diện Chat ---
# Hiển thị các tin nhắn đã có trong lịch sử
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Khu vực nhập liệu của người dùng, cố định ở cuối trang
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Thêm tin nhắn của người dùng vào lịch sử và hiển thị ngay lập tức
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tạo và hiển thị phản hồi của bot
    with st.chat_message("assistant"):
        # Hiển thị spinner trong khi chờ phản hồi
        with st.spinner("AI đang suy nghĩ..."):
            try:
                # Gọi hàm RAG để lấy câu trả lời
                response = generate_response(
                    session_id=st.session_state.session_id,
                    query=prompt,
                    namespace=st.session_state.selected_topic
                )
                st.markdown(response)
                # Thêm phản hồi của bot vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                # Bắt lỗi và hiển thị thông báo thân thiện
                error_message = f"Xin lỗi, đã có lỗi xảy ra trong quá trình xử lý. Vui lòng thử lại. (Lỗi: {e})"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# --- Chức năng phụ ---
# Cung cấp nút để bắt đầu lại cuộc trò chuyện
if len(st.session_state.messages) > 1: # Chỉ hiện nút sau khi có ít nhất 1 câu hỏi
    if st.button("🗑️ Trò chuyện mới"):
        # Reset lại lịch sử tin nhắn và giữ nguyên session ID
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Xin chào! Tôi có thể giúp gì cho bạn về trường THPT Nhân Chính?"
            }
        ]
        st.rerun()