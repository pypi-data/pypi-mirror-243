from batch_pdf.pdfgen.pdf_generator import PDFGenerator
from datetime import datetime
from reportlab.lib.units import mm
from memory_profiler import profile
import psutil
import resource

def create_pdf():
    start_time = datetime.now()    
    pdfgen = PDFGenerator(filename="/CAMS/pdf_wrapper.pdf", BatchSize=20)


    for i in range(1, 5001):
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
    cpu_before = psutil.cpu_percent()
    memory_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB to MB    
    create_pdf()
    cpu_after = psutil.cpu_percent()
    memory_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB to MB

    print(f"CPU 사용량: {cpu_after - cpu_before}%")
    print(f"메모리 사용량: {memory_after - memory_before} MB")