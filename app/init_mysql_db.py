import pymysql
import hashlib
from datetime import datetime, timedelta

def hash_pw(pwd: str) -> str:
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def init_mysql():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='health_user',
        password='health_pass_2026',
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS health_platform DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cursor.execute("USE health_platform;")

    # 1. 用户表 (前台普通用户 + 后台管理员)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sys_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(100) NOT NULL,
        real_name VARCHAR(50) NOT NULL,
        role VARCHAR(20) NOT NULL DEFAULT 'USER',
        gender VARCHAR(10) DEFAULT '男',
        age INT DEFAULT 24,
        height DECIMAL(5,2) DEFAULT 175.0,
        weight DECIMAL(5,2) DEFAULT 68.5,
        target_weight DECIMAL(5,2) DEFAULT 65.0,
        phone VARCHAR(20),
        status INT DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 2. 身体数据历史表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS body_metrics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        height DECIMAL(5,2) NOT NULL,
        weight DECIMAL(5,2) NOT NULL,
        bmi DECIMAL(4,1) NOT NULL,
        systolic_bp INT DEFAULT 120,
        diastolic_bp INT DEFAULT 80,
        heart_rate INT DEFAULT 72,
        record_date DATE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE,
        UNIQUE KEY uk_user_date (user_id, record_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 3. 运动打卡记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_record (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        sport_name VARCHAR(50) NOT NULL,
        duration_min INT NOT NULL,
        calories_burned DECIMAL(6,1) NOT NULL,
        distance_km DECIMAL(6,2) DEFAULT 0.0,
        heart_rate INT DEFAULT 0,
        notes VARCHAR(255),
        workout_date DATE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 4. 饮食记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diet_record (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        meal_type VARCHAR(20) NOT NULL,
        food_name VARCHAR(100) NOT NULL,
        calories DECIMAL(6,1) NOT NULL,
        protein DECIMAL(5,1) DEFAULT 0.0,
        carbs DECIMAL(5,1) DEFAULT 0.0,
        fat DECIMAL(5,1) DEFAULT 0.0,
        diet_date DATE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 5. 运动计划与打卡表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise_plan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(100) NOT NULL,
        plan_type VARCHAR(50) NOT NULL,
        target_val DECIMAL(6,1) NOT NULL,
        current_val DECIMAL(6,1) DEFAULT 0.0,
        unit VARCHAR(20) NOT NULL,
        end_date DATE,
        status VARCHAR(20) DEFAULT '进行中',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 6. 系统公告表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_notice (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        content TEXT NOT NULL,
        author VARCHAR(50) DEFAULT '系统管理员',
        tag VARCHAR(20) DEFAULT '健康科普',
        status INT DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 7. 运动基础数据字典
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sport_dict (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        cal_per_min DECIMAL(4,1) NOT NULL,
        category VARCHAR(30) DEFAULT '有氧运动'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 种子数据清理与初始化
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE sys_user;")
    cursor.execute("TRUNCATE TABLE body_metrics;")
    cursor.execute("TRUNCATE TABLE workout_record;")
    cursor.execute("TRUNCATE TABLE diet_record;")
    cursor.execute("TRUNCATE TABLE exercise_plan;")
    cursor.execute("TRUNCATE TABLE system_notice;")
    cursor.execute("TRUNCATE TABLE sport_dict;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # 预置用户 (1 管理员 + 2 普通用户)
    pwd = hash_pw("123456")
    users = [
        ("admin", pwd, "平台系统管理员", "ADMIN", "男", 30, 178.0, 72.0, 70.0, "13800000000", 1),
        ("user_alex", pwd, "张健 (健身学员)", "USER", "男", 24, 175.0, 68.5, 65.0, "13911112222", 1),
        ("user_lisa", pwd, "李悦 (减脂打卡)", "USER", "女", 22, 165.0, 54.0, 50.0, "13922223333", 1),
    ]
    cursor.executemany("""
    INSERT INTO sys_user (username, password_hash, real_name, role, gender, age, height, weight, target_weight, phone, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, users)

    # 预置运动数据字典
    sports = [
        ("户外慢跑", 10.0, "有氧运动"),
        ("动感单车", 8.5, "有氧运动"),
        ("力量训练", 6.0, "抗阻无氧"),
        ("自由泳", 9.5, "有氧运动"),
        ("高强度跳绳", 11.5, "心肺HIIT"),
        ("羽毛球", 7.0, "球类竞技"),
        ("瑜伽拉伸", 4.0, "柔韧拉伸"),
    ]
    cursor.executemany("INSERT INTO sport_dict (name, cal_per_min, category) VALUES (%s, %s, %s);", sports)

    # 预置系统公告
    notices = [
        ("【健康科普】春夏季科学运动与水分电解质补充指南", "运动前后需注意规律补水，每次训练建议间隔15-20分钟少量慢饮。剧烈运动超过45分钟推荐补充含电解质饮品。", "系统管理员", "健康科普", 1),
        ("【平台公告】个人健康运动管理平台 2.0 正式上线", "欢迎使用本平台！平台现已支持身体指标跟踪、运动打卡、饮食热量平衡与健身目标管理。如遇问题请联系管理员。", "系统管理员", "平台通知", 1),
        ("【运动指南】科学减脂：关于热量赤字与蛋白质配比的解析", "减脂的核心在于建立适度的热量赤字（300-500 kcal/天），同时保证每公斤体重1.6~2.0克优质蛋白质摄入，防止肌肉流失。", "系统管理员", "运动指南", 1),
    ]
    cursor.executemany("INSERT INTO system_notice (title, content, author, tag, status) VALUES (%s, %s, %s, %s, %s);", notices)

    # 预置用户2 (张健) 的身体指标历史 (过去7天)
    today = datetime.now().date()
    weights = [69.8, 69.4, 69.2, 69.0, 68.8, 68.6, 68.5]
    for i, w in enumerate(weights):
        d = (today - timedelta(days=6-i)).strftime("%Y-%m-%d")
        bmi = round(w / (1.75 * 1.75), 1)
        cursor.execute("""
        INSERT INTO body_metrics (user_id, height, weight, bmi, systolic_bp, diastolic_bp, heart_rate, record_date)
        VALUES (2, 175.0, %s, %s, 118, 78, 70, %s);
        """, (w, bmi, d))

    # 预置运动打卡
    workouts = [
        (2, "户外慢跑", 35, 360.0, 5.2, 142, "晨跑 5.2公里，配速稳定在 6分40秒", today.strftime("%Y-%m-%d")),
        (2, "力量训练", 45, 230.0, 0.0, 128, "胸肌哑铃推举与器械夹胸", (today - timedelta(days=1)).strftime("%Y-%m-%d")),
        (2, "动感单车", 40, 320.0, 14.5, 150, "健身房单车晚课，跟骑节奏顺畅", (today - timedelta(days=2)).strftime("%Y-%m-%d")),
        (2, "自由泳", 40, 390.0, 1.2, 135, "室内恒温泳池自由泳 1200米", (today - timedelta(days=3)).strftime("%Y-%m-%d")),
        (2, "高强度跳绳", 25, 280.0, 0.0, 155, "间歇跳绳累计 2500 次", (today - timedelta(days=4)).strftime("%Y-%m-%d")),
        (2, "羽毛球", 60, 420.0, 0.0, 138, "与球友单打三局，心肺挑战极大", (today - timedelta(days=5)).strftime("%Y-%m-%d")),
    ]
    cursor.executemany("""
    INSERT INTO workout_record (user_id, sport_name, duration_min, calories_burned, distance_km, heart_rate, notes, workout_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, workouts)

    # 预置饮食记录
    diets = [
        (2, "早餐", "全麦吐司2片 + 煮鸡蛋2个 + 美式黑咖啡", 380.0, 18.0, 42.0, 8.0, today.strftime("%Y-%m-%d")),
        (2, "午餐", "香煎鸡胸肉150g + 紫米杂粮饭 + 清炒西兰花", 640.0, 46.0, 65.0, 12.0, today.strftime("%Y-%m-%d")),
        (2, "加餐", "脱脂希腊酸奶 + 鲜蓝莓一把", 160.0, 12.0, 18.0, 4.0, today.strftime("%Y-%m-%d")),
        (2, "晚餐", "清蒸巴沙鱼柳 + 甜玉米半根 + 蔬菜沙拉", 460.0, 35.0, 48.0, 7.0, today.strftime("%Y-%m-%d")),
    ]
    cursor.executemany("""
    INSERT INTO diet_record (user_id, meal_type, food_name, calories, protein, carbs, fat, diet_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, diets)

    # 预置运动计划
    plans = [
        (2, "本月户外累计跑量", "跑步", 50.0, 35.2, "公里", (today + timedelta(days=15)).strftime("%Y-%m-%d"), "进行中"),
        (2, "阶段减脂达标目标", "减脂", 65.0, 68.5, "公斤", (today + timedelta(days=30)).strftime("%Y-%m-%d"), "进行中"),
        (2, "每周抗阻训练打卡", "打卡", 12.0, 8.0, "次", (today + timedelta(days=10)).strftime("%Y-%m-%d"), "进行中"),
    ]
    cursor.executemany("""
    INSERT INTO exercise_plan (user_id, title, plan_type, target_val, current_val, unit, end_date, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, plans)

    conn.commit()
    conn.close()
    print("MySQL Database health_platform successfully initialized!")

if __name__ == "__main__":
    init_mysql()
