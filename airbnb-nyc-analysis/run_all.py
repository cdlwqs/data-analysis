"""
run_all.py — 一键复现入口
=========================
依次执行：数据获取 → 清洗 → 建模 → 绘图 → 大屏截图 → 论文生成
用法：python run_all.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"


def run(script, *args):
    cmd = [sys.executable, str(SCRIPTS / script)] + list(args)
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main():
    print("=" * 60)
    print("run_all.py — 一键复现纽约 Airbnb 商业分析项目")
    print("=" * 60)
    run("01_load.py")
    run("02_clean.py")
    run("03_analysis.py")
    run("04_visuals.py")
    run("05_dashboard.py", "--snapshot")
    run("06_report.py")
    print("\n" + "=" * 60)
    print("全部完成。成果：")
    print(f"  图表：{ROOT / 'outputs' / 'figures'}")
    print(f"  论文：{ROOT / '期末大论文.docx'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
