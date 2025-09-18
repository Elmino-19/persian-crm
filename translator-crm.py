# -*- coding: utf-8 -*-
import time
import re
from pathlib import Path
from typing import List
from tqdm import tqdm
from deep_translator import GoogleTranslator

# ---------------------------
# تنظیمات قابل تغییر
# ---------------------------
SRC_FOLDER = "/home/erfan/PycharmProjects/django-crm/docs"         # مسیر پوشه ورودی
DST_FOLDER = "./out"          # مسیر پوشه خروجی
CHUNK_SIZE = 20               # تعداد خطوط هر بلوک
SOURCE_LANG = "auto"            # زبان مبدا (یا None برای auto)
TARGET_LANG = "fa"            # زبان مقصد
SLEEP_BETWEEN = 0.5           # مکث بین هر بلوک ترجمه (ثانیه)
RETRIES = 3                   # تعداد تلاش مجدد
RETRY_DELAY = 1.5             # مکث بین تلاش‌های مجدد (ثانیه)

# ---------------------------
# Preprocess / Postprocess
# ---------------------------
def preprocess_block(text_block: str):
    """
    قفل کردن:
    - بلاک‌های کد چندخطی ```...```
    - inline code `...`
    - لینک‌های Markdown [text](url)
    - تصاویر Markdown ![alt](url)
    - تگ‌های HTML <...>
    """
    placeholders = {}
    counter = 0

    def make_placeholder():
        nonlocal counter
        counter += 1
        return f"{{{{PLACEHOLDER_{counter}}}}}"

    # بلاک‌های کد چندخطی ```...```
    text_block = re.sub(r"```[\s\S]*?```", lambda m: placeholders.setdefault(make_placeholder(), m.group(0)), text_block)

    # inline code `...`
    text_block = re.sub(r"`[^`]+`", lambda m: placeholders.setdefault(make_placeholder(), m.group(0)), text_block)

    # تصاویر Markdown ![alt](url)
    text_block = re.sub(r"!\[[^\]]*\]\([^\)]+\)", lambda m: placeholders.setdefault(make_placeholder(), m.group(0)), text_block)

    # لینک‌های Markdown [text](url)
    text_block = re.sub(r"\[[^\]]+\]\([^\)]+\)", lambda m: placeholders.setdefault(make_placeholder(), m.group(0)), text_block)

    # تگ‌های HTML <...>
    text_block = re.sub(r"<[^>]+>", lambda m: placeholders.setdefault(make_placeholder(), m.group(0)), text_block)

    return text_block, placeholders


def postprocess_block(translated_text: str, placeholders: dict) -> str:
    """بازگردانی بلاک‌های قفل‌شده"""
    for key, original in placeholders.items():
        translated_text = translated_text.replace(key, original)
    return translated_text


# ---------------------------
# File utilities
# ---------------------------
def iter_markdown_files(root: Path):
    """فهرست بازگشتی همه فایل‌های .md"""
    for p in root.rglob("*.md"):
        if p.is_file():
            yield p


def chunk_lines(lines: List[str], size: int):
    """تقسیم لیست خطوط به بلوک‌های N-تایی."""
    for i in range(0, len(lines), size):
        yield lines[i:i + size]


def ensure_parent_dir(path: Path):
    """ایجاد مسیر والد فایل خروجی در صورت عدم وجود."""
    path.parent.mkdir(parents=True, exist_ok=True)


def make_output_path(src_path: Path, src_root: Path, dst_root: Path, suffix_lang: str) -> Path:
    """ساخت مسیر خروجی با حفظ ساختار و تغییر پسوند زبان"""
    rel = src_path.relative_to(src_root)
    stem = rel.stem
    stem = re.sub(r"\.[a-z]{2}$", "", stem)
    new_name = f"{stem}.{suffix_lang}.md"
    return dst_root.joinpath(rel.parent, new_name)


# ---------------------------
# Translation logic
# ---------------------------
def translate_text_block(text: str) -> str:
    """ترجمه یک بلوک متن با deep-translator"""
    text_block, placeholders = preprocess_block(text)
    last_err = None

    for attempt in range(1, RETRIES + 1):
        try:
            translated = GoogleTranslator(
                source=SOURCE_LANG or "auto",
                target=TARGET_LANG
            ).translate(text_block)
            translated = postprocess_block(translated, placeholders)
            return translated
        except Exception as e:
            last_err = e
            if attempt < RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise last_err


def translate_file(src_path: Path, src_root: Path, dst_root: Path):
    """ترجمه یک فایل Markdown و ذخیره خروجی"""
    with src_path.open("r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    translated_chunks: List[str] = []
    for block in chunk_lines(lines, CHUNK_SIZE):
        text_block = "".join(block)
        translated = translate_text_block(text_block)
        translated_chunks.append(translated)
        time.sleep(SLEEP_BETWEEN)

    out_path = make_output_path(src_path, src_root, dst_root, suffix_lang=TARGET_LANG)
    ensure_parent_dir(out_path)
    with out_path.open("w", encoding="utf-8") as f:
        f.write("".join(translated_chunks))


# ---------------------------
# Main execution
# ---------------------------
def translate_markdown_folder():
    src_root = Path(SRC_FOLDER).resolve()
    dst_root = Path(DST_FOLDER).resolve()

    if not src_root.exists() or not src_root.is_dir():
        raise FileNotFoundError(f"❌ دایرکتوری ورودی نامعتبر است: {src_root}")

    files = list(iter_markdown_files(src_root))
    if not files:
        print("⚠️ هیچ فایل Markdown در مسیر ورودی یافت نشد.")
        return

    for p in tqdm(files, desc="Translating .md files", unit="file"):
        try:
            translate_file(p, src_root, dst_root)
        except Exception as e:
            tqdm.write(f"⚠️ خطا در ترجمه فایل {p}: {e}")


if __name__ == "__main__":
    translate_markdown_folder()
