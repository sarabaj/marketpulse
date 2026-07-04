"""
Generates a synthetic dataset of customer reviews across several competing
companies, in a mix of Arabic and English, for demo purposes. In a real
use-case, this data would come from scraped app store reviews, Google
reviews, or social media mentions.
"""
import random
from datetime import datetime, timedelta
import pandas as pd

COMPANIES = ["Nova Bank", "Fintra", "PayEase"]

REVIEW_TEMPLATES = [
    ("The app keeps crashing every time I try to transfer money.", 1),
    ("التطبيق ممتاز وسريع، تجربة رائعة بصراحة", 5),
    ("Customer support never responds, waited 3 days for a reply.", 1),
    ("سهل الاستخدام لكن التصميم يحتاج تحديث", 3),
    ("Great app, but the fees are too high compared to competitors.", 3),
    ("تطبيق حلو بس فيه مشاكل بتسجيل الدخول أحيانًا", 2),
    ("Loving the new update, much faster now!", 5),
    ("لا أنصح به، فقدت أموالي بسبب خطأ بالتطبيق ولا أحد ساعدني", 1),
    ("Decent app, does what it says, nothing special.", 3),
    ("أفضل تطبيق بنكي جربته، الدعم الفني ممتاز وسريع", 5),
    ("The onboarding process is way too long and confusing.", 2),
    ("خدمة العملاء بطيئة جدًا، انتظرت أسبوع للرد", 1),
    ("Simple and intuitive interface, exactly what I needed.", 4),
    ("التطبيق يهنق كثير وقت التحويل بين الحسابات", 2),
    ("Excellent security features, I feel safe using it.", 5),
]


def generate_dataset(n_reviews: int = 250, seed: int = 7) -> pd.DataFrame:
    random.seed(seed)
    base_time = datetime(2026, 1, 1)
    rows = []
    for i in range(n_reviews):
        text, rating = random.choice(REVIEW_TEMPLATES)
        company = random.choice(COMPANIES)
        date = base_time + timedelta(days=random.randint(0, 180))
        rows.append({
            "review_id": i + 1,
            "company": company,
            "review_text": text,
            "rating": rating,
            "date": date.date().isoformat(),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("data/reviews.csv", index=False)
    print(f"Generated {len(df)} reviews across {df['company'].nunique()} companies -> data/reviews.csv")
