# BÀI TẬP LỚN NHÓM 6
# ÁP DỤNG HỒI QUY TUYẾN TÍNH ĐỂ XÂY DỰNG MÔ HÌNH GỢI Ý PHIM

Project cung cấp modul thuật toán hồi quy tuyến tính: Gradient descent, giải đóng (Model)

Các modul này hỗ trợ: fit mô hình (hàm train()), test mô hình (hàm test()), và tính toán (caculate())

Trong folder APP bao gồm Service.py, State_Manager.py, APP.py, ReccomendSys.py

  Service.py : chứa class App dùng để sử dụng để thay đổi, lấy dữ liệu, xử lý các thao tác truy vấn từ người dùng

  ReccomendSys.py :Cung cấp class ReccomendationSystem để thao tác giữa dữ liệu và modul thuật toán học máy

  State_Manager.py : Cung cấp class StateManager để quản lý các trạng thái của App

  APP.py: class App để đóng gói mô hình

folder Graphic: Cung cấp giao diện đồ họa bao gồm: Các assets, các components liên quan đến đồ họa, các màn hình chính

folder Data: cup cấp Data cho mô hình bao gồm: danh sách phim và thể loại (movies.csv), Danh sách id user (users.csv), Ma trận trọng số (users_weight.h5), Lịch sử đánh giá phim (rating.h5)

***LƯU Ý***
  Nếu không có file users_weight.h5, mô hình vẫn có thể chạy và xây dựng lại trọng số dựa trên lịch sử đánh giá của người dùng

Cuối cùng là file main.py: file dùng để chạy chính, mở lên giao diện đồ họa để người dùng thao tác với hệ thống

# LỜI KẾT
  Trong quá trình thực hiện dự án, Nhóm 6 đã rút ra được thêm nhiều kinh nghiệm trong việc xây dựng dự án, việc này sẽ giúp nhóm hoàn thiện hơn trong tư duy lập trình cũng như làm việc nhóm.
  Mô hình tuy đã hoàn thiện nhưng vẫn còn nhiều hạn chế nhưng đây sẽ là tiền đề để nhóm phát triển thêm trong tương lai.
                                                                                                Nhóm 6 xin chân thành cảm ơn!
