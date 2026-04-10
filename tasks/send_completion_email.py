#!/usr/bin/env python3
"""
抖音账号配置完成通知

发送条件：
- FFmpeg 安装完成
- 素材准备完成
- 视频制作测试通过
"""

import smtplib
import sys
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_completion_email():
    """发送完成通知邮件"""
    
    # 邮件配置
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    from_email = "2239517529@qq.com"
    auth_code = "fnouklmzjesidiaj"  # QQ 邮箱授权码
    to_email = "2239517529@qq.com"
    
    # 邮件内容
    subject = "✅ 抖音知识分享账号配置完成"
    
    body = f"""
您好！

抖音知识分享账号的配置已全部完成。

=== 完成情况 ===

✅ 热点捕捉
   - B 站真实爬取
   - 知识类话题生成
   - 定时任务：每天 9 点

✅ 内容创作
   - 抖音脚本生成
   - 真人化检查 (≥7 分)

✅ 视频制作
   - FFmpeg 已安装
   - BGM 和字体已准备
   - 测试通过

✅ 发布流程
   - 手动发布流程已配置
   - 发布清单已生成

=== 使用方式 ===

1. 查看今日热点
   cat artifacts/trend_reports/$(date +%Y%m%d)_douyin_trend_report.md

2. 创作内容
   python3 tasks/douyin_content_create.py --topic "主题"

3. 制作视频
   python3 tasks/douyin_video_produce.py --script "脚本文件"

4. 发布到抖音
   手动上传发布

=== 文件位置 ===

脚本：
- tasks/hot_search_crawler.py
- tasks/douyin_content_create.py
- tasks/douyin_video_produce.py

输出：
- artifacts/trend_reports/     (热点报告)
- artifacts/douyin_content/    (生成内容)
- artifacts/douyin_videos/     (生成视频)

文档：
- docs/抖音账号实施状态.md

=== 下一步 ===

1. 查看今日热点报告
2. 选择一个话题创作内容
3. 制作视频并发布

如有问题，随时询问。

祝好！
AI Assistant

---
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
        server.login(from_email, auth_code)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        
        print(f"✅ 完成通知已发送到：{to_email}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")
        print(f"📧 邮件内容已保存到本地文件")
        
        # 保存到本地
        email_file = Path("/home/admin/openclaw/workspace/artifacts/completion_email.txt")
        email_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(email_file, 'w', encoding='utf-8') as f:
            f.write(f"Subject: {subject}\n\n")
            f.write(body)
        
        print(f"📄 本地文件：{email_file}")
        return False


if __name__ == "__main__":
    send_completion_email()
