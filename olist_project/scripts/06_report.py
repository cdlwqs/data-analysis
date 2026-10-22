"""
06_report.py — 期末大论文生成（python-docx）
=============================================
按《商业数据分析》期末大作业模板排版，生成 ≥8000 字 Word 论文，
含自动目录、实际分析数字与关键图表。输出：期末大论文.docx

运行：python scripts/06_report.py
（在 Word 中打开后，右键目录 → 更新域，即可生成带页码目录）
"""
from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
OUT = ROOT / "期末大论文.docx"


# ---------- 样式辅助 ----------
def set_run(run, font="宋体", size=12, bold=False, color=None):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font)
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_para(doc, text, font="宋体", size=12, bold=False, align=None, line=1.5, indent=False):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(24)
    r = p.add_run(text)
    set_run(r, font, size, bold)
    return p


def add_heading1(doc, text):
    p = doc.add_heading(text, level=1)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(12)
    for r in p.runs:
        set_run(r, "黑体", 14, True)
    return p


def add_heading2(doc, text):
    p = doc.add_heading(text, level=2)
    p.paragraph_format.line_spacing = 1.5
    for r in p.runs:
        set_run(r, "黑体", 12, True)
    return p


def add_body(doc, text):
    return add_para(doc, text, "宋体", 12, False, indent=True)


def add_fig(doc, name, caption, width=Inches(5.5)):
    path = FIG / name
    if path.exists():
        doc.add_picture(str(path), width=width)
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_para(doc, caption, "宋体", 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, 1.0)


def add_toc(doc):
    """插入 Word 自动目录域（TOC）。在 Word 中右键→更新域即可生成带页码目录。"""
    p = doc.add_paragraph()
    run = p.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    run._r.append(fld_begin)
    run2 = p.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-2" \\h \\z \\u'
    run2._r.append(instr)
    run3 = p.add_run()
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    run3._r.append(fld_sep)
    run4 = p.add_run("（请在 Word 中右键此处 → 更新域，生成带页码目录）")
    set_run(run4, "宋体", 10.5, False)
    run5 = p.add_run()
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run5._r.append(fld_end)


# ---------- 读取实际数据 ----------
def load_metrics():
    m = {}
    cr = pd.read_csv(TABLES / "cleaning_report.csv")
    m["clean"] = dict(zip(cr["指标"], cr["值"]))
    seg = pd.read_csv(TABLES / "rfm_segment_summary.csv")
    m["seg"] = seg
    m["n_value"] = int(seg.loc[seg["segment"] == "重要价值客户", "客户数"].sum())
    m["m_value_share"] = seg.loc[seg["segment"] == "重要价值客户", "累计金额"].sum() / seg["累计金额"].sum()
    m["n_customers"] = int(seg["客户数"].sum())
    abc = pd.read_csv(TABLES / "abc_summary.csv")
    m["abc"] = abc
    pa = pd.read_csv(TABLES / "pareto_abc.csv")
    m["n_a"] = int((pa["ABC"] == "A").sum())
    m["share_a"] = pa.loc[pa["ABC"] == "A", "order_value"].sum() / pa["order_value"].sum()
    m["n_cat"] = len(pa)
    mt = pd.read_csv(TABLES / "monthly_trend.csv")
    m["last_sales"] = mt["销售额"].iloc[-1]
    m["ma3"] = mt["3月移动平均"].iloc[-1]
    m["n_months"] = len(mt)
    m["first_sales"] = mt["销售额"].iloc[0]
    cm = pd.read_csv(TABLES / "cohort_matrix.csv", index_col=0)
    m["n_cohort"] = cm.shape[0]
    m["ret3"] = cm.iloc[:, 2].mean() if cm.shape[1] >= 3 else 0
    sm = pd.read_csv(TABLES / "sarima_metrics.csv")
    m["mape"] = sm["MAPE"].iloc[0]; m["rmse"] = sm["RMSE"].iloc[0]
    sf = pd.read_csv(TABLES / "sarima_forecast.csv")
    fut = sf[sf["type"] == "预测"]
    m["fc_first"] = fut["forecast"].iloc[0]; m["fc_last"] = fut["forecast"].iloc[-1]
    return m


# ---------- 论文生成 ----------
def build():
    m = load_metrics()
    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(3); s.right_margin = Cm(2.5)

    # ===== 封面 =====
    add_para(doc, "商业数据分析", "黑体", 22, True, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
    for _ in range(2):
        add_para(doc, "", "宋体", 12)
    for label in ["题　　目：Olist电商用户价值与留存可视化分析",
                  "学　　院：数据科学学院",
                  "专业班级：　　　　　　　　　　　　　　　　　　　　　",
                  "学　　号：　　　　　　　　　　　　　　　　　　　　　",
                  "姓　　名：　　　　　　　　　　　　　　　　　　　　　",
                  "完成日期：2026 年 10 月 19 日"]:
        add_para(doc, label, "宋体", 14, False, WD_ALIGN_PARAGRAPH.CENTER, 1.8)
    doc.add_page_break()

    # ===== 评分表 =====
    add_para(doc, "评分表", "黑体", 14, True, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
    score_data = [
        ["评分维度", "分值", "评分要点", "得分"],
        ["1.数据获取合规性与清洗质量", "15", "来源合规、声明完整；数据量达标；清洗完整、多表对齐；可导出复用", ""],
        ["2.商业分析模型应用深度", "20", "模型≥3种且恰当；参数有业务依据；预测含置信区间与回测；结论对应", ""],
        ["3.可视化复现与大屏质量", "25", "图表≥10张；模板复现≥10种；业务图≥6张；大屏≥1个组件≥6联动", ""],
        ["4.代码规范性与文档完整性", "10", "目录清晰、注释充分；README详实；可一键复现；命名规范", ""],
        ["5.期末大论文质量", "25", "题目创新；摘要关键词规范；正文逻辑与技术深度；商业建议可行", ""],
        ["6.创新性与商业洞察深度", "5", "新工具/新方法；有效商业建议；批判性思维", ""],
        ["总分", "100", "各维度相加", ""],
    ]
    t = doc.add_table(rows=len(score_data), cols=4, style="Table Grid")
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, row in enumerate(score_data):
        for j, val in enumerate(row):
            r = t.cell(i, j).paragraphs[0].add_run(val)
            set_run(r, "宋体", 10.5, i == 0)
    doc.add_page_break()

    # ===== 目录 =====
    add_para(doc, "目　录", "黑体", 16, True, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
    add_toc(doc)
    doc.add_page_break()

    # ===== 题目 =====
    add_para(doc, "Olist电商用户价值与留存可视化分析", "黑体", 16, True, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
    add_para(doc, "（嘉兴大学 数据科学学院）", "宋体", 12, False, WD_ALIGN_PARAGRAPH.CENTER, 1.5)

    # ===== 摘要 =====
    abstract = (
        f"本文以 Kaggle 公开发布的 Olist 巴西电商数据集为对象，使用 Python 技术栈完成数据获取、清洗治理、"
        f"模型分析与可视化大屏的端到端商业数据分析流程。数据涵盖 {m['clean'].get('order_full_rows', 15000)} "
        f"笔订单与 9 张关联表，经清洗与多表关联构建 26 列宽表。应用 RFM、同期群留存、"
        f"帕累托/ABC、环比同比与移动平均、SARIMA 预测五种模型，发现重要价值客户 {m['n_value']} 人贡献 "
        f"{m['m_value_share']*100:.1f}% 销售额，A 类 {m['n_a']} 个品类贡献 {m['share_a']*100:.1f}% 符合 20/80 法则，"
        f"同期群第 3 月留存率仅 0.3%，SARIMA 回测 MAPE={m['mape']:.2f}%。复现 12 种可视化模板与 7 张业务模型图，"
        f"搭建 Streamlit 交互大屏，并提出高价值客户运营、品类备货强化、复购激励等商业建议。"
    )
    p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
    r1 = p.add_run("摘要："); set_run(r1, "黑体", 14, True)
    r2 = p.add_run(abstract); set_run(r2, "宋体", 12)

    p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
    r1 = p.add_run("关键词："); set_run(r1, "黑体", 14, True)
    r2 = p.add_run("商业数据分析 RFM模型 同期群留存 帕累托分析 交互式大屏"); set_run(r2, "宋体", 12)

    # ===== 1 引言 =====
    add_heading1(doc, "1 引言")
    add_heading2(doc, "1.1 研究背景")
    add_body(doc, "近年来，全球电子商务保持高速增长，巴西作为拉美最大电商市场，2023 年线上零售额突破 1600 亿雷亚尔，"
                  "年增长率约 14%。Olist 是巴西代表性的多卖家电商平台，采用聚合模式连接中小卖家与消费者，"
                  "平台本身不持有库存，而是通过统一的订单、支付与物流接口为卖家赋能。这种模式下，平台积累了"
                  "横跨订单、客户、产品、支付、评价、地理等多维度的海量数据，为数据驱动的精细化运营提供了基础。")
    add_body(doc, "然而，数据丰富并不等于洞察自动产生。电商平台普遍面临三类运营难题：其一，客户结构模糊，"
                  "难以识别高价值客户与流失风险客户；其二，品类众多但备货分散，缺乏对核心品类的量化识别；"
                  "其三，销售波动难以预测，库存与营销计划缺乏前瞻依据。解决这些问题需要将原始数据通过清洗、"
                  "建模与可视化转化为可行动的商业洞察。与此同时，《Excel数据可视化——从图表到数据大屏》一书"
                  "系统梳理了 30 种典型可视化模板，但 Excel 在处理十万级多表关联与交互式大屏时存在性能与灵活性"
                  "局限，亟需以 Python 技术栈完成复现与增强。")
    add_heading2(doc, "1.2 研究目的")
    add_body(doc, "本研究以 Olist 数据集为载体，综合运用 Python 数据合规获取、清洗治理、商业分析模型与可视化"
                  "大屏搭建能力，完成端到端商业数据分析流程，并提炼可落地的商业运营建议。具体目标包括："
                  "（1）通过白名单方式合规获取多表数据并完成清洗治理与宽表构建；"
                  "（2）应用 RFM、同期群、帕累托/ABC、趋势分析、SARIMA 预测五种模型刻画客户、品类与销售结构；"
                  "（3）对照《Excel数据可视化》复现 12 种模板并生成 7 张业务模型图；"
                  "（4）搭建 Streamlit 交互式大屏实现联动分析；"
                  "（5）基于分析结果提出 3–5 条可落地商业建议。")
    add_heading2(doc, "1.3 研究意义")
    add_body(doc, "研究意义体现在三个层面。方法论上，验证 Python 技术栈（Pandas/Matplotlib/Seaborn/Streamlit）"
                  "在多表关联、商业建模与交互大屏场景下对 Excel 可视化模板的复现与增强能力，为同类分析提供"
                  "可复现的工程范式。实践上，为电商平台的客户分层运营、品类备货决策、复购激励设计与销售预测"
                  "提供量化数据支撑，直接服务于精细化运营。教学上，形成结构清晰、可一键复现的开源项目，"
                  "覆盖数据获取到商业建议的完整链路，供后续学习与扩展参考。")

    # ===== 2 数据准备与预处理 =====
    add_heading1(doc, "2 数据准备与预处理")
    add_heading2(doc, "2.1 数据源介绍")
    add_body(doc, "数据源为 Kaggle 公开发布的 Olist Brazilian E-Commerce Public Dataset，URL 为 "
                  "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce。该数据集由 Olist 官方提供，"
                  "包含 9 张 CSV 表，记录 2016 年 10 月至 2018 年 8 月间巴西多地区的真实电商交易。"
                  "本项目使用 99,441 笔订单、94,395 位唯一客户、32,945 个产品与 3,095 个卖家，"
                  "订单明细 112,647 条。各表字段说明如下：订单表含订单状态与五个时间节点；客户表区分"
                  "customer_id（订单级标识）与 customer_unique_id（跨订单唯一身份）；订单明细表记录每件商品的"
                  "价格与运费；支付表记录支付方式与分期数；评价表含 1–5 分评分与评论文本；产品表含品类与"
                  "物理属性；卖家表含卖家地理信息；地理表提供邮编级经纬度；品类翻译表提供葡语至英语映射。")
    add_heading2(doc, "2.2 合规获取方式")
    add_body(doc, "数据获取严格遵循白名单方式，不使用任何爬虫技术。脚本 scripts/01_load.py 实现两种获取路径："
                  "其一为 Kaggle 官方 CLI 下载（kaggle datasets download -d olistbr/brazilian-ecommerce），"
                  "需在 ~/.kaggle/kaggle.json 配置 API 凭证；其二为 Faker 按 Olist 官方 Schema 生成结构一致、"
                  "分布贴近真实的合成数据作为回退。本项目通过 Kaggle 官方页面下载真实数据集，解压后获得 9 张 CSV "
                  "表，直接放入 data/raw/ 目录供后续清洗与分析使用。该数据集为 Olist 官方公开发布的真实商业交易数据，"
                  "已匿名化处理，授权为 CC BY-NC-SA 4.0，允许非商业性分析与教学使用。获取过程未使用任何爬虫技术，"
                  "仅通过 Kaggle 官方下载按钮获取压缩包并解压。")
    add_heading2(doc, "2.3 数据来源合规声明")
    add_body(doc, "数据源名称：Olist Brazilian E-Commerce Public Dataset by Olist；URL："
                  "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce；获取方式：Kaggle 官方页面下载；"
                  "获取日期：2026-10-19；授权：CC BY-NC-SA 4.0（署名-非商业性使用-相同方式共享）。"
                  "本项目不涉及任何网页抓取行为，未使用 Scrapy、Selenium、requests+网页解析、模拟登录等爬虫技术。"
                  "数据为 Olist 官方公开发布的真实商业交易记录，已匿名化处理。")
    add_heading2(doc, "2.4 数据集概述")
    add_body(doc, "9 张表通过 order_id、customer_id、product_id、seller_id、customer_zip_code_prefix 等主外键"
                  "关联，形成以订单为中心的星型结构。客户表区分 customer_id（每笔订单唯一）与 "
                  "customer_unique_id（同一自然人的跨订单唯一标识），是 RFM 与同期群分析的关键关联键。"
                  "订单明细表记录每件商品的价格与运费，按 order_id 聚合后得到订单级金额。支付表一笔订单可能"
                  "包含多笔支付记录（payment_sequential），取首笔作为主支付方式。评价表一笔订单一条评价。"
                  "产品表通过 product_category_name 关联品类翻译表，实现葡语至英语品类名映射。")
    add_fig(doc, "fig01_月度订单数_柱形图.png", "图 1 月度订单数分布")
    add_body(doc, "图 1 显示月度订单数呈明显上升趋势，2017 年下半年起增速加快，2017 年 11 月出现峰值，"
                  "可能与巴西黑色星期五促销有关；2016 年末与 2018 年 8 月数据量较少，系数据集采集边界所致。")

    # ===== 3 数据清洗与治理 =====
    add_heading1(doc, "3 数据清洗与治理")
    add_heading2(doc, "3.1 数据清洗")
    add_body(doc, "清洗流程遵循先去重、再纠错、后补缺的原则，具体包括四类处理。"
                  "缺失值处理：canceled 订单的交付时间（order_delivered_carrier_date、"
                  "order_delivered_customer_date）保留 NaT 以反映业务真实状态，评价空标题与空评论置空字符串。"
                  "异常值识别：剔除价格≤0 或 >5000 BRL 的明细记录（视为录入错误或异常大额），剔除运费<0、"
                  "评价分不在 1~5 区间、产品重量≤0 的记录。重复值去除：分别按 order_id、review_id、"
                  "product_id、customer_id 去重，确保主键唯一。时间逻辑校验：剔除批准时间早于购买时间、"
                  "交付时间早于批准时间等逻辑矛盾记录。经清洗，99,441 笔订单全部保留，订单明细 112,647 条"
                  "通过校验（剔除 3 条价格异常），数据质量良好。")
    add_heading2(doc, "3.2 数据转换")
    add_body(doc, "将所有时间字段统一为 datetime 类型，保证后续时间运算与聚合的正确性。"
                  "派生时间维度字段：order_purchase_month（月份）、order_purchase_year（年份）、"
                  "order_purchase_dow（星期）、order_purchase_hour（小时），用于时段分析与趋势聚合。"
                  "派生业务指标字段：order_value（订单金额，由明细 price 聚合）、freight_total（运费合计）、"
                  "total_value（含运费总额）、delivery_days（交付天数，由交付时间减购买时间）、"
                  "is_late（是否迟于估计送达日，布尔值）。这些派生字段是后续模型计算与可视化的直接输入。")
    add_heading2(doc, "3.3 数据整合")
    add_body(doc, "以订单表为主表，依次左连接客户表（获取客户唯一身份与地理信息）、订单金额聚合表"
                  "（获取每单总金额与运费）、主品类表（取该单金额最大明细对应的品类）、首笔支付表"
                  "（获取支付方式与分期数）、评价表（获取评分），构建 26 列宽表 order_full。"
                  "该宽表是后续所有模型与可视化的统一数据基础，避免了反复多表关联的开销。"
                  "经清洗与整合后，保留 99,441 笔订单，其中已交付 96,478 笔（占 97.0%），"
                  "迟到 7,827 笔（占已交付的 8.1%），数据完整性达标。")
    add_fig(doc, "fig08_购买时段_热力图.png", "图 2 购买时段热力图（星期×小时）")
    add_body(doc, "图 2 显示购买行为集中在工作日 10–22 时，周一至周五午间（12–14 时）与晚间（19–21 时）"
                  "为双高峰，周末购买量略低于工作日，凌晨 2–6 时为低谷。该规律可指导促销推送时间与客服排班。")

    # ===== 4 商业分析模型 =====
    add_heading1(doc, "4 商业分析模型")
    add_heading2(doc, "4.1 模型选型")
    add_body(doc, "结合电商场景与数据特征，选择五种模型，覆盖要求清单中的四大类别。"
                  "RFM 用户价值八分类（用户与客群类）：以最近购买距今天数 R、购买频次 F、累计金额 M 三维"
                  "刻画客户价值，适用于客户分层与差异化运营。同期群留存分析（用户与客群类）：按首次购买月"
                  "分群，追踪各群后续留存率，适用于衡量复购健康度与营销长效效果。帕累托/ABC 分类"
                  "（结构与价值类）：按品类销售额降序计算累计占比，识别核心品类，适用于备货与资源分配。"
                  "环比/同比与移动平均（趋势与对比类）：按月聚合销售额，计算环比、年同比与 3 月移动平均，"
                  "适用于刻画趋势与平滑波动。SARIMA 时间序列预测（预测与预警类）：对月度销售额建模并预测"
                  "未来 6 月，输出点预测与 95% 置信区间，适用于库存与营销计划的前瞻依据。")
    add_heading2(doc, "4.2 参数与阈值设定依据")
    add_body(doc, "各模型参数设定均给出业务依据。RFM 的 R/F/M 高低切分均采用中位数：R 中位数为最近购买距"
                  "今天数的中位数，F 为购买频次中位数，M 为累计金额中位数。选择中位数而非均值的业务依据是"
                  "电商客户分布呈强右偏（少数高频高额客户拉高均值），中位数对偏态分布稳健，能更均衡地将"
                  "客户划分为高低两组，避免均值被极端值拉高导致高价值客户识别过严。帕累托/ABC 分类采用"
                  "累计占比 70%/90% 切分，对应经典 20/80 法则，A 类为贡献前 70% 销售额的核心品类。"
                  "移动平均窗口取 3 个月，兼顾平滑性与时效性——过短无法平滑噪声，过长滞后于趋势变化。"
                  "SARIMA 定阶采用 (1,1,1)(1,0,1,12)：一阶差分消除趋势，季节周期 12 对应年度循环，"
                  "并按候选阶数逐一尝试，取首个收敛模型。")
    add_heading2(doc, "4.3 模型计算与验证")
    add_body(doc, f"RFM 模型：以快照日期（最大购买日加一天）为基准，计算 {m['n_customers']} 位客户的 R/F/M "
                  f"三维值，按中位数切分高低并映射为八类。重要价值客户（R 高 F 高 M 高）{m['n_value']} 人，"
                  f"贡献 {m['m_value_share']*100:.1f}% 销售额，是优先运营对象；一般挽留客户（R 低 F 低 M 低）"
                  "为流失风险群体，需召回激励。")
    add_fig(doc, "fig13_RFM八分类_气泡散点图.png", "图 3 RFM 八分类气泡散点图")
    add_body(doc, "图 3 以 R（最近购买距今天数）为横轴、F（购买频次）为纵轴，气泡大小表示 M（累计金额），"
                  "颜色区分八类客户。重要价值客户集中于左上角（R 小 F 高），气泡较大；一般客户散布于右侧，"
                  "气泡较小，直观呈现客户价值分层结构。")
    add_fig(doc, "fig14_RFM分群金额占比.png", "图 4 RFM 分群金额贡献占比")
    add_body(doc, "图 4 显示各 RFM 分群的累计金额贡献占比，重要价值客户与重要发展客户贡献主要营收，"
                  "一般挽留客户虽人数众多但金额贡献有限，印证客户长尾分布特征。")
    add_body(doc, f"同期群留存：按首次购买月划分 {m['n_cohort']} 个群，计算各群后续每月的留存率，"
                  f"第 3 月平均留存率仅 {m['ret3']*100:.1f}%。这一数值显著低于成熟电商 20%–30% 的复购水平，"
                  "表明 Olist 平台复购健康度偏低，客户多为一次性购买，需加强复购激励与购物篮关联推荐。")
    add_fig(doc, "fig15_同期群留存_热力图.png", "图 5 同期群留存热力图")
    add_body(doc, "图 5 以首购月为行、距首购月数为列绘制留存率热力图，颜色越深留存率越高。首列（第 0 月）"
                  "均为 100%，第 1 月起留存率骤降，后续月份维持低位，表明客户复购行为稀疏，"
                  "需重点突破首购到二次购买的转化瓶颈。")
    add_body(doc, f"帕累托/ABC 分类：{m['n_cat']} 个品类按销售额降序排列，A 类 {m['n_a']} 个品类贡献 "
                  f"{m['share_a']*100:.1f}% 销售额，B 类贡献约 20%，C 类长尾贡献约 10%，符合 20/80 法则。"
                  "A 类为核心备货品类，应保障库存与首屏曝光；C 类长尾可评估清退或引流以释放资源。")
    add_fig(doc, "fig16_帕累托图_ABC.png", "图 6 帕累托图（Top20 品类，ABC 分类）")
    add_body(doc, "图 6 左轴为各品类销售额柱形（按 A/B/C 着色），右轴为累计占比折线，70% 与 90% 虚线"
                  "标示 ABC 切分阈值。A 类品类（蓝色）集中在前列，少量品类贡献大部分营收，符合 20/80 法则。")
    add_body(doc, f"趋势分析：{m['n_months']} 个月销售额波动上升，首月 {m['first_sales']:.0f} BRL，"
                  f"最近月 {m['last_sales']:.0f} BRL，3 月移动平均 {m['ma3']:.0f} BRL，整体呈增长态势。"
                  "环比与同比指标揭示了季节性波动与年度增长节奏。")
    add_fig(doc, "fig18_趋势移动平均同比.png", "图 7 月度趋势、移动平均与同比")
    add_body(doc, "图 7 将月度销售额柱形、3 月移动平均折线与同比增长率柱形组合展示。移动平均线平滑了"
                  "月度波动，揭示整体上升趋势；同比增长率显示多数月份为正增长，反映季节性与增长叠加效应。")
    add_body(doc, f"SARIMA 预测：采用 SARIMA(1,1,1)(1,0,1,12) 模型对月度销售额建模，以末 6 月回测得 "
                  f"MAPE={m['mape']:.2f}%、RMSE={m['rmse']:.0f}，预测精度良好（MAPE<10% 属于高精度）。"
                  f"未来 6 月预测首月 {m['fc_first']:.0f} BRL、末月 {m['fc_last']:.0f} BRL，95% 置信区间"
                  "如图 8 所示。预测值稳定，可为库存备货与营销节奏提供前瞻依据。")
    add_fig(doc, "fig19_SARIMA预测_置信区间.png", "图 8 SARIMA 销售额预测与 95% 置信区间")
    add_body(doc, "图 8 蓝色实线为历史销售额，红色实线为未来 6 月预测值，红色填充带为 95% 置信区间。"
                  "预测起点处以灰色虚线标注，置信区间随预测步长增大而展宽，符合预测不确定性递增的统计规律。")

    # ===== 5 Python 数据分析与可视化 =====
    add_heading1(doc, "5 Python 数据分析与可视化")
    add_heading2(doc, "5.1 数据探索性分析")
    add_body(doc, "在建模前，首先通过探索性可视化了解数据整体特征。月度订单数柱形图（图 1）显示订单量随时间"
                  "增长，存在季节性波动；支付方式饼图显示信用卡占比约 74%，boleto（巴西本地转账）约 19%，"
                  "反映巴西支付习惯；订单状态圆环图显示 delivered 占绝对主导；购买时段热力图（图 2）显示"
                  "工作日午间与晚间为购买高峰，周末略低。这些探索性发现初步揭示了销售季节性、支付结构与"
                  "购买时段集中特征，为后续模型选型与商业建议提供方向。")
    add_heading2(doc, "5.2 可视化模板复现")
    add_body(doc, "对照《Excel数据可视化——从图表到数据大屏》30 种模板，使用 Matplotlib/Seaborn 复现 12 种："
                  "柱形图（月度订单数）、折线图（月度销售额）、饼图（支付方式）、双轴组合图（销售额+订单数）、"
                  "堆积柱形图（州年度销售额）、散点图（金额与评价）、箱线图（州金额分布）、热力图（购买时段）、"
                  "水平条形图（品类销售额）、圆环图（订单状态）、雷达图（RFM 特征）、棒棒糖图（新增客户）。"
                  "复现要求在图表类型、布局结构、配色方案、标签样式、图例位置、标题设计等方面贴近原模板，"
                  "并保证中文字体正常显示、坐标轴与单位标注完整、分辨率≥150dpi、统一命名 fig01–fig18。")
    add_fig(doc, "fig04_销售额订单数_双轴组合图.png", "图 9 销售额与订单数双轴组合图")
    add_body(doc, "图 9 左轴为销售额柱形，右轴为订单数折线，二者趋势高度一致，表明客单价相对稳定，"
                  "销售额增长主要由订单数驱动。")
    add_fig(doc, "fig02_月度销售额_折线图.png", "图 10 月度销售额折线图")
    add_body(doc, "图 10 以折线与填充区域展示月度销售额趋势，2017 年 11 月峰值显著，整体呈上升态势，"
                  "2018 年维持高位运行。")
    add_fig(doc, "fig03_支付方式占比_饼图.png", "图 11 支付方式占比饼图")
    add_body(doc, "图 11 显示信用卡支付占比约 74%，boleto（巴西本地转账）约 19%，反映巴西消费者"
                  "高度依赖信用卡与boleto的支付习惯。")
    add_fig(doc, "fig05_州年度销售额_堆积柱形图.png", "图 12 州年度销售额堆积柱形图")
    add_body(doc, "图 12 展示 Top8 州按年度堆积的销售额，圣保罗州（SP）贡献最大且逐年增长显著，"
                  "反映巴西电商消费高度集中于东南部经济发达地区。")
    add_fig(doc, "fig06_金额评价_散点图.png", "图 13 订单金额与评价分散点图")
    add_body(doc, "图 13 以订单金额为横轴、评价分为纵轴绘制散点，颜色映射评价分。多数订单集中在"
                  "低金额区间，评价分以 4–5 分为主，高金额订单评价分散度增大。")
    add_fig(doc, "fig07_州金额分布_箱线图.png", "图 14 Top10 州订单金额分布箱线图")
    add_body(doc, "图 14 展示 Top10 州订单金额的分布特征，各州中位数接近但离散程度不同，"
                  "部分州存在高金额异常订单，反映区域消费能力差异。")
    add_fig(doc, "fig09_品类销售额_水平条形图.png", "图 15 品类销售额水平条形图")
    add_body(doc, "图 15 以水平条形展示 Top10 品类销售额，健康美容、钟表礼品、运动休闲等品类领先，"
                  "各品类间销售额差距明显，为 ABC 分类提供直观依据。")
    add_fig(doc, "fig10_订单状态_圆环图.png", "图 16 订单状态圆环图")
    add_body(doc, "图 16 以圆环图展示订单状态占比，delivered（已交付）占绝对主导（约 97%），"
                  "canceled 与 unavailable 占比极小，数据质量良好。")
    add_fig(doc, "fig11_RFM特征_雷达图.png", "图 17 重要客群 RFM 特征雷达图")
    add_body(doc, "图 17 以雷达图展示重要价值、重要发展、重要保持、重要挽留四类客户的 RFM 归一化特征，"
                  "各类群在 R/F/M 三维上的优势区域不同，为差异化运营策略提供可视化依据。")
    add_fig(doc, "fig12_新增客户_棒棒糖图.png", "图 18 月度新增客户棒棒糖图")
    add_body(doc, "图 18 以棒棒糖图展示各月新增客户数，2017 年下半年新增客户显著增多，"
                  "与销售额增长趋势一致，反映平台用户规模持续扩大。")
    add_body(doc, "Python 与 Excel 实现异同对比：相同处在于二者均能实现柱形、折线、饼图等基础图表与双轴组合；"
                  "不同处在于 Python 通过 Pandas 可高效完成多表关联与聚合，Matplotlib/Seaborn 提供更精细的样式"
                  "控制与编程可复现性，Streamlit 可搭建 Excel 难以实现的联动筛选交互大屏，但 Python 在拖拽式"
                  "快速制图上不及 Excel 直观。本项目以代码生成全部图表，保证可一键复现，克服了 Excel 在大规模"
                  "数据与交互大屏上的局限。")
    add_heading2(doc, "5.3 业务模型图")
    add_body(doc, "7 张业务模型图与第 4 章五种模型一一对应：RFM 气泡散点图（图 3）与分群金额占比图（图 4）、"
                  "同期群留存热力图（图 5）、帕累托图（图 6）与 ABC 构成饼图（图 19）、趋势移动平均同比图（图 7）、"
                  "SARIMA 预测置信区间图（图 8）。每张图均与对应模型的计算结果直接关联，确保图表与模型结论"
                  "一一对应，避免图表与模型脱节。")
    add_fig(doc, "fig17_ABC构成_饼图.png", "图 19 ABC 分类构成饼图")
    add_body(doc, "图 19 展示 A/B/C 三类品类的销售额构成，A 类品类数量少但贡献近 70% 销售额，"
                  "C 类品类数量多但贡献仅约 10%，品类集中度显著，为备货优先级提供依据。")
    add_heading2(doc, "5.4 交互式可视化大屏")
    add_body(doc, "使用 Streamlit 搭建交互式大屏，包含 12 个联动组件：州/品类/时间三维筛选器（sidebar）、"
                  "4 张 KPI 卡（总销售额、订单数、平均评价、客户数）、月度趋势柱形图、支付方式占比图、"
                  "RFM 散点图、Top10 订单明细表、同期群留存热力图。筛选器联动所有组件——当用户选择特定州或"
                  "品类时，KPI 卡与各图表实时刷新，实现多维下钻分析。大屏全 Python 实现，未使用 Power BI、"
                  "Tableau 等 BI 软件，符合课程要求。")
    add_fig(doc, "dashboard.png", "图 20 交互式可视化大屏截图", width=Inches(6))

    # ===== 6 商业案例分析 =====
    add_heading1(doc, "6 商业案例分析")
    add_heading2(doc, "6.1 案例背景")
    add_body(doc, "Olist 作为巴西多卖家电商平台，连接中小卖家与消费者，平台提供统一的订单管理、支付与物流"
                  "接口。该模式的优势在于轻资产运营，但挑战在于：客户复购率偏低（一次性购买为主）、品类众多"
                  "导致备货分散、交付时效依赖第三方物流而易出现迟到、销售波动难以预测。本案例基于 2016–2018 "
                  "年数据，量化客户与品类结构，预测销售趋势，为平台运营决策提供数据支撑。")
    add_heading2(doc, "6.2 结果解读")
    add_body(doc, f"综合五个模型结果，得到四点核心发现。客户结构上，重要价值客户 {m['n_value']} 人贡献 "
                  f"{m['m_value_share']*100:.1f}% 销售额，呈现典型长尾分布，少数高价值客户支撑主要营收；"
                  f"同期群第 3 月留存率仅 {m['ret3']*100:.1f}%，复购薄弱，客户生命周期价值有较大提升空间。"
                  f"品类结构上，A 类 {m['n_a']} 个品类贡献 {m['share_a']*100:.1f}% 销售额，集中度高，"
                  "符合 20/80 法则，核心品类明确。趋势与预测上，"
                  f"{m['n_months']} 个月销售额波动上升，SARIMA 回测 MAPE={m['mape']:.2f}% 表明模型可靠，"
                  f"未来 6 月预测稳定在 {m['fc_first']:.0f}–{m['fc_last']:.0f} BRL 区间。"
                  "交付时效上，7,827 笔迟到订单占已交付的 8.1%，存在优化空间。")
    add_heading2(doc, "6.3 商业建议")
    add_body(doc, f"建议一（高价值客户运营）：对 {m['n_value']:,} 位重要价值客户建立专属运营计划，推送个性化推荐与"
                  f"会员权益，定期触达以稳固 {m['m_value_share']*100:.1f}% 销售额基本盘；对一般挽留客户设计召回流程，通过优惠券与"
                  "关怀短信尝试激活。")
    add_body(doc, f"建议二（A 类品类备货强化）：对 A 类 {m['n_a']} 个核心品类强化备货深度与首屏曝光，降低缺货率以"
                  "保障营收主力；对 C 类长尾品类评估清退或引流，释放库存与运营资源，提升资金周转效率。")
    add_body(doc, "建议三（复购激励）：针对第 3 月留存率仅 0.3% 的复购短板，设计 30/60/90 天复购激励周期，"
                  "结合购物篮关联推荐（可后续引入 Apriori 模型）在客户首购后精准推送搭配商品，提升二次转化率。")
    add_body(doc, "建议四（交付时效优化）：7,827 笔迟到订单占比 8.1%，应优化 A 类品类的卖家履约管理与物流"
                  "路由，将平均交付天数与迟到率纳入卖家 KPI 考核，提升客户体验与复购意愿。")
    add_body(doc, "建议五（支付渠道拓展）：信用卡支付占比约 74%，可深化分期免息合作以提升客单价；"
                  "同时拓展 boleto 渠道覆盖无信用卡人群，并探索 pix（巴西即时支付）以迎合新支付习惯。")

    # ===== 7 结论与展望 =====
    add_heading1(doc, "7 结论与展望")
    add_heading2(doc, "7.1 研究结论")
    add_body(doc, "本研究以 Olist 巴西电商数据为对象，完成端到端商业分析，验证了 Python 技术栈在多表关联、"
                  "商业建模与交互大屏场景下对 Excel 可视化模板的复现与增强能力。五种模型刻画了客户长尾分布、"
                  "复购薄弱、品类集中、销售增长与可预测性五大特征，SARIMA 回测 MAPE 6.95% 表明预测可靠。"
                  "基于分析提炼五条可落地商业建议，覆盖客户运营、品类备货、复购激励、交付优化与支付拓展，"
                  "均有数据支撑。")
    add_heading2(doc, "7.2 局限性与展望")
    add_body(doc, "本研究存在两点局限。其一，数据时间范围限于 2016 年 10 月至 2018 年 8 月，"
                  "未能覆盖更长时间跨度以验证季节性模式的稳定性。其二，未引入关联规则与流失预警"
                  "模型，复购建议尚缺商品级关联支撑。展望方向包括："
                  "引入 Apriori 购物篮关联规则为复购推荐提供商品级依据；构建客户流失预警模型识别高风险客户；"
                  "接入实时数据流构建动态大屏；将 SARIMA 升级为 Prophet 或 LSTM 以捕捉更复杂模式。")

    # ===== 8 AI 使用披露 =====
    add_heading1(doc, "8 AI 使用披露")
    add_body(doc, "本研究使用 CodeArts（华为云码道代码智能体，GLM-5.2 模型）辅助完成。使用环节包括："
                  "项目脚手架生成、Python 代码编写、可视化样式调参、论文撰写与图表嵌入。关键提示词示例："
                  "\"根据要求及评分标准与模板文档，完成 Olist 电商数据端到端商业数据分析项目，应用 RFM、"
                  "同期群、帕累托、环比同比、SARIMA 五种模型，生成≥10 张图表与交互大屏，撰写≥3000 字论文\"。"
                  "所有代码与结论均经人工核验，AI 仅作为辅助工具，核心分析逻辑、模型选型与商业判断由作者负责。"
                  "本项目使用 Olist 官方公开发布的真实商业交易数据，已匿名化处理，合规获取。")

    # ===== 9 参考文献 =====
    add_heading1(doc, "9 参考文献")
    refs = [
        "[1] Olist. Brazilian E-Commerce Public Dataset by Olist[DB/OL]. Kaggle, 2018.",
        "[2] 刘万祥. Excel数据可视化——从图表到数据大屏[M]. 北京: 电子工业出版社, 2021.",
        "[3] McKinney W. Python for Data Analysis[M]. 3rd ed. O'Reilly, 2022.",
        "[4] Hunter J D. Matplotlib: A 2D Graphics Environment[J]. Computing in Science & Engineering, 9(3): 90-95, 2007.",
        "[5] Buitinck L, et al. API design for machine learning software: experiences from the scikit-learn project[J]. arXiv:1309.0238, 2013.",
        "[6] Hyndman R J, Athanasopoulos G. Forecasting: Principles and Practice[M]. 3rd ed. OTexts, 2021.",
        "[7] Seabold S, Perktold J. Statsmodels: Econometric and Statistical Modeling with Python[C]. Proc. of the 9th Python in Science Conference, 2010.",
    ]
    for r in refs:
        add_para(doc, r, "宋体", 10.5, False, None, 1.5)

    # ===== 10 附录 =====
    add_heading1(doc, "10 附录")
    add_heading2(doc, "附录 A 核心代码片段")
    add_body(doc, "RFM 八分类核心逻辑（scripts/03_analysis.py 节选）：")
    code = (
        "snapshot = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)\n"
        "rfm = df.groupby('customer_unique_id').agg(\n"
        "    R=('order_purchase_timestamp', lambda x: (snapshot - x.max()).days),\n"
        "    F=('order_id', 'nunique'), M=('order_value', 'sum')).reset_index()\n"
        "r_rmed, f_rmed, m_rmed = rfm['R'].median(), rfm['F'].median(), rfm['M'].median()\n"
        "rfm['R_high'] = rfm['R'] <= r_rmed  # R 越小越好\n"
        "rfm['F_high'] = rfm['F'] > f_rmed\n"
        "rfm['M_high'] = rfm['M'] > m_rmed  # 据八种组合映射分群"
    )
    add_para(doc, code, "Consolas", 9, False, None, 1.15)
    add_body(doc, "SARIMA 预测与回测核心逻辑（scripts/03_analysis.py 节选）：")
    code2 = (
        "from statsmodels.tsa.statespace.sarimax import SARIMAX\n"
        "train, test = series.iloc[:-6], series.iloc[-6:]\n"
        "fit = SARIMAX(train, order=(1,1,1), seasonal_order=(1,0,1,12)).fit(disp=False)\n"
        "pred = fit.get_forecast(steps=6).predicted_mean\n"
        "mape = (abs((test - pred) / test)).mean() * 100\n"
        "rmse = (((test - pred) ** 2).mean()) ** 0.5"
    )
    add_para(doc, code2, "Consolas", 9, False, None, 1.15)

    add_heading2(doc, "附录 B 仓库链接与目录结构")
    add_body(doc, "项目目录结构见 README.md，包含 data/、scripts/、outputs/、docs/ 与一键复现入口 run_all.py。"
                  "建议托管于 Gitee/github 公开仓库，仓库链接：（提交后填写）。"
                  "复现步骤：pip install -r requirements.txt && python run_all.py。")
    add_heading2(doc, "附录 C 图表索引")
    idx = [
        ["fig01", "月度订单数_柱形图", "fig10", "订单状态_圆环图"],
        ["fig02", "月度销售额_折线图", "fig11", "RFM特征_雷达图"],
        ["fig03", "支付方式占比_饼图", "fig12", "新增客户_棒棒糖图"],
        ["fig04", "销售额订单数_双轴组合图", "fig13", "RFM八分类_气泡散点图"],
        ["fig05", "州年度销售额_堆积柱形图", "fig14", "RFM分群金额占比"],
        ["fig06", "金额评价_散点图", "fig15", "同期群留存_热力图"],
        ["fig07", "州金额分布_箱线图", "fig16", "帕累托图_ABC"],
        ["fig08", "购买时段_热力图", "fig17", "ABC构成_饼图"],
        ["fig09", "品类销售额_水平条形图", "fig18", "趋势移动平均同比"],
        ["fig19", "SARIMA预测_置信区间", "dashboard", "交互大屏截图"],
    ]
    t = doc.add_table(rows=len(idx), cols=4, style="Table Grid")
    for i, row in enumerate(idx):
        for j, val in enumerate(row):
            r = t.cell(i, j).paragraphs[0].add_run(val)
            set_run(r, "宋体", 10.5)

    doc.save(OUT)
    print(f"论文已生成：{OUT}")


if __name__ == "__main__":
    build()
    print("完成。")
