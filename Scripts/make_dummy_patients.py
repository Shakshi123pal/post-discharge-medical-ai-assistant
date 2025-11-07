import json, random, datetime, pathlib
names = ["John Smith","Asha Verma","Ravi Kumar","Meera Shah","Vikram Singh","Fatima Khan","Ajay Mehta","Priya Iyer","Arjun Patel","Neha Joshi","Karan Arora","Sana Ali","Rohan Das","Isha Gupta","Zara Sheikh","Kabir Roy","Anita Rao","Dev Khanna","Kriti Jain","Vivek Goel","Ria Sinha","Om Prakash","Esha Nair","Samar Gill","Nina Paul","Rahul Rana","Sara Thomas","Gaurav Kaul","Anvi Bhat","Yash Agrawal"]
diagnoses = ["CKD Stage 3","CKD Stage 4","Acute Kidney Injury","Nephrotic Syndrome","Hypertension with CKD"]
meds = [
    ["Lisinopril 10mg daily","Furosemide 20mg bid"],
    ["Amlodipine 5mg daily","Sodium Bicarbonate 650mg tid"],
    ["Losartan 50mg daily","Torsemide 10mg daily"]
]
def rand_date():
    start = datetime.date(2024,1,1); end = datetime.date(2025,10,31)
    return start + datetime.timedelta(days=random.randint(0,(end-start).days))
out = []
for n in names:
    d = {
      "patient_name": n,
      "discharge_date": str(rand_date()),
      "primary_diagnosis": random.choice(diagnoses),
      "medications": random.choice(meds),
      "dietary_restrictions": "Low sodium (2g/day), fluid restriction (1.5L/day)",
      "follow_up": "Nephrology clinic in 2 weeks",
      "warning_signs": "Swelling, shortness of breath, decreased urine output",
      "discharge_instructions": "Monitor BP daily, track weight daily"
    }
    out.append(d)
pathlib.Path("data").mkdir(exist_ok=True)
with open("data/patients.jsonl","w",encoding="utf-8") as f:
    for r in out: f.write(json.dumps(r,ensure_ascii=False)+"\n")
print("Wrote data/patients.jsonl with", len(out), "records.")
