# Recommendation Logic

## Versiyon

V1

---

# 1. Projenin Amacı

Bu projenin amacı, kullanıcının seyahat tercihlerini analiz ederek Avrupa şehirleri arasından en uygun destinasyonları önermektir.

Sistem, kullanıcının verdiği cevapları farklı veri kaynaklarından oluşturulan Master Dataset ile karşılaştırarak her şehir için bir uyumluluk puanı hesaplar. Hesaplanan puanlar sonucunda en yüksek uyuma sahip ilk 5 şehir kullanıcıya önerilir.

Öneri sürecinin sonunda yalnızca şehir önerilmez; aynı zamanda her önerinin hangi kriterler doğrultusunda seçildiği de kullanıcıya açıklanır (Explainable Recommendation).

---

# 2. Recommendation Pipeline

Sistem aşağıdaki adımları takip ederek öneri üretir:

1. Kullanıcıdan tercih bilgileri alınır.
2. Hard Constraint kuralları uygulanır.
3. Uygun şehirlerden aday havuzu oluşturulur.
4. Her şehir için ağırlıklı puanlama (Weighted Scoring) yapılır.
5. Puanlar normalize edilerek Compatibility Score hesaplanır.
6. Şehirler en yüksek puandan en düşük puana doğru sıralanır.
7. İlk 5 şehir kullanıcıya önerilir.
8. Her şehir için önerilme nedenleri açıklanır.

---

# 3. Hard Constraints

Hard Constraint kuralları puanlama başlamadan önce uygulanır.

Bu kurallardan herhangi birini sağlamayan şehirler puanlama aşamasına dahil edilmez.

## 3.1 Vize Durumu

Kullanılan sütun:

`visa_required`

Kural:

* Eğer kullanıcının geçerli vizesi yoksa,
* ve şehirin bulunduğu ülke vize gerektiriyorsa,

ilgili şehir aday havuzundan çıkarılır.

Vizeye sahip kullanıcılar için herhangi bir filtre uygulanmaz.

---

# 4. Weighted Scoring

Hard Constraint sonrasında kalan şehirler kullanıcı tercihleri doğrultusunda puanlanır.

Her kriter belirlenmiş maksimum puan kadar katkı sağlar.

Kullanıcının herhangi bir kriter için **"Fark etmez"** cevabını vermesi durumunda ilgili kriter puanlamaya dahil edilmez.

Bu durumda hem şehir puanı hem de maksimum alınabilecek puan yeniden hesaplanır.

Son aşamada tüm şehirler normalize edilerek Compatibility Score (%) hesaplanır.

Bu yaklaşım sayesinde kullanıcı tarafından önemsiz görülen kriterler sonuçları etkilemez.

# 5. Scoring Strategy

## 5.1 Scoring Philosophy

Öneri sistemi, tüm kullanıcı tercihlerini eşit önemde değerlendirmemektedir. Bazı kriterler destinasyon seçiminde belirleyici rol oynarken, bazı kriterler benzer şehirler arasında daha doğru bir sıralama yapılmasını sağlamaktadır.

Bu nedenle puanlama sistemi üç farklı öncelik seviyesine ayrılmıştır.

### Core Criteria

Core Criteria, öneri sisteminin temelini oluşturan ve şehir seçiminde en yüksek etkiye sahip kriterlerdir. Kullanıcının bütçesi, seyahat dönemi, iklim tercihi ve tatil amacı gibi faktörler bu grupta yer almaktadır. Bu kriterler, önerilecek şehirlerin genel uygunluğunu belirlediği için en yüksek ağırlıklara sahiptir.

**V1 kapsamında Core Criteria:**

* Budget
* Travel Season
* Climate Preference
* Travel Style

---

### Preference Criteria

Preference Criteria, kullanıcının ilgi alanlarını ve kişisel beklentilerini yansıtan kriterlerdir. Bu kriterler şehirleri tamamen elemek yerine, aday şehirlerin puanlarını artırmak veya azaltmak amacıyla kullanılmaktadır.

**V1 kapsamında Preference Criteria:**

* Culture
* Beach
* Nature
* Cuisine
* Nightlife
* Safety

---

### Personalization Criteria

Personalization Criteria, benzer puan alan şehirler arasında daha kişiselleştirilmiş öneriler oluşturabilmek amacıyla kullanılmaktadır. Bu kriterler tek başına şehir seçiminde belirleyici değildir; ancak önerilerin kullanıcının seyahat alışkanlıklarına daha uygun hale gelmesini sağlar.

**V1 kapsamında Personalization Criteria:**

* Urban / Seclusion
* Adventure
* Travel Duration
* Travel Group

---

## 5.2 Dynamic Weighting

Her kriter için belirlenmiş maksimum bir puan bulunmaktadır. Ancak kullanıcı tarafından **"Fark etmez"** cevabı verilen kriterler puanlama sürecine dahil edilmez.

Bu durumda ilgili kriter;

* şehir puanına katkı sağlamaz,
* maksimum alınabilecek toplam puandan çıkarılır.

Böylece kullanıcı tarafından önemsiz olarak belirtilen kriterlerin sonuçları etkilemesi engellenir ve her kullanıcı için dinamik bir puanlama sistemi oluşturulur.

---

## 5.3 Compatibility Score

Her şehir, yalnızca aktif kriterler üzerinden puanlanır.

Toplam şehir puanı, aktif maksimum puana bölünerek normalize edilir ve kullanıcıya yüzde (%) cinsinden bir uyumluluk oranı (Compatibility Score) olarak gösterilir.

Bu yaklaşım sayesinde farklı kullanıcıların farklı sayıda aktif kriter seçmesi durumunda dahi sonuçlar adil ve karşılaştırılabilir olmaya devam eder.



| Soru          | Veri Kolonu       | V1 | V2          | V3 |
| ------------- | ----------------- | -- | ----------- | -- |
| Vize          | visa_required     | ✅  |             |    |
| Bütçe         | budget_level      | ✅  |             |    |
| Deniz         | beaches           | ✅  |             |    |
| Güvenlik      | Safety            | ✅  | Crime Index |    |
| Direkt uçuş   | thy_direct_flight |    | ✅           |    |
| Uçuş süresi   | flight_duration   |    | ✅           |    |
| Araç kiralama | walkability       |    |             | ✅  |
| Çocuk         | family_friendly   |    |             | ✅  |


*V1 geliştirilirken yalnızca veri setleri tarafından desteklenen kullanıcı tercihleri sisteme dahil edilmiştir. Yeni kullanıcı tercihleri ancak ilgili veri kaynağı sisteme entegre edildikten sonra sonraki sürümlerde eklenmiştir.*


---

## 5.4 Feature Engineering: Travel Style

V1 kapsamında kullanıcıya sorulan **Travel Style** sorusu doğrudan tek bir veri sütunuyla temsil edilmemektedir.

Bu kriter, Master Dataset içinde yer alan birden fazla şehir özelliğinin birlikte değerlendirilmesiyle oluşturulan türetilmiş bir özelliktir.

Bu nedenle Travel Style, sistemde bir **feature engineering** adımı olarak ele alınmaktadır.

### Travel Style Mapping

| Travel Style | Kullanılan Özellikler |
|---|---|
| Deniz & Relax | `beaches`, `wellness`, `seclusion` |
| Kültürel Gezi | `culture`, `urban`, `cuisine` |
| Doğa & Macera | `nature`, `adventure`, `seclusion` |
| Şehir & Eğlence | `urban`, `nightlife`, `cuisine` |
| Karışık | `culture`, `nature`, `beaches`, `cuisine`, `urban` |

Bu yaklaşım sayesinde kullanıcının genel tatil niyeti tek bir hazır sütuna bağlı kalmadan, mevcut veri setindeki anlamlı özelliklerin kombinasyonu ile temsil edilir.

# 6 
## 6.1 Why Weighted Scoring?

Öneri sistemi içerisinde yer alan tüm kullanıcı tercihleri şehir seçiminde aynı öneme sahip değildir. Bazı kriterler kullanıcının seyahat deneyimini doğrudan etkilerken, bazı kriterler yalnızca benzer şehirler arasında daha doğru bir sıralama yapılmasına yardımcı olmaktadır.

Örneğin bütçe, seyahat dönemi veya tercih edilen tatil tarzı, önerilecek şehirin uygunluğunu belirleyen temel kriterlerdir. Buna karşılık gece hayatı, yerel mutfak veya macera aktiviteleri gibi kriterler daha çok kullanıcının kişisel ilgi alanlarını yansıtmaktadır.

Bu nedenle sistemde eşit ağırlıklı bir puanlama yerine **Weighted Scoring** yaklaşımı tercih edilmiştir. Böylece her kriter, şehir seçimindeki gerçek etkisini yansıtacak şekilde değerlendirilmektedir.

Eşit ağırlıklı puanlama kullanılması durumunda, kullanıcı için kritik öneme sahip kriterler ile ikincil öneme sahip kriterler aynı etkiye sahip olacağından öneri kalitesi düşecektir.

## 6.2 Scoring Principles

Recommendation Engine, şehirleri değerlendirirken belirli puanlama prensiplerini takip etmektedir. Bu prensipler, sistemin tutarlı, açıklanabilir ve kullanıcı odaklı öneriler sunabilmesi amacıyla belirlenmiştir.

### Hard Constraint Önceliği

Puanlama işlemine başlamadan önce Hard Constraint kuralları uygulanır. Zorunlu koşulları sağlamayan şehirler aday havuzundan çıkarılır ve puanlama sürecine dahil edilmez.

### Her Kriter Aynı Öneme Sahip Değildir

Kullanıcı tercihleri şehir seçiminde farklı seviyelerde etkiye sahiptir. Bu nedenle her kriter için farklı maksimum puanlar belirlenmiştir.

### "Fark Etmez" Seçeneği

Kullanıcının herhangi bir kriter için "Fark etmez" cevabını vermesi durumunda ilgili kriter puanlamaya dahil edilmez. Böylece kullanıcı tarafından önemsiz görülen kriterlerin sonuçları etkilemesi engellenir.

### Dinamik Maksimum Puan

Sistemde maksimum alınabilecek puan, yalnızca aktif kriterler üzerinden hesaplanmaktadır. Bu sayede farklı kullanıcıların farklı sayıda kriter seçmesi durumunda puanlar karşılaştırılabilir olmaya devam eder.

### Normalize Edilmiş Sonuç

Şehirlerin toplam puanı, aktif maksimum puana bölünerek Compatibility Score (%) hesaplanır. Böylece kullanıcıya sunulan sonuçlar standart bir ölçekte değerlendirilmiş olur.

## 6.3 Scoring Categories

Recommendation Engine içerisinde kullanılan kriterler, şehir önerisi üzerindeki görevlerine göre üç farklı kategori altında değerlendirilmektedir. Bu sınıflandırma, her kriterin algoritma içerisindeki rolünü daha açık bir şekilde tanımlamak ve puanlama mantığını sistematik hale getirmek amacıyla oluşturulmuştur.

### 6.3.1 Core Criteria

Core Criteria, öneri sisteminin temelini oluşturan kriterlerdir. Bu grupta yer alan kriterler, kullanıcının genel seyahat beklentisini ve destinasyon seçimindeki temel ihtiyaçlarını yansıtır. Bu nedenle algoritma içerisinde en yüksek ağırlıklara sahiptir.

V1 kapsamında Core Criteria aşağıdaki kriterlerden oluşmaktadır:

* Budget
* Travel Season
* Climate Preference
* Travel Style

Bu kriterler, aday şehirlerin genel uygunluğunu belirleyen temel değerlendirme adımını oluşturmaktadır.

---

### 6.3.2 Preference Criteria

Preference Criteria, kullanıcının destinasyondan beklentilerini ve kişisel ilgi alanlarını temsil eden kriterlerden oluşmaktadır. Bu kriterler şehirleri elemek yerine, aday şehirlerin puanlarını artırmak veya azaltmak amacıyla kullanılmaktadır.

V1 kapsamında Preference Criteria aşağıdaki kriterlerden oluşmaktadır:

* Culture
* Beach
* Nature
* Cuisine
* Nightlife
* Safety

Bu kriterler sayesinde öneriler, kullanıcının kişisel ilgi alanlarına daha uygun hale getirilmektedir.

---

### 6.3.3 Personalization Criteria

Personalization Criteria, benzer puan alan şehirler arasında daha kişiselleştirilmiş öneriler oluşturabilmek amacıyla kullanılan destekleyici kriterlerdir. Bu kriterler tek başına şehir seçiminde belirleyici değildir; ancak öneri sisteminin daha hassas ve kullanıcı odaklı çalışmasını sağlamaktadır.

V1 kapsamında Personalization Criteria aşağıdaki kriterlerden oluşmaktadır:

* Urban / Seclusion
* Adventure
* Travel Duration
* Travel Group

Bu kriterler sayesinde benzer özelliklere sahip şehirler arasında daha isabetli bir sıralama yapılabilmektedir.

# 7 Scoring Matrices

Bu bölümde, V1 kapsamında kullanılan her kriter için puanlama mantığı tanımlanmaktadır.

Her kriter için aşağıdaki unsurlar belirtilir:

- Kullanılan veri sütunları
- Maksimum puan
- Kullanıcı cevabına göre puanlama mantığı
- Eksik veri durumunda uygulanacak yaklaşım

## 7.1 Budget Scoring

Budget kriteri, kullanıcının tatil için ayırdığı bütçe ile şehirlerin maliyet yapısı arasındaki uyumu ölçmek amacıyla kullanılmaktadır.

Bu kriter bir Hard Constraint olarak değerlendirilmemektedir. Çünkü kullanıcının seçtiği bütçe seviyesiyle birebir eşleşmeyen bir şehir, diğer kriterlerde yüksek uyum gösterebilir. Örneğin orta bütçeli bir kullanıcı için düşük maliyetli bir şehir hâlâ oldukça uygun bir öneri olabilir.

Bu nedenle Budget kriteri, Soft Scoring kapsamında değerlendirilir.

### Kullanılan Veri Sütunları

- `budget_level`
- `Cost_index`

### Maksimum Puan

Budget kriteri toplamda maksimum **20 puan** değerindedir.

Bu puan iki alt bileşene ayrılmıştır:

| Bileşen | Max Puan |
|---|---:|
| `budget_level` uyumu | 12 |
| `Cost_index` uyumu | 8 |
| Toplam | 20 |

`budget_level`, şehrin genel bütçe sınıfını temsil ederken; `Cost_index`, şehirler arasındaki maliyet farklarını daha hassas şekilde değerlendirmek için kullanılmaktadır.

### Budget Level Scoring Matrix

| Kullanıcı Tercihi | City = Budget | City = Mid-range | City = Luxury |
|---|---:|---:|---:|
| Bütçe önemli değil | Hesaplama dışı | Hesaplama dışı | Hesaplama dışı |
| Düşük bütçe | 12 | 7 | 1 |
| Orta bütçe | 10 | 12 | 6 |
| Yüksek bütçe | 5 | 9 | 12 |

### Cost Index Scoring

`Cost_index` sayısal bir değişken olduğu için sabit eşiklerle değil, veri seti içindeki dağılıma göre değerlendirilecektir.

Bu amaçla şehirler `Cost_index` değerlerine göre üç maliyet segmentine ayrılır:

| Segment | Tanım |
|---|---|
| Low Cost | En düşük %25 |
| Mid Cost | Ortadaki %50 |
| High Cost | En yüksek %25 |

Bu yaklaşım sayesinde maliyet sınıflandırması veri setinin kendi dağılımına göre dinamik olarak yapılır. Böylece ilerleyen versiyonlarda veri seti genişlese bile sistem kendi içinde tutarlı kalmaya devam eder.

### Cost Index Scoring Matrix

| Kullanıcı Tercihi | Low Cost | Mid Cost | High Cost |
|---|---:|---:|---:|
| Bütçe önemli değil | Hesaplama dışı | Hesaplama dışı | Hesaplama dışı |
| Düşük bütçe | 8 | 4 | 1 |
| Orta bütçe | 6 | 8 | 4 |
| Yüksek bütçe | 3 | 6 | 8 |

### Eksik Veri Durumu

Bazı şehirlerde `Cost_index` değeri bulunmamaktadır.

Bu durumda `Cost_index` bileşeni puanlamaya dahil edilmez. Şehir yalnızca `budget_level` uyumu üzerinden değerlendirilir ve Budget kriteri için aktif maksimum puan **20 yerine 12** olarak kabul edilir.

Bu yaklaşım sayesinde eksik `Cost_index` verisi bulunan şehirler sistemden çıkarılmaz; yalnızca daha sınırlı bütçe bilgisiyle değerlendirilir.


## 7.2 Travel Season Scoring

Travel Season kriteri, kullanıcının seyahat etmeyi planladığı dönem ile şehirlerin ziyaret için önerilen dönemleri arasındaki uyumu değerlendirmek amacıyla kullanılmaktadır.

Bu kriter, şehirlerin yıl içerisindeki iklim koşulları, turistik uygunluğu ve genel ziyaret deneyimini dikkate alan bir değerlendirme sağlamaktadır.

### Kullanılan Veri Sütunu

* `Best Time to Visit`

### Maksimum Puan

Travel Season kriteri maksimum **15 puan** değerindedir.

### Scoring Mantığı

Kullanıcının seçtiği mevsim, şehrin `Best Time to Visit` sütununda yer alıyorsa şehir tam puan alır.

Yer almıyorsa puan verilmez.

Bu kriterde kısmi puan uygulanmamaktadır.

Bunun nedeni, bir şehrin kullanıcının seyahat edeceği dönemde öneriliyor olmasının yeterli kabul edilmesidir. Şehrin başka mevsimlerde de öneriliyor olması ek bir avantaj sağlamamaktadır.

### Travel Season Scoring Matrix

| Kullanıcı Tercihi | Şehirin Best Time to Visit Bilgisi | Puan |
| ----------------- | ---------------------------------- | ---: |
| İlkbahar          | Spring içeriyor                    |   15 |
| Yaz               | Summer içeriyor                    |   15 |
| Sonbahar          | Autumn içeriyor                    |   15 |
| Kış               | Winter içeriyor                    |   15 |
| Fark etmez        | Hesaplama dışı                     |    - |
| Eşleşme yok       | İlgili mevsimi içermiyor           |    0 |

### Eksik Veri Durumu

Şehir için `Best Time to Visit` bilgisi bulunmuyorsa Travel Season kriteri ilgili şehir için değerlendirmeye alınmaz ve aktif maksimum puan yeniden hesaplanır.


## 7.3 Climate Preference Scoring

Climate Preference kriteri, kullanıcının tercih ettiği hava sıcaklığı ile şehirlerin ilgili seyahat dönemindeki ortalama sıcaklığı arasındaki uyumu değerlendirmek amacıyla kullanılmaktadır.

Bu kriter, Travel Season kriterinden farklıdır. Travel Season kullanıcının hangi dönemde seyahat edeceğini değerlendirirken, Climate Preference kullanıcının o dönemde nasıl bir hava beklediğini ölçmektedir.

### Kullanılan Veri Sütunu

- `avg_temp_monthly`

### Maksimum Puan

Climate Preference kriteri maksimum **15 puan** değerindedir.

### Scoring Mantığı

Kullanıcının seçtiği seyahat dönemine göre ilgili ayların ortalama sıcaklığı hesaplanır.

| Seyahat Dönemi | Kullanılan Aylar |
|---|---|
| İlkbahar | Mart, Nisan, Mayıs |
| Yaz | Haziran, Temmuz, Ağustos |
| Sonbahar | Eylül, Ekim, Kasım |
| Kış | Aralık, Ocak, Şubat |

Bu kriterde veri dağılımına dayalı percentile yöntemi yerine sabit sıcaklık eşikleri kullanılmıştır.

Bunun nedeni, sıcaklık algısının kullanıcı açısından göreceli değil, daha çok mutlak değerlere dayalı olmasıdır. Örneğin veri setindeki en sıcak şehir 22°C olsa bile, bu değer kullanıcı tarafından “sıcak hava” olarak algılanmayabilir.

Bu nedenle V1 kapsamında aşağıdaki sıcaklık aralıkları kullanılmıştır:

| Climate Segment | Sıcaklık Aralığı |
|---|---|
| Serin | 15°C ve altı |
| Ilık | 15°C - 25°C arası |
| Sıcak | 25°C ve üzeri |

### Climate Preference Scoring Matrix

| Kullanıcı Tercihi | Serin Şehir | Ilık Şehir | Sıcak Şehir |
|---|---:|---:|---:|
| Serin | 15 | 8 | 2 |
| Ilık | 8 | 15 | 8 |
| Sıcak | 2 | 8 | 15 |
| Fark etmez | Hesaplama dışı | Hesaplama dışı | Hesaplama dışı |

### Eksik Veri Durumu

Şehir için `avg_temp_monthly` bilgisi bulunmuyorsa Climate Preference kriteri ilgili şehir için değerlendirmeye alınmaz ve aktif maksimum puan yeniden hesaplanır.


## 7.4 Travel Style Scoring

Travel Style kriteri, kullanıcının genel tatil yönelimini belirlemek amacıyla kullanılmaktadır.

Bu kriter doğrudan veri setinde bulunan tek bir sütuna karşılık gelmemektedir. Bunun yerine mevcut şehir özelliklerinin belirli ağırlıklarla birleştirilmesiyle oluşturulmuş türetilmiş bir kriterdir.

Bu nedenle Travel Style, V1 kapsamında Feature Engineering yaklaşımı ile hesaplanmaktadır.

### Kullanılan Veri Sütunları

- `beaches`
- `culture`
- `nature`
- `adventure`
- `nightlife`
- `wellness`
- `urban`
- `seclusion`
- `cuisine`

### Maksimum Puan

Travel Style kriteri maksimum **10 puan** değerindedir.

Başlangıçta bu kriterin daha yüksek ağırlıkla değerlendirilmesi düşünülmüş olsa da, Travel Style içerisinde kullanılan bazı özellikler ilerleyen kriterlerde tekrar ayrı ayrı değerlendirilmektedir.

Örneğin `beaches`, hem Travel Style içerisinde hem de Beach kriterinde kullanılabilmektedir. Aynı özelliğin birden fazla kriter altında yüksek ağırlıkla değerlendirilmesi double counting etkisi yaratabileceğinden, Travel Style kriterinin maksimum puanı **10** olarak sınırlandırılmıştır.

Bu sayede Travel Style, kullanıcının genel tatil yönelimini belirleyen destekleyici bir başlangıç kriteri olarak çalışır; detaylı kişiselleştirme ise sonraki kriterler ile sağlanır.

### Ağırlıklandırma Mantığı

Her Travel Style seçeneği üç farklı özellikten oluşmaktadır.

| Rol | Maksimum Puan |
|---|---:|
| Primary Feature | 5 |
| Secondary Feature | 3 |
| Supporting Feature | 2 |

Toplam maksimum puan: **10**

### Travel Style Mapping

| Kullanıcı Tercihi | Primary | Secondary | Supporting |
|---|---|---|---|
| Deniz & Relax | `beaches` | `wellness` | `seclusion` |
| Kültürel Gezi | `culture` | `urban` | `cuisine` |
| Doğa & Macera | `nature` | `adventure` | `seclusion` |
| Şehir & Eğlence | `urban` | `nightlife` | `cuisine` |
| Fark etmez | Hesaplama dışı | - | - |

### Scoring Mantığı

İlgili özellikler veri setinde 1 ile 5 arasında puanlanmıştır.

Her özellik aşağıdaki formül ile kendi maksimum ağırlığına ölçeklenir:

\[
Feature\ Score =
\left(
\frac{Feature\ Value}{Maximum\ Feature\ Value}
\right)
\times
Feature\ Weight
\]

V1 kapsamında `Maximum Feature Value = 5` olarak kabul edilmektedir.

Travel Style puanı, Primary, Secondary ve Supporting Feature puanlarının toplamı ile hesaplanır.

\[
Travel\ Style\ Score =
Primary\ Score + Secondary\ Score + Supporting\ Score
\]

### Örnek

Kullanıcı **Deniz & Relax** seçmiştir.

Şehir özellikleri:

- `beaches = 5`
- `wellness = 4`
- `seclusion = 3`

Hesaplama:

- `beaches`: (5 / 5) × 5 = 5
- `wellness`: (4 / 5) × 3 = 2.4
- `seclusion`: (3 / 5) × 2 = 1.2

Toplam Travel Style Score:

5 + 2.4 + 1.2 = **8.6 / 10**

### Eksik Veri Durumu

Travel Style hesaplamasında kullanılan özelliklerden herhangi biri eksikse, ilgili özellik puanlamaya dahil edilmez ve maksimum alınabilecek puan dinamik olarak yeniden hesaplanır.

## 7.5 Preference Criteria Scoring

Preference Criteria, kullanıcının seyahat deneyiminde önem verdiği kişisel tercihleri temsil etmektedir. Bu kriterler şehirleri elemek amacıyla kullanılmaz; bunun yerine aday şehirlerin birbirleri arasındaki sıralamasını daha doğru yapabilmek için değerlendirilir.

V1 kapsamında aşağıdaki kriterler aynı puanlama metodunu kullanmaktadır.

| Kullanıcı Tercihi       | Dataset Sütunu | Maksimum Puan |
| ----------------------- | -------------- | ------------: |
| Deniz Tatili            | `beaches`      |             8 |
| Tarihi ve Kültürel Gezi | `culture`      |             8 |
| Doğa                    | `nature`       |             8 |
| Yerel Mutfak            | `cuisine`      |             7 |
| Gece Hayatı             | `nightlife`    |             7 |
| Güvenlik                | `Safety`       |             8 |
| Şehir Hayatı            | `urban`        |             6 |
| Sakinlik                | `seclusion`    |             6 |
| Macera/Açık Hava        | `adventure`    |             6 |

### Kullanıcı Tercih Seviyeleri

Her kriter için kullanıcı aşağıdaki seçeneklerden birini seçmektedir.

| Kullanıcı Cevabı | Importance Multiplier |
| ---------------- | --------------------: |
| Çok önemli       |                  1.00 |
| Önemli           |                  0.75 |
| Orta             |                  0.50 |
| Az önemli        |                  0.25 |
| Fark etmez       |        Hesaplama dışı |

Kullanıcının **"Fark etmez"** seçeneğini işaretlemesi durumunda ilgili kriter puanlamaya dahil edilmez ve maksimum alınabilecek puan dinamik olarak yeniden hesaplanır.

### Scoring Mantığı

Her şehir için ilgili özellik veri setinde **1 ile 5** arasında puanlanmıştır.

İlk olarak şehir puanı normalize edilir.

[
Normalized\ Feature =
\frac{Feature\ Value}{Maximum\ Feature\ Value}
]

Ardından kullanıcının önem derecesi dikkate alınarak kriter puanı hesaplanır.

[
Criterion\ Score =
Normalized\ Feature
\times
Importance\ Multiplier
\times
Maximum\ Criterion\ Score
]

### Örnek

Kullanıcı, **Deniz Tatili** kriterini **"Çok önemli"** olarak işaretlemiştir.

Şehir için:

* `beaches = 4`

Hesaplama:

* Normalized Feature = 4 / 5 = 0.80
* Importance Multiplier = 1.00
* Maximum Criterion Score = 8

[
0.80 \times 1.00 \times 8 = 6.4
]

Sonuç olarak şehir bu kriterden **6.4 / 8** puan alacaktır.

### Eksik Veri Durumu

İlgili veri sütunu şehir için bulunmuyorsa bu kriter değerlendirmeye alınmaz ve maksimum alınabilecek puan dinamik olarak yeniden hesaplanır.


## 7.6 Travel Duration Scoring

Travel Duration kriteri, kullanıcının planladığı tatil süresi ile şehir için önerilen ideal ziyaret süresi arasındaki uyumu değerlendirmek amacıyla kullanılmaktadır.

Bu kriter, destinasyonun kullanıcının zaman planına uygun olup olmadığını anlamaya yardımcı olur.

### Kullanılan Veri Sütunu

- `ideal_durations`

### Maksimum Puan

Travel Duration kriteri maksimum **5 puan** değerindedir.

### Süre Kategorileri

Kullanıcıdan gün sayısı yerine aşağıdaki kategorilerden biri seçmesi istenir.

| Kullanıcı Tercihi | Açıklama |
|---|---|
| Weekend Trip | 1–3 gün |
| Short Trip | 4–6 gün |
| One Week | 7–9 gün |
| Long Vacation | 10+ gün |
| Fark etmez | Hesaplama dışı |

Dataset içerisinde yer alan `ideal_durations` değerleri de aynı kategorilere dönüştürülür.

### Scoring Mantığı

Kullanıcının seçtiği süre kategorisi ile şehrin ideal süre kategorisi eşleşirse şehir tam puan alır.

Yakın kategoriler kısmi puan alır. Uzak kategoriler düşük puan alır.

### Travel Duration Scoring Matrix

| Kullanıcı Tercihi | Weekend Trip | Short Trip | One Week | Long Vacation |
|---|---:|---:|---:|---:|
| Weekend Trip | 5 | 3 | 1 | 0 |
| Short Trip | 3 | 5 | 3 | 1 |
| One Week | 1 | 3 | 5 | 3 |
| Long Vacation | 0 | 1 | 3 | 5 |
| Fark etmez | Hesaplama dışı | Hesaplama dışı | Hesaplama dışı | Hesaplama dışı |

### Eksik Veri Durumu

Şehir için `ideal_durations` bilgisi bulunmuyorsa Travel Duration kriteri ilgili şehir için değerlendirmeye alınmaz ve aktif maksimum puan yeniden hesaplanır.

# 8. Final Recommendation Score

Hard Constraint aşamasını başarıyla geçen tüm şehirler puanlama sürecine dahil edilir.

Her kriter için hesaplanan puanlar toplanarak şehrin toplam puanı elde edilir.

[
Total\ Score =
\sum_{i=1}^{n} Criterion\ Score_i
]

Ancak kullanıcıların seçtiği kriter sayısı farklı olabileceğinden, yalnızca toplam puanların karşılaştırılması adil bir değerlendirme sağlamamaktadır.

Örneğin bazı kullanıcılar tüm kriterleri önemserken, bazı kullanıcılar birçok kriter için "Fark etmez" seçeneğini işaretleyebilir.

Bu nedenle sistem, her kullanıcı için aktif maksimum puanı yeniden hesaplar.

Sonuç olarak şehirlerin uyumluluk oranı aşağıdaki formül ile hesaplanmaktadır.

[
Compatibility\ Score =
\frac{Total\ Score}
{Active\ Maximum\ Score}
\times 100
]

Bu yaklaşım sayesinde farklı kullanıcı tercihleri arasında adil ve karşılaştırılabilir sonuçlar elde edilmektedir.

# 9. Recommendation Ranking

Hard Constraint ve Scoring aşamalarının tamamlanmasının ardından her şehir için bir **Compatibility Score (%)** hesaplanmış olur.

Recommendation Engine, aday şehirleri Compatibility Score değerlerine göre büyükten küçüğe sıralar.

En yüksek Compatibility Score değerine sahip şehirler kullanıcıya öneri olarak sunulur.

V1 kapsamında kullanıcıya **Top 5** şehir önerilmektedir.

Top 5 öneri tercih edilmesinin temel nedenleri şunlardır:

* Kullanıcıya yalnızca tek bir alternatif sunmamak,
* Çok fazla seçenek oluşturarak karar verme sürecini zorlaştırmamak,
* Benzer uyumluluk skoruna sahip alternatif şehirlerin de değerlendirilmesine olanak sağlamak.

Sonuç ekranında her şehir için aşağıdaki bilgiler gösterilecektir:

* Şehir Adı
* Ülke
* Compatibility Score (%)
* Kısa Şehir Açıklaması
* Önerilme Sebepleri

### Tie-Breaking Logic

V1 kapsamında temel sonuç ekranı Top 5 şehir üzerinden kurgulanmıştır.

Ancak 5. sıradaki şehir ile aynı Compatibility Score değerine sahip başka şehirler varsa, bu şehirler de sonuç listesine dahil edilir.

Bu yaklaşım sayesinde aynı uyumluluk skoruna sahip şehirler yalnızca sıralama pozisyonu nedeniyle dışarıda bırakılmaz.

Örnek:

| Sıra | Şehir | Compatibility Score |
|---|---|---:|
| 1 | Porto | 92 |
| 2 | Valencia | 91 |
| 3 | Florence | 91 |
| 4 | Prague | 91 |
| 5 | Vienna | 90 |
| 6 | Budapest | 90 |

Bu durumda hem Vienna hem de Budapest kullanıcıya gösterilir.

# 10. Explainable Recommendation

Recommendation Engine yalnızca şehir önerisinde bulunmakla kalmaz, aynı zamanda önerinin hangi kriterlere göre yapıldığını da kullanıcıya açık bir şekilde sunar.

Bu yaklaşım sayesinde kullanıcı, önerilen şehrin kendi tercihleriyle hangi açılardan örtüştüğünü görebilir ve sistemin karar mekanizmasını daha iyi anlayabilir.

### Açıklama Oluşturma Mantığı

Her kriter hesaplanırken yalnızca puan üretilmez. Aynı zamanda ilgili kriter için kısa bir açıklama metni de oluşturulur.

Örneğin Budget Scoring fonksiyonu yalnızca bütçe puanını değil, aynı zamanda bütçe uyumunu açıklayan kısa bir metni de üretir.

Bu yaklaşım tüm kriterler için uygulanmaktadır.

### En Güçlü Eşleşmelerin Gösterilmesi

Bir şehir için oluşturulan tüm açıklamalar kullanıcıya gösterilmez.

Bunun yerine en yüksek katkıyı sağlayan kriterler belirlenerek öneri sebepleri oluşturulur.

Böylece kullanıcı yalnızca şehir önerisini en fazla etkileyen kriterleri görür.

### Örnek Sonuç

Porto önerildi çünkü:

* Seçtiğiniz bütçe aralığı ile uyumludur.
* Yaz döneminde ziyaret edilmesi önerilmektedir.
* Ilık hava tercihinize uygundur.
* Güvenlik beklentinizi karşılamaktadır.
* Yerel mutfağı güçlüdür.

Bu yaklaşım sayesinde öneri sistemi yalnızca sonuç üreten değil, aynı zamanda ürettiği sonucu açıklayabilen şeffaf bir karar destek sistemi haline gelmektedir.

#### 10.1 Recommendation Philosophy

Recommendation Engine'in amacı kullanıcı adına tek bir "doğru" şehir seçmek değildir. Amaç, kullanıcının tercihlerine en yüksek uyumu sağlayan alternatifleri belirlemek ve bu önerileri şeffaf bir şekilde sunmaktır. Bu nedenle sistem, kesin karar veren bir yapı yerine açıklanabilir ve kullanıcı odaklı bir karar destek sistemi olarak tasarlanmıştır.

# 11. Future Improvements

Bu proje, modüler bir mimari ile tasarlandığı için yeni veri kaynakları ve yeni değerlendirme kriterleri sisteme kolayca entegre edilebilecek şekilde geliştirilmiştir.

V1 kapsamında temel öneri sistemi oluşturulmuş ve statik veri setleri kullanılmıştır. İlerleyen versiyonlarda sistem aşağıdaki geliştirmeler ile genişletilebilir.

### V2 – Yeni Veri Kaynakları

Bu aşamada mevcut öneri algoritması korunarak sisteme yeni veri kaynakları eklenebilir.

Önerilen geliştirmeler:

* THY direkt uçuş bilgilerinin entegrasyonu
* İstanbul çıkışlı uçuş sürelerinin eklenmesi
* Türkiye'ye olan coğrafi uzaklığın değerlendirilmesi
* Schengen gereksiniminin ülke bazında otomatik değerlendirilmesi
* Güncel yaşam maliyeti verilerinin düzenli olarak güncellenmesi

Bu geliştirmeler mevcut algoritmaya yeni kriterler eklenmesini sağlayacak, ancak mevcut sistem mimarisinde herhangi bir değişiklik gerektirmeyecektir.

---

### V3 – Dinamik Veri Entegrasyonu

V3 kapsamında statik veri setleri yerine gerçek zamanlı veri kaynaklarının kullanılması planlanmaktadır.

Örnek geliştirmeler:

* Gerçek zamanlı hava durumu API entegrasyonu
* Güncel döviz kuru entegrasyonu
* Güncel otel fiyatlarının entegrasyonu
* Güncel etkinlik ve festival bilgilerinin eklenmesi

Bu sayede öneriler yalnızca şehir özelliklerine değil, seyahat tarihindeki güncel koşullara göre de kişiselleştirilebilecektir.

---

# 12. Algorithm Summary Table

Aşağıdaki tablo, V1 kapsamında kullanılan kriterleri, veri kaynaklarını ve hesaplama yöntemlerini özetlemektedir.

| Kriter | Kullanılan Veri | Max Puan | Hesaplama Yöntemi |
|---|---|---:|---|
| Visa Requirement | `visa_required` | Eleme | Hard Constraint |
| Budget | `budget_level`, `Cost_index` | 20 | Matrix + Cost Index Segmentasyonu |
| Travel Season | `Best Time to Visit` | 15 | Exact Match |
| Climate Preference | `avg_temp_monthly` | 15 | Sıcaklık Eşiği |
| Travel Style | Multiple Features | 10 | Weighted Feature Engineering |
| Preference Criteria | `beaches`, `culture`, `nature`, `cuisine`, `nightlife`, `Safety`, `urban`, `seclusion`, `adventure` | 6–8 | Normalize Edilmiş Feature Score |
| Travel Duration | `ideal_durations` | 5 | Category Matching |

### Genel Akış

1. Hard Constraint kuralları uygulanır.
2. Uygun şehir havuzu oluşturulur.
3. Aktif kriterler üzerinden şehir puanları hesaplanır.
4. Active Maximum Score belirlenir.
5. Compatibility Score (%) hesaplanır.
6. Şehirler Compatibility Score değerine göre sıralanır.
7. Top 5 şehir ve aynı skora sahip ek şehirler kullanıcıya gösterilir.
8. En yüksek katkı sağlayan kriterler üzerinden Explainable Recommendation oluşturulur.