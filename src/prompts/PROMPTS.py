# Standard library imports
import os

SYSTEM_PROMPT_FILE = os.path.join(os.path.dirname(__file__), "SYSTEM_PROMPT.txt")
THONG_TIN_TRUONG_FILE = os.path.join(os.path.dirname(__file__), "THONG_TIN_TRUONG.txt")
PHAN_HOI_KHI_LOI_FILE = os.path.join(os.path.dirname(__file__), "PHAN_HOI_KHI_LOI.txt")

def _load_prompt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

SYSTEM_PROMPT = _load_prompt(SYSTEM_PROMPT_FILE)
THONG_TIN_TRUONG = _load_prompt(THONG_TIN_TRUONG_FILE)
PHAN_HOI_KHI_LOI = _load_prompt(PHAN_HOI_KHI_LOI_FILE)

__all__ = ["SYSTEM_PROMPT", "THONG_TIN_TRUONG", "PHAN_HOI_KHI_LOI"]



