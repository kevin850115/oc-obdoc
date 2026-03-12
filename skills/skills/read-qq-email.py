#!/usr/bin/env python3
"""
QQ 邮箱读取技能
功能：通过 IMAP 协议读取 QQ 邮箱邮件
需要：QQ 邮箱开启 IMAP 服务 + 授权码
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import os

# QQ 邮箱配置
QQ_EMAIL = "yefeng850115@qq.com"  # QQ 邮箱账号
QQ_AUTH_CODE = "quvrnmucmlxhcbeb"     # QQ 邮箱授权码
IMAP_SERVER = "imap.qq.com"
IMAP_PORT = 993

def get_auth_code():
    """
    获取 QQ 邮箱授权码的步骤：
    1. 登录 QQ 邮箱网页版
    2. 设置 → 账户
    3. 开启 POP3/SMTP/IMAP 服务
    4. 生成授权码
    5. 复制授权码（16 位字符串）
    """
    return QQ_AUTH_CODE

def decode_mime_words(s):
    """解码 MIME 编码的字符串"""
    if not s:
        return ""
    decoded = decode_header(s)
    return ''.join(
        part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
        for part, encoding in decoded
    )

def connect_to_qq_mail():
    """连接到 QQ 邮箱"""
    try:
        # 创建 IMAP 连接
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        
        # 登录
        auth_code = get_auth_code()
        mail.login(QQ_EMAIL, auth_code)
        
        print(f"✅ 成功连接到 {QQ_EMAIL}")
        return mail
    except Exception as e:
        print(f"❌ 连接失败：{str(e)}")
        print("\n💡 可能的问题：")
        print("1. QQ 邮箱未开启 IMAP 服务")
        print("2. 授权码错误")
        print("3. 网络连接问题")
        return None

def list_folders(mail):
    """列出所有邮箱文件夹"""
    try:
        status, folders = mail.list()
        print("\n📁 邮箱文件夹：")
        for folder in folders:
            print(f"  - {folder.decode('utf-8')}")
        return folders
    except Exception as e:
        print(f"❌ 获取文件夹失败：{str(e)}")
        return []

def get_unread_emails(mail, folder='INBOX', limit=10):
    """获取未读邮件"""
    try:
        # 选择邮箱文件夹
        mail.select(folder)
        
        # 搜索未读邮件
        status, messages = mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            print("❌ 搜索邮件失败")
            return []
        
        email_ids = messages[0].split()
        
        if not email_ids:
            print("ℹ️ 没有未读邮件")
            return []
        
        # 获取最新 limit 封邮件
        email_ids = email_ids[-limit:]
        
        emails = []
        for email_id in email_ids:
            email_data = read_email(mail, email_id)
            if email_data:
                emails.append(email_data)
        
        return emails
    except Exception as e:
        print(f"❌ 获取邮件失败：{str(e)}")
        return []

def read_email(mail, email_id):
    """读取单封邮件"""
    try:
        # 获取邮件内容
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        
        if status != 'OK':
            return None
        
        # 解析邮件
        msg = email.message_from_bytes(msg_data[0][1])
        
        # 解码发件人
        from_ = decode_mime_words(msg.get('From', ''))
        
        # 解码主题
        subject = decode_mime_words(msg.get('Subject', ''))
        
        # 获取日期
        date_str = msg.get('Date', '')
        try:
            date_obj = email.utils.parsedate_to_datetime(date_str)
            date_formatted = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except:
            date_formatted = date_str
        
        # 获取邮件正文
        body = ""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # 附件
                if "attachment" in content_disposition:
                    filename = decode_mime_words(part.get_filename())
                    if filename:
                        attachments.append(filename)
                # 正文
                elif content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8')
                    except:
                        body = part.get_payload(decode=True).decode('gbk', errors='ignore')
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8')
            except:
                body = msg.get_payload(decode=True).decode('gbk', errors='ignore')
        
        # 限制正文长度
        if len(body) > 500:
            body = body[:500] + "..."
        
        return {
            'id': email_id.decode(),
            'from': from_,
            'subject': subject,
            'date': date_formatted,
            'body': body,
            'attachments': attachments
        }
    except Exception as e:
        print(f"❌ 读取邮件失败：{str(e)}")
        return None

def mark_as_read(mail, email_id):
    """标记邮件为已读"""
    try:
        mail.store(email_id, '+FLAGS', '\\Seen')
        return True
    except Exception as e:
        print(f"❌ 标记失败：{str(e)}")
        return False

def delete_email(mail, email_id):
    """删除邮件"""
    try:
        mail.store(email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
        return True
    except Exception as e:
        print(f"❌ 删除失败：{str(e)}")
        return False

def print_email_summary(emails):
    """打印邮件摘要"""
    if not emails:
        return
    
    print("\n" + "="*60)
    print(f"📧 共 {len(emails)} 封未读邮件")
    print("="*60)
    
    for i, email_data in enumerate(emails, 1):
        print(f"\n【{i}】{email_data['subject']}")
        print(f"📍 发件人：{email_data['from']}")
        print(f"⏰ 时间：{email_data['date']}")
        print(f"📋 正文：{email_data['body'][:100]}...")
        if email_data['attachments']:
            print(f"📎 附件：{', '.join(email_data['attachments'])}")
        print("-"*60)

def save_to_file(emails, filename='qq_emails.md'):
    """保存邮件到文件（不同步钉钉）"""
    if not emails:
        return
    
    output_path = f'/home/admin/.openclaw/workspace/obsidian-docs/content/Resources/{filename}'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 📧 QQ 邮箱未读邮件\n\n")
        f.write(f"> **读取时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"> **邮箱：** {QQ_EMAIL}\n")
        f.write(f"> **数量：** {len(emails)} 封\n\n")
        f.write("---\n\n")
        
        for i, email_data in enumerate(emails, 1):
            f.write(f"## 【{i}】{email_data['subject']}\n\n")
            f.write(f"**发件人：** {email_data['from']}\n\n")
            f.write(f"**时间：** {email_data['date']}\n\n")
            f.write(f"**正文：**\n\n```\n{email_data['body']}\n```\n\n")
            
            if email_data['attachments']:
                f.write(f"**附件：** {', '.join(email_data['attachments'])}\n\n")
            
            f.write("---\n\n")
    
    print(f"✅ 邮件已保存到：{output_path}")
    print(f"🌐 GitHub 链接：https://kevin850115.github.io/oc-obdoc/content/Resources/{filename.replace('.md', '')}")

def main():
    """主函数"""
    print("="*60)
    print("📧 QQ 邮箱读取工具")
    print("="*60)
    print(f"📧 邮箱：{QQ_EMAIL}")
    print(f"🌐 服务器：{IMAP_SERVER}:{IMAP_PORT}")
    print("="*60)
    print()
    
    # 检查配置
    if QQ_EMAIL == "your_qq_number@qq.com" or QQ_AUTH_CODE == "your_auth_code":
        print("❌ 请先配置 QQ 邮箱账号和授权码！")
        print()
        print("💡 配置步骤：")
        print("1. 编辑文件：/home/admin/.openclaw/workspace/skills/read-qq-email.py")
        print("2. 修改 QQ_EMAIL 为你的 QQ 邮箱账号")
        print("3. 修改 QQ_AUTH_CODE 为你的 QQ 邮箱授权码")
        print()
        print("💡 获取授权码步骤：")
        print("1. 登录 QQ 邮箱网页版 (mail.qq.com)")
        print("2. 点击 设置 → 账户")
        print("3. 开启 POP3/SMTP/IMAP 服务")
        print("4. 点击 生成授权码")
        print("5. 按提示发送短信验证")
        print("6. 复制 16 位授权码（不含空格）")
        return
    
    # 连接邮箱
    mail = connect_to_qq_mail()
    if not mail:
        return
    
    # 列出文件夹
    # list_folders(mail)
    
    # 获取未读邮件
    print("\n📬 正在获取未读邮件...")
    emails = get_unread_emails(mail, 'INBOX', limit=10)
    
    # 打印摘要
    print_email_summary(emails)
    
    # 保存到文件
    if emails:
        save_to_file(emails)
        
        # 询问是否标记为已读
        choice = input("\n💡 是否将所有邮件标记为已读？(y/n): ")
        if choice.lower() == 'y':
            for email_data in emails:
                mark_as_read(mail, email_data['id'].encode())
            print("✅ 已标记为已读")
    
    # 关闭连接
    mail.close()
    mail.logout()
    
    print("\n" + "="*60)
    print("✅ 任务完成！")
    print("="*60)

if __name__ == '__main__':
    main()
