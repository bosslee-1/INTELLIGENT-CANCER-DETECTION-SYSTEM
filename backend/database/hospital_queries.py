import datetime
from database.config import query

# ======================
# CREATE HOSPITAL
# ======================
def create_hospital(
    hospital_id,
    name,
    email,
    phone,
    address,
    city,
    state,
    postal_code,
    country,
    hospital_type
):
    sql = """
        INSERT INTO hospital (
            id, name, email, phone, address, city, state,
            postal_code, country, hospital_type, created_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING *
    """

    result = query(sql, [
        hospital_id,
        name,
        email,
        phone,
        address,
        city,
        state,
        postal_code,
        country,
        hospital_type,
        datetime.datetime.utcnow()
    ])

    return result[0] if result else None


# ======================
# GET ALL HOSPITALS
# ======================
def get_all_hospitals():
    sql = "SELECT * FROM hospital ORDER BY created_at DESC"
    return query(sql)


# ======================
# GET HOSPITAL BY ID
# ======================
def get_hospital_by_id(hospital_id):
    sql = "SELECT * FROM hospital WHERE id = %s"
    result = query(sql, [hospital_id])
    return result[0] if result else None


# ======================
# GET HOSPITAL BY EMAIL
# ======================
def get_hospital_by_email(email):
    sql = "SELECT * FROM hospital WHERE email = %s"
    result = query(sql, [email])
    return result[0] if result else None


# ======================
# UPDATE HOSPITAL
# ======================
def update_hospital(
    hospital_id,
    name=None,
    email=None,
    phone=None,
    address=None,
    city=None,
    state=None,
    postal_code=None,
    country=None,
    hospital_type=None
):
    sql = """
        UPDATE hospital SET
            name = COALESCE(%s, name),
            email = COALESCE(%s, email),
            phone = COALESCE(%s, phone),
            address = COALESCE(%s, address),
            city = COALESCE(%s, city),
            state = COALESCE(%s, state),
            postal_code = COALESCE(%s, postal_code),
            country = COALESCE(%s, country),
            hospital_type = COALESCE(%s, hospital_type),
            updated_at = %s
        WHERE id = %s
        RETURNING *
    """

    result = query(sql, [
        name,
        email,
        phone,
        address,
        city,
        state,
        postal_code,
        country,
        hospital_type,
        datetime.datetime.utcnow(),
        hospital_id
    ])

    return result[0] if result else None


# ======================
# DELETE HOSPITAL
# ======================
def delete_hospital(hospital_id):
    sql = "DELETE FROM hospital WHERE id = %s"
    return query(sql, [hospital_id])