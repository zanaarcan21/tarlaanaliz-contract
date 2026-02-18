# Contracts Version Lock

<!-- BOUND:CONTRACTS_VERSION -->

Bu dosya, **tarlaanaliz-contracts** repository'sinin normatif sürüm kilitleme dosyasıdır.

## 📌 Mevcut Versiyon

```yaml
version: 1.0.0
sha256: 67f38af5b8c45712eda35d7d6a64a1a346e464adf4c8aa125b62334e8255731d
created_at: 2026-01-26T10:00:00Z
breaking_change: false
```

## 📋 Versiyon Bilgisi

- **version**: Semantic Versioning (MAJOR.MINOR.PATCH)
- **sha256**: Tüm contract dosyalarının birleşik SHA-256 hash'i
- **created_at**: Versiyonun oluşturulma zamanı (ISO 8601, UTC)
- **breaking_change**: Bu versiyonda breaking change var mı?

## 🔒 Hash Hesaplama

Hash, aşağıdaki dosyaların içeriğinden hesaplanır:

```
schemas/**/*.json
enums/**/*.json
api/**/*.yaml
```

**Hesaplama komutu**:
```bash
python tools/pin_version.py
```

Bu komut:
1. Yukarıdaki tüm dosyaları toplar
2. İçeriklerini birleştirir (deterministic sıralama ile)
3. SHA-256 hash hesaplar
4. Bu dosyayı günceller

## 🎯 SemVer Kuralları

### MAJOR (X.0.0)

Breaking change'ler MAJOR bump gerektirir:

- ✅ Zorunlu alan ekleme (`required` listesine ekleme)
- ✅ Alan tipini değiştirme (`string` → `number`)
- ✅ Enum değeri silme
- ✅ Zorunlu parametreyi değiştirme
- ✅ HTTP metodu değiştirme
- ✅ Endpoint path'i değiştirme
- ✅ Response yapısını değiştirme

**MAJOR bump gereksinimi**:
- Migration guide zorunlu (`docs/migration_guides/`)
- Breaking change flag `true` olmalı
- Consumer repository'ler güncelleme için bilgilendirilmeli

### MINOR (x.Y.0)

Geriye dönük uyumlu yeni özellikler:

- ✅ Opsiyonel alan ekleme
- ✅ Enum'a yeni değer ekleme
- ✅ Yeni endpoint ekleme
- ✅ Response'a opsiyonel alan ekleme

### PATCH (x.y.Z)

Geriye dönük uyumlu düzeltmeler:

- ✅ Dokümantasyon düzeltmesi
- ✅ Örnek güncellemesi
- ✅ Açıklama (description) değişikliği
- ✅ Validasyon constraint'i gevşetme

## 🔄 Consumer Repository Kullanımı

### 1. Pin'leme

Consumer repository kendi `CONTRACTS_VERSION.md` dosyasını oluşturur:

```bash
# tarlaanaliz-platform/CONTRACTS_VERSION.md
version: 1.0.0
sha256: a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
created_at: 2026-01-26T10:00:00Z
breaking_change: false
```

### 2. CI Doğrulama

Consumer'ın CI'sında hash kontrolü:

```yaml
name: Verify Contracts

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true  # contracts submodule

      - name: Verify contracts hash
        run: |
          cd contracts/
          EXPECTED_HASH=$(grep "^sha256:" ../CONTRACTS_VERSION.md | cut -d' ' -f2)
          ACTUAL_HASH=$(find schemas enums api -type f \( -name "*.json" -o -name "*.yaml" \) \
            -exec sha256sum {} \; | sort | sha256sum | cut -d' ' -f1)
          
          if [ "$EXPECTED_HASH" != "$ACTUAL_HASH" ]; then
            echo "ERROR: Contract hash mismatch!"
            echo "Expected: $EXPECTED_HASH"
            echo "Actual: $ACTUAL_HASH"
            exit 1
          fi
```

### 3. Güncelleme

Consumer güncelleme adımları:

1. **Yeni versiyonu incele**:
   ```bash
   cd contracts/
   git fetch
   git log HEAD..origin/main
   ```

2. **Breaking change kontrolü**:
   ```bash
   grep "breaking_change: true" CONTRACTS_VERSION.md
   ```

3. **Migration guide oku** (breaking change varsa):
   ```bash
   cat docs/migration_guides/field_v1_to_v2.md
   ```

4. **Pin'i güncelle**:
   ```bash
   cd contracts/
   git checkout v2.0.0
   cd ..
   cp contracts/CONTRACTS_VERSION.md .
   ```

5. **Kodu güncelle** (migration guide'a göre)

6. **Test**:
   ```bash
   npm run types:gen  # veya python -m tools.generate_types
   npm test
   ```

## 📊 Versiyon Geçmişi

| Versiyon | Tarih | Breaking | Açıklama |
|----------|-------|----------|----------|
| 1.0.0 | 2026-01-26 | No | Initial release |

Detaylı değişiklikler için [CHANGELOG.md](CHANGELOG.md) dosyasına bakın.

## 🛠️ Tooling

### Hash Güncelleme

```bash
# Contract repo'da
python tools/pin_version.py

# Output:
# ✓ Version: 1.0.0
# ✓ SHA-256: a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
# ✓ CONTRACTS_VERSION.md updated
```

### Breaking Change Detection

```bash
# Previous version ile compare
python tools/breaking_change_detector.py --from v0.9.0 --to HEAD

# Output:
# ⚠ BREAKING CHANGES DETECTED:
#   - schemas/core/field.v1.schema.json: Added required field 'crop_type'
#   - enums/mission_status.enum.v1.json: Removed value 'DEPRECATED_STATUS'
# 
# ACTION REQUIRED:
#   1. Bump MAJOR version
#   2. Create migration guide
#   3. Set breaking_change: true
```

## 🚨 Kritik Kurallar

### ❌ Yapılmaması Gerekenler

1. **Manuel hash düzenleme** — Hash her zaman `tools/pin_version.py` ile üretilmeli
2. **Breaking change'siz MAJOR bump** — MAJOR her zaman migration guide gerektirir
3. **Hash kontrolü olmadan deploy** — CI'da hash kontrolü zorunlu
4. **Consumer'a zorla push** — Consumer'lar kendi zamanlarında update eder

### ✅ Yapılması Gerekenler

1. **Breaking change'de MAJOR bump** — SemVer kurallarına uy
2. **Migration guide yaz** — Breaking change varsa detaylı rehber
3. **Consumer'ları bilgilendir** — GitHub release + Slack/email
4. **Hash'i doğrula** — Her release öncesi `tools/pin_version.py` çalıştır

## 📞 Destek

- **Hash mismatch**: Contracts submodule'ü güncelleyin veya pin'i kontrol edin
- **Breaking change**: Migration guide'a bakın (`docs/migration_guides/`)
- **Version conflict**: Consumer repo owner'ı ile iletişime geçin

---

**Not**: Bu dosya `tools/pin_version.py` tarafından otomatik güncellenir.  
Manuel düzenleme yapılmamalıdır.

**Son Güncelleme**: 2026-01-26  
**Standart**: JSON Schema Draft 2020-12
