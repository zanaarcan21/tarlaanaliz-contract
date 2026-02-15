tarlaanaliz-contracts/
├─ README.md
│  # (Amaç: Contract-first repo manifestosu + “tek doğru sözleşme” prensipleri)
│  # (Normatif Standart: JSON Schema Draft 2020-12 — tüm JSON Schema dosyaları bu standarda göre yazılır)
│  # (İlk etap kullanım kuralı: Sadece 2020-12’nin şu iki özelliği zorunlu tutulur:
│  #   1) $defs: tekrar kullanılan tip/alt şema tanımları için
│  #   2) unevaluatedProperties:false: şema dışı alan sızmasını engellemek için
│  #  Not: İleride ihtiyaç oldukça (dependentSchemas, if/then/else, dynamicRef vb.) kontrollü eklenir.)
│  # (Kritik Güvenlik: email/TCKN/OTP YOK — kimlik: telefon + 6 haneli PIN; PII minimum, loglar maskeli)
│  # (Kullanım: Consumer repo’lar (platform/edge/worker) CONTRACTS_VERSION.md + SHA-256 ile bu repo’yu pinler)
│  # (Build akışı: tools/validate.py → tests/ → tools/breaking_change_detector.py → release → tools/sync_to_repos.sh)
│
├─ CONTRACTS_VERSION.md
│  # (Amaç: Contract paketini kilitleyen tek kaynak sürüm + içerik hash’i)
│  # (İçerik: semver=vX.Y.Z + sha256 + created_at + breaking_change=true/false)
│  # (Kural: Şema/enum/API’de breaking-change varsa MAJOR artırılmadan merge/release yapılamaz)
│  # (İlişki: Consumer repo’larda aynı dosya bulunur; CI’da birebir eşleşme beklenir)
│
├─ CHANGELOG.md
│  # (Amaç: Değişiklik günlüğü (insan-okur); release notlarının kaynağı)
│  # (Format: Keep a Changelog + SemVer; Added/Changed/Deprecated/Removed/Fixed/Security)
│  # (Kural: Breaking-change her zaman MIGRATION GUIDE ile linklenir)
│
├─ LICENSE
│  # (Amaç: Lisans metni)
│
├─ .gitignore
│  # (Amaç: generated/*, venv, node_modules, .pytest_cache, dist/build, coverage vb. dışlamak)
│
├─ package.json
│  # (Amaç: Node/TS toolchain — OpenAPI bundle + JSON Schema validate + TS type generation)
│  # (İçerik: Ajv (2020-12 uyumlu validator) + json-schema-to-typescript + (opsiyonel) openapi bundler)
│  # (Scripts: types:gen, schema:validate, openapi:bundle, test, lint)
│  # (Kural: Ajv tarafında Draft 2020-12 metaschema etkin; Draft-07 kullanımına izin verilmez)
│
├─ pyproject.toml
│  # (Amaç: Python toolchain — schema validate + test koşumu + (opsiyonel) python model generation)
│  # (İçerik: jsonschema (Draft202012Validator) + pytest + (opsiyonel) datamodel-codegen)
│  # (Kural: Draft 2020-12 dışı $schema string’i FAIL; unevaluatedProperties:false policy kontrolü zorunlu)
│
├─ schemas/
│  # (Amaç: Normatif veri sözleşmeleri (JSON Schema Draft 2020-12))
│  # (Genel Kurallar:
│  #  - Her schema dosyası $schema=2020-12 içerir
│  #  - object tiplerinde unevaluatedProperties:false uygulanır (sızıntı önleme)
│  #  - Tekrarlı alt tipler $defs ile tanımlanır ve $ref ile kullanılır
│  #  - “PII yok” prensibi: worker/* ve core/user.v1 kesinlikle PII içermez)
│
│  ├─ core/
│  │  # (Amaç: Platformun çekirdek varlıkları; PII’den arındırılmış, rol-bağımsız temel modeller)
│  │
│  │  ├─ field.v1.schema.json
│  │  │  # (Amaç: Tarla kaydı: FieldID, boundary ref, ürün/ekim sezonu referansları)
│  │  │  # (2020-12 Kullanımı: $defs(GeoRef, SeasonRef); unevaluatedProperties:false)
│  │  │  # (Kural: owner bilgisi core’a gömülmez; erişim yetkisi RBAC + ayrı ilişkilerle yönetilir)
│  │  │  # (Tüketenler: platform_public API, events/field_created)
│  │  │
│  │  ├─ mission.v1.schema.json
│  │  │  # (Amaç: Uçuş görevi: MissionID, FieldID, zaman, durum, uçuş planı/ham veri referansları)
│  │  │  # (İlişki: enums/mission_status; pilot ataması event’le izlenir (events/mission_assigned))
│  │  │  # (Kural: PII içermez; pilot_id core’da zorunlu alan değildir (operasyonel ilişki event’te)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(FileRef, TimeWindow))
│  │  │
│  │  ├─ user.v1.schema.json
│  │  │  # (Amaç: Kullanıcı çekirdeği (PII’siz): user_id, role, status, rbac_claims, created_at)
│  │  │  # (Kritik Kural: email/TCKN/OTP alanı YOK)
│  │  │  # (İlişki: enums/role; auth tarafı sadece token/claims üretir)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(RbacClaims))
│  │  │
│  │  └─ user_pii.v1.schema.json
│  │     # (Amaç: Minimum PII: yalnızca telefon + PIN türevleri (hash) ve saklama etiketi)
│  │     # (Kritik Kural: email/TCKN/OTP YOK; SMS OTP yok; doğrulama: telefon + 6 haneli PIN)
│  │     # (Önerilen alanlar: phone_e164, phone_hash, phone_last4, pin_hash, pin_updated_at, pii_retention_tag)
│  │     # (Kural: Bu şema yalnızca PII kasasında tutulur; platform operatör/pilot arayüzlerinde asla dönülmez)
│  │     # (2020-12: unevaluatedProperties:false; $defs(Hash, Phone))
│  │
│  ├─ edge/
│  │  # (Amaç: Edge/Kiosk ingest sözleşmeleri; hash/AV/kanıt zinciri (chain-of-custody) için normatif formatlar)
│  │
│  │  ├─ intake_manifest.v1.schema.json
│  │  │  # (Amaç: İstasyona alınan batch manifesti: bütünlük, kanıt, izlenebilirlik)
│  │  │  # (Alanlar: batch_id, kiosk_id, operator_id, card_id, mission_id, field_id,
│  │  │           files[{path,size,sha256,mime}], created_at, signature, av_scan_result)
│  │  │  # (Kural: files[*].sha256 zorunlu; av_scan_result olmadan RELEASE edilemez)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(FileEntry, AvScanResult, Signature))
│  │  │  # (Tüketenler: edge_local API, platform_internal ingest endpoint’i, quarantine_event)
│  │  │
│  │  ├─ edge_metadata.v1.schema.json
│  │  │  # (Amaç: İstasyon cihazı meta + güvenlik durumu; offline çalışmada doğrulanabilirlik)
│  │  │  # (Alanlar: kiosk_id, app_version, certificate_expires, av_signature_version,
│  │  │           disk_space_gb, os_version, hardware_fingerprint, offline_mode=true)
│  │  │  # (Kural: certificate_expires CI/policy ile zorunlu; süresi geçmiş cert ile ingest reddedilir)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(Version, Fingerprint))
│  │  │
│  │  └─ quarantine_event.v1.schema.json
│  │     # (Amaç: Karantina olayı: hash/AV/policy ihlali; kanıt ve karar kaydı)
│  │     # (Alanlar: event_id, batch_id, reason_code, threat_type, decision, evidence_refs, created_at)
│  │     # (İlişki: enums/threat_type, enums/quarantine_decision)
│  │     # (2020-12: unevaluatedProperties:false; $defs(EvidenceRef))
│  │
│  ├─ worker/
│  │  # (Amaç: YZ iş sözleşmeleri (job/result). PII kesinlikle içermez.)
│  │
│  │  ├─ analysis_job.v1.schema.json
│  │  │  # (Amaç: Analiz işi: veri referansları + model/parametre + öncelik)
│  │  │  # (Alanlar: job_id, field_id, mission_id, batch_id, analysis_type, crop_type,
│  │  │  #          requires_calibrated (kalibre zorunlu mu), calibration_result_ref (kalibrasyon çıktısı ref), qc_report_ref (QC raporu ref),
│  │  │           inputs[{uri,sha256}], constraints, priority, requested_at)
│  │  │  # (Kural: inputs hash zorunlu; job “veri kanıtı” ile birlikte yürür)
│  │  │  # (İlişki: enums/analysis_type, enums/crop_type; platform_internal API)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(InputRef, Constraints))
│  │  │
│  │  └─ analysis_result.v1.schema.json
│  │     # (Amaç: Analiz sonucu: özet + metrikler + katman referansları + model parmak izi)
│  │     # (Alanlar: job_id, status, summary, layers[{layer_id,uri,style_ref}],
│  │     #          metrics, created_at, model_fingerprint)
│  │     # (İlişki: platform/layer_registry; platform_public API)
│  │     # (2020-12: unevaluatedProperties:false; $defs(LayerRef, Metrics))
│  │
│  ├─ events/
│  │  # (Amaç: Domain event sözleşmeleri. Audit, replay, entegrasyon için “tek doğru” format)
│  │
│  │  ├─ field_created.v1.schema.json
│  │  │  # (Amaç: Field oluşturuldu olayı: actor + diff + zaman)
│  │  │  # (Kural: actor_user_id PII değildir; gerçek kimlik PII kasasındadır)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(Diff))
│  │  │
│  │  ├─ mission_assigned.v1.schema.json
│  │  │  # (Amaç: Mission atama olayı: görev-pilot eşleştirme ve sorumluluk başlangıcı)
│  │  │  # (Kural: Email bildirim semantiği yok; notification kanalı bağımsız/konfigüre edilir)
│  │  │  # (2020-12: unevaluatedProperties:false)
│  │  │
│  │  └─ analysis_completed.v1.schema.json
│  │     # (Amaç: Analiz tamamlandı olayı: job/result referansı, zaman, status)
│  │     # (2020-12: unevaluatedProperties:false)
│  │
│  ├─ shared/
│  │  # (Amaç: Ortak tipler (geo, para, opsiyonel adres). Re-use için $defs referansları)
│  │
│  │  ├─ geojson.v1.schema.json
│  │  │  # (Amaç: GeoJSON Feature/FeatureCollection tipleri)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(Geometry, Properties))
│  │  │
│  │  ├─ money.v1.schema.json
│  │  │  # (Amaç: Para: amount + currency + tax flags)
│  │  │  # (2020-12: unevaluatedProperties:false; $defs(CurrencyCode))
│  │  │
│  │  └─ address.v1.schema.json
│  │     # (Amaç: Opsiyonel adres; fatura/operasyon için. Zorunlu değil)
│  │     # (Kural: PII minimizasyonu; kullanılmadıkça toplanmaz)
│  │     # (2020-12: unevaluatedProperties:false)
│  │
│  └─ platform/
│     # (Amaç: Platform içi fiyat/komisyon/katman kayıt defteri sözleşmeleri)
│  │  ├─ calibrated_dataset_manifest.v1.schema.json   [YENİ]  # [KR-082]
│  │  │  # (Amaç: Producer sonrası “kalibre paket” manifesti: hangi çıktı dosyaları, ölçek, raporlar, hash’ler)
│  │  │  # (Alanlar: batch_id, mission_id, field_id, producer_tool, reflectance_scale, outputs[{uri,sha256,type}], reports[{uri,sha256,type}], created_at)
│  │  │  # (Kural: reflectance_scale + reports zorunlu; outputs hash zorunlu)
│  │  │
│  │  ├─ calibration_result.v1.schema.json            [YENİ]  # [KR-082]
│  │  │  # (Amaç: Kalibrasyon çıktısı özeti: yöntem, panel kullanımı, parametreler, doğrulama metrikleri)
│  │  │  # (Alanlar: calibration_id, producer_tool, method, panel_used, irradiance_info, scale, created_at, notes)
│  │  │
│  │  └─ qc_report.v1.schema.json                      [YENİ]  # [KR-082]
│  │     # (Amaç: QC raporu: PASS/WARN/FAIL + flags + recommended_action)
│  │     # (Alanlar: qc_id, status, flags[], saturation_pct, scale_ambiguous, recommended_action, created_at)
│  │     # (Kural: Platform QC Gate ve Worker doğrulaması bu raporu baz alır)

│
│     ├─ pricing.v1.schema.json
│     │  # (Amaç: Fiyat kitabı + snapshot (immutability) sözleşmesi)
│     │  # (Kural: Snapshot geçmişe dönük değiştirilemez; order/receipt referansı snapshot’a bağlanır)
│     │  # (2020-12: unevaluatedProperties:false; $defs(PriceItem))
│     │
│     ├─ payroll.v1.schema.json
│     │  # (Amaç: İl operatörü/pilot paylaşımları için payout kalemleri)
│     │  # (2020-12: unevaluatedProperties:false; $defs(PayoutLine))
│     │
│     ├─ payment_intent.v1.schema.json
│     │  # (Amaç: PaymentIntent v1 — ödeme/manuel onay akışı için sözleşme)
│     │  # (İçerik: payer{...}, target{...}, amount, method, status, payment_ref, price_snapshot_id, expires_at)
│     │
│     ├─ payment_intent.v2.schema.json
│     │  # (Amaç: PaymentIntent v2 — sade alanlar (payer_user_id, target_type/id, amount_kurus, paid_at/cancelled_at/refunded_at))
│     │  # (Not: payment_status.v2 ile REFUNDED/iade alanlarını destekler)
│     │
│     └─ layer_registry.v1.schema.json
│        # (Amaç: Layer Registry: çıktı katmanlarının anlam/legend/style standardı)
│        # (İlişki: worker/analysis_result.layers)
│        # (2020-12: unevaluatedProperties:false; $defs(StyleRef, LegendItem))
│
├─ enums/
│  # (Amaç: Enum sözleşmeleri. API + schema + UI aynı kaynaktan beslenir)
│
│  ├─ crop_type.enum.v1.json
│  │  # (Amaç: Ürün tipleri; GAP öncelikleri dahil)
│  │  # (İçerik: COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL, ...)
│  │  # (Kural: Enum değişimi breaking-change sayılabilir; migration guide zorunlu olabilir)
│  │
│  ├─ role.enum.v1.json
│  │  # (Amaç: Roller: FARMER, PILOT, ILOPERATOR, COOP_ADMIN, PLATFORM_ADMIN, SUPPORT, ...)
│  │  # (Kural: RBAC claims ile eşleşir; UI yetkileri bu enum’a bağlıdır)
│  │
│  ├─ mission_status.enum.v1.json
│  │  # (Amaç: Görev durumları)
│  │  # (İçerik: PLANNED, ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED, VERIFIED, ...)
│  │
│  ├─ analysis_type.enum.v1.json
│  │  # (Amaç: Analiz tipleri: NDVI, NDRE, HEALTH, DISEASE, PEST, WEED, WATER_STRESS, N_STRESS, ...)
│  │
│  ├─ threat_type.enum.v1.json
│  │  # (Amaç: Karantina tehdit tipleri: MALWARE, HASH_MISMATCH, POLICY_VIOLATION, ...)
│  │
│  ├─ payment_method.v1.json
│  │  # (Amaç: Ödeme yöntemi: CREDIT_CARD veya IBAN_TRANSFER)
│  │  # (Not: IBAN_TRANSFER = dekont e‑posta + manuel onay akışı)
│  │
│  ├─ payment_status.v1.json
│  │  # (Amaç: Ödeme durumu v1: PAYMENT_PENDING/PAID/REJECTED/EXPIRED/CANCELLED)
│  │
│  ├─ payment_status.v2.json
│  │  # (Amaç: Ödeme durumu v2: v1 + REFUNDED (iade senaryosu))
│  │
│  ├─ payment_target_type.v1.json
│  │  # (Amaç: Ödeme hedefi (PaymentIntent target_type): MISSION veya SUBSCRIPTION)
│  │
│  └─ quarantine_decision.enum.v1.json
│     # (Amaç: Karantina kararları: QUARANTINED, RELEASED, DELETED, MANUAL_REVIEW_REQUIRED, ...)
│
├─ ssot/
│  ├─ README.md
│  │  # (Amaç: Bu repo için SSOT haritası; kr_registry + contracts_ssot nasıl okunur?)
│  ├─ kr_registry.md
│  │  # (Amaç: KR kodlarının kanonik kaynağı; bileşen SSOT dosyaları buradan türetilir)
│  └─ contracts_ssot.md
│     # (Amaç: Contracts bileşeni için filtered view + uygulama notları; KR üretmez)
│
├─ api/
│  # (Amaç: OpenAPI sözleşmeleri (public/internal/edge-local). JSON Schema’lara referans verir)
│
│  ├─ platform_public.v1.yaml
│  │  # (Amaç: Web+Mobil public API. Farmer/Coop UI tüketir)
│  │  # (Kural: PII minimizasyonu; email/tckn/otp yok)
│  │  # (İlişki: schemas/* + enums/*)
│  │
│  ├─ platform_internal.v1.yaml
│  │  # (Amaç: Platform-Edge-Worker servisleri arası internal API)
│  │  # (İçerik: ingest bildirimi, job/result kabulü, audit/event post)
│  │
│  ├─ edge_local.v1.yaml
│  │  # (Amaç: Kiosk offline local API (UI↔kiosk). Batch oluşturma, scan sonuçları, imzalama)
│  │
│  └─ components/
│     # (Amaç: OpenAPI parça bileşenleri (param/schemas/responses/security) — tekrar kullanım)
│
│     ├─ parameters.yaml
│     │  # (Amaç: Ortak query/path parametreleri: field_id, mission_id, pagination)
│     │
│     ├─ schemas.yaml
│     │  # (Amaç: OpenAPI schema köprüsü — JSON Schema referanslarını tek noktadan bağlamak)
│     │
│     ├─ responses.yaml
│     │  # (Amaç: Standart hata/başarı response şablonları)
│     │
│     └─ security_schemes.yaml
│        # (Amaç: Auth şemaları: phone+PIN oturum token’ı (JWT/opaque) + RBAC claims)
│        # (Kural: OTP yok; email yok; TCKN yok)
│
├─ docs/
│  # (Amaç: Politika + kanonik dokümanlar + örnek payload + migration rehberleri + checklistler)
│
│  ├─ README.md
│  │  # (Amaç: Dokümantasyon giriş haritası — “hangi soruya hangi dosya?”)
│  │
│  ├─ versioning_policy.md
│  │  # (Amaç: SemVer + breaking-change kuralları + deprecation + release prosedürü)
│  │  # (Not: JSON Schema standardı Draft 2020-12 olarak burada da tekilleştirilir)
│  │
│  ├─ canonical/
│  │  # (Amaç: Tek doğru işleyiş dokümanları (v2.4 seti))
│  │
│  │  ├─ README.md
│  │  │  # (Amaç: Kanonik referans sistemi; docx içindeki referansların indeksi)
│  │  │
│  │  ├─ KANONIK_URUN_ISLEYIS_REHBERI_v2_4_.docx
│  │  │  # (Amaç: Rol/akış, veri minimizasyonu, kimlik modeli (phone+PIN), KVKK sınırları)
│  │  │
│  │  ├─ GELISTIRICI_UYGULAMA_PAKETI_v2_4_.docx
│  │  │  # (Amaç: MVP API listesi, kabul kriterleri, PR/CI/Release kapıları, güvenlik checklist’leri)
│  │  │
│  │  └─ SAHA_OPERASYON_SOP_v2_4_.docx
│  │     # (Amaç: Pilot+İstasyon SOP: ingest, karantina, hash/AV, offline süreçler, kanıt zinciri)
│  │
│  ├─ examples/
│  │  # (Amaç: Şemalara birebir uyan örnek JSON’lar; testlerin kaynağı)
│  │
│  │  ├─ README.md
│  │  │  # (Amaç: Örneklerin hangi schema’ya karşılık geldiği ve nasıl validate edileceği)
│  │  │
│  │  ├─ field.example.json
│  │  │  # (Amaç: schemas/core/field.v1.schema.json örnek payload)
│  │  │
│  │  ├─ mission.example.json
│  │  │  # (Amaç: schemas/core/mission.v1.schema.json örnek payload)
│  │  │
│  │  ├─ intake_manifest.example.json
│  │  │  # (Amaç: schemas/edge/intake_manifest.v1.schema.json örnek payload)
│  │  │
│  │  ├─ analysis_job.example.json
│  │  │  # (Amaç: schemas/worker/analysis_job.v1.schema.json örnek payload)
│  │  │
│  │  └─ analysis_result.example.json
│  │     # (Amaç: schemas/worker/analysis_result.v1.schema.json örnek payload)
│  │
│  ├─ migration_guides/
│  │  # (Amaç: Versiyon geçişleri; breaking-change’lerde zorunlu)
│  │
│  │  ├─ README.md
│  │  │  # (Amaç: Migration guide yazım kuralları + checklist)
│  │  │
│  │  ├─ MIGRATION_GUIDE_TEMPLATE.md
│  │  │  # (Amaç: Standart şablon: kapsam, adımlar, örnekler, rollback)
│  │  │
│  │  └─ field_v1_to_v2.md
│  │     # (Amaç: Örnek migration (şablon doğrulama için))
│  │
│  └─ checklists/
│     # (Amaç: SDLC kapıları için yazılı kontrol listeleri)
│
│     ├─ PR_GATE_CHECKLIST.md
│     │  # (Amaç: PR öncesi: validate/tests/breaking-change/forbidden-field guard/version pin)
│     │
│     ├─ CI_GATE_CHECKLIST.md
│     │  # (Amaç: CI’da otomatik koşacak kontroller ve beklenen çıktılar)
│     │
│     └─ RELEASE_GATE_CHECKLIST.md
│        # (Amaç: Yayın öncesi: changelog/migration/semver/consumer sync doğrulaması)
│
├─ tools/
│  # (Amaç: Doğrulama + sürümleme + type üretimi + repo sync otomasyonları)
│
│  ├─ validate.py
│  │  # (Amaç: Tek komutla tüm doğrulamalar)
│  │  # (Kontroller:
│  │  #  - JSON Schema Draft 2020-12 validate (tüm schemas/*.json)
│  │  #  - Policy: object’lerde unevaluatedProperties:false zorunluluğu
│  │  #  - Forbidden-field guard: email/tckn/otp anahtarları/alan adları FAIL
│  │  #  - Enum dosyaları format + benzersizlik + alfabetik/konvansiyon kontrolleri
│  │  #  - OpenAPI lint + schema reference bütünlüğü)
│  │  # (Çıktı: CI uyumlu pass/fail + rapor)
│  │
│  ├─ pin_version.py
│  │  # (Amaç: CONTRACTS_VERSION.md güncelle (semver + sha256) + changelog bağla)
│  │  # (Kural: Breaking-change=true ise major bump zorunlu)
│  │
│  ├─ breaking_change_detector.py
│  │  # (Amaç: Önceki versiyonla şimdiki şemaları diff’leyip breaking-change tespit etmek)
│  │  # (Çıktı: Makine-okur rapor + PR yorum formatı)
│  │
│  ├─ generate_types.sh
│  │  # (Amaç: JSON Schema’dan TS/Python type üretimini tetiklemek)
│  │  # (Kural: Üretilen dosyalar generated/* altında; elle editlenmez)
│  │
│  └─ sync_to_repos.sh
│     # (Amaç: Consumer repo’lara (platform/edge/worker) contracts sync + hash uyumu doğrulama)
│
├─ generated/
│  # (Amaç: Otomatik üretilen tipler; source-of-truth değildir)
│
│  ├─ typescript/
│  │  # (Amaç: TS tipleri)
│  │  ├─ index.d.ts
│  │  │  # (Amaç: TS tiplerinin tek giriş noktası)
│  │  └─ field.d.ts
│  │     # (Amaç: Field tipi; schemas/core/field ile birebir)
│  │
│  └─ python/
│     # (Amaç: Python tipleri)
│     ├─ __init__.py
│     │  # (Amaç: Python package giriş dosyası)
│     └─ field.py
│        # (Amaç: Field modeli; schemas/core/field ile birebir)
│
├─ tests/
│  # (Amaç: Contract repo testleri; CI zorunlu)
│
│  ├─ test_validate_all_schemas.py
│  │  # (Amaç: tools/validate.py tüm şemaları ve policy’leri geçiyor mu?)
│  │
│  ├─ test_examples_match_schemas.py
│  │  # (Amaç: docs/examples/* örnekleri şemalara %100 uyuyor mu?)
│  │
│  └─ test_no_breaking_changes.py
│     # (Amaç: breaking-change detector çıktısı semver ile uyumlu mu?)
│
└─ .github/
   # (Amaç: CI/CD workflow’ları)
   └─ workflows/
      ├─ contract_validation.yml
      │  # (Amaç: Her PR’da: validate + tests + breaking-change + forbidden-field guard + 2020-12 policy)
      │  # (Trigger: Pull request)
      │  # (Steps: 1) Checkout 2) tools/validate.py 3) pytest tests/ 4) raporla)
      │  # (Failure: Fail olursa merge engellenir)
      │
      └─ auto_sync.yml
         # (Amaç: Main’e merge/push sonrası consumer repo’lara sync PR’ı aç)
         # (Trigger: Main branch push)
         # (Steps: 1) tools/sync_to_repos.sh 2) PR oluştur 3) hash/version uyum kontrolü)
         # (İlişki: platform/, edge/, worker/ repo’larının workflow’ları ve CONTRACTS_VERSION pinleme)