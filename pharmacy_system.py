"""Pharmacy Prescription and Stock Management System."""

import json
import sqlite3
from datetime import datetime

# Global state
conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create and populate the patient database."""
    cur = conn.cursor()
    cur.execute("CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)")
    cur.execute("INSERT INTO patients VALUES ('P1', 'Kavya', 'penicillin')")
    cur.execute("INSERT INTO patients VALUES ('P2', 'Arjun', 'none')")
    cur.execute("INSERT INTO patients VALUES ('P3', 'Meena', 'ibuprofen')")
    conn.commit()


def find_patient(name):
    """Find a patient by name."""
    cur = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add stock for a medicine."""
    if batch_log is None:
        batch_log = []

    stock[drug] = {
        "units": stock.get(drug, {}).get("units", 0) + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense medicine to a patient."""
    try:
        patient = find_patient(patient_name)[0]

        if drug.lower() in patient[1].lower():
            print("Allergy warning for", patient_name)
            return False

        stock[drug]["units"] -= units

        prescriptions.append(
            {
                "patient": patient[0],
                "drug": drug,
                "units": units,
                "time": str(datetime.now()),
            }
        )

        return True

    except (IndexError, KeyError):
        return False


def expiring_soon(days=30):
    """Return medicines expiring within specified days."""
    soon = []

    for medicine in stock:
        exp = datetime.strptime(stock[medicine]["expiry"], "%Y-%m-%d")

        if (exp - datetime.now()).days < days:
            soon.append(medicine)

    return soon


def export_prescriptions(file="prescriptions.json"):
    """Export prescriptions to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file)


def load_stock(file="stock.json"):
    """Load stock information from a JSON file."""
    global stock

    try:
        with open(file, "r", encoding="utf-8") as input_file:
            stock = json.load(input_file)

    except FileNotFoundError:
        stock = {}


def print_stock():
    """Display current pharmacy stock."""
    print("Pharmacy Stock")

    for drug in stock:
        print(
            drug,
            "->",
            stock[drug]["units"],
            "units, expires",
            stock[drug]["expiry"],
        )


def main():
    """Execute pharmacy workflow."""
    setup_database()

    load_stock()

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", -15, "2026-11-30")

    print("Arjun gets Amoxicillin:", dispense("Arjun", "Amoxicillin", 30))
    print("Kavya gets Penicillin:", dispense("Kavya", "Penicillin", 10))
    print("Meena gets ibuprofen:", dispense("Meena", "ibuprofen", 2))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))

    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"

    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())

    export_prescriptions()
    print_stock()


main()
