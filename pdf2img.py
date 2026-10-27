import fitz
doc = fitz.open("期末大论文.pdf")
print(f"总页数: {len(doc)}")
for i in range(6, min(12, len(doc))):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"page_{i+1}.png")
    print(f"page_{i+1}.png saved")
doc.close()
