# Coding Standards

## 1. Naming Conventions

- Python değişkenleri İngilizce ve `snake_case` formatında yazılacaktır.
- Fonksiyon isimleri İngilizce ve `snake_case` formatında yazılacaktır.
- Constant isimleri `UPPER_CASE` formatında yazılacaktır.
- Dictionary key değerleri İngilizce ve `snake_case` formatında yazılacaktır.

## 2. User-Facing Text

- Kullanıcıya gösterilen tüm metinler Türkçe olacaktır.
- Kod içindeki teknik değişkenler İngilizce kalacaktır.

## 3. Dataset Columns

- Ham veri setlerindeki sütun isimleri mümkün olduğunca değiştirilmeden kullanılacaktır.
- Gerekli durumlarda normalize edilmiş yardımcı sütunlar oluşturulabilir.
- Örneğin: `city_key`, `country_key`

## 4. Constants

- Magic number kullanılmayacaktır.
- Puanlama matrisleri, multiplier değerleri ve sabit metinler constant olarak tanımlanacaktır.
- Algoritma kararları fonksiyon içine gömülmeyecektir.

## 5. Scoring Functions

Her scoring fonksiyonu `ScoreResult` formatında çıktı döndürecektir.

Beklenen yapı:

```python
{
    "criterion": "budget",
    "score": 12.0,
    "max_score": 20.0,
    "reason": "Seçtiğiniz bütçe aralığı ile uyumludur.",
    "active": True
}

## 6. No Preference Logic
Kullanıcı bir kriter için Fark etmez seçerse ilgili kriter puanlamaya dahil edilmez.
Bu durumda fonksiyon active=False, score=0, max_score=0 döndürür.

## 7. Missing Data Logic
Eksik veri bulunan kriterler şehir için puanlamaya dahil edilmez.
Eksik veri nedeniyle şehir aday havuzundan çıkarılmaz.
Fonksiyon active=False, score=0, max_score=0 döndürür.

## 8. Function Responsibility
Her fonksiyon tek bir iş yapmalıdır.
Scoring fonksiyonları yalnızca kendi kriterinin puanını hesaplamalıdır.
Genel sıralama ve final skor hesaplama recommendation_engine.py içinde yapılacaktır.

## 9. Documentation Consistency
Kod tarafındaki her scoring fonksiyonu recommendation_design.md içinde tanımlanan metodolojiyle uyumlu olmalıdır.
Metodoloji değişirse önce doküman, sonra kod güncellenmelidir.