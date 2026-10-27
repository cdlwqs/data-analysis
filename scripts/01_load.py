"""
01_load.py — 数据加载（解压 gzip 原始文件）
"""
from pathlib import Path
import gzip
import shutil

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data" / "raw"
SRC_GZ = RAW_DIR / "listings.csv.gz"
DST_CSV = RAW_DIR / "listings.csv"


def main():
    # 若已解压则跳过
    if DST_CSV.exists():
        print(f"[跳过] 已存在解压文件: {DST_CSV}")
        return

    if not SRC_GZ.exists():
        raise FileNotFoundError(f"未找到源文件: {SRC_GZ}")

    # gzip 解压
    with gzip.open(SRC_GZ, "rb") as f_in, open(DST_CSV, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    size_mb = DST_CSV.stat().st_size / 1024 / 1024
    print(f"[完成] 解压成功: {DST_CSV} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
