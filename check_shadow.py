from docx import Document
from lxml import etree

doc = Document('期末大论文.docx')
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("图1 "):
        print(f"段{i}: [{p.text[:50]}]")
        # 完整段落XML
        xml = etree.tostring(p._element, pretty_print=True).decode()
        # 搜索阴影相关属性
        for keyword in ['shadow', 'shd', 'effect', 'outline', 'emboss', 'imprint', 'vanish']:
            if keyword in xml.lower():
                print(f"  发现属性: {keyword}")
        # 打印完整XML（截取关键部分）
        print("  完整XML:")
        print(xml[:2000])
        break

# 也检查Normal样式
print("\n=== Normal样式XML ===")
normal = doc.styles['Normal']
xml = etree.tostring(normal.element, pretty_print=True).decode()
for keyword in ['shadow', 'shd', 'effect', 'outline', 'emboss', 'imprint']:
    if keyword in xml.lower():
        print(f"  发现属性: {keyword}")
print(xml[:1500])
