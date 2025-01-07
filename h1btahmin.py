import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Veri setini yükleme
file_path = 'h1bvisa.xlsx'
df = pd.read_excel(file_path)

# Gerekli sütunları seçme
df = df[['CASE_STATUS', 'JOB_TITLE', 'EMPLOYER_NAME', 'WORKSITE_CITY']]

# Eksik verileri kontrol etme ve temizleme
df.dropna(inplace=True)

# CASE_STATUS'u ikili sınıflandırmaya dönüştürme
df['CASE_STATUS_BINARY'] = df['CASE_STATUS'].apply(lambda x: 1 if x == 'Certified' else 0)

# Tüm kategorik değişkenleri string'e dönüştürme
kategorik_sutunlar = ['JOB_TITLE', 'EMPLOYER_NAME', 'WORKSITE_CITY']
for sutun in kategorik_sutunlar:
    df[sutun] = df[sutun].astype(str)

# Global Label Encoder'lar
label_encoders = {sutun: LabelEncoder() for sutun in kategorik_sutunlar}

# Tüm veriyi kodlama
for sutun in kategorik_sutunlar:
    df[f'{sutun}_ENCODED'] = label_encoders[sutun].fit_transform(df[sutun])

# Özellikler ve hedef değişken
X = df[[f'{sutun}_ENCODED' for sutun in kategorik_sutunlar]]
y = df['CASE_STATUS_BINARY']

# SMOTE ile veri dengeleme
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, 
    test_size=0.2, 
    random_state=42, 
    stratify=y_resampled
)

# Model Pipeline
model_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(
        n_estimators=100, 
        random_state=42, 
        class_weight='balanced'
    ))
])

# Modeli eğitme
model_pipeline.fit(X_train, y_train)

# Test seti performansı
y_pred = model_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Doğruluğu: {accuracy * 100:.2f}%")
print("\nSınıflandırma Raporu:")
print(classification_report(y_test, y_pred))

def predict(job_title, employer_name, worksite_city):
    # Tek bir örnek veri için DataFrame oluştur
    sample_data = pd.DataFrame({
        'JOB_TITLE': [job_title],
        'EMPLOYER_NAME': [employer_name],
        'WORKSITE_CITY': [worksite_city]
    })

    # Eğitim verisindeki benzersiz değerleri toplama
    unique_values = {col: set(df[col].unique()) for col in kategorik_sutunlar}

    # Güvenli dönüştürme fonksiyonu
    def safe_transform(value, encoder, unique_values):
        if value not in unique_values:
            return len(encoder.classes_)  # Bilinmeyen sınıf
        return encoder.transform([value])[0]

    # Giriş verilerini kodla
    for sutun in kategorik_sutunlar:
        sample_data[f'{sutun}_ENCODED'] = sample_data[sutun].apply(
            lambda x: safe_transform(x, label_encoders[sutun], unique_values[sutun])
        )

    # Kodlanmış özellikleri seç
    X_sample = sample_data[[f'{sutun}_ENCODED' for sutun in kategorik_sutunlar]]

    # Tahmin yap ve olasılığı al
    tahmin = model_pipeline.predict(X_sample)[0]
    olasilik = model_pipeline.predict_proba(X_sample)[0][tahmin] * 100

    return round(olasilik, 2)  # Yüzde olarak döndür