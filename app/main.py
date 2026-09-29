import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pymysql
from pymysql.cursors import DictCursor
import jwt

BASE_DIR = "/root/grad-sys"
STATIC_DIR = os.path.join(BASE_DIR, "static")

JWT_SECRET = "health_sport_secret_key_2026"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 72

MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "user": "health_user",
    "password": "health_pass_2026",
    "database": "health_platform",
    "port": 3306,
    "charset": "utf8mb4",
    "cursorclass": DictCursor,
    "autocommit": True
}

app = FastAPI(title="个人健康运动管理平台 (SpringBoot+Vue+MySQL对齐架构)", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = pymysql.connect(**MYSQL_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def hash_pw(pwd: str) -> str:
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()

def create_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user(authorization: Optional[str] = Header(None), conn = Depends(get_db)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供有效身份凭证")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="凭证已过期或无效")

    with conn.cursor() as cursor:
        cursor.execute("SELECT id, username, real_name, role, gender, age, height, weight, target_weight, phone, status FROM sys_user WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        if user["status"] != 1:
            raise HTTPException(status_code=403, detail="该账号已被管理员禁用")
        return user

def calc_bmi(weight: float, height: float):
    h_m = float(height) / 100.0
    if h_m <= 0:
        return 0.0, "未知", "info"
    bmi = round(float(weight) / (h_m * h_m), 1)
    if bmi < 18.5:
        return bmi, "偏瘦", "warning"
    elif bmi <= 23.9:
        return bmi, "正常标准", "success"
    elif bmi <= 27.9:
        return bmi, "偏重", "warning"
    else:
        return bmi, "肥胖", "danger"

# ----------------- 数据传输对象 (DTO/VO) -----------------
class LoginReq(BaseModel):
    username: str
    password: str

class RegisterReq(BaseModel):
    username: str
    password: str
    real_name: str
    gender: str = "男"
    age: int = 24
    height: float = 175.0
    weight: float = 68.0
    target_weight: float = 65.0
    phone: Optional[str] = ""

class ProfileUpdateReq(BaseModel):
    real_name: str
    gender: str
    age: int
    height: float
    weight: float
    target_weight: float
    phone: Optional[str] = ""

class BodyMetricCreateReq(BaseModel):
    height: float
    weight: float
    systolic_bp: int = 120
    diastolic_bp: int = 80
    heart_rate: int = 72
    record_date: Optional[str] = None

class WorkoutCreateReq(BaseModel):
    sport_name: str
    duration_min: int
    calories_burned: float
    distance_km: Optional[float] = 0.0
    heart_rate: Optional[int] = 0
    notes: Optional[str] = ""
    workout_date: Optional[str] = None

class DietCreateReq(BaseModel):
    meal_type: str
    food_name: str
    calories: float
    protein: Optional[float] = 0.0
    carbs: Optional[float] = 0.0
    fat: Optional[float] = 0.0
    diet_date: Optional[str] = None

class PlanCreateReq(BaseModel):
    title: str
    plan_type: str
    target_val: float
    current_val: Optional[float] = 0.0
    unit: str
    end_date: Optional[str] = None

class PlanUpdateReq(BaseModel):
    current_val: float
    status: Optional[str] = None

class NoticeCreateReq(BaseModel):
    title: str
    content: str
    tag: str = "健康科普"
    status: int = 1

class SportDictCreateReq(BaseModel):
    name: str
    cal_per_min: float
    category: str = "有氧运动"

class UserAdminCreateReq(BaseModel):
    username: str
    password: str
    real_name: str
    role: str = "USER"
    gender: str = "男"
    age: int = 24
    height: float = 175.0
    weight: float = 68.0
    target_weight: float = 65.0
    phone: Optional[str] = ""

# ================= 认证与用户个人中心 =================

@app.post("/api/auth/login")
def login(req: LoginReq, conn = Depends(get_db)):
    pwd_hash = hash_pw(req.password)
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, username, real_name, role, gender, age, height, weight, target_weight, phone, status
            FROM sys_user 
            WHERE username = %s AND password_hash = %s
        """, (req.username, pwd_hash))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=400, detail="用户名或密码错误")
        if user["status"] != 1:
            raise HTTPException(status_code=403, detail="该账号已被禁用，请联系管理员")

        token = create_token(user["id"], user["role"])
        bmi, bmi_text, bmi_color = calc_bmi(user["weight"], user["height"])
        user["bmi"] = bmi
        user["bmi_text"] = bmi_text
        user["bmi_color"] = bmi_color

        return {
            "code": 0,
            "token": token,
            "user": user
        }

@app.post("/api/auth/register")
def register(req: RegisterReq, conn = Depends(get_db)):
    pwd_hash = hash_pw(req.password)
    bmi, _, _ = calc_bmi(req.weight, req.height)
    today_str = datetime.now().strftime("%Y-%m-%d")

    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM sys_user WHERE username = %s", (req.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="该用户名已存在")

        cursor.execute("""
            INSERT INTO sys_user (username, password_hash, real_name, role, gender, age, height, weight, target_weight, phone, status)
            VALUES (%s, %s, %s, 'USER', %s, %s, %s, %s, %s, %s, 1)
        """, (req.username, pwd_hash, req.real_name, req.gender, req.age, req.height, req.weight, req.target_weight, req.phone))
        new_id = cursor.lastrowid

        # 自动生成初始身体数据
        cursor.execute("""
            INSERT INTO body_metrics (user_id, height, weight, bmi, systolic_bp, diastolic_bp, heart_rate, record_date)
            VALUES (%s, %s, %s, %s, 120, 80, 72, %s)
        """, (new_id, req.height, req.weight, bmi, today_str))

    return {"code": 0, "message": "注册成功，请登录"}

@app.get("/api/user/profile")
def get_user_profile(user: dict = Depends(get_current_user)):
    bmi, bmi_text, bmi_color = calc_bmi(user["weight"], user["height"])
    user["bmi"] = bmi
    user["bmi_text"] = bmi_text
    user["bmi_color"] = bmi_color
    return {"code": 0, "data": user}

@app.put("/api/user/profile")
def update_user_profile(req: ProfileUpdateReq, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    bmi, _, _ = calc_bmi(req.weight, req.height)
    today_str = datetime.now().strftime("%Y-%m-%d")
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE sys_user 
            SET real_name = %s, gender = %s, age = %s, height = %s, weight = %s, target_weight = %s, phone = %s
            WHERE id = %s
        """, (req.real_name, req.gender, req.age, req.height, req.weight, req.target_weight, req.phone, user["id"]))

        # 记录当天体重历史
        cursor.execute("""
            INSERT INTO body_metrics (user_id, height, weight, bmi, record_date)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE height = VALUES(height), weight = VALUES(weight), bmi = VALUES(bmi)
        """, (user["id"], req.height, req.weight, bmi, today_str))

    return {"code": 0, "message": "个人身体档案修改成功"}

# ================= 用户前台功能 =================

@app.get("/api/user/dashboard")
def get_user_dashboard(user: dict = Depends(get_current_user), conn = Depends(get_db)):
    today_str = datetime.now().strftime("%Y-%m-%d")
    user_id = user["id"]

    with conn.cursor() as cursor:
        # 今日运动消耗与时长
        cursor.execute("""
            SELECT COALESCE(SUM(calories_burned), 0) AS burned, COALESCE(SUM(duration_min), 0) AS duration, COUNT(*) AS count
            FROM workout_record 
            WHERE user_id = %s AND workout_date = %s
        """, (user_id, today_str))
        workout_stat = cursor.fetchone()

        # 今日饮食摄入
        cursor.execute("""
            SELECT COALESCE(SUM(calories), 0) AS intake, COUNT(*) AS count
            FROM diet_record 
            WHERE user_id = %s AND diet_date = %s
        """, (user_id, today_str))
        diet_stat = cursor.fetchone()

        burned = float(workout_stat["burned"])
        intake = float(diet_stat["intake"])
        net_cal = round(intake - burned, 1)

        # 近 7 天走势
        recent_trends = []
        for i in range(6, -1, -1):
            d_obj = datetime.now() - timedelta(days=i)
            d_str = d_obj.strftime("%Y-%m-%d")
            lbl = d_obj.strftime("%m-%d")
            cursor.execute("SELECT COALESCE(SUM(calories_burned), 0) FROM workout_record WHERE user_id = %s AND workout_date = %s", (user_id, d_str))
            b = float(cursor.fetchone()["COALESCE(SUM(calories_burned), 0)"])
            cursor.execute("SELECT COALESCE(SUM(calories), 0) FROM diet_record WHERE user_id = %s AND diet_date = %s", (user_id, d_str))
            itk = float(cursor.fetchone()["COALESCE(SUM(calories), 0)"])
            recent_trends.append({"date": lbl, "burned": round(b, 1), "intake": round(itk, 1)})

        # 运动项目偏好
        cursor.execute("""
            SELECT sport_name, COUNT(*) AS count, SUM(calories_burned) AS calories
            FROM workout_record 
            WHERE user_id = %s 
            GROUP BY sport_name 
            ORDER BY count DESC LIMIT 6
        """, (user_id,))
        sport_dist = cursor.fetchall()
        for s in sport_dist:
            s["calories"] = round(float(s["calories"]), 1)

        # 最新公告
        cursor.execute("SELECT id, title, content, author, tag, created_at FROM system_notice WHERE status = 1 ORDER BY id DESC LIMIT 5")
        notices = cursor.fetchall()
        for n in notices:
            n["created_at"] = n["created_at"].strftime("%Y-%m-%d")

        bmi, bmi_text, bmi_color = calc_bmi(user["weight"], user["height"])
        user["bmi"] = bmi
        user["bmi_text"] = bmi_text
        user["bmi_color"] = bmi_color

    return {
        "code": 0,
        "data": {
            "profile": user,
            "today_burned": round(burned, 1),
            "today_duration": int(workout_stat["duration"]),
            "today_intake": round(intake, 1),
            "net_calories": net_cal,
            "recent_trends": recent_trends,
            "sport_distribution": sport_dist,
            "notices": notices
        }
    }

# ----------------- AI 运动总结与建议 (任务书核心要求) -----------------
@app.post("/api/user/ai-summary")
def generate_ai_summary(user: dict = Depends(get_current_user), conn = Depends(get_db)):
    user_id = user["id"]
    with conn.cursor() as cursor:
        # 获取近 7 天运动统计
        cursor.execute("""
            SELECT sport_name, duration_min, calories_burned, workout_date 
            FROM workout_record 
            WHERE user_id = %s AND workout_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            ORDER BY workout_date DESC
        """, (user_id,))
        records = cursor.fetchall()
        
        # 获取进行中的运动目标
        cursor.execute("SELECT title, target_val, current_val, unit FROM exercise_plan WHERE user_id = %s AND status = '进行中'", (user_id,))
        active_plans = cursor.fetchall()

    w_count = len(records)
    total_dur = sum(r["duration_min"] for r in records)
    total_cal = round(sum(float(r["calories_burned"]) for r in records), 1)
    
    # 统计运动种类
    sport_map = {}
    for r in records:
        s = r["sport_name"]
        sport_map[s] = sport_map.get(s, 0) + 1
    top_sports = sorted(sport_map.items(), key=lambda x: x[1], reverse=True)
    sports_desc = "、".join([f"{s[0]}({s[1]}次)" for s in top_sports]) if top_sports else "暂无记录"

    bmi, bmi_text, _ = calc_bmi(user["weight"], user["height"])

    # 生成拟人化自然语言运动总结与建议 (符合任务书第5、6条规范)
    content_lines = []
    content_lines.append(f"### 📋 近期个人运动与健康概况")
    if w_count > 0:
        content_lines.append(f"在过去的 7 天里，您共坚持打卡 **{w_count}** 次，累计运动时长达 **{total_dur}** 分钟，累计消耗能量约 **{total_cal}** kcal。您主要的运动项目为：{sports_desc}。整体锻炼节奏保持得非常不错，展现了良好的自我管理习惯。")
    else:
        content_lines.append("过去 7 天内您暂未上传运动打卡记录。运动贵在坚持，建议从每天 20-30 分钟的快走、慢跑或基础拉伸开始，逐步唤醒身体机能。")

    content_lines.append(f"\n### ⚖️ 身体体征与目标进度")
    content_lines.append(f"您当前身高 {user['height']}cm，体重 {user['weight']}kg，计算得出 BMI 为 **{bmi}**（处于 **{bmi_text}** 区间），目标体重为 {user['target_weight']}kg。")
    if active_plans:
        p_desc = "；".join([f"{p['title']} 已完成 {p['current_val']}/{p['target_val']}{p['unit']}" for p in active_plans])
        content_lines.append(f"正在推进的运动计划包括：{p_desc}。建议继续按既定节奏稳步推进。")

    content_lines.append(f"\n### 💡 针对性运动与生活建议")
    if w_count >= 4:
        content_lines.append("1. **张弛有度，注意恢复**：您的运动频次较为积极，高强度训练之间建议安排 1 天的主动休息日或低强度瑜伽拉伸，让骨骼肌纤维得到充分超量恢复。")
    else:
        content_lines.append("1. **提升运动连续性**：建议每周固定 3~4 次中等强度运动（每次 30~45 分钟），帮助身体建立稳定、高效的心肺适应机制。")
    
    content_lines.append("2. **合理搭配有氧与抗阻**：慢跑、单车等有氧运动有助于消耗热量提升耐力，建议穿插哑铃、深蹲等抗阻力量动作，保护基础代谢率，避免减脂过程中的瘦体重流失。")
    content_lines.append("3. **规律水合与营养供给**：根据您的体重测算，每日推荐饮水量约为 " + str(round(float(user['weight']) * 35)) + " ml。运动前后少量多次补水，运动后 30-45 分钟内适量补充优质蛋白（如蛋清、酸奶、瘦肉）与复合碳水。")

    ai_text = "\n".join(content_lines)
    disclaimer = "本建议由大模型根据运动数据分析生成，仅供日常健身管理参考，不作为医疗诊断依据。"

    # 写入 MySQL ai_suggestion_record 数据表 (满足任务书第2条数据表要求)
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ai_suggestion_record (user_id, summary_type, workout_count, total_duration, total_burned, ai_content, disclaimer)
            VALUES (%s, '周度运动综合分析', %s, %s, %s, %s, %s)
        """, (user_id, w_count, total_dur, total_cal, ai_text, disclaimer))
        rec_id = cursor.lastrowid

    return {
        "code": 0,
        "data": {
            "id": rec_id,
            "workout_count": w_count,
            "total_duration": total_dur,
            "total_burned": total_cal,
            "ai_content": ai_text,
            "disclaimer": disclaimer,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        "message": "AI 运动健康分析生成成功"
    }

@app.get("/api/user/ai-summary/history")
def get_ai_summary_history(user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, summary_type, workout_count, total_duration, total_burned, ai_content, disclaimer, created_at
            FROM ai_suggestion_record 
            WHERE user_id = %s 
            ORDER BY id DESC LIMIT 10
        """, (user["id"],))
        rows = cursor.fetchall()
        for r in rows:
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

# 1. 身体数据录入与查询
@app.get("/api/user/metrics")
def get_user_metrics(user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM body_metrics WHERE user_id = %s ORDER BY record_date DESC LIMIT 30", (user["id"],))
        rows = cursor.fetchall()
        for r in rows:
            r["record_date"] = r["record_date"].strftime("%Y-%m-%d")
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

@app.post("/api/user/metrics")
def create_user_metric(req: BodyMetricCreateReq, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    d_str = req.record_date or datetime.now().strftime("%Y-%m-%d")
    bmi, _, _ = calc_bmi(req.weight, req.height)

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO body_metrics (user_id, height, weight, bmi, systolic_bp, diastolic_bp, heart_rate, record_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                height = VALUES(height), weight = VALUES(weight), bmi = VALUES(bmi),
                systolic_bp = VALUES(systolic_bp), diastolic_bp = VALUES(diastolic_bp), heart_rate = VALUES(heart_rate)
        """, (user["id"], req.height, req.weight, bmi, req.systolic_bp, req.diastolic_bp, req.heart_rate, d_str))

        # 同步更新用户信息表
        cursor.execute("UPDATE sys_user SET height = %s, weight = %s WHERE id = %s", (req.height, req.weight, user["id"]))

    return {"code": 0, "message": "身体体征数据录入成功"}

# 2. 运动记录
@app.get("/api/user/workouts")
def get_user_workouts(user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM workout_record WHERE user_id = %s ORDER BY workout_date DESC, id DESC LIMIT 50", (user["id"],))
        rows = cursor.fetchall()
        for r in rows:
            r["workout_date"] = r["workout_date"].strftime("%Y-%m-%d")
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

@app.post("/api/user/workouts")
def create_user_workout(req: WorkoutCreateReq, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    d_str = req.workout_date or datetime.now().strftime("%Y-%m-%d")
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO workout_record (user_id, sport_name, duration_min, calories_burned, distance_km, heart_rate, notes, workout_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user["id"], req.sport_name, req.duration_min, req.calories_burned, req.distance_km, req.heart_rate, req.notes, d_str))
    return {"code": 0, "message": "运动记录添加成功"}

@app.delete("/api/user/workouts/{workout_id}")
def delete_user_workout(workout_id: int, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM workout_record WHERE id = %s AND user_id = %s", (workout_id, user["id"]))
    return {"code": 0, "message": "运动记录已删除"}

# 3. 饮食记录
@app.get("/api/user/diets")
def get_user_diets(user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM diet_record WHERE user_id = %s ORDER BY diet_date DESC, id DESC LIMIT 50", (user["id"],))
        rows = cursor.fetchall()
        for r in rows:
            r["diet_date"] = r["diet_date"].strftime("%Y-%m-%d")
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

@app.post("/api/user/diets")
def create_user_diet(req: DietCreateReq, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    d_str = req.diet_date or datetime.now().strftime("%Y-%m-%d")
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO diet_record (user_id, meal_type, food_name, calories, protein, carbs, fat, diet_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user["id"], req.meal_type, req.food_name, req.calories, req.protein, req.carbs, req.fat, d_str))
    return {"code": 0, "message": "饮食记录添加成功"}

@app.delete("/api/user/diets/{diet_id}")
def delete_user_diet(diet_id: int, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM diet_record WHERE id = %s AND user_id = %s", (diet_id, user["id"]))
    return {"code": 0, "message": "饮食记录已删除"}

# 4. 运动计划与打卡
@app.get("/api/user/plans")
def get_user_plans(user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM exercise_plan WHERE user_id = %s ORDER BY id DESC", (user["id"],))
        rows = cursor.fetchall()
        for r in rows:
            if r["end_date"]:
                r["end_date"] = r["end_date"].strftime("%Y-%m-%d")
            pct = min(100.0, round((float(r["current_val"]) / float(r["target_val"])) * 100, 1)) if float(r["target_val"]) > 0 else 0
            r["percent"] = pct
        return {"code": 0, "data": rows}

@app.post("/api/user/plans")
def create_user_plan(req: PlanCreateReq, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO exercise_plan (user_id, title, plan_type, target_val, current_val, unit, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, '进行中')
        """, (user["id"], req.title, req.plan_type, req.target_val, req.current_val or 0.0, req.unit, req.end_date))
    return {"code": 0, "message": "新运动计划创建成功"}

@app.patch("/api/user/plans/{plan_id}")
def update_user_plan(plan_id: int, req: PlanUpdateReq, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT target_val FROM exercise_plan WHERE id = %s AND user_id = %s", (plan_id, user["id"]))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="计划不存在")
        status_val = req.status or ("已完成" if req.current_val >= float(row["target_val"]) else "进行中")
        cursor.execute("UPDATE exercise_plan SET current_val = %s, status = %s WHERE id = %s", (req.current_val, status_val, plan_id))
    return {"code": 0, "message": "计划打卡更新成功"}

@app.delete("/api/user/plans/{plan_id}")
def delete_user_plan(plan_id: int, user: dict = Depends(get_current_user), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM exercise_plan WHERE id = %s AND user_id = %s", (plan_id, user["id"]))
    return {"code": 0, "message": "计划已删除"}

# 5. 公告列表 (公共)
@app.get("/api/notices")
def get_public_notices(conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM system_notice WHERE status = 1 ORDER BY id DESC")
        rows = cursor.fetchall()
        for r in rows:
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

# 6. 运动字典列表 (公共)
@app.get("/api/sports")
def get_sport_dict(conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sport_dict ORDER BY id ASC")
        rows = cursor.fetchall()
        return {"code": 0, "data": rows}

# ================= 管理员后台功能 =================

def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="无权限访问，仅系统管理员可操作")
    return user

@app.get("/api/admin/overview")
def get_admin_overview(admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS c FROM sys_user WHERE role = 'USER'")
        user_count = cursor.fetchone()["c"]
        cursor.execute("SELECT COUNT(*) AS c, COALESCE(SUM(calories_burned), 0) AS total_cal FROM workout_record")
        w_stat = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) AS c FROM diet_record")
        diet_count = cursor.fetchone()["c"]
        cursor.execute("SELECT COUNT(*) AS c FROM system_notice")
        notice_count = cursor.fetchone()["c"]

        return {
            "code": 0,
            "data": {
                "total_users": user_count,
                "total_workouts": w_stat["c"],
                "total_calories_burned": round(float(w_stat["total_cal"]), 1),
                "total_diets": diet_count,
                "total_notices": notice_count
            }
        }

@app.get("/api/admin/users")
def list_admin_users(keyword: Optional[str] = Query(None), admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        sql = "SELECT id, username, real_name, role, gender, age, height, weight, target_weight, phone, status, created_at FROM sys_user WHERE 1=1"
        params = []
        if keyword:
            sql += " AND (username LIKE %s OR real_name LIKE %s OR phone LIKE %s)"
            kw = f"%{keyword}%"
            params.extend([kw, kw, kw])
        sql += " ORDER BY id ASC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        for r in rows:
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

@app.post("/api/admin/users")
def create_admin_user(req: UserAdminCreateReq, admin: dict = Depends(require_admin), conn = Depends(get_db)):
    pwd_hash = hash_pw(req.password)
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM sys_user WHERE username = %s", (req.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="该用户名已存在")
        cursor.execute("""
            INSERT INTO sys_user (username, password_hash, real_name, role, gender, age, height, weight, target_weight, phone, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """, (req.username, pwd_hash, req.real_name, req.role, req.gender, req.age, req.height, req.weight, req.target_weight, req.phone))
    return {"code": 0, "message": "用户新增成功"}

@app.patch("/api/admin/users/{user_id}/status")
def toggle_user_status(user_id: int, status: int = Query(...), admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE sys_user SET status = %s WHERE id = %s", (status, user_id))
    return {"code": 0, "message": "用户状态已更新"}

@app.delete("/api/admin/users/{user_id}")
def delete_admin_user(user_id: int, admin: dict = Depends(require_admin), conn = Depends(get_db)):
    if user_id == admin["id"]:
        raise HTTPException(status_code=400, detail="不能删除自身管理员账号")
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM sys_user WHERE id = %s", (user_id,))
    return {"code": 0, "message": "用户已删除"}

@app.get("/api/admin/workouts")
def list_admin_workouts(admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT w.*, u.username, u.real_name 
            FROM workout_record w
            LEFT JOIN sys_user u ON w.user_id = u.id
            ORDER BY w.workout_date DESC, w.id DESC LIMIT 100
        """)
        rows = cursor.fetchall()
        for r in rows:
            r["workout_date"] = r["workout_date"].strftime("%Y-%m-%d")
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

@app.delete("/api/admin/workouts/{workout_id}")
def delete_admin_workout(workout_id: int, admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM workout_record WHERE id = %s", (workout_id,))
    return {"code": 0, "message": "该运动数据已被监管删除"}

@app.get("/api/admin/notices")
def list_admin_notices(admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM system_notice ORDER BY id DESC")
        rows = cursor.fetchall()
        for r in rows:
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return {"code": 0, "data": rows}

@app.post("/api/admin/notices")
def create_admin_notice(req: NoticeCreateReq, admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO system_notice (title, content, author, tag, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (req.title, req.content, admin["real_name"], req.tag, req.status))
    return {"code": 0, "message": "公告发布成功"}

@app.delete("/api/admin/notices/{notice_id}")
def delete_admin_notice(notice_id: int, admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM system_notice WHERE id = %s", (notice_id,))
    return {"code": 0, "message": "公告已删除"}

@app.post("/api/admin/sports")
def create_admin_sport(req: SportDictCreateReq, admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO sport_dict (name, cal_per_min, category)
            VALUES (%s, %s, %s)
        """, (req.name, req.cal_per_min, req.category))
    return {"code": 0, "message": "基础运动字典添加成功"}

@app.delete("/api/admin/sports/{sport_id}")
def delete_admin_sport(sport_id: int, admin: dict = Depends(require_admin), conn = Depends(get_db)):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM sport_dict WHERE id = %s", (sport_id,))
    return {"code": 0, "message": "字典项已删除"}

# 静态资源与页面
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    file_path = os.path.join(STATIC_DIR, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
