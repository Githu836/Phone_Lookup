# 📱 Phone Number Information Lookup Tool

A lightweight, standalone **Python CLI utility** for retrieving structured information about phone numbers using international numbering standards.

This tool is designed for **data validation, educational use, OSINT basics, and automation**, leveraging the official `phonenumbers` library.

---

## 🚀 Features

- ✔ Phone number format validation
- 🌍 Country and country code detection
- 📡 Carrier / operator identification
- 🕒 Time zone lookup
- 📞 Number type classification (Mobile, Fixed Line, VoIP, etc.)
- 🇮🇩 Indonesian provider detection based on prefix
- 🎨 Colored and readable CLI output
- 📂 Single number & batch file processing
- 💾 Optional JSON output export

---

## 🧱 Technology Stack

- Python 3.8+
- [`phonenumbers`](https://github.com/daviddrysdale/python-phonenumbers)
- `requests`
- `colorama`
- `argparse`

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Githu836/Phone_Lookup.git
cd Phone_Lookup

Install dependencies:

pip install phonenumbers requests colorama

> Dependencies will be installed automatically if missing.
```



---

## ⚙️ Usage

Lookup a single phone number
```
python tool.py +6281234567890

python tool.py 081234567890
```
---

## Batch lookup from file
```
python tool.py --file numbers.txt
```
## Example numbers.txt:
```
+6281234567890
+14155552671
+447911123456
```

---

## Export results to JSON

```
python tool.py +6281234567890 --output result.json
```

---

## List supported country codes
```
python tool.py --list-countries
```

---

## 📊 Sample Output

📞 Phone Number: +6281234567890
🌍 Country: 🇮🇩 Indonesia
🔢 Country Code: +62

✓ Valid: True
✓ Carrier: Telkomsel
✓ Time Zones: Asia/Jakarta
✓ Number Type: MOBILE
⏰ Timestamp: 2025-01-01 12:00:00


---

# 🔐 Limitations & Disclaimer

## ⚠️ This tool does NOT perform:

real-time location tracking

cell tower triangulation

SS7 / IMSI access

call or message interception


All information is derived from:

public numbering databases

prefix-based detection

optional third-party APIs


Carrier and region data are indicative only and may change due to number portability.

This project is intended for legal and ethical use only.


---

## 📌 Project Status

✔ Stable CLI utility

✔ Educational / OSINT basic usage

❌ Not a surveillance or intelligence system



---

## 🛣️ Roadmap (Optional)

Confidence scoring per data point

Metadata source attribution

Modular API integration

Improved error classification

Packaging for PyPI distribution



---

# 👤 Author

Faqih
Independent Developer
Indonesia 🇮🇩
