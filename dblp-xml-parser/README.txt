BÀI TẬP LAB 2: Viết Chương trình đọc thông tin từ file xml của trang dblp sau đó lưu xuống một CSDL quan hệ về các bài báo khoa học.

Sinh viên thực hiện:
	1. HUỲNH THIỆN TÙNG 	19522492
	2. NGUYỄN THÀNH VƯƠNG 	19522542
	3. LÊ THỊ THANH THANH	19520954

Link repository trên github của nhóm: https://github.com/tuilatung/CS232/tree/master/dblp-xml-parser



1. Các thư viện sử dụng: 
- Built-in: lxml.etree, pathlib.Path, sqlite3
- Others: pandas, unidecode

2. Nếu có lỗi thiếu thư viện:
	+ pip install pandas
	+ pip install Unidecode

3. Chú ý change path của file dblp.xml và file parsed_data.csv cũng như file dblp.db
   Thông thường khi giải nén chúng ta nên kiểm tra và sửa đường dẫn cho đúng

4. Làm sao để chạy?
	+ Chạy file main.py trước để có được file parsed_data.csv
	+ Sau đó chạy file convert2sqlite.py để tạo ra file database có tên dblp.db


5. Yêu cầu:
	+ Python 3
	+ Tải file dblp.xml từ trang: https://dblp.org/xml/
	+ Cài đặt các thư viện đã liệt kê trên mục 1