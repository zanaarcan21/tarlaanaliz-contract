# Contracts — Component SSOT (Filtered View)


## KR Domain Paketleri İndeksi (Navigasyon)

**KR Şablonu (Kanonik):**
1) Amaç
2) Kapsam / Applies-to
3) Zorunluluklar (MUST) — test edilebilir maddeler
4) Kanıt / Artefact (manifest, raporlar, sertifika, event)
5) Audit / Log (olay adları + correlation_id)
6) Hata Modları / Quarantine kararları
7) Test / Kabul Kriterleri (E2E senaryolar)
8) Cross-refs (ilgili KR’ler)

**Not:** Bu bölüm sadece navigasyon içindir. Asıl normatif metin her KR başlığının altındadır.

### A) Security & Isolation
- KR-070 — Worker Isolation & Egress Policy
- KR-071 — One-way Data Flow + Allowlist Yerleşimi (Ingress)
- KR-073 — Untrusted File Handling + AV1/AV2 + Sandbox

### B) Data Lifecycle & Evidence (Chain of Custody)
- KR-072 — Dataset Lifecycle + Kanıt Zinciri (manifest/hash/signature/verification)
- KR-018 — Radiometric Calibration Hard Gate (QC + Certificate)
- KR-081 — Contract-First / Schema Gates (CI)

### C) Orchestration & Operations
- KR-017 — YZ Analiz Hattı (Şemsiye KR: 070–073 ayrıştırması)
- KR-015 — Pilot kapasite/planlama alt kuralları

### D) Payments & Governance
- KR-033 — Ödeme + Manuel Onay + Audit


**Tarih:** 2026-02-02  
**Bu dosya ne yapar?** Bu bileşen için geçerli KR’leri listeler ve *bileşen-özel uygulama notlarını* toplar.  
**Bu dosya ne yapmaz?** Yeni KR üretmez; normatif metin için `kr_registry.md` kanoniktir.

## Kapsam

Bu doküman, `tarlaanaliz-contracts` tarafında API/JSON Schema sözleşmelerini etkileyen kuralları içerir.

## Cross‑ref kuralları (bu bileşen için)

- Metinde her zaman `[KR-xxx]` kullanılır.
- Eğer başka bileşene bağımlılık varsa, “bkz.” ile o bileşenin SSOT’una **ve** registry’ye bağlanır.  
  Örn: “bkz. `worker_ssot.md` + [KR-018]”
- Alias görürsen: `[KR-082] (alias of KR-018)` biçimini koru; normatif kararlar KR-018’den okunur.
- Contracts tarafında şema referansı gerekiyorsa, ilgili JSON Schema dosya yolu veya OpenAPI route’u **mutlaka** belirtilir (bkz. [KR-081]).

## Bu bileşenin “tek doğru çıktısı”
- OpenAPI (public/internal)
- JSON Schema (AnalysisJob, CalibratedDatasetManifest, PaymentIntent vb.)
- CI doğrulamaları (schema validation, backwards compatibility)

## Bu bileşende geçerli KR listesi

| KR | Başlık | Kısa normatif özet |
| --- | --- | --- |
| [KR-000](kr_registry.md#kr-000) | Bu doküman seti nasıl okunur? | Saha adımları ve DJI entegrasyon ayrıntıları ayrı bir SOP dokümanında tutulur |
| [KR-001](kr_registry.md#kr-001) | Proje Özeti | *Amaç:** Çiftçilerin ürün kaybını erken uyarı ile azaltmak ve dönüm bazlı analiz hizmeti satmak. Başlangıç bölgesi GAP, ardından Türkiye geneline ölçekleme. |
| [KR-002](kr_registry.md#kr-002) | Harita Katmanı Anlamları (Renk + Desen) | | Katman | Renk | Desen | |
| [KR-017](kr_registry.md#kr-017) | YZ Modeli ile Analiz | *Veri Akışı:** "FieldID + bitki türü + MissionID; PII yok" bu bilgiler sadece uçuş yapacak drone pilotuna ve hafıza kartlarına işlenir. |
| [KR-018](kr_registry.md#kr-018) | Tam Radyometrik Kalibrasyon Zorunluluğu (Radiometric Calibration: ışık/sensör etkilerini düzeltme) | Model eğitimi (training: modelin öğrenmesi) ve saha sonuçları arasında tutarlılık (training-serving parity: eğitim/çalıştırma aynı dağılım). |
| [KR-029](kr_registry.md#kr-029) | YZ Eğitim Geri Bildirimi (Training Feedback Loop) | *Amaç:** Uzman düzeltmelerini YZ modeline geri beslemek ve model iyileştirmesi yapmak. |
| [KR-032](kr_registry.md#kr-032) | Training Export Standardı | *Amaç:** Uzman feedback'lerini standart formatta export ederek model eğitim pipeline'ına aktarmak. |
| [KR-041](kr_registry.md#kr-041) | SDLC Kapıları (Gate) - Zorunlu Kontroller | Contracts pinleme: CONTRACTS_VERSION (SemVer) + CONTRACTS_SHA256 zorunlu; değişiklikte breaking-change kontrolü |
| [KR-043](kr_registry.md#kr-043) | Test Checklist (Senaryo Bazlı) | | Senaryo | Adımlar (özet) | Beklenen Sonuç | Kanıt/Artefakt | |
| [KR-080](kr_registry.md#kr-080) | Ana İş Akışları için Teknik Kurallar | Bu bölüm; ana iş akışlarının iş planı anlatısında zaten bulunan kısımlarını tekrar etmez. Sadece teknik spesifikasyonda eklenen/sertleştirilen kuralları listeler. |
| [KR-081](kr_registry.md#kr-081) | Kontrat Şemaları (Contract-First) — Kanonik JSON Schema | *Amaç:** "olmalı" seviyesinden çıkıp, kodlamadan önce ortak dilin **makine-doğrulanabilir** (machine-verifiable) hale gelmesi. |
| [KR-082](kr_registry.md#kr-082) | RADIOMETRY / Radyometrik Kalibrasyon (Uyumluluk Etiketi) | Bu madde, **[KR-018] Tam Radyometrik Kalibrasyon Zorunluluğu** ile **aynı zorunluluğu** “KR-082” etiketiyle de referanslayabilmek için eklenmiştir. |

---

## Uygulama notları şablonu (KR başına)

Aşağıdaki blok, bu bileşende bir KR uygulanırken doldurulacak standart alanlardır:

### Şablon
- **Amaç:** (Bu bileşende KR’nin hangi problemi çözdüğü)
- **Girişler/Çıkışlar:** (input/output, event/command, dosya formatı)
- **Hard gate mi? Warn mı?:** (fail-fast / degrade)
- **Log/Audit kanıtı:** (hangi log, hangi alanlar, hangi correlation id)
- **Test/Acceptance:** (unit/integration/e2e kriterleri)
- **Cross‑refs:** (diğer bileşenlerdeki bağımlı KR’ler)

### KR-000 — Bu doküman seti nasıl okunur?

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-001 — Proje Özeti

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-002 — Harita Katmanı Anlamları (Renk + Desen)

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-017 — YZ Modeli ile Analiz

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-018 — Tam Radyometrik Kalibrasyon Zorunluluğu (Radiometric Calibration: ışık/sensör etkilerini düzeltme)

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-029 — YZ Eğitim Geri Bildirimi (Training Feedback Loop)

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-032 — Training Export Standardı

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-041 — SDLC Kapıları (Gate) - Zorunlu Kontroller

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-043 — Test Checklist (Senaryo Bazlı)

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-080 — Ana İş Akışları için Teknik Kurallar

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-081 — Kontrat Şemaları (Contract-First) — Kanonik JSON Schema

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---

### KR-082 — RADIOMETRY / Radyometrik Kalibrasyon (Uyumluluk Etiketi)

- **Amaç:** 
- **Girişler/Çıkışlar:** 
- **Hard gate mi? Warn mı?:** 
- **Log/Audit kanıtı:** 
- **Test/Acceptance:** 
- **Cross‑refs:** 

---



### KR-072 — Dataset Lifecycle + Kanıt Zinciri — Contract-First

- **Amaç:** veri akışını sözleşmeye bağlamak; tamper/malware tartışmalarını teknik kanıtla çözmek.
- **Dataset durumları (enum, zorunlu):**
  - `RAW_INGESTED`, `RAW_SCANNED_EDGE_OK`, `RAW_HASH_SEALED`, `CALIBRATED`, `CALIBRATED_SCANNED_CENTER_OK`,
    `DISPATCHED_TO_WORKER`, `ANALYZED`, `DERIVED_PUBLISHED`, `ARCHIVED`, `REJECTED_QUARANTINE`
- **Zorunlu şemalar:**
  - `schemas/edge/dataset_manifest.v1.schema.json`
  - `schemas/edge/scan_report.v1.schema.json` (AV1/AV2 ortak)
  - `schemas/edge/verification_report.v1.schema.json` (hash match/mismatch)
  - `schemas/edge/calibration_result.v1.schema.json` + `schemas/edge/qc_report.v1.schema.json`
  - `schemas/edge/transfer_batch.v1.schema.json` (chunk/resume)
  - (platform) `schemas/platform/evidence_bundle_ref.v1.schema.json` (ham değil, referans)
- **Hard gate:**
  - `analysis_job.v1` yalnızca `CALIBRATED_SCANNED_CENTER_OK` dataset_ref kabul eder.
  - Hash mismatch / AV fail / QC fail → `REJECTED_QUARANTINE`.
- **Örnekler + CI:**
  - `docs/examples/` altında example JSON’lar şemaya uymalı.
  - CI: validate_all_schemas + examples_match + breaking_change_detector.

---

- **Test/Acceptance:** Örnek JSON’lar şemaya uyar; mismatch senaryosu otomatik test edilir.


### KR-073 — Untrusted File Handling + Malware (AV1/AV2)

- **Amaç:** ham dosyaları untrusted input olarak ele almak; tarama + doğrulama raporlarını kontratlaştırmak.
- **scan_report.v1 (zorunlu alanlar):**
  - engine_id, signatures_version, started_at/ended_at, scanned_files[{path,size,sha256}], result(PASS/FAIL), findings[], quarantined
- **verification_report.v1 (zorunlu alanlar):**
  - manifest_hash, computed_hashes, mismatches[], decision(ACCEPT/REJECT), reason
- **Hard gate:** PASS olmadan dataset durum ilerleyemez; decision REJECT → `REJECTED_QUARANTINE`.

---

- **Test/Acceptance:** EICAR/benzeri test vektörleri lab’da doğrulanır; rapor formatı şemaya uyar.
