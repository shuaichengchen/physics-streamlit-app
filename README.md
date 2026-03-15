# 物理前沿知识融入初中物理教学案例展示平台

这是一个基于 Streamlit 的论文展示型网站，包含三个案例：
- 深海探测与浮力教学
- 激光雷达与光现象教学
- 新能源汽车与电学教学

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 目录结构

```text
streamlit_site_package/
├─ app.py
├─ requirements.txt
├─ sample_survey.csv
├─ assets/
│  ├─ submarine_structure.png
│  ├─ lidar_scan.jpg
│  └─ ev_platform.jpg
└─ .streamlit/
   └─ config.toml
```

## 部署建议

将整个目录上传到支持 Python/Streamlit 的平台即可。默认入口文件为 `app.py`。

## 图片替换

替换 `assets/` 内同名文件即可，应用会自动读取。
