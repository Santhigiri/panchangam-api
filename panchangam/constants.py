# Load Nakshatra names and boundaries
NAKSHATRA_NAMES = [
    "Aswathy", 
    "Bharani", 
    "Karthika", 
    "Rohini", 
    "Makayiram",
    "Thiruvathira", 
    "Punartham", 
    "Pooyam",
    "Aayilyam", 
    "Makam", 
    "Pooram", 
    "Uthram",
    "Atham",
    "Chithira",
    "Chothi",
    "Vishagam",
    "Anizham",
    "Thrikketta",
    "Moolam",
    "Pooradam",
    "Uthradam",
    "Thiruvonam",
    "Avittam",
    "Chathayam",
    "Poororuttathi",
    "Uthrattathi",
    "Revathi"
]

NAKSHATRA_BOUNDARIES = [i*(360/27) for i in range(1,28)]


THITHI_NAMES = [
    # Shukla Paksha (Waxing Moon)
    "Prathama (Shukla Paksha)",
    "Dwitiya (Shukla Paksha)",
    "Tritiya (Shukla Paksha)",
    "Chaturthi (Shukla Paksha)",
    "Panchami (Shukla Paksha)",
    "Shashthi (Shukla Paksha)",
    "Saptami (Shukla Paksha)",
    "Ashtami (Shukla Paksha)",
    "Navami (Shukla Paksha)",
    "Dashami (Shukla Paksha)",
    "Ekadashi (Shukla Paksha)",
    "Dwadashi (Shukla Paksha)",
    "Trayodashi (Shukla Paksha)",
    "Chaturdashi (Shukla Paksha)",
    "Pournami",  # Full Moon (no Paksha suffix needed)

    # Krishna Paksha (Waning Moon)
    "Prathama (Krishna Paksha)",
    "Dwitiya (Krishna Paksha)",
    "Tritiya (Krishna Paksha)",
    "Chaturthi (Krishna Paksha)",
    "Panchami (Krishna Paksha)",
    "Shashthi (Krishna Paksha)",
    "Saptami (Krishna Paksha)",
    "Ashtami (Krishna Paksha)",
    "Navami (Krishna Paksha)",
    "Dashami (Krishna Paksha)",
    "Ekadashi (Krishna Paksha)",
    "Dwadashi (Krishna Paksha)",
    "Trayodashi (Krishna Paksha)",
    "Chaturdashi (Krishna Paksha)",
    "Amavasya"  # New Moon (no Paksha suffix needed)
]


class Coordinates:
    SG_LATITUDE = 8.631891978113215
    SG_LONGITUDE = 76.8977255008525

DEFAULT_TIMEZONE = 'Asia/Kolkata'
