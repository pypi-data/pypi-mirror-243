from reportlab.pdfgen.canvas import Canvas
from datetime import datetime
from reportlab.lib.units import mm
from memory_profiler import profile

@profile
def create_pdf():
    start_time = datetime.now()
    pdfgen = Canvas(filename="/CAMS/origin.pdf")


    for i in range(1, 1001):
        pdfgen.drawImage("sample/test.png", 0, 0, 210.82 * mm, 297.18 * mm)
        # 폰트 설정
        pdfgen.setFont("Helvetica", 12)

        # 왼쪽 상단에서부터 1부터 10까지의 더미 텍스트 상자 생성
        for i in range(1, 21):
            text = f"Test Input {i}"
            y = 800 - (i/5 * 50)
            if i % 5 == 0:
                x = 50
            else:
                x = 50 * (i % 5)
            pdfgen.drawString(x, y, text)
        pdfgen.showPage()

    pdfgen.save()
    print(f"elapsed time : {datetime.now() - start_time}")

if __name__ == '__main__':
    create_pdf()