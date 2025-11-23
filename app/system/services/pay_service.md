import time
import random
import string
import hashlib
import hmac
from urllib.parse import quote
import xml.etree.ElementTree as ET
import requests
# from flask import Flask, jsonify

# app = Flask(__name__)

# 从环境变量获取敏感信息
MCH_ID = "商户号"
APP_ID = "小程序ID"
API_KEY = "API密钥"
NOTIFY_URL = "https://yourdomain.com/wechat/notify"
PRIVATE_KEY_PATH = "path/to/apiclient_key.pem"
CERT_PATH = "path/to/apiclient_cert.pem"

def generate_nonce_str(length=32):
    """生成随机字符串"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_client_ip(request):
    """获取客户端IP"""
    return request.remote_addr

def get_sign(params, api_key):
    """生成签名"""
    # 按ASCII排序并拼接 key=value&...
    sorted_params = sorted(params.items())
    param_str = '&'.join([f"{k}={v}" for k, v in sorted_params if v != ''])
    # 添加API密钥
    param_str += f"&key={api_key}"
    
    # MD5签名（微信部分接口使用）
    # return hashlib.md5(param_str.encode('utf-8')).hexdigest().upper()
    
    # HMAC-SHA256签名（推荐使用）
    signature = hmac.new(api_key.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature.upper()

@app.route('/wechat/pay', methods=['POST'])
def wechat_pay():
    # 假设从前端获取订单ID
    order_id = request.json.get("orderId")
    
    # 构造请求参数
    params = {
        "appid": APP_ID,
        "mch_id": MCH_ID,
        "nonce_str": generate_nonce_str(),
        "body": "商品描述",
        "out_trade_no": f"ORDER{order_id}{int(time.time())}",
        "total_fee": 100,  # 金额（分）
        "spbill_create_ip": get_client_ip(request),
        "notify_url": NOTIFY_URL,
        "trade_type": "JSAPI",  # 小程序支付固定为JSAPI
        "openid": request.json.get("openId")  # 需要用户openId
    }
    
    # 生成签名
    params["sign"] = get_sign(params, API_KEY)
    
    # 构造XML请求体
    xml_data = "<xml>"
    for k, v in params.items():
        xml_data += f"<{k}>{v}</{k}>"
    xml_data += "</xml>"
    
    # 发送统一下单请求
    response = requests.post(
        "https://api.mch.weixin.qq.com/pay/unifiedorder",
        data=xml_data.encode('utf-8'),
        cert=(CERT_PATH, PRIVATE_KEY_PATH)
    )
    
    # 解析XML响应
    root = ET.fromstring(response.text)
    if root.find("return_code").text == "SUCCESS":
        prepay_id = root.find("prepay_id").text
        # 生成前端所需参数
        pay_params = {
            "timeStamp": str(int(time.time())),
            "nonceStr": generate_nonce_str(),
            "package": f"prepay_id={prepay_id}",
            "signType": "RSA"  # 微信推荐使用RSA
        }
        # 生成最终支付签名
        pay_sign = get_sign(pay_params, API_KEY)
        pay_params["paySign"] = pay_sign
        return jsonify(pay_params)
    else:
        return jsonify({"error": "微信支付接口调用失败", "detail": root.find("return_msg").text}), 500


# 支付回调
@app.route('/wechat/notify', methods=['POST'])
def wechat_notify():
    # 解析微信回调XML
    root = ET.fromstring(request.data)
    data = {child.tag: child.text for child in root}
    
    # 验证签名
    if verify_sign(data, API_KEY):
        if data["return_code"] == "SUCCESS" and data["result_code"] == "SUCCESS":
            # 处理业务逻辑
            order_id = data["out_trade_no"]
            # ... 更新订单状态 ...
            
            # 返回成功响应
            return "<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>"
    return "<xml><return_code><![CDATA[FAIL]]></return_code></xml>"

def verify_sign(data, api_key):
    """验证微信回调签名"""
    sign = data.pop("sign", None)
    local_sign = get_sign(data, api_key)
    return sign == local_sign



'''
1. 生成私钥与 CSR 请求
使用 OpenSSL 工具生成私钥和证书签名请求（CSR）：

bash
# 生成私钥（2048位）
openssl genrsa -out apiclient_key.pem 2048

# 生成 CSR 文件（后续上传到微信商户平台）
openssl req -new -key apiclient_key.pem -out apiclient.csr
执行命令时会提示输入以下信息：

Common Name (CN)：填写你的域名（如 yourdomain.com）
Country Name：国家代码（如 CN）
Organization Name：公司名称
2. 上传 CSR 到微信商户平台
登录 微信商户平台
进入 账户设置 → API 安全 → 管理证书
选择 申请证书，上传生成的 apiclient.csr 文件
微信审核通过后，会生成 apiclient_cert.pem（公钥证书）
3. 下载并保存证书
在微信商户平台下载生成的证书文件（通常为 apiclient_cert.pem）
将证书文件与之前生成的私钥 apiclient_key.pem 一起部署到服务器：
bash
# 示例目录结构
/path/to/certs/
├── apiclient_cert.pem   # 公钥证书
└── apiclient_key.pem    # 私钥文件
4. 证书格式转换（可选）
如果微信返回的证书格式不是 PEM，需转换为 PEM 格式：

bash
# 如果证书是 DER 格式，转换为 PEM
openssl x509 -inform der -in apiclient_cert.der -out apiclient_cert.pem
5. 验证证书有效性
使用 OpenSSL 检查证书内容：

bash
# 查看公钥证书信息
openssl x509 -in apiclient_cert.pem -text -noout

# 查看私钥信息
openssl rsa -in apiclient_key.pem -check
6. 配置到 Python 后端
在 Python 代码中引用证书路径：

python
# 示例配置
CERT_PATH = "/path/to/certs/apiclient_cert.pem"
PRIVATE_KEY_PATH = "/path/to/certs/apiclient_key.pem"

# 发送请求时携带证书
response = requests.post(
    "https://api.mch.weixin.qq.com/pay/unifiedorder",
    data=xml_data.encode('utf-8'),
    cert=(CERT_PATH, PRIVATE_KEY_PATH)
)
注意事项
私钥安全

私钥文件（apiclient_key.pem）必须严格保密，禁止上传到代码仓库或公共目录。
建议设置文件权限为 600（仅限服务器进程读取）：
bash
chmod 600 /path/to/certs/apiclient_key.pem
证书更新

微信支付证书有效期为 1 年，需定期在商户平台更新。
更新后需重新下载 apiclient_cert.pem 并替换服务器文件。
测试环境

本地开发时可使用沙箱测试，但正式环境必须使用真实证书。
完整证书管理流程参考：微信支付 API 安全指南

'''