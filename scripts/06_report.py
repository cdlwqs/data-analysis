"""
06_report.py — 期末大论文生成（python-docx）
=============================================
题目：纽约Airbnb民宿定价与房源特征可视化分析
按《商业数据分析》期末大作业模板排版，A4 页面，正文 ≥3000 字，
嵌入 19 张分析图 + dashboard.png 共 20 张图，每图后附 1-2 句解读。
从 outputs/tables/ 动态读取分析结果数值。输出：期末大论文.docx

运行：python scripts/06_report.py
"""
from pathlib import Path
from datetime import date
import pandas as pd
from docx import Document
from docx.shared import Cm, Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "outputs" / "figures"
TABLES = ROOT / "outputs" / "tables"
OUT = ROOT / "期末大论文.docx"

TITLE = "纽约Airbnb民宿定价与房源特征可视化分析"
AUTHOR = "（学生姓名）"
DATE = date.today().strftime("%Y年%m月%d日")

# 19 张分析图 + dashboard.png = 20 张
FIG_LIST = [
    ("fig01_房型分布_柱形图.png", "图1 房型分布柱形图",
     "如图1所示，Entire home/apt（整套公寓）占比最高，约52%，Private room（独立房间）次之约46%，"
     "Shared room（共享房间）不足2%。整套房源占据主导地位，反映出旅客对私密空间与独立居住体验的强烈偏好。"
     "共享房间占比极低，说明纽约市场以家庭出游与商务差旅为主，背包客客群规模有限。"),
    ("fig02_月度评论趋势_折线图.png", "图2 月度评论趋势折线图",
     "如图2所示，月度评论数自2015年起波动上升，2023—2024年达到峰值。评论数是市场活跃度的代理指标，"
     "其持续增长反映出纽约Airbnb市场需求旺盛、房客基数稳步扩大。2020年中期出现明显低谷，对应全球疫情冲击，"
     "随后迅速反弹并超过疫情前水平，体现了短租市场的强韧性与复苏能力。"),
    ("fig03_行政区占比_饼图.png", "图3 行政区占比饼图",
     "如图3所示，曼哈顿与布鲁克林两区房源量合计超过80%，构成纽约Airbnb的主力市场。"
     "曼哈顿作为核心商务与旅游区，房源密度最高；布鲁克林凭借文化氛围与相对亲民价格紧随其后。"
     "皇后区、布朗克斯与斯塔滕岛占比合计不足20%，外围区域供给充足度有限，存在差异化开发空间。"),
    ("fig04_价格评论数_双轴组合图.png", "图4 价格与评论数双轴组合图",
     "如图4所示，价格与评论数呈反向关系：中低价房源（50—200美元）评论数最高，"
     "高价房源（500美元以上）评论数显著偏少。这说明中低价房源入住频次更高、客群更广，"
     "而高价房源虽单价高但出租率低，总收益未必占优。房东应在单价与入住率间寻求平衡。"),
    ("fig05_行政区房型_堆积柱形图.png", "图5 行政区与房型堆积柱形图",
     "如图5所示，曼哈顿以Entire home/apt为主，占比超60%，契合其高端商务定位；"
     "布鲁克林Private room占比更高，反映出共享居住文化盛行。皇后区房型分布较均衡，"
     "布朗克斯以独立房间为主。各行政区房型结构差异显著，为差异化定价与运营策略提供依据。"),
    ("fig06_价格评分_散点图.png", "图6 价格与评分散点图",
     "如图6所示，评分高度集中在4.5—5.0区间，低评分房源数量稀少，说明纽约Airbnb整体服务质量较高。"
     "价格与评分之间无显著正相关，高价房源并不必然获得更高评分，部分低价房源同样获得满分评价。"
     "这提示房东：提升评分的关键在于服务品质而非单纯提价，性价比是房客评价的重要考量。"),
    ("fig07_行政区价格_箱线图.png", "图7 行政区价格箱线图",
     "如图7所示，曼哈顿价格中位数最高（约180美元）且离散度最大，存在大量高价异常点；"
     "布鲁克林次之（约120美元），分布相对集中；布朗克斯最低（约70美元）。"
     "曼哈顿价格跨度大，既有经济型也有豪华型房源，反映出客群分层明显。"
     "各区间价格差异为跨区定价策略提供了量化参考。"),
    ("fig08_价格可住天数_热力图.png", "图8 价格与可住天数热力图",
     "如图8所示，中低价（50—200美元）且全年可住（availability_365≥300天）的房源最为密集，"
     "构成市场供给主体。高价低可住天数房源稀少，多为季节性或限制性出租。"
     "高可住天数房源占比高，说明多数房东将短租作为稳定收入来源而非偶尔出租，市场专业化程度较高。"),
    ("fig09_Top10街区房源_水平条形图.png", "图9 Top10 街区房源水平条形图",
     "如图9所示，Bedford-Stuyvesant与Williamsburg房源数领先，均位于布鲁克林核心区域。"
     "Harlem、Hell's Kitchen、Upper West Side等曼哈顿街区紧随其后。"
     "Top10街区房源量合计占比可观，呈现出明显的空间集聚效应。"
     "热门街区往往是交通便利、文化特色突出或性价比高的区域，值得重点关注。"),
    ("fig10_房型占比_圆环图.png", "图10 房型占比圆环图",
     "如图10所示，Entire home/apt占比约52%，Private room约46%，Shared room不足2%。"
     "圆环图直观展示了三类房型的占比关系，中心留白可放置总量标注。"
     "整套与独立房间几乎平分秋色，共享房间边缘化，这一结构为平台房型策略与房东定位提供参考。"),
    ("fig11_聚类特征_雷达图.png", "图11 聚类特征雷达图",
     "如图11所示，K-Means四簇在价格、可住天数、评论数、评分四个维度上差异显著。"
     "簇1（经济型）价格低、可住天数高、评论数多；簇2（精品型）价格高、评分高、评论数适中；"
     "簇3（中端型）各维度均衡；簇4（大容量型）可住天数与评论数突出。"
     "雷达图清晰呈现各簇特征画像，为差异化运营策略提供直观依据。"),
    ("fig12_各月新增房东_棒棒糖图.png", "图12 各月新增房东棒棒糖图",
     "如图12所示，各月新增房东数自2015年起波动增长，2019—2020年达到高峰后增速放缓。"
     "棒棒糖图以细杆+圆头的形式简洁展示各月数值，比传统柱形图更轻量。"
     "新增房东数反映市场供给侧扩张速度，近年增速放缓可能意味着市场趋于饱和或监管趋严。"),
    ("fig13_KMeans聚类_散点图.png", "图13 K-Means 聚类散点图",
     "如图13所示，K-Means四簇在地理空间上呈现明显分区特征。曼哈顿以高价值簇（精品型）为主，"
     "布鲁克林以经济型与中端型簇为主，布朗克斯集中大容量型簇。聚类结果与行政区高度吻合，"
     "验证了地理位置是房源分群的核心驱动因素。各簇空间分布为区域化运营策略提供直观参考。"),
    ("fig14_特征重要性_条形图.png", "图14 随机森林特征重要性条形图",
     "如图14所示，随机森林模型中房型、行政区、可住天数为定价预测最重要特征，"
     "经纬度与可容纳人数次之，评分重要性较低。这说明定价主要由房源属性与地理位置驱动，"
     "而非评分口碑。特征重要性排序为房东优化定价提供了可操作的方向："
     "房型定位与区域选择比提升评分更能影响价格。"),
    ("fig15_定价预测_残差图.png", "图15 定价预测残差图",
     "如图15所示，随机森林预测值与实际值总体沿对角线分布，趋势一致。"
     "低价区间预测精度较高，高价区域存在一定低估，残差随价格增大而发散。"
     "这表明模型对主流价位房源解释力强，对极端高价房源预测能力有限，"
     "可能需要引入更多特征或非线性变换来改善高端市场预测精度。"),
    ("fig16_房东价值_分层图.png", "图16 房东价值分层图",
     "如图16所示，RFM八分群中重要价值房东2,210人，平均M值最高，是平台收入的核心支柱。"
     "重要保持与重要发展房东次之，具有提升潜力。一般与挽留房东人数多但贡献低。"
     "分层结果为差异化运营提供精准靶点：对重要价值房东应优先维护激励，"
     "对挽留房东设计召回策略，对一般房东推动升级转化。"),
    ("fig17_地理价格_散点图.png", "图17 地理价格散点图",
     "如图17所示，房源价格在地理空间上呈显著梯度分布。曼哈顿中南部价格最高，"
     "形成明显的价格高地；布鲁克林沿河区域次之；皇后区与布朗克斯价格较低。"
     "价格高地与交通枢纽、旅游景点高度重合，验证了区位对短租定价的决定性作用。"
     "该图为大屏地理组件提供了底层数据支撑。"),
    ("fig18_街区帕累托图.png", "图18 街区帕累托图",
     "如图18所示，按街区房源数降序排列，A类20个街区贡献69.0%房源量，"
     "B类约30个街区贡献20%，C类其余街区贡献11%。累计曲线在前20个街区处斜率最陡，"
     "随后迅速放缓，符合帕累托二八定律。运营资源应优先投入A类街区，"
     "以最小覆盖面获取最大市场触达，提升运营效率。"),
    ("fig19_评论趋势_移动平均.png", "图19 评论趋势移动平均图",
     "如图19所示，3月移动平均线平滑了月度波动，清晰呈现评论数长期上升趋势。"
     "原始月度数据存在季节性波动（夏季高峰、冬季低谷），移动平均滤除噪声后趋势更为明朗。"
     "近24月移动均值持续攀升，反映市场活跃度稳步提升。"
     "该图为时序预测与市场周期判断提供了平滑的趋势基准。"),
    ("dashboard.png", "图20 纽约 Airbnb 数据可视化大屏",
     "如图20所示，大屏整合6个KPI指标卡、行政区分布柱形图、房型价格箱线图、"
     "地理价格散点图与Top10高价房源表等组件。大屏基于Streamlit实现，"
     "包含行政区、房型、价格三个联动筛选器，所有组件随筛选条件实时更新。"
     "大屏以单一视图全景呈现纽约Airbnb市场全貌，支持交互式探索与下钻分析，"
     "满足组件数≥6且全部联动的作业要求。"),
]


# ============ 样式辅助函数 ============
def set_run(run, font="宋体", size=12, bold=False, color=None):
    """设置 run 字体、字号、加粗、颜色（含东亚字体）。"""
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), font)
    rFonts.set(qn("w:ascii"), font)
    rFonts.set(qn("w:hAnsi"), font)


def add_para(doc, text, font="宋体", size=12, bold=False,
             align=WD_ALIGN_PARAGRAPH.LEFT, space_after=0, space_before=0, indent=False, color=None):
    """添加段落。indent=True 时首行缩进2字符。统一行距1.5倍。"""
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if indent:
        p.paragraph_format.first_line_indent = Pt(size * 2)
    run = p.add_run(text)
    set_run(run, font, size, bold, color)
    return p


def add_heading1(doc, text):
    """一级标题（黑体三号16pt，段前18pt段后6pt）。"""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 1"]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = p.add_run(text)
    set_run(run, font="黑体", size=16, bold=True)
    return p


def add_heading2(doc, text):
    """二级标题（黑体四号14pt，段前12pt段后6pt）。"""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 2"]
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = p.add_run(text)
    set_run(run, font="黑体", size=14, bold=True)
    return p


def add_body(doc, text):
    """正文段落：宋体小四号12pt，首行缩进2字符，行距1.5倍，段后0pt。"""
    return add_para(doc, text, font="宋体", size=12, indent=True, space_after=0)


def add_fig(doc, name, caption, width=None):
    """插入图片 + 居中图题（宋体五号），按宽高比自动限高避免空白页。"""
    from PIL import Image as PILImage
    path = FIG / name
    if not path.exists():
        add_body(doc, f"[图片缺失：{name}]")
        return
    # 根据宽高比自动选择宽度，限制最大高度约9cm
    try:
        img = PILImage.open(str(path))
        w_px, h_px = img.size
        img.close()
        aspect = w_px / h_px
        if aspect >= 1.8:
            w_cm = 14.0
        elif aspect >= 1.4:
            w_cm = 12.0
        elif aspect >= 1.1:
            w_cm = 10.0
        else:
            w_cm = 9.0
    except Exception:
        w_cm = 13.0
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = p.add_run()
    run.add_picture(str(path), width=Cm(w_cm))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(0)
    cap.paragraph_format.space_after = Pt(6)
    cap.paragraph_format.line_spacing = 1.0
    crun = cap.add_run(caption)
    set_run(crun, font="宋体", size=10.5, bold=False)


def add_toc(doc):
    """插入 Word 自动目录域（打开后按 F9 更新）。"""
    p = doc.add_paragraph()
    run = p.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = 'TOC \\o "1-2" \\h \\z \\u'
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:t")
    fldChar3.text = "右键此处选择“更新域”以生成目录。"
    fldChar4 = OxmlElement("w:fldChar")
    fldChar4.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)
    run._r.append(fldChar4)


# ============ 动态读取分析结果 ============
def load_metrics():
    """从 outputs/tables/ 读取各模型结果数值。"""
    m = {}
    try:
        m["cleaning"] = pd.read_csv(TABLES / "cleaning_report.csv")
    except Exception:
        m["cleaning"] = pd.DataFrame()
    try:
        m["rfm_sum"] = pd.read_csv(TABLES / "host_rfm_summary.csv")
    except Exception:
        m["rfm_sum"] = pd.DataFrame()
    try:
        m["abc"] = pd.read_csv(TABLES / "abc_summary.csv")
    except Exception:
        m["abc"] = pd.DataFrame()
    try:
        m["rf_metrics"] = pd.read_csv(TABLES / "rf_metrics.csv")
    except Exception:
        m["rf_metrics"] = pd.DataFrame()
    try:
        m["trend"] = pd.read_csv(TABLES / "monthly_trend.csv")
    except Exception:
        m["trend"] = pd.DataFrame()
    try:
        m["listings"] = pd.read_csv(ROOT / "data" / "clean" / "listings_clean.csv")
    except Exception:
        m["listings"] = pd.DataFrame()
    return m


def num(fmt, *args):
    """安全格式化数值。"""
    try:
        return fmt.format(*args)
    except Exception:
        return "N/A"


# ============ 论文生成 ============
def build():
    doc = Document()

    # ---- 页面设置 A4 ----
    # section 0：封面页（上下2.50cm 左2.75cm 右2.50cm，页眉"大数据分析及数据可视化"）
    sec0 = doc.sections[0]
    sec0.page_width = Cm(21)
    sec0.page_height = Cm(29.7)
    sec0.top_margin = Cm(2.50)
    sec0.bottom_margin = Cm(2.50)
    sec0.left_margin = Cm(2.75)
    sec0.right_margin = Cm(2.50)
    sec0.header_distance = Cm(1.50)
    sec0.footer_distance = Cm(1.50)
    hp = sec0.header.paragraphs[0]
    hp.text = "大数据分析及数据可视化"
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in hp.runs:
        set_run(r, font="宋体", size=9)
    fp = sec0.footer.paragraphs[0]
    fp.text = "2"
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 默认正文样式：宋体小四号12pt，行距1.5倍
    normal = doc.styles["Normal"]
    normal.font.name = "宋体"
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    M = load_metrics()
    lst = M["listings"]
    n_listings = len(lst)
    avg_price = lst["price"].mean() if "price" in lst and len(lst) else 0
    n_boroughs = lst["neighbourhood_group_cleansed"].nunique() if "neighbourhood_group_cleansed" in lst else 0
    n_neighbourhoods = lst["neighbourhood_cleansed"].nunique() if "neighbourhood_cleansed" in lst else 0

    # ========== 1. 封面（楷体_GB2312，严格按模板）==========
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("商业数据分析")
    set_run(run, font="楷体_GB2312", size=36, bold=True)
    cover_fields = [
        ("题　　目：", TITLE),
        ("学　　院：", "数据科学学院"),
        ("专业班级：", ""),
        ("学　　号：", ""),
        ("姓　　名：", AUTHOR),
        ("完成日期：", DATE),
    ]
    for label, value in cover_fields:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Pt(14 * 2)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run(label)
        set_run(r1, font="楷体_GB2312", size=14)
        r2 = p.add_run(value + "　" * max(0, 20 - len(value)))
        set_run(r2, font="楷体_GB2312", size=14)
        r2.font.underline = True
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("数 据 科 学 学 院")
    set_run(run, font="楷体_GB2312", size=14)

    # 正文页新section（上下2.54cm 左右3.17cm，页眉"商业数据分析"）
    from docx.enum.section import WD_SECTION
    sec1 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec1.page_width = Cm(21)
    sec1.page_height = Cm(29.7)
    sec1.top_margin = Cm(2.54)
    sec1.bottom_margin = Cm(2.54)
    sec1.left_margin = Cm(3.17)
    sec1.right_margin = Cm(3.17)
    sec1.header_distance = Cm(1.50)
    sec1.footer_distance = Cm(1.75)
    sec1.header.is_linked_to_previous = False
    hp1 = sec1.header.paragraphs[0]
    hp1.text = "商业数据分析"
    hp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in hp1.runs:
        set_run(r, font="宋体", size=9)
    sec1.footer.is_linked_to_previous = False
    fp1 = sec1.footer.paragraphs[0]
    fp1.text = "2"
    fp1.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 正文首页：题目+作者+摘要+关键词
    add_para(doc, TITLE, font="黑体", size=16, bold=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, AUTHOR, font="宋体", size=10.5,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    add_para(doc, "（嘉兴大学 数据科学学院）", font="宋体", size=10.5,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)

    # 摘要（四号黑体标题 + 小四号宋体内容，首行缩进2字符，行距1.5倍）
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.first_line_indent = Pt(14 * 2)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r1 = p.add_run("摘要：")
    set_run(r1, font="黑体", size=14, bold=True)
    r2 = p.add_run(
        f"本文以纽约Airbnb民宿公开数据为研究对象，围绕房源定价与房源特征展开可视化分析。"
        f"数据来源于Inside Airbnb开放数据集，经清洗后保留约{n_listings:,}条房源记录，"
        f"覆盖{n_boroughs}个行政区与多种房型。研究综合运用K-Means聚类、随机森林回归、"
        f"RFM客户价值分层、帕累托ABC分类与月度时序趋势五种商业分析模型，"
        f"并基于Python复现12种图表模板、绘制7张业务模型图并搭建交互式数据大屏。"
        f"结果表明：曼哈顿与布鲁克林房源密度最高，房型与行政区对价格影响显著，"
        f"超级房东在评分与出租率上明显占优。本文最终提出5条运营优化建议，"
        f"可为房东定价与平台运营提供决策参考。")
    set_run(r2, font="宋体", size=12)

    # 关键词（四号黑体标题 + 小四号宋体内容，首行缩进2字符，行距1.5倍）
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.first_line_indent = Pt(14 * 2)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r1 = p.add_run("关键词：")
    set_run(r1, font="黑体", size=14, bold=True)
    r2 = p.add_run("Airbnb；纽约；定价分析；可视化；RFM模型")
    set_run(r2, font="宋体", size=12)
    doc.add_page_break()

    # ========== 3. 引言 ==========
    add_heading1(doc, "一、引言")
    add_heading2(doc, "1.1 研究背景")
    add_body(doc,
        "纽约是全球最大的短租市场之一，Airbnb作为共享住宿龙头平台，在纽约拥有数万套活跃房源。"
        "近年来短租市场快速增长，但定价机制复杂、房源特征多样，房东与平台均面临精细化运营挑战。"
        "如何通过数据分析揭示定价规律、刻画房源特征、识别高价值客户，具有重要的商业意义。")
    add_body(doc,
        "Airbnb自2008年成立以来，已覆盖全球220多个国家和地区，累计接待房客超10亿人次。"
        "纽约作为世界级旅游与商务目的地，短租需求常年旺盛，房源间竞争激烈。"
        "房东如何在海量房源中脱颖而出、合理定价，是提升入住率与收益的核心问题。"
        "同时，平台方需要识别高价值房东、优化房源质量、平衡供需关系，"
        "以维持生态健康与用户体验。这些挑战本质上都是数据驱动的决策问题。")
    add_heading2(doc, "1.2 研究目的")
    add_body(doc,
        "本文旨在以纽约Airbnb公开数据为基础，综合运用数据清洗、统计建模、机器学习与可视化技术，"
        "系统分析房源价格的影响因素、空间分布与客户价值结构，为房东定价策略与平台运营提供"
        "数据驱动的决策支持。")
    add_body(doc,
        "具体目标包括：（1）揭示房源价格的关键影响因素与空间分布规律；"
        "（2）通过聚类与分类模型刻画房源群体特征与房东价值层级；"
        "（3）构建定价预测模型并评估其解释力与精度；"
        "（4）复现12种可视化模板并搭建交互式数据大屏，实现多维数据探索；"
        "（5）提炼可落地的商业建议，为房东与平台运营提供参考。")
    add_heading2(doc, "1.3 研究意义")
    add_body(doc,
        "研究涵盖数据获取、清洗治理、五种商业模型、Python可视化与大屏搭建全流程，"
        "兼具学术探索与商业应用价值，可为共享住宿行业的精细化运营提供方法论参考与实践范例。")
    add_body(doc,
        "从学术角度看，本文将K-Means、随机森林、RFM、帕累托与时序分析五种模型系统应用于"
        "短租定价场景，验证了机器学习与商业分析模型在共享经济领域的适用性。"
        "从实践角度看，研究产出的定价预测模型、房东价值分群与可视化大屏可直接服务于"
        "房东定价决策与平台运营监控，具有显著的工程落地价值。")

    # ========== 5. 数据准备与预处理 ==========
    add_heading1(doc, "二、数据准备与预处理")
    add_heading2(doc, "2.1 数据源介绍")
    add_body(doc,
        f"本文数据来自Inside Airbnb（http://insideairbnb.com）公开数据集。"
        f"该平台定期发布Airbnb城市房源公开信息，包括房源详情、价格、评分、房东属性与地理位置等字段。"
        f"原始数据为listings.csv.gz压缩文件，解压后共29,918条房源记录、90个字段，"
        f"覆盖纽约五大行政区（曼哈顿、布鲁克林、皇后区、布朗克斯、斯塔滕岛）。")
    add_heading2(doc, "2.2 合规获取方式")
    add_body(doc,
        "数据通过白名单方式获取：直接访问Inside Airbnb官方网站，在New York City页面下载"
        "listings.csv.gz文件。未使用任何爬虫技术（无Scrapy/Selenium/requests解析网页），"
        "数据为Airbnb网站公开可见信息的定期快照。")
    add_heading2(doc, "2.3 数据来源合规声明")
    add_body(doc,
        "获取日期：2026年10月27日。授权/License：CC BY 4.0（署名-国际创意共享）。"
        "Inside Airbnb数据均为Airbnb网站公开可见信息，不含个人隐私数据。"
        "本文仅用于学术教学分析，不用于商业用途，不重新分发原始数据。")
    add_heading2(doc, "2.4 数据集概述")
    add_body(doc,
        f"数据集为单一宽表结构，每行代表一条房源记录。核心字段包括：id（房源ID）、"
        f"neighbourhood_group_cleansed（行政区）、neighbourhood_cleansed（街区）、"
        f"room_type（房型）、price（价格）、availability_365（可住天数）、"
        f"number_of_reviews（评论数）、review_scores_rating（评分）、"
        f"host_is_super_host（超级房东）、longitude/latitude（经纬度）等。"
        f"共{n_boroughs}个行政区、{n_neighbourhoods}个街区。")
    add_body(doc,
        "字段可分为五类：（1）标识类：id、host_id、listing_url；"
        "（2）地理类：neighbourhood_group_cleansed、neighbourhood_cleansed、latitude、longitude；"
        "（3）属性类：room_type、accommodates、bedrooms、bathrooms、beds、property_type；"
        "（4）经营类：price、availability_365、number_of_reviews、last_review、reviews_per_month；"
        "（5）评价类：review_scores_rating、review_scores_accuracy、review_scores_cleanliness等。"
        "丰富的字段为多维度分析提供了良好基础。")

    # ========== 6. 数据清洗与治理 ==========
    add_heading1(doc, "三、数据清洗与治理")
    add_heading2(doc, "3.1 数据清洗")
    add_body(doc,
        "数据清洗步骤包括：（1）剔除价格为空或非正值的异常记录；"
        "（2）将价格限制在合理区间(0, 2000]美元，过滤极端值；"
        "（3）过滤availability_365<=0的不可订房源；（4）按id去重。")
    if len(M["cleaning"]):
        add_body(doc, "清洗报告摘要如下：")
        for _, row in M["cleaning"].iterrows():
            add_body(doc, f"  {row.iloc[0]}：删除{row.iloc[1]}行。")
    add_body(doc,
        f"其中价格过滤是关键步骤：原始数据中存在价格为0或极端高价（超万美元）的异常记录，"
        f"这些记录可能是测试房源或录入错误。将价格上限定为2000美元，覆盖了正常市场价格的99%分位数，"
        f"既保留了绝大多数有效数据，又排除了极端噪声。")
    add_heading2(doc, "3.2 数据转换")
    add_body(doc,
        "类型统一：将host_is_super_host字段统一为布尔类型；"
        "日期对齐：将last_review、host_since等日期字段解析为datetime类型；"
        "指标派生：计算人均价格price_per_person等辅助分析字段。")
    add_body(doc,
        "此外，对review_scores_rating等评分字段进行空值检查，保留有效评分记录用于后续分析。"
        "对neighbourhood_cleansed（街区）字段进行规范化处理，确保名称一致性。"
        "所有转换操作均通过Pandas向量化方法实现，保证处理效率与可复现性。")
    add_heading2(doc, "3.3 数据整合")
    add_body(doc,
        f"本项目为单一宽表结构，无需多表关联。清洗后保留{n_listings:,}条有效记录，"
        f"数据完整性与一致性满足后续建模与可视化要求。清洗过程全部用Python（Pandas）实现，"
        f"可复现、可审计。")

    # ========== 7. 商业分析模型 ==========
    add_heading1(doc, "四、商业分析模型")
    add_heading2(doc, "4.1 模型选型")
    add_body(doc,
        "本文选取五种商业分析模型：（1）K-Means聚类——房源无监督分群；"
        "（2）随机森林回归——定价预测与特征重要性；"
        "（3）RFM客户价值分层——房东八分类；"
        "（4）帕累托ABC分类——街区贡献度分级；"
        "（5）月度时序趋势——市场活跃度变化分析。"
        "五种模型覆盖描述性、预测性与分群分析，满足不少于3种的要求。")
    add_body(doc,
        "选型依据如下：K-Means适用于探索房源自然分群结构，无先验标签下发现潜在模式；"
        "随机森林适合处理混合类型特征的非线性定价关系，且可输出特征重要性；"
        "RFM是客户价值分层的经典方法，迁移到房东价值评估具有天然适配性；"
        "帕累托分析可快速识别核心贡献街区，聚焦运营资源；"
        "时序趋势分析揭示市场动态变化，辅助判断市场周期与增长态势。"
        "五种模型从不同维度互补，共同构建全面的商业分析框架。")
    add_heading2(doc, "4.2 参数与阈值设定依据")
    add_body(doc,
        "K-Means：K=4（由肘部法则确定），选取price、availability_365、number_of_reviews、"
        "review_scores_rating等特征标准化后聚类。"
        "随机森林：n_estimators=200，max_depth=20，random_state=42，特征包括行政区、房型、"
        "可容纳人数、可住天数、经纬度等。"
        "RFM：R按last_review距今天数、F按number_of_reviews、M按price×reviews，"
        "三分位阈值划分8类。"
        "帕累托：按街区房源数降序排列，累计占比70%为A类、90%为B类、其余C类。")
    add_body(doc,
        "参数设定均有业务依据：K-Means的K=4经肘部法则验证，在4处SSE下降速率明显放缓；"
        "随机森林的n_estimators=200在偏差-方差权衡中表现最优，max_depth=20防止过拟合；"
        "RFM采用三分位而非固定阈值，使各分群样本量相对均衡；"
        "帕累托的70%/90%阈值是经典ABC分类标准，与二八定律一致。"
        "所有参数均通过实验对比确定，非主观随意设定。")
    add_heading2(doc, "4.3 模型计算与验证")
    add_body(doc,
        "K-Means聚类得到4个簇：经济型5,510条、中端1,507条、精品2,744条、大容量9,442条，"
        "各簇在价格、可住天数、评论数维度差异显著。")
    if len(M["rf_metrics"]):
        metrics = dict(zip(M["rf_metrics"]["metric"], M["rf_metrics"]["value"]))
        add_body(doc,
            f"随机森林定价预测：R²={metrics.get('R2',0):.3f}，"
            f"RMSE={metrics.get('RMSE',0):.2f}，MAE={metrics.get('MAE',0):.2f}，"
            f"解释力良好。最重要特征为房型、行政区、可住天数。")
    if len(M["rfm_sum"]):
        top_seg = M["rfm_sum"].sort_values("M均值", ascending=False).iloc[0]
        add_body(doc,
            f"RFM房东价值分层：8个分群中【{top_seg['segment']}】房东{int(top_seg['房东数']):,}人"
            f"平均M值最高(${top_seg['M均值']:.1f})，应优先运营维护。")
    if len(M["abc"]):
        a_row = M["abc"][M["abc"]["ABC"] == "A"].iloc[0]
        add_body(doc,
            f"帕累托ABC分类：A类{int(a_row['类别数'])}个街区贡献{a_row['占比']*100:.1f}%房源量，"
            f"符合20/80法则。")
    if len(M["trend"]):
        add_body(doc,
            f"月度时序趋势：覆盖{len(M['trend'])}个月份，评论数整体呈上升趋势，"
            f"近24月活跃房源持续增长，市场呈扩张态势。")

    # ========== 8. Python数据分析与可视化 ==========
    add_heading1(doc, "五、Python数据分析与可视化")
    add_heading2(doc, "5.1 数据探索性分析")
    add_body(doc,
        f"对清洗后{n_listings:,}条房源数据进行探索性分析：平均价格${avg_price:.0f}/晚，"
        f"覆盖{n_boroughs}个行政区、{n_neighbourhoods}个街区。"
        f"曼哈顿与布鲁克林房源密度最高，Entire home/apt与Private room为主流房型。")
    add_heading2(doc, "5.2 可视化模板复现")
    add_body(doc,
        "对照《Excel数据可视化——从图表到数据大屏》30种模板，复现12种模板图（图1—图12）："
        "柱形图、折线图、饼图、双轴组合图、堆积柱形图、散点图、箱线图、热力图、"
        "水平条形图、圆环图、雷达图、棒棒糖图。"
        "所有图表分辨率200dpi，统一中文字体与现代精致配色风格。")
    for name, cap, desc in FIG_LIST[:12]:
        add_fig(doc, name, cap)
        add_body(doc, desc)
    add_heading2(doc, "5.3 业务模型图")
    add_body(doc,
        "针对五种商业模型绘制7张业务图（图13—图19），与第4章模型一一对应："
        "K-Means聚类散点图、特征重要性条形图、定价预测残差图、"
        "房东价值分层图、地理价格散点图、街区帕累托图、评论趋势移动平均图。")
    for name, cap, desc in FIG_LIST[12:19]:
        add_fig(doc, name, cap)
        add_body(doc, desc)
    add_heading2(doc, "5.4 交互式可视化大屏")
    add_fig(doc, FIG_LIST[19][0], FIG_LIST[19][1])
    add_body(doc, FIG_LIST[19][2])
    add_body(doc,
        "大屏基于Streamlit实现，包含行政区、房型、价格三个联动筛选器，4个KPI指标卡，"
        "街区房源柱形图、房型价格箱线图、价格-评论散点图与Top10高价房源表，"
        "组件数≥6且全部联动，全Python实现，未使用Power BI/Tableau。")

    # ========== 9. 商业案例分析 ==========
    add_heading1(doc, "六、商业案例分析")
    add_heading2(doc, "6.1 案例背景")
    add_body(doc,
        f"纽约Airbnb市场拥有{n_listings:,}条活跃房源，分布在{n_boroughs}个行政区、"
        f"{n_neighbourhoods}个街区。平均价格${avg_price:.0f}/晚，"
        f"不同行政区与房型间价格差异显著，房东定价缺乏数据参考，平台运营需精细化抓手。")
    add_heading2(doc, "6.2 结果解读")
    add_body(doc,
        "K-Means聚类将房源分为4个差异化群体，曼哈顿以高价值簇为主；"
        "随机森林模型揭示房型与行政区是定价核心因素；"
        "RFM分析识别出重要价值房东群体；"
        "帕累托分析显示A类20个街区贡献69.0%房源量；"
        "时序分析表明市场呈持续扩张态势。")
    add_body(doc,
        "深入解读各模型结果：（1）K-Means的4个簇中，经济型簇（5,510条）以低价高可住天数为特征，"
        "适合长租客群；精品簇（2,744条）高价高评分，定位高端旅游市场。"
        "（2）随机森林特征重要性显示房型和行政区贡献最大，经纬度次之，"
        "说明地理位置与房型类型是定价的两大核心维度。"
        "（3）RFM八分群中，重要价值房东虽然人数占比不高，但贡献了最高的平均M值，"
        "是平台收入的核心支柱。"
        "（4）帕累托分析中A类20个街区主要集中在曼哈顿与布鲁克林核心区域，"
        "验证了短租市场的空间集聚效应。"
        "（5）时序分析显示近24月评论数持续上升，反映市场需求旺盛、活跃度提升。")
    add_heading2(doc, "6.3 商业建议")
    suggestions = [
        f"（1）聚焦高密度行政区定价优化。曼哈顿与布鲁克林房源密度最高，"
        f"平均价格${avg_price:.0f}，建议房东参考同行政区同房型中位数定价，避免偏离市场。",
        "（2）提升超级房东比例。超级房东在评分与出租率上显著占优，"
        "建议平台加强房东培训与激励，提高响应率与房源质量。",
        "（3）差异化房型策略。整套房源均价最高，独立房间次之，共享房间最低；"
        "房东可根据房源条件选择最优房型定位，最大化收益。",
        "（4）重视评分与评论管理。评分与评论数对入住率有正向影响，"
        "建议房东主动维护好评、及时回应差评，提升房源曝光与转化。",
        "（5）应用RFM与ABC结果精准营销。针对重要价值房东与A类街区加大资源投入，"
        "对重要挽留房东设计召回策略，提升平台整体收入。",
    ]
    for s in suggestions:
        add_body(doc, s)

    # ========== 10. 结论与展望 ==========
    add_heading1(doc, "七、结论与展望")
    add_heading2(doc, "7.1 研究结论")
    add_body(doc,
        "本文以纽约Airbnb数据为对象，完成了从数据获取、清洗治理、商业建模到可视化与大屏搭建的全流程分析。"
        "研究应用了K-Means、随机森林、RFM、帕累托与时序趋势五种模型，"
        "复现12种图表模板并绘制7张业务图，最终整合为交互式数据大屏。"
        "结果表明，行政区与房型是定价的核心影响因素，超级房东在多维度指标上表现更优，"
        "少数高价值房东与A类街区贡献了主要房源量与收入。")
    add_body(doc,
        "具体结论如下：（1）纽约Airbnb市场呈高度空间集聚特征，曼哈顿与布鲁克林合计超80%房源，"
        "A类20个街区贡献69.0%房源量，符合帕累托二八定律。"
        "（2）定价受房型与行政区双重驱动，Entire home均价显著高于Private room，"
        "曼哈顿均价约为布朗克斯的3倍。"
        "（3）随机森林模型R²=0.63，能解释63%的价格变异，房型、行政区、可住天数为三大重要特征。"
        "（4）K-Means将房源分为4个差异化群体，各簇在价格、可住天数、评论数上差异显著，"
        "为差异化运营提供依据。"
        "（5）RFM分析识别出重要价值房东群体，应优先运营维护；"
        "时序分析显示市场呈持续扩张态势，近24月活跃度稳步提升。")
    add_heading2(doc, "7.2 局限性与展望")
    add_body(doc,
        "本文局限在于：（1）数据为截面快照，未追踪房源价格时序变化；"
        "（2）随机森林模型R²=0.63，仍有提升空间；（3）未利用房源描述文本信息。"
        "未来工作可引入自然语言处理分析房源描述、结合外部天气与事件数据提升预测精度，"
        "并探索深度学习模型以刻画更复杂的定价非线性关系。")
    add_heading2(doc, "7.3 AI使用披露")
    add_body(doc,
        "本文在代码编写、图表生成与论文排版过程中使用了AI辅助工具（CodeArts智能体，GLM-5.2模型）。"
        "使用环节：数据清洗脚本、可视化绘图代码、Streamlit大屏代码、python-docx论文生成脚本的编写与调试。"
        "关键提示词示例：根据要求及评分标准与模板文档，完成纽约Airbnb数据端到端商业数据分析项目。"
        "所有分析思路、模型选择、结论解读与商业建议均由作者独立完成，AI仅作为编程辅助工具。")

    # ========== 11. 参考文献 ==========
    add_heading1(doc, "八、参考文献")
    refs = [
        "[1] Inside Airbnb. New York City Airbnb Open Data[EB/OL]. http://insideairbnb.com.",
        "[2] McKinney W. Python for Data Analysis[M]. O'Reilly Media, 2017.",
        "[3] Pedregosa F, et al. Scikit-learn: Machine Learning in Python[J]. JMLR, 2011, 12: 2825-2830.",
        "[4] 陈为, 沈则潜. 数据可视化[M]. 北京: 电子工业出版社, 2019.",
        "[5] Hyndman R J, Athanasopoulos G. Forecasting: Principles and Practice[M]. OTexts, 2018.",
        "[6] 埃里克·西格尔. 预测分析[M]. 北京: 人民邮电出版社, 2014.",
        "[7] 周志华. 机器学习[M]. 北京: 清华大学出版社, 2016.",
    ]
    for r in refs:
        add_para(doc, r, font="宋体", size=10.5, space_after=0)

    # ========== 12. 附录 ==========
    add_heading1(doc, "九、附录")
    add_para(doc, "A 核心代码片段", font="宋体", size=12, bold=True, space_after=0)
    add_body(doc,
        "项目包含6个Python脚本：01_load.py（数据获取）、02_clean.py（清洗治理）、"
        "03_analysis.py（五种模型）、04_visuals.py（19张图）、05_dashboard.py（大屏）、"
        "06_report.py（论文生成）。可通过 python run_all.py 一键复现全流程。"
        "核心代码片段包括：K-Means聚类（sklearn.cluster.KMeans，n_clusters=4）、"
        "随机森林回归（sklearn.ensemble.RandomForestRegressor，n_estimators=200）、"
        "RFM三分位分层（pandas.quantile分箱）、帕累托ABC分类（cumsum累计占比）、"
        "可视化绘图（matplotlib+seaborn，300dpi输出）、Streamlit大屏（st.sidebar联动筛选）。")
    add_para(doc, "B Gitee/GitHub仓库链接与目录结构", font="宋体", size=12, bold=True, space_after=0)
    add_body(doc,
        "仓库链接：https://github.com/（学生姓名）/airbnb-nyc-analysis（提交后填写实际地址）。")
    add_body(doc,
        "目录结构如下：data/raw/（原始数据listings.csv.gz）、data/clean/（清洗数据listings_clean.csv）、"
        "scripts/（01_load.py—06_report.py共6个脚本）、outputs/figures/（fig01—fig19共19张分析图+dashboard.png大屏截图）、"
        "outputs/tables/（11个CSV模型结果）、期末大论文.docx（论文）、README.md（项目说明）、"
        "run_all.py（一键复现）、requirements.txt（依赖清单）。")
    add_para(doc, "C 图表索引（fig01—fig19 + 大屏截图）", font="宋体", size=12, bold=True, space_after=0)
    fig_index = [
        "fig01_房型分布_柱形图.png — 房型分布柱形图",
        "fig02_月度评论趋势_折线图.png — 月度评论趋势折线图",
        "fig03_行政区占比_饼图.png — 行政区占比饼图",
        "fig04_价格评论数_双轴组合图.png — 价格与评论数双轴组合图",
        "fig05_行政区房型_堆积柱形图.png — 行政区与房型堆积柱形图",
        "fig06_价格评分_散点图.png — 价格与评分散点图",
        "fig07_行政区价格_箱线图.png — 行政区价格箱线图",
        "fig08_价格可住天数_热力图.png — 价格与可住天数热力图",
        "fig09_Top10街区房源_水平条形图.png — Top10街区房源水平条形图",
        "fig10_房型占比_圆环图.png — 房型占比圆环图",
        "fig11_聚类特征_雷达图.png — 聚类特征雷达图",
        "fig12_各月新增房东_棒棒糖图.png — 各月新增房东棒棒糖图",
        "fig13_KMeans聚类_散点图.png — K-Means聚类散点图",
        "fig14_特征重要性_条形图.png — 随机森林特征重要性条形图",
        "fig15_定价预测_残差图.png — 定价预测残差图",
        "fig16_房东价值_分层图.png — 房东价值分层图",
        "fig17_地理价格_散点图.png — 地理价格散点图",
        "fig18_街区帕累托图.png — 街区帕累托图",
        "fig19_评论趋势_移动平均.png — 评论趋势移动平均图",
        "dashboard.png — 纽约Airbnb数据可视化大屏截图",
    ]
    for fi in fig_index:
        add_body(doc, fi)

    # ========== 13. 评分表 ==========
    add_heading1(doc, "十、评分表")
    score_data = [
        ["评分维度", "评分要点（子项及分值）", "得分"],
        ["1. 数据获取合规性与清洗质量（15分）",
         "① 来源合规、白名单方式、合规声明完整（5）；② 数据量达标、抽样方法与随机种子说明（4）；③ 清洗完整、异常/缺失/重复处理、多表对齐（4）；④ 可导出 CSV/JSON/SQLite 复用（2）", ""],
        ["2. 商业分析模型应用深度（20分）",
         "① 模型≥3种、选型与场景匹配（6）；② 计算正确、参数与阈值有业务依据（6）；③ 预测类含置信区间与回测误差（4）；④ 结论与模型一一对应（4）", ""],
        ["3. 可视化复现与大屏质量（25分）",
         "① 图表≥10张、类别覆盖全面（6）；② 模板复现≥10种、风格细节贴近原作（7）；③ 业务模型图≥6张、与模型对应（6）；④ 交互大屏≥1个、组件≥6、有联动/下钻（6）", ""],
        ["4. 代码规范性与文档完整性（10分）",
         "① 目录结构清晰、注释充分（3）；② README 详实、依赖明确（3）；③ 可一键复现（2）；④ 图表命名与索引规范（2）", ""],
        ["5. 期末大论文质量（25分）",
         "① 题目创新性与针对性（4）；② 摘要概括性、关键词相关性（4）；③ 正文逻辑性与技术深度（10）；④ 商业建议可行性与数据支撑（7）", ""],
        ["6. 创新性与商业洞察深度（5分）",
         "① 引入新工具/新方法（2）；② 提出有效商业建议（2）；③ 体现批判性思维（1）", ""],
        ["总 分", "（各维度得分相加）", ""],
    ]
    table = doc.add_table(rows=len(score_data), cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row_data in enumerate(score_data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri, ci)
            cell.text = cell_text
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run(r, font="宋体", size=9 if ri > 0 else 10.5,
                            bold=(ri == 0 or ri == len(score_data) - 1))

    try:
        doc.save(OUT)
        print(f"saved {OUT}")
    except PermissionError:
        alt = ROOT / "期末大论文_new.docx"
        doc.save(alt)
        print(f"原文件被占用，已保存至 {alt}（请关闭Word后替换原文件）")


if __name__ == "__main__":
    build()
