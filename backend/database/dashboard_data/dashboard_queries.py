from backend.database.config import get_db_connection


# =========================
# DASHBOARD STATS
# =========================
def get_dashboard_stats(hospital_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Today assessments
        cursor.execute(
            """
                select count(*) from assessment
                where hospital_id=%s
                and date(created_at) = current_date

             """,
            (hospital_id,),
        )

        today = cursor.fetchone()[0]

        # High risk cases
        cursor.execute(
            """
                select count(*) from assessment
                where hospital_id=%s
                and risk_level = 'HIGH'
            """,
            (hospital_id,),
        )
        high_risk = cursor.fetchone()[0]

        # Cancer detected
        cursor.execute(
            """
            SELECT COUNT(*) FROM assessment
            WHERE hospital_id = %s AND cancer_type IS NOT NULL
        """,
            (hospital_id,),
        )
        cancers = cursor.fetchone()[0]

        # Active doctors
        cursor.execute(
            """
            SELECT COUNT(*) FROM users
            WHERE hospital_id = %s AND role = 'doctor'
        """,
            (hospital_id,),
        )
        doctors = cursor.fetchone()[0]

        # Chart data
        cursor.execute(
            """
            SELECT risk_level, cancer_type, confidence
            FROM assessment
            WHERE hospital_id = %s
        """,
            (hospital_id,),
        )
        assessments = cursor.fetchall()

        return {
            "today": today,
            "high_risk": high_risk,
            "cancers": cancers,
            "doctors": doctors,
            "assessments": assessments,
        }

    except Exception as e:
        pass
    finally:
        cursor.close()
        conn.close()


# =========================
# RECENT ASSESSMENTS
# =========================
def get_recent_assessments(hospital_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                a.id,
                a.created_at,
                a.risk_level,
                a.cancer_type,
                a.confidence,
                a.symptoms_json,

                p.full_name AS patient_name,
                p.age,
                p.gender,

                u.full_name AS doctors_name

            FROM assessment a
            JOIN patient p ON a.patient_id = p.id  # “For each assessment, attach the patient who was assessed”
           
            JOIN users u ON a.doctor_id = u.id

            WHERE a.hospital_id = %s
            ORDER BY a.created_at DESC
            LIMIT 10
        """,
            (hospital_id,),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


# =========================
# ALERTS
# =========================
def get_alerts(hospital_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                a.created_at,
                a.cancer_type,
                a.confidence,
                p.full_name
            FROM assessment a
            JOIN patient p ON a.patient_id = p.id
            WHERE a.hospital_id = %s
            AND a.risk_level = 'HIGH'
            ORDER BY a.created_at DESC
            LIMIT 5
        """,
            (hospital_id,),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()
