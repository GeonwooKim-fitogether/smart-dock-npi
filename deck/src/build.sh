# 덱 다시 만들기 — deck/src 안에서 실행: cd deck/src && sh build.sh
# 1) base-v23.html 에 쪽별 수정·추가를 차례로 적용해 smart-dock-slide-asis-tobe.html 을 만든다
# 2) 결과를 deck/ 로 복사한다 (PDF 는: python3 make_pdf.py ../../exports/SmartDock_기획_YYYY-MM-DD.pdf)
set -e
python3 deck_v24.py
python3 userflow.py
python3 ab_pages.py
python3 result_page.py
cp smart-dock-slide-asis-tobe.html ../smart-dock-slide-asis-tobe.html
echo "built: deck/smart-dock-slide-asis-tobe.html"
