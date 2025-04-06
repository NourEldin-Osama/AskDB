import random
import sqlite3

from faker import Faker

# Connect to (or create) the sqlite database
conn = sqlite3.connect("realestate.db")
cursor = conn.cursor()

# Create table for properties
cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY,
        address TEXT,
        city TEXT,
        price REAL,
        bedrooms INTEGER,
        bathrooms INTEGER,
        square_meters INTEGER,
        listing_date TEXT
    )
""")

# Create table for clients
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT
    )
""")

# Create linking table between clients and properties
cursor.execute("""
    CREATE TABLE IF NOT EXISTS client_properties (
        id INTEGER PRIMARY KEY,
        property_id INTEGER,
        client_id INTEGER,
        listed_date TEXT,
        FOREIGN KEY(property_id) REFERENCES properties(id),
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
""")

# Create Faker instance for Egyptian Arabic data
fake = Faker("ar_SA")
Faker.seed(0)

# Egyptian cities
egyptian_cities = [
    "القاهرة",
    "الإسكندرية",
    "الجيزة",
    "شرم الشيخ",
    "الغردقة",
    "المنصورة",
    "طنطا",
    "أسوان",
    "الأقصر",
    "بورسعيد",
    "دمياط",
    "الفيوم",
    "سوهاج",
    "أسيوط",
]

# Egyptian districts/neighborhoods
egyptian_districts = [
    "المعادي",
    "مدينة نصر",
    "الزمالك",
    "المهندسين",
    "وسط البلد",
    "الدقي",
    "الهرم",
    "حدائق القبة",
    "مصر الجديدة",
    "عين شمس",
    "الشروق",
    "التجمع الخامس",
    "6 أكتوبر",
    "الرحاب",
    "مدينتي",
    "العبور",
]

# Egyptian street names
egyptian_streets = [
    "شارع محمد علي",
    "شارع الهرم",
    "شارع جمال عبد الناصر",
    "شارع الجلاء",
    "شارع رمسيس",
    "شارع الجمهورية",
    "شارع شبرا",
    "شارع المعز",
    "شارع الأزهر",
    "شارع السلام",
    "شارع الملك فيصل",
    "شارع عباس العقاد",
    "شارع مكرم عبيد",
]

# Property types in Arabic
property_types = ["شقة", "فيلا", "دوبلكس", "بنتهاوس", "ستوديو", "شاليه"]

# Insert fake Egyptian clients
client_ids = []
for _ in range(10):
    name = fake.name()
    email = fake.email()
    # Egyptian mobile numbers typically start with 01
    phone = "01" + str(random.randint(0, 2)) + "".join([str(random.randint(0, 9)) for _ in range(8)])
    cursor.execute("INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
    client_ids.append(cursor.lastrowid)

# Insert fake properties with Egyptian addresses
property_ids = []
for _ in range(50):
    street = random.choice(egyptian_streets)
    district = random.choice(egyptian_districts)
    building_number = str(random.randint(1, 300))
    # Format address in Egyptian style: Street name, building number, district
    address = f"{street} رقم {building_number}، {district}"
    city = random.choice(egyptian_cities)
    # Convert prices to Egyptian Pound (LE) range
    price = round(random.uniform(500_000, 15_000_000), 2)  # Wider range for Egyptian real estate
    bedrooms = random.randint(1, 6)
    bathrooms = random.randint(1, 4)
    # Square meters which is used in Egypt
    square_meters = random.randint(60, 400)
    listing_date = fake.date_between(start_date="-2y", end_date="today").isoformat()

    cursor.execute(
        "INSERT INTO properties (address, city, price, bedrooms, bathrooms, square_meters, listing_date) VALUES "
        "(?, ?, ?, ?, ?, ?, ?)",
        (address, city, price, bedrooms, bathrooms, square_meters, listing_date),
    )
    property_ids.append(cursor.lastrowid)

# Link properties and clients
for property_id in property_ids:
    client_id = random.choice(client_ids)
    listed_date = fake.date_between(start_date="-2y", end_date="today").isoformat()
    cursor.execute(
        "INSERT INTO client_properties (property_id, client_id, listed_date) VALUES (?, ?, ?)",
        (property_id, client_id, listed_date),
    )

conn.commit()
conn.close()
