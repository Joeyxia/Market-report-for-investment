# 2026-02-28 邮箱系统记忆设置

## 需求
建立完整的邮箱管理系统，包括邮箱配置信息、联系人管理、邮件发送记录等，确保所有邮件相关信息都结构化存储。

## 数据库表设计建议

### 1. email_config 表（邮箱配置信息）
- config_id: INTEGER PRIMARY KEY AUTOINCREMENT
- smtp_server: TEXT - SMTP服务器地址
- smtp_port: INTEGER - SMTP端口
- email_address: TEXT - 发送邮箱地址
- display_name: TEXT - 显示名称
- auth_method: TEXT - 认证方式
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- is_active: BOOLEAN DEFAULT TRUE - 是否激活

### 2. email_contacts 表（邮件联系人）
- contact_id: INTEGER PRIMARY KEY AUTOINCREMENT  
- name: TEXT - 联系人姓名
- email_address: TEXT - 邮箱地址
- category: TEXT - 分类（如"report_recipient", "admin", "client"等）
- notes: TEXT - 备注信息
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- is_active: BOOLEAN DEFAULT TRUE

### 3. email_history 表（邮件发送历史）
- email_id: INTEGER PRIMARY KEY AUTOINCREMENT
- subject: TEXT - 邮件标题
- body_content: TEXT - 邮件正文内容
- recipient_ids: TEXT - 收件人ID列表（JSON格式）
- cc_ids: TEXT - 抄送人ID列表（JSON格式）
- bcc_ids: TEXT - 密送人ID列表（JSON格式）
- report_date: DATE - 关联的报告日期（如果适用）
- email_type: TEXT - 邮件类型（如"daily_report", "alert", "summary"等）
- status: TEXT - 发送状态（"sent", "failed", "queued"）
- sent_at: DATETIME - 发送时间
- error_message: TEXT - 错误信息（如果失败）

### 4. email_templates 表（邮件模板）
- template_id: INTEGER PRIMARY KEY AUTOINCREMENT
- template_name: TEXT - 模板名称
- subject_template: TEXT - 标题模板
- body_template: TEXT - 正文模板
- variables: TEXT - 模板变量（JSON格式）
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP

## 实施计划

### 第一阶段：数据库表创建
1. 在现有OpenViking数据库中添加上述4个表
2. 设置适当的索引和外键约束
3. 验证表结构正确性

### 第二阶段：数据迁移和初始化
1. 获取当前邮箱配置信息并存入email_config表
2. **需要用户提供Amy的邮箱地址**以初始化email_contacts表
3. 如果有历史邮件记录，迁移至email_history表

### 第三阶段：集成到日常工作流
1. 更新每日报告生成流程，在发送邮件时自动记录到email_history
2. 创建联系人管理接口
3. 实现邮件模板系统

## 当前待办事项
- [ ] **获取Amy的邮箱地址**（关键依赖）
- [ ] 创建数据库表结构
- [ ] 初始化邮箱配置
- [ ] 测试邮件发送和记录功能

## 数据保留策略
- 所有邮件历史永久保留
- 联系人信息定期备份
- 配置变更保留版本历史