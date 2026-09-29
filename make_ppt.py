import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # 配色方案
    COLOR_PRIMARY_DARK = RGBColor(6, 95, 70)     # #065f46 深森林绿
    COLOR_PRIMARY = RGBColor(16, 185, 129)       # #10b981 翡翠绿
    COLOR_ACCENT = RGBColor(59, 130, 246)        # #3b82f6 活力蓝
    COLOR_BG_LIGHT = RGBColor(248, 250, 252)     # #f8fafc 浅灰底色
    COLOR_CARD_BG = RGBColor(255, 255, 255)      # #ffffff 卡片纯白
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)       # #0f172a 沉稳正文黑
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748b 辅助灰
    COLOR_BORDER = RGBColor(226, 232, 240)       # #e2e8f0 边框淡灰
    COLOR_ORANGE = RGBColor(234, 88, 12)         # #ea580c 警示暖橙
    COLOR_INDIGO = RGBColor(79, 70, 229)         # #4f46e5 管理员紫

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_LIGHT
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_tag="毕业设计系统总结汇报"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.0))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_tag = tf.paragraphs[0]
        p_tag.text = f"● {category_tag}"
        p_tag.font.name = "Microsoft YaHei"
        p_tag.font.size = Pt(12)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_PRIMARY_DARK
        p_tag.space_after = Pt(4)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Microsoft YaHei"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_MAIN

    def add_card(slide, left, top, width, height, title, items, tag="", tag_color=COLOR_PRIMARY_DARK):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_BORDER
        card.line.width = Pt(1)

        tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = f"【{tag}】"
            p_tag.font.name = "Microsoft YaHei"
            p_tag.font.size = Pt(11)
            p_tag.font.bold = True
            p_tag.font.color.rgb = tag_color
            p_tag.space_after = Pt(2)
            p_t = tf.add_paragraph()
        else:
            p_t = tf.paragraphs[0]

        p_t.text = title
        p_t.font.name = "Microsoft YaHei"
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN
        p_t.space_after = Pt(8)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"• {it}"
            p_it.font.name = "Microsoft YaHei"
            p_it.font.size = Pt(12)
            p_it.font.color.rgb = COLOR_TEXT_MUTED
            p_it.space_after = Pt(6)

    # ================= Slide 1: 封面页 =================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🏃 毕业设计核心成果全景汇报"
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(167, 243, 208) # 浅绿
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "个人健康运动管理平台的设计与实现"
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "大白话讲透：系统做了什么、怎么运行的、大模型AI如何赋能，以及技术全貌"
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(209, 250, 229)
    p.space_after = Pt(36)

    p = tf1.add_paragraph()
    p.text = "架构规范：SpringBoot契约 + Vue3响应式 + MySQL8.0数据持久化 + 真实大模型API接入\n部署环境：已正式部署至阿里云 Linux VPS (Port: 8090) 稳定常驻运行"
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(240, 253, 244)

    # ================= Slide 2: 为什么做这个系统？（大白话痛点拆解） =================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "为什么要做这款系统？—— 解决日常生活里的真痛点")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "零散记录像'打水漂'",
             [
                 "很多人想管住嘴、迈开腿，但通常都在微信群、备忘录里随手一记。",
                 "隔几天回头看，记录东一块西一块，根本不知道自己总共运动了多少天。",
                 "数据没有归档整理，无法沉淀为有价值的个人健康数字资产。"
             ],
             tag="痛点一：散乱无章", tag_color=COLOR_ORANGE)

    add_card(s2, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "文字记录不会'算账'",
             [
                 "普通备忘录只能记下吃了什么、跑了多少米，但它不知道这代表什么。",
                 "身体BMI是否健康？今天到底形成了热量赤字（减脂）还是热量盈余（储能）？",
                 "缺乏量化算法与自动化折算，导致盲目锻炼、很难看到科学正反馈。"
             ],
             tag="痛点二：缺乏算力", tag_color=COLOR_ORANGE)

    add_card(s2, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "商业软件变成了'大卖场'",
             [
                 "像Keep、薄荷健康等大型商业应用，打开先弹3秒开屏广告。",
                 "界面塞满了直播带货、健身打卡社区、充值年费VIP买课推荐。",
                 "普通人就想干干净净记个步、查个体重，却要在花哨的功能堆里找半天。"
             ],
             tag="痛点三：臃肿繁杂", tag_color=COLOR_ORANGE)

    # ================= Slide 3: 什么是“能量天平”？（核心特色大白话） =================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "什么是“能量天平”？—— 系统的核心计算法则")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "吃多少 vs 消耗多少，心里一本账",
             [
                 "【净卡路里差】= 今日饮食总摄入 - 今日运动总消耗。",
                 "差值为负数：说明形成了'热量赤字'，身体正在调用脂肪储备供能，减脂阶段达标！",
                 "差值为正数：说明形成了'热量结余'，多余热量有储积风险，需增加锻炼或控制晚饭。",
                 "系统每当你打卡一次运动或记录一餐饮食，顶部能量天平立刻秒级重新核算，即时反馈！"
             ],
             tag="能量收支核心模型", tag_color=COLOR_PRIMARY_DARK)

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "身体关键指标四重奏",
             [
                 "【BMI 身体质量指数】：按体重(kg)/身高²(m²)自动换算，红绿黄健康标签直观分级（偏瘦/正常/偏重/肥胖）。",
                 "【基础代谢率 (BMR)】：采用国际 Mifflin-St Jeor 权威公式，算出用户'躺着不动一天最低所需消耗'，守护身体底线。",
                 "【每日推荐饮水】：根据用户实测体重，按 35ml/kg 标准动态测算，提醒规律补充水分。",
                 "【血压与静息心率跟踪】：高压/低压/脉搏历史建档，全方位监测心血管机能。"
             ],
             tag="健康量化四件套", tag_color=COLOR_ACCENT)

    # ================= Slide 4: 用户端能干啥？（前台核心功能清单） =================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "用户前台能干啥？—— 为日常锻炼打造的顺手工具")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(2.5),
             "日常运动打卡流水",
             [
                 "支持慢跑、单车、力量训练、游泳、跳绳、球类、瑜伽等主流项目。",
                 "输入时长自动折算消耗卡路里，记录配速里程、心率与锻炼心得。"
             ],
             tag="运动模块", tag_color=COLOR_PRIMARY_DARK)

    add_card(s4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(2.5),
             "健康饮食营养记录",
             [
                 "按早餐、午餐、晚餐、加餐分餐记录食物明细与总热量。",
                 "同步统计蛋白质、碳水化合物、脂肪三大基础营养素。"
             ],
             tag="饮食模块", tag_color=COLOR_PRIMARY_DARK)

    add_card(s4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(2.5),
             "运动计划目标管理",
             [
                 "设立跑量、体重达标或每周打卡次数等阶段性 Flag 目标。",
                 "内置动态进度条，支持快速累加打卡，达标自动变绿。"
             ],
             tag="计划模块", tag_color=COLOR_PRIMARY_DARK)

    add_card(s4, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.5),
             "近 7 天双轨走势图与运动偏好大盘",
             [
                 "绿色柱子代表每日运动消耗，蓝色柱子代表每日饮食摄入，近7天收支对比一目了然。",
                 "根据累计打卡自动统计用户的'运动偏好占比'，看出自己是更偏向有氧还是力量。"
             ],
             tag="可视化大盘", tag_color=COLOR_ACCENT)

    add_card(s4, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.5),
             "个人档案修改与体征录入",
             [
                 "身高、体重、目标体重随时修改，自动同步重新计算 BMI 并归档历史体重。",
                 "支持随时补录体征测量历史，趋势线随时调阅。"
             ],
             tag="档案管理", tag_color=COLOR_ACCENT)

    # ================= Slide 5: 管理端管什么？（后台管理功能大白话） =================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "管理员后台管什么？—— 像'物业管家'一样稳健运行")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(2.5),
             "全平台运行态势概览 (KPI大盘)",
             [
                 "一眼看清全站注册总用户数、全站打卡总次数、全站累计消耗热量。",
                 "掌握平台整体用户活跃度，无需手工统计报表。"
             ],
             tag="管理工作台", tag_color=COLOR_INDIGO)

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5),
             "用户信息管理与状态开关",
             [
                 "表格化展示所有注册用户，支持按用户名、真实姓名、手机号模糊检索。",
                 "配有一键 Switch 账号开关（随时启用或禁用违规用户），带超级管理员误删防护。"
             ],
             tag="用户中心", tag_color=COLOR_INDIGO)

    add_card(s5, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.5),
             "全站运动流水穿透监管",
             [
                 "后台可查阅全站所有用户上传的打卡明细与卡路里记录。",
                 "若发现恶意刷量或虚假异常数据，管理员可一键监管删除，维护平台纯净。"
             ],
             tag="数据监管", tag_color=COLOR_INDIGO)

    add_card(s5, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.5),
             "公告发布与基础运动字典维护",
             [
                 "公告发布：向全平台推送科普指南、运动技巧或系统升级通告。",
                 "运动字典：自由维护运动项目及其每分钟参考卡路里系数，前台打卡即可自动调用。"
             ],
             tag="系统配置", tag_color=COLOR_INDIGO)

    # ================= Slide 6: 本系统最亮眼的黑科技 —— 生成式 AI 深度融入 =================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "系统的核心亮点 —— 生成式 AI 深度融入与自然语言教练")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "AI 运动私人教练：会看数据、会讲人话",
             [
                 "【不讲套话，基于真实打卡】：系统提取用户近 7 天真实打卡次数（如5次）、总时长（185分钟）、总消耗（1580 kcal）及主打项目，输入大模型Prompt上下文。",
                 "【阶段周报总结】：AI 会生成通俗自然的点评：'过去7天您坚持了5次打卡，以慢跑和单车为主，节奏非常好…'。",
                 "【定制生活化建议】：结合 BMI 及目标进度，针对性提示'适当补充优质蛋白'、'安排休息日防疲劳'、'推荐饮水2398ml'。",
                 "【落盘归档】：生成结果不仅呈现在前端，还会自动存入 MySQL 的 ai_suggestion_record 历史表中！"
             ],
             tag="任务书核心第5、6条", tag_color=COLOR_PRIMARY_DARK)

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "两条极其重要的工程底线与技术防护",
             [
                 "【红线一：严禁医疗诊断（合规防范）】：",
                 "任务书明确要求：'不将医疗诊断类AI作为课题内容'。系统在每一份 AI 建议底部均强制附带橙色显著提示：'⚠️ 本建议仅供日常健身参考，不作为医疗诊断依据'。",
                 "【红线二：大模型超时与失败容错（健全防御）】：",
                 "大模型外部 API 偶尔会遇到网络抖动、超时或鉴权失败（任务书第8条特意要求测试此类场景）。",
                 "系统内置了本地智能降级引擎，在外部 API 故障时自动无缝接管，保证系统绝不白屏、绝不报错、永远可用！"
             ],
             tag="工程安全与容错规范", tag_color=COLOR_ORANGE)

    # ================= Slide 7: 软件工程里的“人机协同”（任务书第10条：学生主体） =================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "软件工程人机协同 —— 'AI辅助、人机协同、人工核验、学生主体'")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "阶段一：需求与建模",
             [
                 "【AI 辅助】：使用大模型头脑风暴，罗列健身人群在运动打卡、分餐、BMI监测上的典型需求。",
                 "【学生主体核验】：结合毕业设计 15 周开发周期，剔除华而不实的社交与电商逻辑，提炼出 5 大用户核心功能。",
                 "借助 AI 起草初始 SQL 脚本，学生核对第三范式与外键级联关系，规范字段类型。"
             ],
             tag="设计阶段", tag_color=COLOR_PRIMARY_DARK)

    add_card(s7, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "阶段二：编码与深度Debug",
             [
                 "【AI 辅助】：生成 RESTful 路由脚手架、MySQL 异步查询逻辑及 ElementUI 基础模板。",
                 "【学生排查修复实战】：",
                 "① 发现 HTML 规范对自定义组件自闭合标签支持差（<el-table-column /> 会导致表头嵌套坍塌），学生人工将其重构成完整闭合标签，彻底根治 Bug！",
                 "② 针对手机屏幕排版进行深度媒体查询优化，消除单字折行。"
             ],
             tag="开发阶段", tag_color=COLOR_ACCENT)

    add_card(s7, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "阶段三：测试与答辩准备",
             [
                 "【AI 辅助】：利用大模型自动生成边界测试用例（如超长输入、0数据、极端BMI等）。",
                 "【人机协同测试】：学生真机执行测试用例，并在无头浏览器（Headless Chrome）中模拟 375px 手机端与 1280px 电脑端多分辨率校验。",
                 "【过程记录】：完整保留关键开发 Prompt 与交互历史，答辩时能够讲透底层每一行代码原理！"
             ],
             tag="测试阶段", tag_color=COLOR_INDIGO)

    # ================= Slide 8: 底层数据库设计（MySQL 8张大表大白话） =================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "数据库设计 —— MySQL 中的 8 张核心大表（通俗大白话拆解）")

    tables = [
        ("sys_user", "全平台用户花名册", "保存用户名、加密密码、真实姓名、角色(USER/ADMIN)、身高体重与账号启禁状态。"),
        ("body_metrics", "身体体征记账本", "记录每次测量的身高、体重、算好的BMI、血压高低压、静息心率与测量日期。"),
        ("sport_dict", "运动项目标准字典", "定义运动名称（如单车/慢跑）、运动大类及每分钟参考消耗系数，给前台计算卡路里做依据。"),
        ("workout_record", "运动流汗打卡流水", "记录谁、哪天、做了什么运动、练了多少分钟、消耗了多少卡路里、运动里程与心得。"),
        ("diet_record", "一日三餐饮食清单", "记录谁、哪餐（早中晚加餐）、吃了什么食物、摄入了多少卡路里与三大营养素。"),
        ("exercise_plan", "阶段Flag目标表", "立下的运动Flag（如月跑50公里），保存目标值、当前已完成进度、百分比与状态。"),
        ("ai_suggestion_record", "AI教练评语档案库", "专门存储大语言模型生成的阶段性运动周报、量化分析点评与健康运动建议文本。"),
        ("system_notice", "系统公共大喇叭", "存放管理员发布的健康科普知识、运动技巧与平台维护通知，支持标签筛选。")
    ]

    for idx, (t_name, t_label, t_desc) in enumerate(tables):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8) if col == 0 else Inches(6.8)
        y = Inches(1.6 + row * 1.3)

        c = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(1.15))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_BG
        c.line.color.rgb = COLOR_BORDER
        c.line.width = Pt(1)

        tb = s8.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), Inches(5.3), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = f"🗃️ {t_name} —— {t_label}"
        p1.font.name = "Microsoft YaHei"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_PRIMARY_DARK
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = t_desc
        p2.font.name = "Microsoft YaHei"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # ================= Slide 9: 实际运行与部署效果（实测数据） =================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "实际运行与云端部署效果 —— 经过深度调优的真机实测")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(2.5),
             "极简低资源消耗调优 (轻量高并发)",
             [
                 "【实测内存】：后端服务仅占 38.9MB 内存，MySQL 数据库仅占 32.1MB 内存！",
                 "关闭了耗内存的 Performance Schema，调优缓冲池与连接数，整机留有 500MB+ 空闲内存，轻巧不卡顿。",
                 "配置 systemd 系统守护进程，开机自启、崩溃自愈，确保答辩演示 100% 稳定。"
             ],
             tag="服务器运行指标", tag_color=COLOR_PRIMARY_DARK)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5),
             "手机与电脑深度自适应优化",
             [
                 "【手机移动端 (<768px)】：单列流式卡片，表格横向触控滑动，顶栏与弹窗完美分层，无任何文字截断或折行。",
                 "【电脑宽屏端 (1280px+)】：自适应双栏网格与柱状大盘，数据对齐严谨，空间利用充盈。",
                 "真机多分辨率视觉分析（Headless Chrome截图+视觉审查）双重达标！"
             ],
             tag="多端排版体验", tag_color=COLOR_ACCENT)

    add_card(s9, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.5),
             "云端公网即时体验通道",
             [
                 "公网在线体验地址：http://<server-ip>:8090/ （随时公网访问，评委老师手机/电脑扫码直接开看）",
                 "预置答辩演示账号：",
                 "① 管理员后台账号：admin （密码：123456）—— 查看全站监管、用户启禁与字典配置；",
                 "② 健身学员前台账号：user_alex （张健）—— 体验打卡、7天走势图与一键生成 AI 运动周报；",
                 "③ 减脂打卡前台账号：user_lisa （李悦）—— 体验多用户饮食与计划数据隔离；",
                 "顶部还贴心配备了免密秒切下拉菜单，现场答辩汇报时无需繁琐退登，1秒切换身份演示！"
             ],
             tag="部署上线信息", tag_color=COLOR_PRIMARY_DARK)

    # ================= Slide 10: 总结与答辩结语 =================
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg10.line.fill.background()

    tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.2))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "🎯 毕业设计成果结语"
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(167, 243, 208)
    p.space_after = Pt(14)

    p = tf10.add_paragraph()
    p.text = "小而美、真实可用、严谨合规的工程实践"
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(20)

    conclusions = [
        "1. 架构完整：扎实完成了 B/S 前后端分离全套系统开发与 MySQL 关系数据库设计；",
        "2. 业务闭环：从身体指标、运动打卡到饮食营养与目标推进，实现了能量天平全链路闭环；",
        "3. AI赋能特色：严格遵循任务书规范，真实接入大模型生成通俗运动周报，并坚守非医疗诊断底线；",
        "4. 工程规范：践行'AI辅助、人机协同、人工核验、学生主体'，代码经受住实机与多端考验。"
    ]
    for c in conclusions:
        p = tf10.add_paragraph()
        p.text = c
        p.font.name = "Microsoft YaHei"
        p.font.size = Pt(15)
        p.font.color.rgb = RGBColor(240, 253, 244)
        p.space_after = Pt(8)

    p_end = tf10.add_paragraph()
    p_end.text = "\n恳请各位评委老师与指导老师批评指正！谢谢！"
    p_end.font.name = "Microsoft YaHei"
    p_end.font.size = Pt(16)
    p_end.font.bold = True
    p_end.font.color.rgb = RGBColor(253, 224, 71) # 黄色高亮

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    out_file = "/root/grad-sys/static/个人健康运动管理平台_毕设总结报告.pptx"
    create_presentation(out_file)
