from src.database.pinecone_client import get_context_by_query


print(get_context_by_query("đội ngũ giáo viên", "thong_tin_truong"))