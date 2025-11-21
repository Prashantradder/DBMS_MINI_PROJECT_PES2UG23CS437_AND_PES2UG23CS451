# import streamlit as st
# import pandas as pd
# from sqlalchemy import text
# from db_config import get_engine
# from utils.db_helpers import fetch_all
# from utils.auth import (
#     student_exists, account_exists, verify_student_login,
#     create_login_password, create_full_student_account,
#     verify_admin_login
# )


# # =====================================================================
# #                          LOGIN PAGE
# # =====================================================================
# def login_ui():
#     st.title("🔐 Login Portal")

#     # --------------------- Student Login ---------------------
#     st.header("Student Login")

#     srn = st.text_input("Enter SRN")

#     if st.button("Next"):
#         st.session_state.temp_srn = srn
#         st.rerun()

#     if "temp_srn" in st.session_state:
#         srn = st.session_state.temp_srn

#         # ---- Case 3: SRN not found → Create full account (no password) ----
#         if not student_exists(srn):
#             st.warning("SRN not found. Please create your student account.")

#             st.subheader("Create Full Account")
#             with st.form("full_signup_form", clear_on_submit=True):
#                 name = st.text_input("Full Name")
#                 dept = st.text_input("Department")
#                 year = st.number_input("Year", min_value=1, max_value=4)
#                 contact = st.text_input("Contact Number")

#                 if st.form_submit_button("Create Account"):
#                     create_full_student_account(srn, name, dept, year, contact)
#                     st.success("Account created! Now create your password.")
#                     del st.session_state.temp_srn
#                     st.session_state.temp_srn = srn   # Go to Case 2
#                     st.rerun()
#             return

#         # ---- Case 2: SRN exists but password missing ----
#         if not account_exists(srn):
#             st.info("Your SRN exists but password not set yet.")

#             st.subheader("Create Password")
#             with st.form("pwd_form", clear_on_submit=True):
#                 pwd = st.text_input("Create Password", type="password")

#                 if st.form_submit_button("Set Password"):
#                     create_login_password(srn, pwd)
#                     st.success("Password created! You can now login.")
#                     del st.session_state.temp_srn
#                     st.rerun()
#             return

#         # ---- Case 1: SRN + Password exists → Login ----
#         st.subheader("Login")
#         with st.form("login_form", clear_on_submit=True):
#             pwd = st.text_input("Password", type="password")
#             if st.form_submit_button("Login"):
#                 if verify_student_login(srn, pwd):
#                     st.session_state.logged_in = True
#                     st.session_state.role = "user"
#                     st.session_state.srn = srn
#                     st.success("Login successful!")
#                     del st.session_state.temp_srn
#                     st.rerun()
#                 else:
#                     st.error("Incorrect password!")
#         return

#     # --------------------- Admin Login ---------------------
#     st.header("Admin Login")

#     admin_name = st.text_input("Admin Username")
#     admin_pwd = st.text_input("Admin Password", type="password")

#     if st.button("Login as Admin"):
#         if verify_admin_login(admin_name, admin_pwd):
#             st.session_state.logged_in = True
#             st.session_state.role = "admin"
#             st.success("Admin login successful!")
#             st.rerun()
#         else:
#             st.error("Invalid admin credentials")


# # =====================================================================
# #                 DELETE CONFIRMATION POPUP
# # =====================================================================
# def confirm_delete(message, key):
#     st.warning(message)
#     c1, c2 = st.columns(2)
#     with c1:
#         yes = st.button("Confirm Delete", key=f"y{key}")
#     with c2:
#         no = st.button("Cancel", key=f"n{key}")
#     if yes:
#         return True
#     if no:
#         return False
#     return None


# # =====================================================================
# #                          ADMIN DASHBOARD
# # =====================================================================
# def admin_dashboard():
#     st.title("🎓 Admin Panel")

#     menu = ["Home", "Students", "Clubs", "Events", "Sponsors", "Results", "Logout"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     if choice == "Logout":
#         st.session_state.clear()
#         st.rerun()

#     # -------------------- HOME --------------------
#     if choice == "Home":
#         st.header("Dashboard Summary")
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Students", len(fetch_all("SELECT * FROM Student")))
#         col2.metric("Clubs", len(fetch_all("SELECT * FROM Club")))
#         col3.metric("Events", len(fetch_all("SELECT * FROM Event")))
#         col4.metric("Sponsors Added", len(fetch_all("SELECT * FROM Event_Sponsor")))

#     # -------------------- STUDENTS --------------------
#     if choice == "Students":
#         st.header("📚 Student Management")
#         df = fetch_all("SELECT * FROM Student ORDER BY SRN")

#         # Filter by year
#         years = ["All"] + sorted(df["Year"].unique())
#         y = st.selectbox("Filter by Year", years)
#         if y != "All":
#             df = df[df["Year"] == int(y)]

#         # Search
#         q = st.text_input("Search by SRN or Name")
#         if q:
#             df = df[df.apply(lambda r: q.lower() in r["SRN"].lower()
#                              or q.lower() in r["Student_Name"].lower(), axis=1)]

#         st.dataframe(df, use_container_width=True)

#     # -------------------- CLUBS --------------------
#     if choice == "Clubs":
#         st.header("🎯 Club Management")

#         df = fetch_all("SELECT * FROM Club ORDER BY Club_ID")
#         st.subheader("Existing Clubs")
#         st.dataframe(df, use_container_width=True)

#         # Add club
#         st.subheader("➕ Add New Club")
#         with st.form("add_club", clear_on_submit=True):
#             cname = st.text_input("Club Name")
#             ctype = st.text_input("Club Type")
#             coord = st.text_input("Faculty Coordinator")
#             add_btn = st.form_submit_button("Add Club")

#             if add_btn:
#                 try:
#                     next_id = int(fetch_all("SELECT IFNULL(MAX(Club_ID),0)+1 AS id FROM Club")['id'][0])
#                     sql = text("INSERT INTO Club VALUES (:id, :name, :type, :coord)")
#                     engine = get_engine()
#                     with engine.connect() as conn:
#                         conn.execute(sql, {"id": next_id, "name": cname, "type": ctype, "coord": coord})
#                         conn.commit()
#                     st.success("🎉 Club Added Successfully!")
#                     st.rerun()
#                 except Exception as e:
#                     st.error(f"Error: {e}")

#         # Update club
#         st.subheader("✏️ Update Club")
#         if not df.empty:
#             cid = st.selectbox("Select Club ID", df["Club_ID"].tolist())
#             row = df[df["Club_ID"] == cid].iloc[0]

#             with st.form("update_club", clear_on_submit=True):
#                 newname = st.text_input("Club Name", row["Club_Name"])
#                 newtype = st.text_input("Club Type", row["Club_Type"])
#                 newcoord = st.text_input("Faculty Coordinator", row["Faculty_Coordinator"])
#                 if st.form_submit_button("Update Club"):
#                     try:
#                         sql = text("""
#                             UPDATE Club SET Club_Name=:n, Club_Type=:t, Faculty_Coordinator=:c
#                             WHERE Club_ID=:id
#                         """)
#                         engine = get_engine()
#                         with engine.connect() as conn:
#                             conn.execute(sql, {"n": newname, "t": newtype,
#                                                "c": newcoord, "id": int(cid)})
#                             conn.commit()
#                         st.success("✅ Club Updated Successfully!")
#                         st.rerun()
#                     except Exception as e:
#                         st.error(e)
    
#     # -------------------- VIEW CLUB REGISTRATIONS --------------------
#         st.subheader("👥 Students Registered for Clubs")

#         club_reg_list = fetch_all("SELECT Club_ID, Club_Name FROM Club ORDER BY Club_ID")

#         selected_club_view = st.selectbox(
#             "Select Club",
#             [f"{row.Club_ID} - {row.Club_Name}" for idx, row in club_reg_list.iterrows()],
#             key="club_view_members"
#         )

#         club_id_view = int(selected_club_view.split(" - ")[0])

#         club_members = fetch_all(f"""
#             SELECT s.SRN, s.Student_Name, s.Department, s.Year, r.Domain
#             FROM Recruitment r
#             JOIN Student s ON r.SRN = s.SRN
#             WHERE r.Club_ID = {club_id_view}
#         """)

#         st.dataframe(club_members, use_container_width=True)
    

    

#     # -------------------- EVENTS --------------------
#     if choice == "Events":
#         st.header("🎫 Event Management")

#         df = fetch_all("SELECT * FROM Event ORDER BY Event_ID")

#         # Filter
#         types = ["All"] + sorted(df["Event_Type"].unique())
#         t = st.selectbox("Filter by Event Type", types)
#         if t != "All":
#             df = df[df["Event_Type"] == t]

#         st.dataframe(df, use_container_width=True)

#         # Add event
#         st.subheader("➕ Add Event")
#         with st.form("add_event", clear_on_submit=True):
#             name = st.text_input("Event Name")
#             etype = st.text_input("Event Type")
#             date = st.date_input("Event Date")
#             venue = st.text_input("Venue")
#             pay = st.number_input("Payment", min_value=0.0, format="%f")
#             club = st.number_input("Club ID", min_value=1)

#             if st.form_submit_button("Add Event"):
#                 try:
#                     next_id = int(fetch_all("SELECT IFNULL(MAX(Event_ID),0)+1 AS id FROM Event")['id'][0])
#                     sql = text("""
#                         INSERT INTO Event VALUES (:id, :name, :type, :date, :venue, :pay, :cid)
#                     """)
#                     engine = get_engine()
#                     with engine.connect() as conn:
#                         conn.execute(sql, {
#                             "id": next_id, "name": name, "type": etype,
#                             "date": date, "venue": venue,
#                             "pay": float(pay), "cid": int(club)
#                         })
#                         conn.commit()
#                     st.success("🎉 Event Added Successfully!")
#                     st.rerun()
#                 except Exception as e:
#                     st.error(e)

#         # Update/Delete
#         st.subheader("✏️ Update or ❌ Delete Event")
#         df_all = fetch_all("SELECT * FROM Event ORDER BY Event_ID")
#         if not df_all.empty:
#             eid = st.selectbox("Select Event ID", df_all["Event_ID"])
#             row = df_all[df_all["Event_ID"] == eid].iloc[0]

#             with st.form("update_event", clear_on_submit=True):
#                 newname = st.text_input("Event Name", row["Event_Name"])
#                 newtype = st.text_input("Event Type", row["Event_Type"])
#                 newdate = st.date_input("Date", pd.to_datetime(row["Date"]))
#                 newvenue = st.text_input("Venue", row["Venue"])
#                 newpay = st.number_input("Payment", value=float(row["Payment"]))
#                 newclub = st.number_input("Club ID", value=int(row["Club_ID"]))

#                 if st.form_submit_button("Update Event"):
#                     try:
#                         sql = text("""
#                             UPDATE Event SET Event_Name=:n, Event_Type=:t, Date=:d, Venue=:v,
#                             Payment=:p, Club_ID=:cid WHERE Event_ID=:id
#                         """)
#                         engine = get_engine()
#                         with engine.connect() as conn:
#                             conn.execute(sql, {
#                                 "n": newname, "t": newtype, "d": newdate,
#                                 "v": newvenue, "p": float(newpay),
#                                 "cid": int(newclub), "id": int(eid)
#                             })
#                             conn.commit()
#                         st.success("✅ Event Updated Successfully!")
#                         st.rerun()
#                     except Exception as e:
#                         st.error(e)

#             if st.button("Delete Event"):
#                 resp = confirm_delete(f"Delete Event ID {eid} permanently?", key=f"ev{eid}")
#                 if resp is True:
#                     try:
#                         engine = get_engine()
#                         with engine.connect() as conn:
#                             conn.execute(text("DELETE FROM Event WHERE Event_ID=:id"), {"id": int(eid)})
#                             conn.commit()
#                         st.success("❌ Event Deleted")
#                         st.rerun()
#                     except Exception as e:
#                         st.error(e)

#         # -------------------- VIEW EVENT REGISTRATIONS --------------------
#         st.subheader("👥 Students Registered for Events")

#         event_list_view = fetch_all("SELECT Event_ID, Event_Name FROM Event ORDER BY Event_ID")

#         selected_event_view = st.selectbox(
#             "Select Event",
#             [f"{row.Event_ID} - {row.Event_Name}" for idx, row in event_list_view.iterrows()],
#             key="event_view_regs"
#         )

#         event_id_view = int(selected_event_view.split(" - ")[0])

#         event_regs = fetch_all(f"""
#             SELECT er.Reg_ID, s.SRN, s.Student_Name, s.Department, s.Year, er.Registered_On
#             FROM Event_Registration er
#             JOIN Student s ON er.SRN = s.SRN
#             WHERE er.Event_ID = {event_id_view}
#             ORDER BY er.Reg_ID
#         """)

#         st.dataframe(event_regs, use_container_width=True)
#     # -------------------- SPONSORS --------------------
#     if choice == "Sponsors":
#         st.header("💰 Sponsorship Management")

#         df = fetch_all("""
#             SELECT es.Event_ID, es.Sponsor_ID, s.Sponsor_Name, es.Amount
#             FROM Event_Sponsor es
#             LEFT JOIN Sponsor s ON es.Sponsor_ID = s.Sponsor_ID
#             ORDER BY es.Event_ID
#         """)
#         st.dataframe(df, use_container_width=True)

#         # Fetch sponsor list
#         sponsor_df = fetch_all("SELECT Sponsor_ID, Sponsor_Name FROM Sponsor")

#         # Fetch event list
#         event_df = fetch_all("SELECT Event_ID, Event_Name FROM Event")

#         st.subheader("➕ Add or ✏️ Update Sponsorship")

#         with st.form("sponsor_form", clear_on_submit=True):

#             # Select Event from dropdown
#             selected_event = st.selectbox(
#                 "Event",
#                 [f"{row.Event_ID} - {row.Event_Name}" for idx, row in event_df.iterrows()]
#             )
#             ev = int(selected_event.split(" - ")[0])  # Extract Event ID

#             # Select Sponsor by NAME
#             selected_sponsor = st.selectbox(
#                 "Sponsor",
#                 sponsor_df["Sponsor_Name"].tolist()
#             )
#             # Extract Sponsor ID from name
#             sid = int(sponsor_df[sponsor_df["Sponsor_Name"] == selected_sponsor]["Sponsor_ID"].iloc[0])

#             # Amount must be > 0
#             amt = st.number_input("Amount (must be > 0)", min_value=1.0, format="%f")

#             submit = st.form_submit_button("Save")

#             if submit:
#                 try:
#                     engine = get_engine()

#                     # Check if already present
#                     exists = fetch_all(
#                         f"SELECT * FROM Event_Sponsor WHERE Event_ID={ev} AND Sponsor_ID={sid}"
#                     )

#                     if exists.empty:
#                         sql = text("INSERT INTO Event_Sponsor (Event_ID, Sponsor_ID, Amount) VALUES (:e, :s, :a)")
#                         message = "Added"
#                     else:
#                         sql = text("UPDATE Event_Sponsor SET Amount=:a WHERE Event_ID=:e AND Sponsor_ID=:s")
#                         message = "Updated"

#                     with engine.connect() as conn:
#                         conn.execute(sql, {"e": ev, "s": sid, "a": float(amt)})
#                         conn.commit()

#                     st.success(f"🎉 Sponsorship {message} Successfully!")
#                     st.rerun()

#                 except Exception as e:
#                     st.error(f"Error: {e}")


#     # -------------------- RESULTS --------------------
   
#     if choice == "Results":
#         st.header("🏆 Add Result")

#         # ----------- RESULT TABLE: SHOW ALL RESULTS -----------
#         st.subheader("📄 All Results")

#         df_results = fetch_all("""
#             SELECT r.Result_ID, r.Position, s.Student_Name, e.Event_Name
#             FROM Result r
#             JOIN Student s ON r.SRN = s.SRN
#             JOIN Event e ON r.Event_ID = e.Event_ID
#             ORDER BY r.Result_ID
#         """)

#         st.dataframe(df_results, use_container_width=True)

#         st.markdown("---")

#         # ----------- ADD RESULT FORM -----------
#         st.subheader("➕ Add Result")

#         events_df = fetch_all("SELECT Event_ID, Event_Name FROM Event")

#         if events_df.empty:
#             st.info("No events available.")
#         else:

#             # Event dropdown
#             selected_event = st.selectbox(
#                 "Select Event",
#                 [f"{row.Event_ID} - {row.Event_Name}" for idx, row in events_df.iterrows()]
#             )

#             event_id = int(selected_event.split(" - ")[0])

#             with st.form("add_result_form", clear_on_submit=True):

#                 srn = st.text_input("Student SRN")

#                 position = st.selectbox(
#                     "Position",
#                     ["Winner", "Runner-Up", "Participant"]
#                 )

#                 submit = st.form_submit_button("Add Result")

#                 if submit:
#                     try:
#                         next_id = int(fetch_all("SELECT IFNULL(MAX(Result_ID),0)+1 AS id FROM Result")['id'][0])
#                         sql = text("""
#                             INSERT INTO Result (Result_ID, Position, SRN, Event_ID)
#                             VALUES (:id, :pos, :srn, :ev)
#                         """)

#                         engine = get_engine()
#                         with engine.connect() as conn:
#                             conn.execute(sql, {
#                                 "id": next_id,
#                                 "pos": position,
#                                 "srn": srn,
#                                 "ev": event_id
#                             })
#                             conn.commit()

#                         st.success("🏆 Result Added Successfully!")
#                         st.rerun()

#                     except Exception as e:
#                         st.error(f"Error: {e}")

# # =====================================================================
# #                       STUDENT DASHBOARD
# # =====================================================================
# def user_dashboard():
#     st.title("🎓 Student Dashboard")

#     menu = ["My Clubs", "Events", "Results", "Logout"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     # --------------------- LOGOUT ---------------------
#     if choice == "Logout":
#         st.session_state.clear()
#         st.rerun()

#     # --------------------- MY CLUBS ---------------------
#     if choice == "My Clubs":
#         srn = st.session_state.srn
#         st.header("📌 My Clubs")

#         df = fetch_all(f"""
#             SELECT c.Club_Name, c.Club_Type
#             FROM Recruitment r
#             JOIN Club c ON r.Club_ID = c.Club_ID
#             WHERE r.SRN='{srn}'
#         """)

#         st.dataframe(df, use_container_width=True)

#     # --------------------- EVENTS (VIEW + REGISTER) ---------------------
#     if choice == "Events":
#         srn = st.session_state.srn
#         st.header("📅 Available Events")

#         event_df = fetch_all("""
#             SELECT Event_ID, Event_Name, Event_Type, Date, Venue
#             FROM Event ORDER BY Date
#         """)

#         st.dataframe(event_df, use_container_width=True)

#         st.subheader("📝 Register for an Event")

#         selected_event = st.selectbox(
#             "Select Event",
#             [f"{row.Event_ID} - {row.Event_Name}" for idx, row in event_df.iterrows()],
#             key="event_reg_select"
#         )

#         event_id = int(selected_event.split(" - ")[0])

#         if st.button("Register for Event"):
#             try:
#                 exists = fetch_all(f"""
#                     SELECT * FROM Event_Registration
#                     WHERE SRN='{srn}' AND Event_ID={event_id}
#                 """)

#                 if not exists.empty:
#                     st.warning("⚠️ Already registered!")
#                 else:
#                     next_id = int(fetch_all("""
#                         SELECT IFNULL(MAX(Reg_ID),0)+1 AS id 
#                         FROM Event_Registration
#                     """)['id'][0])

#                     sql = text("""
#                         INSERT INTO Event_Registration (Reg_ID, SRN, Event_ID)
#                         VALUES (:id, :srn, :ev)
#                     """)

#                     engine = get_engine()
#                     with engine.connect() as conn:
#                         conn.execute(sql, {"id": next_id, "srn": srn, "ev": event_id})
#                         conn.commit()

#                     st.success("🎉 Registered Successfully!")
#                     st.rerun()

#             except Exception as e:
#                 st.error(f"Error: {e}")

#         # --------------------- MY EVENT REGISTRATIONS ---------------------
#         st.subheader("📄 My Event Registrations")

#         reg_df = fetch_all(f"""
#             SELECT e.Event_Name, e.Date, e.Venue
#             FROM Event_Registration er
#             JOIN Event e ON er.Event_ID = e.Event_ID
#             WHERE er.SRN='{srn}'
#         """)

#         st.dataframe(reg_df, use_container_width=True)

#     # --------------------- RESULTS ---------------------
#     if choice == "Results":
#         srn = st.session_state.srn
#         st.header("🏆 My Results")

#         df = fetch_all(f"""
#             SELECT r.Position, e.Event_Name
#             FROM Result r
#             JOIN Event e ON r.Event_ID = e.Event_ID
#             WHERE r.SRN='{srn}'
#         """)

#         st.dataframe(df, use_container_width=True)



import streamlit as st
import pandas as pd
from sqlalchemy import text
from db_config import get_engine
from utils.db_helpers import fetch_all
from utils.auth import (
    student_exists, account_exists, verify_student_login,
    create_login_password, create_full_student_account,
    verify_admin_login
)

# ---------------------------
# Login page
# ---------------------------
def login_ui():
    st.title("🔐 Login Portal")

    # Student Login
    st.header("Student Login")
    srn = st.text_input("Enter SRN", key="login_srn")

    if st.button("Next", key="login_next"):
        # store temp srn for flow
        st.session_state.temp_srn = srn
        st.rerun()

    if "temp_srn" in st.session_state:
        srn = st.session_state.temp_srn

        # Case 3: SRN not in Student -> create full account (no password asked here)
        if not student_exists(srn):
            st.warning("SRN not found. Please create your student account.")
            st.subheader("Create Full Account")
            with st.form("full_signup_form", clear_on_submit=True):
                name = st.text_input("Full Name", key="full_name")
                dept = st.text_input("Department", key="full_dept")
                year = st.number_input("Year", min_value=1, max_value=4, key="full_year")
                contact = st.text_input("Contact Number", key="full_contact")

                if st.form_submit_button("Create Account"):
                    try:
                        create_full_student_account(srn, name, dept, year, contact)
                        st.success("Account created! Now create your password.")
                        # move to Case 2 (password creation)
                        del st.session_state.temp_srn
                        st.session_state.temp_srn = srn
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating account: {e}")
            return

        # Case 2: SRN exists but password missing -> create password
        if not account_exists(srn):
            st.info("Your SRN exists but password not set yet.")
            st.subheader("Create Password")
            with st.form("pwd_form", clear_on_submit=True):
                pwd = st.text_input("Create Password", type="password", key="pwd_new")

                if st.form_submit_button("Set Password"):
                    try:
                        create_login_password(srn, pwd)
                        st.success("Password created! You can now login.")
                        if "temp_srn" in st.session_state:
                            del st.session_state.temp_srn
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error setting password: {e}")
            return

        # Case 1: SRN + Password exists -> login form
        st.subheader("Login")
        with st.form("login_form", clear_on_submit=True):
            pwd = st.text_input("Password", type="password", key="pwd_login")
            if st.form_submit_button("Login"):
                try:
                    if verify_student_login(srn, pwd):
                        st.session_state.logged_in = True
                        st.session_state.role = "user"
                        st.session_state.srn = srn
                        st.success("Login successful!")
                        if "temp_srn" in st.session_state:
                            del st.session_state.temp_srn
                        st.rerun()
                    else:
                        st.error("Incorrect password!")
                except Exception as e:
                    st.error(f"Login error: {e}")
        return

    # Admin Login (below student flow)
    st.header("Admin Login")
    admin_name = st.text_input("Admin Username", key="admin_user")
    admin_pwd = st.text_input("Admin Password", type="password", key="admin_pwd")

    if st.button("Login as Admin", key="admin_login_btn"):
        try:
            if verify_admin_login(admin_name, admin_pwd):
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.success("Admin login successful!")
                st.rerun()
            else:
                st.error("Invalid admin credentials")
        except Exception as e:
            st.error(f"Admin login error: {e}")


# ---------------------------
# Confirm delete (simple)
# ---------------------------
def confirm_delete(message, key):
    st.warning(message)
    c1, c2 = st.columns(2)
    with c1:
        yes = st.button("Confirm Delete", key=f"y{key}")
    with c2:
        no = st.button("Cancel", key=f"n{key}")
    if yes:
        return True
    if no:
        return False
    return None


# ---------------------------
# Admin dashboard
# ---------------------------
def admin_dashboard():
    st.title("🎓 Admin Panel")
    menu = ["Home", "Students", "Clubs", "Events", "Sponsors", "Results", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Logout":
        st.session_state.clear()
        st.rerun()

    # HOME
    if choice == "Home":
        st.header("Dashboard Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Students", len(fetch_all("SELECT * FROM Student")))
        col2.metric("Clubs", len(fetch_all("SELECT * FROM Club")))
        col3.metric("Events", len(fetch_all("SELECT * FROM Event")))
        col4.metric("Sponsors Added", len(fetch_all("SELECT * FROM Event_Sponsor")))

    # STUDENTS
    if choice == "Students":
        st.header("📚 Student Management")
        df = fetch_all("SELECT * FROM Student ORDER BY SRN")

        years = ["All"] + sorted(df["Year"].unique()) if not df.empty else ["All"]
        y = st.selectbox("Filter by Year", years)
        if y != "All":
            df = df[df["Year"] == int(y)]

        q = st.text_input("Search by SRN or Name")
        if q and not df.empty:
            df = df[df.apply(lambda r: q.lower() in str(r["SRN"]).lower() or q.lower() in str(r["Student_Name"]).lower(), axis=1)]

        st.dataframe(df, use_container_width=True)

    # CLUBS
    if choice == "Clubs":
        st.header("🎯 Club Management")

        df = fetch_all("SELECT * FROM Club ORDER BY Club_ID")
        st.subheader("Existing Clubs")
        st.dataframe(df, use_container_width=True)

        # Add club
        st.subheader("➕ Add New Club")
        with st.form("add_club", clear_on_submit=True):
            cname = st.text_input("Club Name")
            ctype = st.text_input("Club Type")
            coord = st.text_input("Faculty Coordinator")
            if st.form_submit_button("Add Club"):
                try:
                    next_id = int(fetch_all("SELECT IFNULL(MAX(Club_ID),0)+1 AS id FROM Club")['id'][0])
                    sql = text("INSERT INTO Club VALUES (:id, :name, :type, :coord)")
                    engine = get_engine()
                    with engine.connect() as conn:
                        conn.execute(sql, {"id": next_id, "name": cname, "type": ctype, "coord": coord})
                        conn.commit()
                    st.success("🎉 Club Added Successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        # Update club
        st.subheader("✏️ Update Club")
        if not df.empty:
            cid = st.selectbox("Select Club ID", df["Club_ID"].tolist(), key="update_club_id")
            row = df[df["Club_ID"] == cid].iloc[0]

            with st.form("update_club", clear_on_submit=True):
                newname = st.text_input("Club Name", row["Club_Name"])
                newtype = st.text_input("Club Type", row["Club_Type"])
                newcoord = st.text_input("Faculty Coordinator", row["Faculty_Coordinator"])
                if st.form_submit_button("Update Club"):
                    try:
                        sql = text("""
                            UPDATE Club SET Club_Name=:n, Club_Type=:t, Faculty_Coordinator=:c
                            WHERE Club_ID=:id
                        """)
                        engine = get_engine()
                        with engine.connect() as conn:
                            conn.execute(sql, {"n": newname, "t": newtype, "c": newcoord, "id": int(cid)})
                            conn.commit()
                        st.success("✅ Club Updated Successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(e)

        # View club registrations (inside Clubs menu)
        st.subheader("👥 Students Registered for Clubs")
        club_reg_list = fetch_all("SELECT Club_ID, Club_Name FROM Club ORDER BY Club_ID")
        if club_reg_list.empty:
            st.info("No clubs found.")
        else:
            selected_club_view = st.selectbox(
                "Select Club",
                [f"{row.Club_ID} - {row.Club_Name}" for idx, row in club_reg_list.iterrows()],
                key="club_view_members"
            )
            club_id_view = int(selected_club_view.split(" - ")[0])
            club_members = fetch_all(f"""
                SELECT s.SRN, s.Student_Name, s.Department, s.Year, r.Domain
                FROM Recruitment r
                JOIN Student s ON r.SRN = s.SRN
                WHERE r.Club_ID = {club_id_view}
            """)
            st.dataframe(club_members, use_container_width=True)

    # EVENTS
    if choice == "Events":
        st.header("🎫 Event Management")
        df = fetch_all("SELECT * FROM Event ORDER BY Event_ID")

        types = ["All"] + sorted(df["Event_Type"].unique()) if not df.empty else ["All"]
        t = st.selectbox("Filter by Event Type", types, key="filter_event_type")
        if t != "All":
            df = df[df["Event_Type"] == t]

        st.dataframe(df, use_container_width=True)

        # Add Event
        st.subheader("➕ Add Event")
        with st.form("add_event", clear_on_submit=True):
            name = st.text_input("Event Name", key="add_event_name")
            etype = st.text_input("Event Type", key="add_event_type")
            date = st.date_input("Event Date", key="add_event_date")
            venue = st.text_input("Venue", key="add_event_venue")
            pay = st.number_input("Payment", min_value=0.0, format="%f", key="add_event_pay")
            club = st.number_input("Club ID", min_value=1, key="add_event_club")

            if st.form_submit_button("Add Event"):
                try:
                    next_id = int(fetch_all("SELECT IFNULL(MAX(Event_ID),0)+1 AS id FROM Event")['id'][0])
                    sql = text("INSERT INTO Event VALUES (:id, :name, :type, :date, :venue, :pay, :cid)")
                    engine = get_engine()
                    with engine.connect() as conn:
                        conn.execute(sql, {"id": next_id, "name": name, "type": etype, "date": date, "venue": venue, "pay": float(pay), "cid": int(club)})
                        conn.commit()
                    st.success("🎉 Event Added Successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(e)

        # Update/Delete Event
        st.subheader("✏️ Update or ❌ Delete Event")
        df_all = fetch_all("SELECT * FROM Event ORDER BY Event_ID")
        if not df_all.empty:
            eid = st.selectbox("Select Event ID", df_all["Event_ID"], key="update_event_sel")
            row = df_all[df_all["Event_ID"] == eid].iloc[0]

            with st.form("update_event", clear_on_submit=True):
                newname = st.text_input("Event Name", row["Event_Name"], key="upd_name")
                newtype = st.text_input("Event Type", row["Event_Type"], key="upd_type")
                newdate = st.date_input("Date", pd.to_datetime(row["Date"]), key="upd_date")
                newvenue = st.text_input("Venue", row["Venue"], key="upd_venue")
                newpay = st.number_input("Payment", value=float(row["Payment"]), key="upd_pay")
                newclub = st.number_input("Club ID", value=int(row["Club_ID"]), key="upd_club")

                if st.form_submit_button("Update Event"):
                    try:
                        sql = text("""
                            UPDATE Event SET Event_Name=:n, Event_Type=:t, Date=:d, Venue=:v,
                            Payment=:p, Club_ID=:cid WHERE Event_ID=:id
                        """)
                        engine = get_engine()
                        with engine.connect() as conn:
                            conn.execute(sql, {"n": newname, "t": newtype, "d": newdate, "v": newvenue, "p": float(newpay), "cid": int(newclub), "id": int(eid)})
                            conn.commit()
                        st.success("✅ Event Updated Successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(e)

            if st.button("Delete Event", key=f"delete_event_{eid}"):
                resp = confirm_delete(f"Delete Event ID {eid} permanently?", key=f"ev{eid}")
                if resp is True:
                    try:
                        engine = get_engine()
                        with engine.connect() as conn:
                            # delete dependent rows first to satisfy FKs (if any)
                            conn.execute(text("DELETE FROM Event_Sponsor WHERE Event_ID=:id"), {"id": int(eid)})
                            conn.execute(text("DELETE FROM Result WHERE Event_ID=:id"), {"id": int(eid)})
                            conn.execute(text("DELETE FROM Event_Judge WHERE Event_ID=:id"), {"id": int(eid)})
                            conn.execute(text("DELETE FROM Event_Registration WHERE Event_ID=:id"), {"id": int(eid)})
                            conn.execute(text("DELETE FROM Event WHERE Event_ID=:id"), {"id": int(eid)})
                            conn.commit()
                        st.success("❌ Event Deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(e)

        # View Event Registrations (inside Events menu)
        st.subheader("👥 Students Registered for Events")
        event_list_view = fetch_all("SELECT Event_ID, Event_Name FROM Event ORDER BY Event_ID")
        if event_list_view.empty:
            st.info("No events found.")
        else:
            selected_event_view = st.selectbox("Select Event", [f"{row.Event_ID} - {row.Event_Name}" for idx, row in event_list_view.iterrows()], key="event_view_regs")
            event_id_view = int(selected_event_view.split(" - ")[0])
            event_regs = fetch_all(f"""
                SELECT er.Reg_ID, s.SRN, s.Student_Name, s.Department, s.Year, er.Registered_On
                FROM Event_Registration er
                JOIN Student s ON er.SRN = s.SRN
                WHERE er.Event_ID = {event_id_view}
                ORDER BY er.Reg_ID
            """)
            st.dataframe(event_regs, use_container_width=True)

    # SPONSORS
    if choice == "Sponsors":
        st.header("💰 Sponsorship Management")
        df = fetch_all("""
            SELECT es.Event_ID, es.Sponsor_ID, s.Sponsor_Name, es.Amount
            FROM Event_Sponsor es
            LEFT JOIN Sponsor s ON es.Sponsor_ID = s.Sponsor_ID
            ORDER BY es.Event_ID
        """)
        st.dataframe(df, use_container_width=True)

        sponsor_df = fetch_all("SELECT Sponsor_ID, Sponsor_Name FROM Sponsor")
        event_df = fetch_all("SELECT Event_ID, Event_Name FROM Event")

        st.subheader("➕ Add or ✏️ Update Sponsorship")
        with st.form("sponsor_form", clear_on_submit=True):
            if event_df.empty:
                st.info("No events available to sponsor.")
            else:
                selected_event = st.selectbox("Event", [f"{row.Event_ID} - {row.Event_Name}" for idx, row in event_df.iterrows()], key="spon_event")
                ev = int(selected_event.split(" - ")[0])
                if sponsor_df.empty:
                    st.info("No sponsors found. Add sponsors in the DB first.")
                else:
                    selected_sponsor = st.selectbox("Sponsor", sponsor_df["Sponsor_Name"].tolist(), key="spon_sponsor")
                    sid = int(sponsor_df[sponsor_df["Sponsor_Name"] == selected_sponsor]["Sponsor_ID"].iloc[0])
                    amt = st.number_input("Amount (must be > 0)", min_value=1.0, format="%f", key="spon_amt")
                    if st.form_submit_button("Save Sponsorship"):
                        try:
                            engine = get_engine()
                            exists = fetch_all(f"SELECT * FROM Event_Sponsor WHERE Event_ID={ev} AND Sponsor_ID={sid}")
                            if exists.empty:
                                sql = text("INSERT INTO Event_Sponsor (Event_ID, Sponsor_ID, Amount) VALUES (:e, :s, :a)")
                                message = "Added"
                            else:
                                sql = text("UPDATE Event_Sponsor SET Amount=:a WHERE Event_ID=:e AND Sponsor_ID=:s")
                                message = "Updated"
                            with engine.connect() as conn:
                                conn.execute(sql, {"e": ev, "s": sid, "a": float(amt)})
                                conn.commit()
                            st.success(f"🎉 Sponsorship {message} Successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    # RESULTS
    if choice == "Results":
        st.header("🏆 Add Result")

        st.subheader("📄 All Results")
        df_results = fetch_all("""
            SELECT r.Result_ID, r.Position, s.Student_Name, e.Event_Name
            FROM Result r
            JOIN Student s ON r.SRN = s.SRN
            JOIN Event e ON r.Event_ID = e.Event_ID
            ORDER BY r.Result_ID
        """)
        st.dataframe(df_results, use_container_width=True)

        st.markdown("---")
        st.subheader("➕ Add Result")
        events_df = fetch_all("SELECT Event_ID, Event_Name FROM Event")
        if events_df.empty:
            st.info("No events available.")
        else:
            selected_event = st.selectbox("Select Event", [f"{row.Event_ID} - {row.Event_Name}" for idx, row in events_df.iterrows()], key="add_res_event")
            event_id = int(selected_event.split(" - ")[0])
            with st.form("add_result_form", clear_on_submit=True):
                srn_input = st.text_input("Student SRN", key="res_srn")
                position = st.selectbox("Position", ["Winner", "Runner-Up", "Participant"], key="res_pos")
                if st.form_submit_button("Add Result"):
                    try:
                        next_id = int(fetch_all("SELECT IFNULL(MAX(Result_ID),0)+1 AS id FROM Result")['id'][0])
                        sql = text("INSERT INTO Result (Result_ID, Position, SRN, Event_ID) VALUES (:id, :pos, :srn, :ev)")
                        engine = get_engine()
                        with engine.connect() as conn:
                            conn.execute(sql, {"id": next_id, "pos": position, "srn": srn_input, "ev": event_id})
                            conn.commit()
                        st.success("🏆 Result Added Successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

# ---------------------------
# Student dashboard
# ---------------------------
def user_dashboard():
    st.title("🎓 Student Dashboard")
    menu = ["My Clubs", "Events", "Results", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Logout":
        st.session_state.clear()
        st.rerun()

    # # My Clubs
    # if choice == "My Clubs":
    #     srn = st.session_state.srn
    #     st.header("📌 My Clubs")
    #     df = fetch_all(f"""
    #         SELECT c.Club_Name, c.Club_Type
    #         FROM Recruitment r
    #         JOIN Club c ON r.Club_ID = c.Club_ID
    #         WHERE r.SRN = '{srn}'
    #     """)
    #     st.dataframe(df, use_container_width=True)

    # --------------------- MY CLUBS ---------------------
    if choice == "My Clubs":
        srn = st.session_state.srn
        st.header("📌 My Clubs")

        # Show clubs student has already joined
        my_clubs = fetch_all(f"""
            SELECT c.Club_Name, c.Club_Type
            FROM Recruitment r
            JOIN Club c ON r.Club_ID = c.Club_ID
            WHERE r.SRN = '{srn}'
        """)
        st.subheader("✔ Joined Clubs")
        st.dataframe(my_clubs, use_container_width=True)

        st.markdown("---")

        # ---------------------------------
        # Show ALL clubs (for registration)
        # ---------------------------------
        st.subheader("📝 Register for a Club")

        clubs_df = fetch_all("SELECT Club_ID, Club_Name, Club_Type FROM Club ORDER BY Club_ID")
        st.dataframe(clubs_df, use_container_width=True)

        # Dropdown
        selected_club = st.selectbox(
            "Select Club to Register",
            [f"{row.Club_ID} - {row.Club_Name}" for idx, row in clubs_df.iterrows()],
            key="club_reg_select"
        )
        club_id = int(selected_club.split(" - ")[0])

        # Domain input
        domain = st.text_input("Enter your Domain (example: Graphics, Robotics, Acting, Music...)")

        # Fetch student contact (needed by your table)
        student_contact = fetch_all(f"SELECT Contact_Info FROM Student WHERE SRN='{srn}'")
        try:
            contact = student_contact['Contact_Info'][0]
        except:
            contact = ""

        # Register button
        if st.button("Register for this Club"):
            try:
                # Prevent duplicate registration
                exists = fetch_all(f"""
                    SELECT * FROM Recruitment 
                    WHERE SRN='{srn}' AND Club_ID={club_id}
                """)

                if not exists.empty:
                    st.warning("⚠️ You are already registered in this club.")
                else:
                    # Next recruitment ID
                    next_id = int(fetch_all("""
                        SELECT IFNULL(MAX(Rec_ID),0)+1 AS id FROM Recruitment
                    """)['id'][0])

                    sql = text("""
                        INSERT INTO Recruitment (Rec_ID, Domain, SRN, S_Contact_Info, Club_ID)
                        VALUES (:rid, :dom, :srn, :contact, :cid)
                    """)

                    engine = get_engine()
                    with engine.connect() as conn:
                        conn.execute(sql, {
                            "rid": next_id,
                            "dom": domain,
                            "srn": srn,
                            "contact": contact,
                            "cid": club_id
                        })
                        conn.commit()

                    st.success("🎉 Successfully Registered for Club!")
                    st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")


    # Events (view + register)
    if choice == "Events":
        srn = st.session_state.srn
        st.header("📅 Available Events")
        event_df = fetch_all("SELECT Event_ID, Event_Name, Event_Type, Date, Venue FROM Event ORDER BY Date")
        st.dataframe(event_df, use_container_width=True)

        st.subheader("📝 Register for an Event")
        if event_df.empty:
            st.info("No events available.")
        else:
            selected_event = st.selectbox("Select Event", [f"{row.Event_ID} - {row.Event_Name}" for idx, row in event_df.iterrows()], key="event_reg_select")
            event_id = int(selected_event.split(" - ")[0])

            if st.button("Register for Event", key="user_register_btn"):
                try:
                    exists = fetch_all(f"SELECT * FROM Event_Registration WHERE SRN='{srn}' AND Event_ID={event_id}")
                    if not exists.empty:
                        st.warning("⚠️ You have already registered for this event.")
                    else:
                        next_id = int(fetch_all("SELECT IFNULL(MAX(Reg_ID),0)+1 AS id FROM Event_Registration")['id'][0])
                        sql = text("INSERT INTO Event_Registration (Reg_ID, SRN, Event_ID) VALUES (:id, :srn, :ev)")
                        engine = get_engine()
                        with engine.connect() as conn:
                            conn.execute(sql, {"id": next_id, "srn": srn, "ev": event_id})
                            conn.commit()
                        st.success("🎉 Successfully Registered for Event!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        st.subheader("📄 My Event Registrations")
        reg_df = fetch_all(f"""
            SELECT e.Event_Name, e.Date, e.Venue
            FROM Event_Registration er
            JOIN Event e ON er.Event_ID = e.Event_ID
            WHERE er.SRN = '{srn}'
        """)
        st.dataframe(reg_df, use_container_width=True)

    # Results
    if choice == "Results":
        srn = st.session_state.srn
        st.header("🏆 My Results")
        df = fetch_all(f"""
            SELECT r.Position, e.Event_Name
            FROM Result r
            JOIN Event e ON r.Event_ID = e.Event_ID
            WHERE r.SRN = '{srn}'
        """)
        st.dataframe(df, use_container_width=True)


# ---------------------------
# Main app
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_ui()
else:
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        user_dashboard()
