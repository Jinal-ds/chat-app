# frontend/app.py
import streamlit as st
import requests
from datetime import datetime, timezone, timedelta


import os
API = os.getenv("API_URL", "http://localhost:8000")
# ✅ uses "http://backend:8000" inside Docker
#    uses "http://localhost:8000" when running locally
# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="💬 Chat App",
    page_icon="💬",
    layout="wide"
)

# ── Helper: Auth headers ──────────────────────────────────
def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

# ── Helper: Format timestamp ──────────────────────────────
def fmt_time(iso_str):
    dt = datetime.fromisoformat(iso_str.replace("Z", ""))
    # Convert UTC → IST (UTC + 5:30)
    IST = timezone(timedelta(hours=5, minutes=30))
    dt_ist = dt.replace(tzinfo=timezone.utc).astimezone(IST)
    return dt_ist.strftime("%I:%M %p")

# ── Initialize session state ──────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "current_room" not in st.session_state:
    st.session_state.current_room = None

# ═══════════════════════════════════════════════════════════
# PAGE 1 — AUTH (Login / Register)
# ═══════════════════════════════════════════════════════════
def auth_page():
    st.title("💬 Chat App")
    st.subheader("Welcome! Please login or register.")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # --- Login Tab ---
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", use_container_width=True):
            if not email or not password:
                st.error("Please fill all fields")
            else:
                res = requests.post(f"{API}/auth/login", json={
                    "email": email,
                    "password": password
                })
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.user = data["user"]
                    st.success(f"Welcome back, {data['user']['name']}! 🎉")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Login failed"))

    # --- Register Tab ---
    with tab2:
        name = st.text_input("Full Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register", use_container_width=True):
            if not name or not email or not password:
                st.error("Please fill all fields")
            else:
                res = requests.post(f"{API}/auth/register", json={
                    "name": name,   
                    "email": email,
                    "password": password
                })
                if res.status_code == 201:
                    st.success("Account created! Please login. ✅")
                else:
                # ✅ Safely parse error — handle empty body
                    try:
                        detail = res.json().get("detail", "Registration failed")
                    except Exception:
                        detail = f"Error {res.status_code}: {res.text or 'Registration failed'}"
                    st.error(detail)

# ═══════════════════════════════════════════════════════════
# PAGE 2 — ROOMS LIST
# ═══════════════════════════════════════════════════════════
def rooms_page():
    # --- Sidebar ---
    with st.sidebar:
        st.title("💬 Chat App")
        st.write(f"👤 **{st.session_state.user['name']}**")
        st.write(f"📧 {st.session_state.user['email']}")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.current_room = None
            st.rerun()

    st.title("💬 Chat Rooms")

    # --- Create new room ---
    with st.expander("➕ Create New Room"):
        room_name = st.text_input("Room Name")
        room_desc = st.text_input("Description (optional)")
        if st.button("Create Room"):
            if not room_name:
                st.error("Room name is required")
            else:
                res = requests.post(
                    f"{API}/rooms/",
                    json={"name": room_name, "description": room_desc},
                    headers=auth_headers()
                )
                if res.status_code == 201:
                    st.success(f"Room '{room_name}' created! ✅")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Failed to create room"))

    st.divider()

    # --- List all rooms ---
    res = requests.get(f"{API}/rooms/", headers=auth_headers())

    if res.status_code == 200:
        rooms = res.json()
        if not rooms:
            st.info("No rooms yet. Create one above! 👆")
        else:
            st.subheader(f"🏠 Available Rooms ({len(rooms)})")
            for room in rooms:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"### 💬 {room['name']}")
                    if room.get("description"):
                        st.caption(room["description"])
                with col2:
                    if st.button("Enter →", key=f"enter_{room['id']}"):
                        st.session_state.current_room = room
                        st.rerun()
                st.divider()
    else:
        st.error("Failed to load rooms")

# ═══════════════════════════════════════════════════════════
# PAGE 3 — CHAT ROOM
# ═══════════════════════════════════════════════════════════
def chat_page():
    room = st.session_state.current_room

    # --- Sidebar ---
    with st.sidebar:
        st.title("💬 Chat App")
        st.write(f"👤 **{st.session_state.user['name']}**")
        st.divider()
        st.write(f"📍 **Current Room:**")
        st.write(f"💬 {room['name']}")
        if room.get("description"):
            st.caption(room["description"])
        st.divider()
        if st.button("⬅️ Back to Rooms", use_container_width=True):
            st.session_state.current_room = None
            st.rerun()
        if st.button("🔄 Refresh Messages", use_container_width=True):
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.current_room = None
            st.rerun()

    st.title(f"💬 {room['name']}")

    # --- Load messages ---
    res = requests.get(
        f"{API}/rooms/{room['id']}/messages",
        headers=auth_headers(),
        params={"limit": 50}
    )

    if res.status_code == 200:
        messages = res.json()
        messages = list(reversed(messages))  # oldest first

        if not messages:
            st.info("No messages yet. Say hello! 👋")
        else:
            for msg in messages:
                is_me = msg["sender_name"] == st.session_state.user["name"]

                if is_me:
                    # My messages — right aligned
                    col1, col2 = st.columns([2, 3])
                    with col2:
                        st.markdown(
                            f"""
                            <div style='background:#0084ff;color:white;
                                        padding:10px 15px;border-radius:18px 18px 4px 18px;
                                        margin:4px 0;text-align:right'>
                                <b>{msg['content']}</b>
                                <br><small style='opacity:0.7'>{fmt_time(msg['created_at'])}</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if st.button("🗑️ Delete", key=f"del_{msg['id']}"):
                            res = requests.delete(
                                f"{API}/rooms/{room['id']}/messages/{msg['id']}",
                                headers=auth_headers()
                            )
                            if res.status_code == 204:
                                st.success("Message deleted! ✅")
                                st.rerun()
                            else:
                                st.error("Failed to delete message")
                else:
                    # Other's messages — left aligned
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        st.markdown(
                            f"""
                            <div style='background:#f0f0f0;color:#000;
                                        padding:10px 15px;border-radius:18px 18px 18px 4px;
                                        margin:4px 0'>
                                <small style='color:#666'>👤 {msg['sender_name']}</small><br>
                                <b>{msg['content']}</b>
                                <br><small style='color:#999'>{fmt_time(msg['created_at'])}</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
    else:
        st.error("Failed to load messages")

    st.divider()

    # --- Send message ---
    col1, col2 = st.columns([5, 1])
    with col1:
        message = st.text_input(
            "Message",
            placeholder="Type your message...",
            label_visibility="collapsed",
            key="msg_input"
        )
    with col2:
        send = st.button("Send 📨", use_container_width=True)

    if send:
        if not message.strip():
            st.error("Message cannot be empty")
        else:
            res = requests.post(
                f"{API}/rooms/{room['id']}/messages",
                json={"content": message},
                headers=auth_headers()
            )
            if res.status_code == 201:
                st.rerun()
            else:
                st.error("Failed to send message")

# ═══════════════════════════════════════════════════════════
# ROUTER — decides which page to show
# ═══════════════════════════════════════════════════════════
if not st.session_state.token:
    auth_page()
elif st.session_state.current_room:
    chat_page()
else:
    rooms_page()