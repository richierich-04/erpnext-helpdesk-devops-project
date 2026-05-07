#!/usr/bin/env python3
import random
import subprocess
from datetime import datetime, timedelta

DB_USER = "root"
DB_PASS = "MygateDockerDbPass123!"
DB_NAME = "_b2004f3628a4238c"
CONTAINER = "frappe_docker-db-1"

SUBJECTS = [
    "Unable to access employee portal",
    "Laptop not connecting to VPN",
    "Email not syncing on mobile",
    "Printer offline on 3rd floor",
    "Software installation request - VS Code",
    "Password reset required for ERP login",
    "Internet connectivity issue at workstation",
    "Zoom audio not working during calls",
    "Request for additional monitor",
    "Office 365 license activation failed",
    "Slack notifications not working",
    "Cannot open shared drive folder",
    "System running slow after update",
    "New joiner laptop setup request",
    "Antivirus alert on workstation",
]

STATUSES = ["Open", "Replied", "Resolved", "Closed"]
STATUS_WEIGHTS = [40, 25, 20, 15]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]
PRIORITY_WEIGHTS = [20, 50, 20, 10]
OWNERS = ["support@mygate.com", "helpdesk@mygate.com", "it@mygate.com"]
TICKET_TYPES = ["Question", "Bug", "Feature", "Incident"]
STATUS_CATEGORY_MAP = {"Open": "Open", "Replied": "Open", "Resolved": "Closed", "Closed": "Closed"}

def run_sql(sql):
    cmd = ["docker", "exec", "-i", CONTAINER, "mariadb", "-u" + DB_USER, "-p" + DB_PASS, DB_NAME]
    result = subprocess.run(cmd, input=sql, capture_output=True, text=True)
    if result.returncode != 0:
        print("  SQL Error: " + result.stderr.strip())
    return result.stdout.strip()

def get_max_ticket_id():
    out = run_sql("SELECT MAX(name) FROM `tabHD Ticket`;")
    lines = out.strip().split("\n")
    val = lines[-1].strip() if lines else "9290"
    try:
        return int(val)
    except ValueError:
        return 9290

def insert_new_tickets(count=2):
    max_id = get_max_ticket_id()
    now = datetime.now()
    for i in range(1, count + 1):
        tid = max_id + i
        subject = random.choice(SUBJECTS).replace("'", "''")
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
        priority = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]
        sc = STATUS_CATEGORY_MAP[status]
        tt = random.choice(TICKET_TYPES)
        owner = random.choice(OWNERS)
        creation = (now - timedelta(minutes=random.randint(0,30))).strftime("%Y-%m-%d %H:%M:%S")
        modified = now.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO `tabHD Ticket` (name,creation,modified,modified_by,owner,docstatus,idx,subject,raised_by,status,priority,status_category,ticket_type) VALUES (" + str(tid) + ",'" + creation + "','" + modified + "','" + owner + "','" + owner + "',0,0,'" + subject + "','" + owner + "','" + status + "','" + priority + "','" + sc + "','" + tt + "');"
        run_sql(sql)
        print("  + Ticket #" + str(tid) + ": [" + priority + "] " + status + " - " + subject)

def update_existing_tickets(count=3):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = run_sql("SELECT name FROM `tabHD Ticket` WHERE status IN ('Open','Replied') ORDER BY RAND() LIMIT 20;")
    lines = [l.strip() for l in out.strip().split("\n") if l.strip().isdigit()]
    if not lines:
        print("  No open tickets to update.")
        return
    for tid in random.sample(lines, min(count, len(lines))):
        new_status = random.choices(["Replied","Resolved","Closed"], weights=[50,30,20])[0]
        sc = STATUS_CATEGORY_MAP[new_status]
        extra = ""
        if new_status in ("Resolved","Closed"):
            extra = ",resolution_date='" + now + "',resolution_time=3600"
        sql = "UPDATE `tabHD Ticket` SET status='" + new_status + "',status_category='" + sc + "',modified='" + now + "'" + extra + " WHERE name=" + str(tid) + ";"
        run_sql(sql)
        print("  ~ Ticket #" + str(tid) + " -> " + new_status)

def print_summary():
    out = run_sql("SELECT status, COUNT(*) as count FROM `tabHD Ticket` GROUP BY status ORDER BY count DESC;")
    print("\n  Ticket summary:")
    for line in out.strip().split("\n")[1:]:
        print("    " + line)

if __name__ == "__main__":
    print("\n" + "="*45)
    print("  HD Ticket Seeder - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*45)
    print("\n[1/2] Inserting new tickets...")
    insert_new_tickets(count=random.randint(1,3))
    print("\n[2/2] Progressing existing tickets...")
    update_existing_tickets(count=random.randint(2,4))
    print_summary()
    print("\n  Done.\n")
