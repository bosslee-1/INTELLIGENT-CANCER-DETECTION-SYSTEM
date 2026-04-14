# Supabase with Raw SQL


"""
ICDS - Database Configuration
Use DATABASE_URL in .env for PostgreSQL in production.
"""


import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    """Connect to Supabase PostgreSQL"""
    if not DATABASE_URL:
        raise Exception("❌ DATABASE_URL is not set in .env file")

    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


def init_database():
    """Create all necessary tables in Supabase"""
    conn = get_db_connection()
    cur = conn.cursor()

    print("Creating all tables if they dont exists....")

    # 1. Hospital Table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS hospital (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            hospital_type TEXT,
            address TEXT,
            verified BOOLEAN DEFAULT true,
            active BOOLEAN DEFAULT true,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """
    )

    # 2. User Table (Doctors & Admins)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS "user" (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            role TEXT DEFAULT 'doctor',
            hospital_id TEXT REFERENCES hospital(id),
            active BOOLEAN DEFAULT true,
            last_login TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """
    )

    # 3. Patient Table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patient (
            id TEXT PRIMARY KEY,
            hospital_id TEXT REFERENCES hospital(id),
            full_name TEXT NOT NULL,
            age INTEGER,
            gender INTEGER,           -- 1 = Male, 0 = Female
            contact TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """
    )

    # 4. Assessment Table (ML Prediction Results)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS assessment (
            id TEXT PRIMARY KEY,
            hospital_id TEXT REFERENCES hospital(id),
            patient_id TEXT REFERENCES patient(id),
            doctor_id TEXT REFERENCES "user"(id),
            risk_level TEXT,          -- HIGH, MEDIUM, LOW
            confidence FLOAT,
            cancer_type TEXT,
            symptoms_json TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """
    )

    # 5. OTPCode Table (Important for registration & login)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS otp_code (
            id SERIAL PRIMARY KEY,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            purpose TEXT,                    -- 'registration', 'login', 'reset_password'
            expires_at TIMESTAMPTZ NOT NULL,
            used BOOLEAN DEFAULT false,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """
    )

    # 6. AuditLog Table (Optional but good for security)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            hospital_id TEXT,
            action TEXT,
            resource TEXT,
            resource_id TEXT,
            details TEXT,
            ip_address TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """
    )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ All Supabase tables created successfully!")
