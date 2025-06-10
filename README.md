
````markdown
# 💡 Marzneshin IP Limit Bot

مدیریت اتصال کاربران به سرویس‌های شما با بررسی IP — همراه با سیستم ادمین چندلایه (نماینده فروش)، محدودیت اختصاصی، پنل تلگرام، و تنظیمات پیشرفته.

---

## 🚀 نصب سریع

### نصب خودکار با اسکریپت آماده:

```bash
sudo bash -c "$(curl -sL https://github.com/soltanihara/MarzneshinIpLimit/raw/main/script.sh)"
````

### یا نصب دستی (پیشنهادی برای توسعه‌دهنده‌ها):

```bash
git clone https://github.com/soltanihara/MarzneshinIpLimit.git
cd MarzneshinIpLimit
pip install -r requirements.txt
python run_telegram.py
```

---

## ⚙️ تنظیم اولیه (`config.json`)

قبل از اجرای ربات، یک فایل `config.json` با ساختار زیر بسازید:

```json
{
  "TOKEN": "توکن ربات تلگرام",
  "ADMINS": [
    { "id": 123456789, "role": "superadmin" },
    { "id": 987654321, "role": "admin" }
  ],
  "GENERAL_LIMIT": 20,
  "CHECK_INTERVAL": 60,
  "USER_CHECK_INTERVAL": 45
}
```

> ⚠️ توجه: فقط ادمین‌های اصلی (superadmin) می‌توانند ادمین جدید تایید یا حذف کنند.

---

## 📲 لیست دستورات ربات

| دستور                       | توضیح                                                                      |
| --------------------------- | -------------------------------------------------------------------------- |
| `/start`                    | شروع کار با ربات - در صورت نیاز درخواست تأیید برای ادمین جدید ارسال می‌شود |
| `/panel`                    | نمایش پنل مدیریتی با دکمه‌های شیشه‌ای                                      |
| `/create_config`            | تنظیم اولیه (یوزرنیم، پسورد، ...)                                          |
| `/set_special_limit`        | تنظیم محدودیت خاص برای کاربر (مثال: `test_user limit: 5`)                  |
| `/show_special_limit`       | نمایش لیست کاربران با محدودیت خاص                                          |
| `/set_general_limit_number` | تنظیم محدودیت پیش‌فرض (برای کاربرانی که محدودیت خاص ندارند)                |
| `/unlimit_user <username>`  | بازگرداندن کاربر به حالت عادی (ریست شمارنده محدودیت)                       |
| `/set_check_interval`       | تعیین فاصله زمانی بررسی کاربران (ثانیه)                                    |
| `/set_time_to_active_users` | زمان در نظر گرفتن یک کاربر به‌عنوان فعال (ثانیه)                           |
| `/online_users`             | نمایش کاربران آنلاین محدودشده                                              |
| `/set_except_user`          | افزودن کاربر به لیست استثنا                                                |
| `/remove_except_user`       | حذف از لیست استثنا                                                         |
| `/show_except_users`        | نمایش کاربران مستثنا                                                       |
| `/country_code`             | محدودسازی بررسی IP بر اساس کشور انتخاب‌شده                                 |
| `/add_admin`                | افزودن ادمین جدید (نیاز به تأیید توسط superadmin)                          |
| `/remove_admin`             | حذف ادمین                                                                  |
| `/admins_list`              | نمایش لیست ادمین‌های فعال                                                  |
| `/backup`                   | دریافت فایل `config.json` برای بکاپ گیری                                   |

---

## 👤 نقش‌ها و دسترسی‌ها

| نقش          | توضیح                                                                   |
| ------------ | ----------------------------------------------------------------------- |
| `superadmin` | ادمین اصلی، دسترسی کامل دارد، می‌تواند ادمین جدید اضافه یا حذف کند      |
| `admin`      | فقط به کاربران خودش دسترسی دارد و نمی‌تواند سایر ادمین‌ها را مدیریت کند |

> وقتی یک ادمین جدید وارد می‌شود، باید توسط یک superadmin تأیید شود.

---

## 📂 ساختار فایل‌ها

| مسیر                      | کاربرد                                             |
| ------------------------- | -------------------------------------------------- |
| `config.json`             | تنظیمات اصلی سیستم                                 |
| `detected_users.json`     | ذخیره کاربران و IPهای شناسایی‌شده                  |
| `logs/log_admin_<id>.txt` | فایل لاگ اختصاصی هر ادمین                          |
| `script.sh`               | اسکریپت نصب خودکار روی سرور یا VPS                 |
| `run_telegram.py`         | فایل اصلی اجرای ربات تلگرام                        |
| `api.py` (در حال توسعه)   | API برای مدیریت از طریق درخواست‌های HTTP (اختیاری) |

---

## 🧪 نمونه ساختار کاربر در فایل `detected_users.json`

```json
{
  "test_user": {
    "ips": ["1.2.3.4", "5.6.7.8"],
    "outOfLimitCount": 2,
    "adminId": 987654321,
    "limit": 5
  }
}
```

* `limit` : تعداد IP مجاز اختصاصی این کاربر
* `adminId` : ادمینی که مسئول این کاربر است

---
---
For manage the app use marzneshiniplimit command:

up Start services
down Stop services
restart Restart services
status Show status
logs Show logs
token Set telegram bot token
admins Set telegram admins
install Install MarzneshinIpLimit
update Update latest version
uninstall Uninstall MarzneshinIpLimit
install-script Install MarzneshinIpLimit script

---
## 💬 پشتیبانی

در صورت نیاز به راهنمایی بیشتر یا پیشنهاد ویژگی‌های جدید، خوشحال می‌شویم که در [صفحه Issues](https://github.com/soltanihara/MarzneshinIpLimit/issues) مطرح کنید.

---

## 📄 مجوز

این پروژه تحت لایسنس MIT منتشر شده است.
کپی، تغییر و استفاده آزاد است با رعایت ذکر منبع.

---

```
