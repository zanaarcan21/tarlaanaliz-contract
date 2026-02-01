# Yeni eklenen dosyalar (KR-082)

Bu paket, contracts repo'na **yeni eklenen** 3 adet JSON Schema dosyasını içerir:

- `schemas/platform/calibrated_dataset_manifest.v1.schema.json`
- `schemas/platform/calibration_result.v1.schema.json`
- `schemas/platform/qc_report.v1.schema.json`

## Yerel repoya ekleme (Windows PowerShell)

1) Repo köküne gir:
```powershell
cd C:\path\to\tarlaanaliz-contracts
```

2) Bu zip'i aç ve içindeki `tarlaanaliz-contracts\schemas\platform\` altındaki 3 dosyayı
senin repodaki `schemas\platform\` klasörüne kopyala.

Alternatif: zip'i repo kökünde açarsan, klasör yapısı otomatik oturur.

3) Doğrula:
```powershell
git status
```

4) Commit + push:
```powershell
git add schemas/platform/*.schema.json
git commit -m "Add KR-082 calibration/QC platform schemas (v1)"
git push
```

## Notlar
- JSON Schema standardı: Draft 2020-12
- `unevaluatedProperties:false` ile schema dışı alan sızıntısı engellenir.
- PII (kişisel veri) içermez.
