# 剪映 CLI 登录指南

## 登录方式

### 方式 1: 手动登录（推荐）

```bash
dreamina login
```

会打开浏览器，用抖音/头条账号登录。

### 方式 2: Headless 登录（适合 AI Agent）

```bash
dreamina login --headless
```

会输出一个 JSON，需要复制到剪映网页版完成授权。

---

## 登录后生成视频

### 检查积分
```bash
dreamina user_credit
```

### 生成 AI 工具推荐视频

```bash
dreamina text2video \
  --prompt="AI 工具推荐，5 个效率工具展示，科技感背景，文字动画，抖音竖屏风格" \
  --duration=15 \
  --ratio=9:16 \
  --video_resolution=720p \
  --model_version=seedance2.0fast \
  --poll=60
```

### 查看任务列表
```bash
dreamina list_task --gen_status=success
```

### 查询结果
```bash
dreamina query_result --submit_id=<任务 ID>
```

---

## 生成参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `--prompt` | 视频描述 | 详细描述场景 |
| `--duration` | 时长（秒） | 5-15 秒 |
| `--ratio` | 比例 | 9:16（抖音竖屏） |
| `--video_resolution` | 分辨率 | 720p |
| `--model_version` | 模型 | seedance2.0fast |
| `--poll` | 等待时间 | 60 秒 |

---

## 提示词模板

### AI 工具推荐
```
AI 工具推荐，5 个效率工具展示，科技感背景，文字动画，抖音竖屏风格，专业演示，高清质量
```

### 开场钩子
```
震惊风格开场，红色警告图标，黑色背景，大字标题，抖音热门风格
```

### 工具展示
```
软件界面展示，科技感边框，文字说明，平滑转场，专业演示风格
```

---

**注意**: 首次使用可能需要在剪映网页版完成授权确认。
