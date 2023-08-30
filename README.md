## 大华智慧园区综合管理平台存在SQL注入 POC
```
fofa:body="/WPMS/"||title="智慧园区综合管理平台"||body="/WPMS/asset/img/black/QR-code-V4.003-owner.png"||body="/WPMS/asset/img/black/zhyq.png"
```
```
Usage:
  python3 dahua_sqlScan.py -h
  python3 dahua_sqlScan.py -u http://www.example.com 单个url测试
  python3 dahua_sqlScan.py -f url.txt 批量检测
```
![](https://github.com/csdcsdcsdcsdcsd/Dahua_SqlInjection_Scan/blob/main/DaHua.png)
会在当前目录生成存在漏洞的vuln.txt文件
![](https://github.com/csdcsdcsdcsdcsd/Dahua_SqlInjection_Scan/blob/main/vuln.png)
## 免责声明
由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，作者不为此承担任何责任。
