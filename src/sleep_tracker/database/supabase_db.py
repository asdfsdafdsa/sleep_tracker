from supabase import create_client, Client
from datetime import date
import httpx

SUPABASE_URL = "SUPABASE_URL"
SUPABASE_KEY = "SUPABASE_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_user(login, password):
    try:
        response = supabase.table("users").select("*").eq("login", login).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == password:
                return user
        return None
    except httpx.ConnectError:
        raise Exception("Нет подключения к интернету. Проверьте сеть и попробуйте снова.")
    except Exception as e:
        raise Exception(f"Ошибка при подключении к серверу: {str(e)}")

def save_sleep_data(login, sleep_time, wake_time, wellbeing, comment=""):
    today = str(date.today())
    data = {
        "login": login,
        "date": today,
        "sleep_time": sleep_time,
        "wake_time": wake_time,
        "wellbeing": wellbeing,
        "comment": comment
    }
    try:
        supabase.table("sleep_logs").insert(data).execute()
        return True
    except Exception as e:
        print(f"Ошибка при сохранении сна: {e}")
        return False

def fetch_sleep_logs(login=None, date=None):
    query = supabase.table("sleep_logs").select("*")
    if login:
        query = query.eq("login", login)
    if date:
        query = query.eq("date", date)
    try:
        data = query.execute().data
        return data
    except Exception as e:
        print(f"Ошибка при получении истории сна: {e}")
        return []

def has_today_entry(login):
    today = date.today().isoformat()
    try:
        response = supabase.table('sleep_logs').select('id').eq('login', login).eq('date', today).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Ошибка при проверке сегодняшней записи: {e}")
        return False 