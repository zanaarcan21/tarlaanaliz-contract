# TarlaAnaliz – Geliştirici ve Uygulama Paketi (Contracts)
**Sürüm:** v2.6 Master (split) | **Tarih:** 2026-02-02

**Normatif kaynak:** `ssot/kr_registry.md` + bileşen SSOT görünümleri.

> Bu dosya seti **kural yazmaz**; SSOT’taki KR’lerin her bileşende **nasıl uygulanacağını** anlatır.
> Çelişki halinde SSOT kazanır.

## Kapsam

- Contracts (schema/API sözleşmeleri) ve breaking-change yönetimi.
- Normatif KR metinleri: `ssot/contracts_ssot.md` ve `ssot/kr_registry.md`.

## 7. Temel API Endpoint'leri (MVP)

**Not:** Kimlik modeli tüm kullanıcılar için aynı - **telefon + 6 haneli PIN** (e-posta YOK)

| Metot | Endpoint | Yetki | Açıklama |
|-------|----------|-------|----------|
| GET | /auth/me | Tümü | Profil + rol listesi |
| POST | /auth/register | Anonim | Kayıt: telefon + PIN |
| POST | /auth/login | Anonim | Giriş: telefon + PIN |
| POST | /fields | FARMER_*/COOP_* | Tarla oluştur |
| POST | /missions | FARMER_*/COOP_* | Analiz talebi |
| GET | /missions?scope=mine | Yetkili | Rol bazlı görev listesi |
| GET | /pilot/payroll/preview | PILOT | Hakediş önizleme |

---

# BÖLÜM C: Güvenlik Katmanları


## EK-1) SSOT Kanonik Tarif (Kopyala–Yapıştır)


## Contracts Versiyonlama Kuralları (şablon)

- Schema değişiklikleri “breaking” ise: yeni `vN` şeması eklenir, eskisi deprecation sürecine girer.
- Platform/Worker/Edge uyumluluğu: `kr_registry` üzerinden hangi KR’nin hangi schema alanına dayandığı belirtilir.
- Her schema için:
  - Amaç
  - Zorunlu alanlar
  - Güvenlik (PII/secret) notları
  - Uyum testleri (contract validation)

> Not: Bu bölüm uygulama kılavuzudur; normatif alan tanımları contracts repo şemalarındadır.
