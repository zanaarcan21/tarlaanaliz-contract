# Contract Audit Report — 2026-02-20

<!-- BOUND:AUDIT_2026_02_20 -->

## A) Executive Summary
1. Kapsamda istenen dizinlerde toplam **80 dosya** tarandı (`schemas, enums, api, tools, tests, docs, ssot, .github/workflows`).
2. Schema testleri ve validator lokal ortamda geçti (`pytest`, `tools/validate.py`).
3. CI gate akışında bazı kontroller **uyarıya düşürülmüş** durumda; fail-fast gate davranışı zayıf.
4. Breaking-change denetimi PR’da çalışıyor ama sonucu bloklamıyor (`continue-on-error: true` + warning only).
5. Checksum doğrulaması gate’i başarısız olduğunda pipeline’ı durdurmuyor.
6. OpenAPI lint adımı fail üretmiyor (hem `|| echo` hem `continue-on-error: true`).
7. Draft 2020-12 kontrolü yalnız `schemas/` altında; `enums/` kapsam dışı.
8. `enums/user_role.enum.v1.json` Draft-07 kullanıyor; Draft 2020-12 standardıyla çelişkili.
9. Forbidden-field gate sadece `schemas/` tarıyor; `api/` ve örnek içerik tarama dışında.
10. OpenAPI metadata’da `contact.email` alanı mevcut; KR-050 hassasiyeti açısından gri alan/ihlal riski.
11. SSOT/KR kanonik eşleştirme için repo içindeki `ssot/kr_registry.md` mevcut, fakat kullanıcı girdisindeki `TARLAANALIZ_SSOT...txt` ve `IS_PLANI_AKIS...docx` dosyaları repoda bulunmadı.

## B) BULGULAR

| severity | alan | dosya | kanıt | öneri |
|---|---|---|---|---|
| BLOCKER | CI Gate / Breaking | `.github/workflows/contract_validation.yml` | `detect-breaking-changes` adımında `continue-on-error: true`; sonra sadece `::warning` basılıyor. | Breaking tespitinde job `exit 1` ile fail olmalı (KR-041 / KR-081). |
| BLOCKER | CI Trigger Kapsamı | `.github/workflows/contract_validation.yml` | Trigger path’lerinde `enums/**`, `docs/examples/**`, `ssot/**`, `.github/workflows/**` (diğer workflow) yok. | Trigger kapsamı contract etkili tüm dizinleri içerecek şekilde genişletilmeli. |
| MAJOR | Draft 2020-12 uyumu | `enums/user_role.enum.v1.json` | `$schema: "http://json-schema.org/draft-07/schema#"`. | Draft 2020-12’ye yükseltilmeli ve CI denetimi `enums/`u da kapsamalı. |
| MAJOR | Checksum Gate | `.github/workflows/contract_validation.yml` | `python3 tools/pin_version.py --verify || echo ...` + `continue-on-error: true`. | Checksum verify başarısızlığında pipeline fail etmeli (KR-041). |
| MAJOR | OpenAPI Gate | `.github/workflows/contract_validation.yml` | `spectral lint ... || echo ...` + `continue-on-error: true`. | Lint sonucu gate’i bloklamalı; en azından warn değil fail-severity uygulanmalı. |
| MAJOR | Forbidden fields kapsamı | `.github/workflows/contract_validation.yml` | `grep ... schemas/` sadece schema tarıyor. | `api/**/*.yaml`, `docs/examples/*.json` ve gerekirse `enums/` da taranmalı. |
| MAJOR | KR-050 riski (PII) | `api/platform_public.v1.yaml` | `info.contact.email` alanı mevcut. | KR-050 yorumu kurum kanonuna göre netleştirilmeli; izin yoksa `email` anahtarı kaldırılmalı/değiştirilmeli. |
| MINOR | SSOT kaynak tamlığı | repo kökü | Kullanıcı girdisindeki `TARLAANALIZ_SSOT...txt` ve `IS_PLANI_AKIS...docx` bulunamadı. | Tam kanonik kıyas için bu artefaktlar repoya eklenmeli veya audit’e sağlanmalı. |
| NIT | Enum tekilleştirme | `enums/user_role.enum.v1.json`, `enums/role.enum.v1.json` | Benzer role enumları birlikte duruyor; referanslar `role.enum.v1.json`a gidiyor. | Kullanılmayan enum için deprecation/temizlik planı çıkarılmalı. |

## C) KR/SSOT Uyum Matrisi (özet)

| KR | Repo karşılığı | Test/Gate var mı? | Durum |
|---|---|---|---|
| KR-081 | `schemas/`, `api/`, `tools/validate.py`, `tests/` | Var (`pytest`, schema validator, workflow) | **Kısmi uyum** (gate’lerin bir kısmı non-blocking) |
| KR-041 | `tools/pin_version.py`, `tools/breaking_change_detector.py`, workflow | Var | **Kısmi uyum** (breaking/checksum fail-blocking değil) |
| KR-050 | `schemas/core/user*.json`, forbidden-field testleri | Var | **Kısmi uyum** (`api/` taraması gate’de yok; `contact.email` riski) |
| KR-018 / KR-082 | Calibration/QC şemaları + manifest şemaları | Var (schema/tests seviyesinde) | Uyumlu (kritik çelişki tespit edilmedi) |
| KR-033 | Payment şemaları/enums (`payment_*`) | Var | Uyumlu (bu auditte blocker yok) |

## D) Önerilen Patch’ler (uygulanmadı)

```diff
diff --git a/.github/workflows/contract_validation.yml b/.github/workflows/contract_validation.yml
@@
 on:
   pull_request:
     branches: [main, develop]
     paths:
       - 'schemas/**'
+      - 'enums/**'
       - 'api/**'
+      - 'docs/examples/**'
+      - 'ssot/**'
       - 'tools/**'
       - 'tests/**'
-      - '.github/workflows/contract_validation.yml'
+      - '.github/workflows/**'
@@
-      - name: Detect breaking changes
+      - name: Detect breaking changes
@@
-        continue-on-error: true
+        continue-on-error: false
@@
       - name: Check breaking changes
         if: steps.breaking.outputs.has_breaking == 'true'
         run: |
-          echo "::warning::Breaking changes detected! This PR requires MAJOR version bump."
-          echo "::warning::Please ensure this is intentional and coordinated with consumers."
-          # Don't fail - just warn
+          echo "::error::Breaking changes detected! MAJOR bump + migration artifacts required."
+          exit 1
@@
       - name: Verify checksums
         run: |
-          python3 tools/pin_version.py --verify || echo "No version pinned yet"
-        continue-on-error: true
+          python3 tools/pin_version.py --verify
@@
       - name: Lint OpenAPI specs
         run: |
-          spectral lint api/**/*.yaml --fail-severity=warn || echo "OpenAPI linting completed"
-        continue-on-error: true
+          spectral lint api/**/*.yaml --fail-severity=warn
@@
-          INVALID=$(find schemas -name "*.json" -exec grep -L "draft/2020-12" {} \;)
+          INVALID=$(find schemas enums -name "*.json" -exec grep -L "draft/2020-12" {} \;)
@@
-          if grep -r -i -E "\"($FORBIDDEN)\"" schemas/; then
+          if grep -r -i -E "\"($FORBIDDEN)\"" schemas/ api/ docs/examples/; then
             echo "::error::Forbidden fields found in schemas!"
             echo "::error::Per KR-050: NO email, NO TCKN, NO OTP allowed"
             exit 1
           fi
```

```diff
diff --git a/enums/user_role.enum.v1.json b/enums/user_role.enum.v1.json
@@
-  "$schema": "http://json-schema.org/draft-07/schema#",
+  "$schema": "https://json-schema.org/draft/2020-12/schema",
+  "$id": "https://api.tarlaanaliz.com/enums/user_role.enum.v1.json",
```

## E) Risk kalır mı?
- Evet. Özellikle breaking-change/checksum/openapi gate’lerinin non-blocking kalması durumunda KR-041/KR-081 için üretim öncesi kaçak riski sürer.
