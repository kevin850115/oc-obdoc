#!/usr/bin/env python3
"""
阿里云域名帮助文档抓取脚本
"""
import os
import re
import json
import hashlib
from urllib.parse import urlparse, urljoin

# 初始链接列表
INITIAL_LINKS = [
    "https://help.aliyun.com/zh/dws/developer-reference/api-domain-2018-01-29-overview",
    "https://help.aliyun.com/zh/dws/developer-reference/quick-start",
    "https://help.aliyun.com/zh/dws/product-overview/domain-name-fees",
    "https://help.aliyun.com/zh/dws/product-overview/limits",
    "https://help.aliyun.com/zh/dws/product-overview/terms",
    "https://help.aliyun.com/zh/dws/product-overview/what-is-domains",
    "https://help.aliyun.com/zh/dws/support/concepts",
    "https://help.aliyun.com/zh/dws/support/dns-resolution-and-access-issues",
    "https://help.aliyun.com/zh/dws/support/domain-name-related-policies-and-rules",
    "https://help.aliyun.com/zh/dws/support/faq-about-domain-name-transfer-and-ownership-changes",
    "https://help.aliyun.com/zh/dws/support/faq-about-payments-and-invoices",
    "https://help.aliyun.com/zh/dws/support/faq-about-transactions",
    "https://help.aliyun.com/zh/dws/support/protocols-related-domain-name-value-added-services",
    "https://help.aliyun.com/zh/dws/support/protocols-related-to-domain-name-registration",
    "https://help.aliyun.com/zh/dws/support/protocols-related-to-domain-name-transactions",
    "https://help.aliyun.com/zh/dws/support/registration-and-verification-issues",
    "https://help.aliyun.com/zh/dws/support/renewal-and-redemption-issues",
    "https://help.aliyun.com/zh/dws/support/search-for-and-recover-domains",
    "https://help.aliyun.com/zh/dws/support/security-compliance-issues",
    "https://help.aliyun.com/zh/dws/user-guide/anti-scam-tips-for-domain-name-transaction",
    "https://help.aliyun.com/zh/dws/user-guide/authorize-a-ram-user-to-manage-domain-names",
    "https://help.aliyun.com/zh/dws/user-guide/blacklisted-domain-names",
    "https://help.aliyun.com/zh/dws/user-guide/change-dns-servers-for-a-domain-name",
    "https://help.aliyun.com/zh/dws/user-guide/cybersquatting",
    "https://help.aliyun.com/zh/dws/user-guide/delegated-purchase-of-domain-names",
    "https://help.aliyun.com/zh/dws/user-guide/domain-name-display-page",
    "https://help.aliyun.com/zh/dws/user-guide/domain-name-group-management",
    "https://help.aliyun.com/zh/dws/user-guide/domain-name-push-with-prices",
    "https://help.aliyun.com/zh/dws/user-guide/download-a-domain-name-certificate",
    "https://help.aliyun.com/zh/dws/user-guide/enable-the-transfer-prohibition-lock",
    "https://help.aliyun.com/zh/dws/user-guide/enable-the-update-prohibition-lock",
    "https://help.aliyun.com/zh/dws/user-guide/fixed-price-1",
    "https://help.aliyun.com/zh/dws/user-guide/fixed-price-2",
    "https://help.aliyun.com/zh/dws/user-guide/handling-of-copyright-infringements-and-domain-name-abuse",
    "https://help.aliyun.com/zh/dws/user-guide/how-to-complete-domain-name-authentication",
    "https://help.aliyun.com/zh/dws/user-guide/how-to-register-a-domain-name",
    "https://help.aliyun.com/zh/dws/user-guide/mi-store",
    "https://help.aliyun.com/zh/dws/user-guide/modify-domain-name-information",
    "https://help.aliyun.com/zh/dws/user-guide/modify-registrant-contact-information-or-transfer-domain-name-ownership",
    "https://help.aliyun.com/zh/dws/user-guide/online-transfer",
    "https://help.aliyun.com/zh/dws/user-guide/open-rate-domain-name",
    "https://help.aliyun.com/zh/dws/user-guide/publish-domain-name-sales-information",
    "https://help.aliyun.com/zh/dws/user-guide/purchase-a-registered-domain-name",
    "https://help.aliyun.com/zh/dws/user-guide/query-the-basic-information-of-a-domain-name",
    "https://help.aliyun.com/zh/dws/user-guide/query-whether-a-domain-name-is-registrable-and-tradable",
    "https://help.aliyun.com/zh/dws/user-guide/redeem-a-domain-name",
    "https://help.aliyun.com/zh/dws/user-guide/renew-domain-names",
    "https://help.aliyun.com/zh/dws/user-guide/reservation-on-hichina",
    "https://help.aliyun.com/zh/dws/user-guide/retrieve-a-domain-name",
    "https://help.aliyun.com/zh/dws/user-guide/service-fees-for-domain-name-transactions",
    "https://help.aliyun.com/zh/dws/user-guide/transfer-a-domain-name-from-alibaba-cloud-to-another-registrar",
    "https://help.aliyun.com/zh/dws/user-guide/transfer-a-domain-name-to-alibaba-cloud",
    "https://help.aliyun.com/zh/dws/user-guide/use-the-security-lock-of-domain-name-registries",
    "https://help.aliyun.com/zh/dws/user-guide/what-is-domain-name-transaction",
    "https://help.aliyun.com/zh/dws/user-guide/whois-lookup-1"
]

OUTPUT_DIR = "/home/admin/doc/domain-help"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
LINKS_FILE = os.path.join(OUTPUT_DIR, "links.json")

def normalize_url(url):
    """标准化 URL，移除锚点"""
    if '#' in url:
        url = url.split('#')[0]
    return url

def url_to_filename(url):
    """将 URL 转换为安全的文件名"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    # 替换特殊字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', path)
    if not filename:
        filename = "index"
    return filename + ".md"

if __name__ == "__main__":
    # 创建目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # 保存链接列表
    with open(LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(INITIAL_LINKS),
            "links": INITIAL_LINKS
        }, f, ensure_ascii=False, indent=2)
    
    print(f"已保存 {len(INITIAL_LINKS)} 个初始链接到 {LINKS_FILE}")
    print(f"输出目录：{OUTPUT_DIR}")
    print(f"图片目录：{IMAGES_DIR}")
