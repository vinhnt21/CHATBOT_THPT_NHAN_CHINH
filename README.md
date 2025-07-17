# 🏫 Chatbot THCS Nhân Chính

[![Streamlit](https://img.shields.io/badge/Streamlit-FF6B6B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-4285F4?style=for-the-badge&logo=openai&logoColor=white)](https://deepseek.com/)

Hệ thống chatbot AI thông minh cho trường THCS Nhân Chính với khả năng hỏi đáp theo chủ đề và quản lý tài liệu kiến thức.

## ✨ Tính năng chính

### 💬 Chatbot thông minh
- **Topic-based chat**: Hỏi đáp theo chủ đề cụ thể (Thông tin trường, Môn Toán)
- **RAG Architecture**: Retrieval Augmented Generation cho câu trả lời chính xác
- **Streaming responses**: Hiển thị câu trả lời theo thời gian thực
- **Source citations**: Trích dẫn nguồn tài liệu được sử dụng

### 📚 Quản lý Knowledge Base
- **Multi-format support**: PDF, Word, Text, Markdown
- **Intelligent processing**: Tự động chia nhỏ và tạo embeddings
- **Topic organization**: Phân loại tài liệu theo chủ đề
- **Search & filter**: Tìm kiếm và lọc tài liệu dễ dàng

### 📊 Analytics & Monitoring
- **System health**: Theo dõi trạng thái các services
- **Usage statistics**: Thống kê sử dụng theo thời gian
- **Error monitoring**: Giám sát và quản lý lỗi hệ thống
- **Performance metrics**: Đo lường hiệu suất chi tiết

## 🏗️ Kiến trúc hệ thống

```
Frontend (Streamlit) → RAG Pipeline (LlamaIndex) → LLM (DeepSeek API)
                                    ↓
Vector Database (Pinecone) ← Embeddings (OpenAI) ← Documents
                                    ↓
                           Database (MongoDB)
```

### Tech Stack
- **Frontend**: Streamlit (Python web framework)
- **LLM**: DeepSeek API (cost-effective language model)
- **Embeddings**: OpenAI Ada-002 (high-quality text embeddings)
- **Vector DB**: Pinecone (managed vector database)
- **Database**: MongoDB Atlas (document database)
- **RAG Framework**: LlamaIndex (document processing & retrieval)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd CHATBOT_THCS_NHAN_CHINH
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
```

Required API keys:
- **DeepSeek API**: [Get key here](https://platform.deepseek.com/)
- **OpenAI API**: [Get key here](https://platform.openai.com/)
- **Pinecone API**: [Get key here](https://app.pinecone.io/) (Serverless API v3+)
- **MongoDB**: [Setup here](https://cloud.mongodb.com/)

### 4. Configure Environment
```bash
# Copy and edit Streamlit secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API keys
```

### 5. Setup Pinecone Index
```bash
# Setup Pinecone index với dimension 1536 cho text-embedding-3-small
python setup_pinecone_index.py
```

### 6. Run Application
```bash
# Option 1: Using the startup script (recommended)
python run_app.py

# Option 2: Direct Streamlit command
streamlit run main.py
```

Ứng dụng sẽ chạy tại: `http://localhost:8501`

## 📋 Environment Variables

Create `.env` file with following variables:

```bash
# Required API Keys
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
OPENAI_API_KEY=sk-your-openai-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here

# Pinecone Serverless Configuration (New API)
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

# MongoDB
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/

# Optional Configuration
DEBUG=false
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=10
RATE_LIMIT_QUERIES_PER_MINUTE=30
```

## 🎯 Sử dụng

### 🏠 Trang chủ
- Tổng quan về hệ thống
- Điều hướng nhanh đến các chức năng
- Hướng dẫn sử dụng cơ bản

### 💬 Chat với AI Bot
1. Click **"🚀 Bắt đầu Chat"** từ trang chủ
2. Chọn chủ đề: **🏫 Thông tin trường**
3. Đặt câu hỏi hoặc chọn câu hỏi gợi ý
4. Nhận câu trả lời từ AI với ngữ cảnh lịch sử chat
5. Có thể chat liên tục, hệ thống nhớ cuộc trò chuyện

**Tính năng Chat:**
- ✅ Session management với UUID
- ✅ Chat history trong memory
- ✅ Streaming responses
- ✅ Error handling
- ✅ Topic-based context filtering

### 📚 Quản lý tài liệu
1. Truy cập page **📚 Knowledge Base**
2. Tab **📤 Tải lên**:
   - Chọn file (PDF, Word, Text, MD)
   - Chọn chủ đề phù hợp
   - Click "Bắt đầu xử lý"
3. Tab **📖 Duyệt tài liệu**:
   - Tìm kiếm và lọc tài liệu
   - Chỉnh sửa hoặc xóa tài liệu
   - Xem chi tiết và metadata

### Theo dõi Analytics
1. Truy cập page **📊 Analytics**
2. **System Health**: Kiểm tra trạng thái services
3. **Usage Stats**: Xem thống kê sử dụng
4. **Error Monitoring**: Theo dõi lỗi hệ thống
5. **Performance**: Đo lường hiệu suất

## 🔧 Cấu hình nâng cao

### Pinecone Setup (Serverless)
```bash
# Index will be created automatically with these settings:
dimension: 1536  # text-embedding-3-small dimension
metric: cosine
cloud: aws (or gcp)
region: us-east-1 (or your preferred region)
spec: ServerlessSpec

# Or run setup script:
python setup_pinecone_index.py
```

### MongoDB Collections
- `documents`: Metadata tài liệu
- `error_logs`: Log lỗi hệ thống
- `chat_sessions`: Lịch sử chat
- `embedding_cache`: Cache embeddings

### Prompt Management
Tất cả prompts được quản lý tại `config/prompts.py`:
- Topic-specific prompts
- System prompts
- Error handling prompts
- Dynamic prompt generation

## 🐛 Troubleshooting

### Common Issues

**1. Import Error**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. API Key Missing**
```bash
# Solution: Check .env file
cp .env.example .env
# Edit .env with your API keys
```

**3. MongoDB Connection Failed**
```bash
# Solution: Check connection string
# Ensure IP is whitelisted in MongoDB Atlas
```

**4. Pinecone Vector Dimension Mismatch**
```bash
# Error: Vector dimension 1536 does not match the dimension of the index 1024
# Solution: Run setup script to recreate index with correct dimension
python setup_pinecone_index.py
```

**5. Pinecone Index Not Found**
```bash
# Solution: Run setup script or create index manually
python setup_pinecone_index.py

# Manual creation:
# Index name: thcs-nhan-chinh-kb
# Dimension: 1536 (for text-embedding-3-small)
# Spec: ServerlessSpec (cloud=aws, region=us-east-1)
```

### Debug Mode
```bash
# Enable debug in .env
DEBUG=true
LOG_LEVEL=DEBUG

# Check logs in terminal
streamlit run main.py
```

## 📊 Cost Optimization

### DeepSeek vs OpenAI
- **DeepSeek**: ~$0.14/1M tokens (95% cost savings)
- **OpenAI GPT-4**: ~$10-30/1M tokens

### Pinecone Free Tier
- 1 index, 100K vectors
- Suitable for demo và small-scale usage

### MongoDB Atlas
- 512MB free tier
- Enough for metadata và logs

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add environment variables
4. Deploy automatically

### Local Production
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment
export DEBUG=false
export LOG_LEVEL=INFO

# Run with production config
streamlit run main.py --server.port 8501
```

## 📖 Documentation

- **Technical Spec**: `overview.md`
- **Configuration**: `config/` directory
- **Source Code**: `src/` directory
- **UI Pages**: `pages/` directory

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Issues & Questions
- GitHub Issues: [Create issue](https://github.com/your-repo/issues)
- Email: support@thcsnhanchinh.edu.vn

### Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LlamaIndex Guide](https://docs.llamaindex.ai/)
- [DeepSeek API Docs](https://platform.deepseek.com/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)

---

**Made with ❤️ for THCS Nhân Chính**

*Powered by Streamlit, DeepSeek, LlamaIndex & Modern AI Stack* 