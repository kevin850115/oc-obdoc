#!/usr/bin/env python3
"""
QQ 邮箱智能助手（智小香专属版）
功能：
1. 读取 QQ 邮箱邮件
2. 检测包含"智小香"关键词的邮件
3. 自动执行邮件中的指令
4. 通过钉钉通知执行结果
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime
import os
import re
import requests
import subprocess

# ==================== 配置区域 ====================

# QQ 邮箱配置
QQ_EMAIL = "yefeng850115@qq.com"
QQ_AUTH_CODE = "quvrnmucmlxhcbeb"
IMAP_SERVER = "imap.qq.com"
IMAP_PORT = 993

# 钉钉配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=bf0b510617430e0a2ff2d1dc670790eaa430f93a986bf2fa4e5c06e5c0d9a6a9"

# 关键词
KEYWORD = "智小香"

# ==================== 工具函数 ====================

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
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(QQ_EMAIL, QQ_AUTH_CODE)
        print(f"✅ 成功连接到 {QQ_EMAIL}")
        return mail
    except Exception as e:
        print(f"❌ 连接失败：{str(e)}")
        return None

def get_emails_by_keyword(mail, keyword, folder='INBOX', limit=10):
    """根据关键词获取邮件"""
    try:
        mail.select(folder)
        
        # 搜索所有邮件
        status, messages = mail.search(None, 'ALL')
        
        if status != 'OK':
            return []
        
        email_ids = messages[0].split()
        
        if not email_ids:
            return []
        
        # 获取最新 limit 封邮件
        email_ids = email_ids[-limit:]
        
        matched_emails = []
        for email_id in email_ids:
            email_data = read_email(mail, email_id)
            if email_data:
                # 检查是否包含关键词
                content = f"{email_data['subject']} {email_data['body']}"
                if keyword in content:
                    matched_emails.append(email_data)
        
        return matched_emails
    except Exception as e:
        print(f"❌ 获取邮件失败：{str(e)}")
        return []

def read_email(mail, email_id):
    """读取单封邮件"""
    try:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        
        if status != 'OK':
            return None
        
        msg = email.message_from_bytes(msg_data[0][1])
        
        from_ = decode_mime_words(msg.get('From', ''))
        subject = decode_mime_words(msg.get('Subject', ''))
        
        date_str = msg.get('Date', '')
        try:
            date_obj = email.utils.parsedate_to_datetime(date_str)
            date_formatted = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except:
            date_formatted = date_str
        
        body = ""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if "attachment" in content_disposition:
                    filename = decode_mime_words(part.get_filename())
                    if filename:
                        attachments.append(filename)
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

# ==================== 指令识别与执行 ====================

def parse_command(email_body, email_subject):
    """解析邮件中的指令"""
    content = f"{email_subject}\n{email_body}"
    
    commands = []
    
    # 指令模式 1：执行命令
    # 格式：执行：xxx 或 运行：xxx
    exec_pattern = r'(?:执行 | 运行 | 运行命令)[:：]\s*(.+?)(?:\n|$)'
    exec_matches = re.findall(exec_pattern, content, re.IGNORECASE)
    for match in exec_matches:
        commands.append({
            'type': 'exec',
            'command': match.strip()
        })
    
    # 指令模式 2：读取文件
    # 格式：读取文件：xxx
    read_pattern = r'(?:读取文件 | 查看文件)[:：]\s*(.+?)(?:\n|$)'
    read_matches = re.findall(read_pattern, content, re.IGNORECASE)
    for match in read_matches:
        commands.append({
            'type': 'read',
            'path': match.strip()
        })
    
    # 指令模式 3：保存内容
    # 格式：保存到：xxx，内容：yyy
    save_pattern = r'(?:保存到 | 写入)[:：]\s*(.+?)(?:，|,|内容)[:：]\s*(.+?)(?:\n|$)'
    save_matches = re.findall(save_pattern, content, re.IGNORECASE)
    for match in save_matches:
        commands.append({
            'type': 'save',
            'path': match[0].strip(),
            'content': match[1].strip()
        })
    
    # 指令模式 4：发送邮件
    # 格式：发送邮件到：xxx，主题：yyy，内容：zzz
    email_pattern = r'(?:发送邮件 | 发送邮件到)[:：]\s*(.+?)(?:，|,).*?(?:主题 | 标题)[:：]\s*(.+?)(?:，|,).*?(?:内容)[:：]\s*(.+?)(?:\n|$)'
    email_matches = re.findall(email_pattern, content, re.IGNORECASE)
    for match in email_matches:
        commands.append({
            'type': 'email',
            'to': match[0].strip(),
            'subject': match[1].strip(),
            'content': match[2].strip()
        })
    
    # 指令模式 5：通用指令（包含"请"的请求）
    if not commands:
        general_pattern = r'智小香，请 (.+?)(?:\n|$)'
        general_matches = re.findall(general_pattern, content, re.IGNORECASE)
        for match in general_matches:
            commands.append({
                'type': 'general',
                'request': match.strip()
            })
    
    return commands

def execute_command(command):
    """执行单个指令"""
    cmd_type = command.get('type')
    result = {
        'success': False,
        'output': '',
        'error': ''
    }
    
    try:
        if cmd_type == 'exec':
            # 执行系统命令
            cmd = command.get('command')
            print(f"🔧 执行命令：{cmd}")
            
            # 安全检查：禁止危险命令
            dangerous_cmds = ['rm -rf', 'rm -fr', 'drop table', 'delete from', 'mkfs', 'dd']
            if any(danger in cmd.lower() for danger in dangerous_cmds):
                result['error'] = '❌ 禁止执行危险命令'
                return result
            
            process = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            result['success'] = (process.returncode == 0)
            result['output'] = process.stdout
            result['error'] = process.stderr
            
        elif cmd_type == 'read':
            # 读取文件
            path = command.get('path')
            print(f"📖 读取文件：{path}")
            
            if not os.path.exists(path):
                result['error'] = f'❌ 文件不存在：{path}'
                return result
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            result['success'] = True
            result['output'] = content[:2000]  # 限制长度
            
        elif cmd_type == 'save':
            # 保存文件
            path = command.get('path')
            content = command.get('content')
            print(f"💾 保存到：{path}")
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            result['success'] = True
            result['output'] = f'✅ 文件已保存：{path}'
            
        elif cmd_type == 'general':
            # 通用请求（记录请求，后续可扩展）
            request = command.get('request')
            print(f"💡 收到请求：{request}")
            
            result['success'] = True
            result['output'] = f'✅ 已收到请求：{request}\n\n（通用请求已记录，后续会实现具体功能）'
            
    except subprocess.TimeoutExpired:
        result['error'] = '❌ 命令执行超时'
    except Exception as e:
        result['error'] = f'❌ 执行失败：{str(e)}'
    
    return result

# ==================== 钉钉通知 ====================

def send_dingtalk_notification(email_info, commands, results):
    """发送钉钉通知"""
    
    # 构建消息内容
    text = f"## 📧 智小香智能邮件处理\n\n"
    text += f"**发件人：** {email_info['from']}\n"
    text += f"**主题：** {email_info['subject']}\n"
    text += f"**时间：** {email_info['date']}\n\n"
    text += f"---\n\n"
    
    text += f"**🔍 检测到关键词：** 智小香\n\n"
    
    if commands:
        text += f"**📋 识别到 {len(commands)} 个指令：**\n\n"
        
        for i, (cmd, result) in enumerate(zip(commands, results), 1):
            cmd_type = cmd.get('type')
            
            if cmd_type == 'exec':
                text += f"**【{i}】执行命令：** `{cmd.get('command')}`\n"
            elif cmd_type == 'read':
                text += f"**【{i}】读取文件：** `{cmd.get('path')}`\n"
            elif cmd_type == 'save':
                text += f"**【{i}】保存文件：** `{cmd.get('path')}`\n"
            elif cmd_type == 'general':
                text += f"**【{i}】通用请求：** {cmd.get('request')}\n"
            
            if result.get('success'):
                text += f"✅ 执行成功\n"
                if result.get('output'):
                    output = result['output'][:200]
                    if len(result['output']) > 200:
                        output += "..."
                    text += f"> {output}\n"
            else:
                text += f"❌ 执行失败\n"
                if result.get('error'):
                    text += f"> {result['error']}\n"
            
            text += "\n"
    else:
        text += f"**💡 未识别到具体指令**\n\n"
        text += f"邮件内容摘要：\n"
        text += f"> {email_info['body'][:300]}...\n\n"
    
    text += "---\n\n"
    text += f"*智小香智能助手 🌙*\n"
    
    # 发送钉钉消息
    try:
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "📧 智小香智能邮件处理",
                "text": text
            }
        }
        
        response = requests.post(DINGTALK_WEBHOOK, json=data, timeout=10)
        result = response.json()
        
        if result.get('errcode') == 0:
            print("✅ 钉钉通知已发送")
            return True
        else:
            print(f"❌ 钉钉发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 通知发送失败：{str(e)}")
        return False

# ==================== 主函数 ====================

def main():
    """主函数"""
    print("="*60)
    print("📧 QQ 邮箱智能助手（智小香专属版）")
    print("="*60)
    print(f"📧 邮箱：{QQ_EMAIL}")
    print(f"🔍 关键词：{KEYWORD}")
    print(f"🌐 服务器：{IMAP_SERVER}:{IMAP_PORT}")
    print("="*60)
    print()
    
    # 连接邮箱
    mail = connect_to_qq_mail()
    if not mail:
        return
    
    # 获取包含关键词的邮件
    print(f"\n🔍 正在搜索包含'{KEYWORD}'的邮件...")
    matched_emails = get_emails_by_keyword(mail, KEYWORD, 'INBOX', limit=20)
    
    if not matched_emails:
        print(f"ℹ️ 未找到包含'{KEYWORD}'的邮件")
        mail.close()
        mail.logout()
        return
    
    print(f"✅ 找到 {len(matched_emails)} 封匹配邮件")
    print()
    
    # 处理每封邮件
    for email_info in matched_emails:
        print("="*60)
        print(f"📧 处理邮件：{email_info['subject']}")
        print("="*60)
        
        # 解析指令
        print("\n🔍 解析指令...")
        commands = parse_command(email_info['body'], email_info['subject'])
        
        if commands:
            print(f"✅ 识别到 {len(commands)} 个指令")
            
            # 执行指令
            print("\n🔧 执行指令...")
            results = []
            for cmd in commands:
                result = execute_command(cmd)
                results.append(result)
            
            # 发送钉钉通知
            print("\n📱 发送钉钉通知...")
            send_dingtalk_notification(email_info, commands, results)
        else:
            print("ℹ️ 未识别到具体指令")
            
            # 发送通知（仅记录）
            send_dingtalk_notification(email_info, [], [])
        
        print()
    
    # 关闭连接
    mail.close()
    mail.logout()
    
    print("="*60)
    print("✅ 任务完成！")
    print("="*60)

if __name__ == '__main__':
    main()
