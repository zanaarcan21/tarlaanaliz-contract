# Contract Audit Report — 2026-02-20
<!-- BOUND:AUDIT_REPORT -->

## A) Executive Summary
1. Envanter tamamlandı: hedef kapsamda 76 izlenen dosya tarandı (`schemas/enums/api/tools/tests/docs/ssot/.github/workflows`).
2. JSON Schema dosyaları Draft 2020-12 açısından mevcut gate’lerde geçiyor; örnek JSON testleri de geçiyor.
3. CI’de breaking-change tespiti çalışıyor ama **gate etmiyor** (sadece warning) → KR-041 ile uyumsuz.
4. CI’de checksum doğrulaması **continue-on-error** ve “No version pinned yet” ile geçilebiliyor → KR-041 ile uyumsuz.
5. CI tetik yolları `enums/`, `docs/`, `ssot/`, `CONTRACTS_VERSION.md` değişimlerini kapsamıyor; kritik sözleşme materyali gate dışı kalabiliyor.
6. OpenAPI lint adımı fail üretmiyor (`continue-on-error: true` + `|| echo`) ve özet job’una bağlanmıyor.
7. Forbidden-field kontrolü workflow’da sadece `schemas/` dizininde; örnek JSON/OpenAPI için aynı CI guard yok.
8. Repo dokümantasyonu “tüm object tiplerinde `unevaluatedProperties:false`” diyor; ancak birden fazla şemada nested object alanları bu zorunluluğu taşımıyor.
9. SSOT/KR referansları mevcut; ancak uygulanan CI davranışı özellikle KR-041 zorunluluklarını hard gate seviyesinde tamamlamıyor.

## B) BULGULAR

| Severity | Alan | Dosya | Kanıt (snippet) | KR Ref | Öneri |
|---|---|---|---|---|---|
| BLOCKER | CI Gate / Breaking Change | `.github/workflows/contract_validation.yml` | `continue-on-error: true` + `# Don't fail - just warn` | KR-041 | Breaking change varsa job `exit 1` ile fail etmeli.
| BLOCKER | CI Gate / Checksum | `.github/workflows/contract_validation.yml` | `python3 tools/pin_version.py --verify || echo "No version pinned yet"` + `continue-on-error: true` | KR-041 | Checksum doğrulaması zorunlu fail gate olmalı; bypass kaldırılmalı.
| MAJOR | CI Trigger Coverage | `.github/workflows/contract_validation.yml` | `paths:` altında `schemas/**`, `api/**`, `tools/**`, `tests/**`; `enums/**`, `docs/**`, `ssot/**`, `CONTRACTS_VERSION.md` yok | KR-041, KR-081 | Tetik yollarına eksik contract materyalleri eklenmeli.
| MAJOR | OpenAPI Gate Etkisiz | `.github/workflows/contract_validation.yml` | `npm install -g @stoplight/spectral-cli` adımı npm policy E403 ile kırılabiliyor | KR-081 | Lint adımı fail koşuluna bağlanmalı, summary needs listesine eklenmeli.
| MAJOR | Forbidden Field Coverage | `.github/workflows/contract_validation.yml` | `grep ... schemas/` (yalnızca schemas) | KR-050, KR-081 | `api/` ve `docs/examples/*.json` için de aynı guard uygulanmalı.
| MAJOR | Contract Strictness Gap | `docs/checklists/PR_GATE_CHECKLIST.md` + `schemas/**` | Doküman: “All object types have unevaluatedProperties:false”; şemalarda nested object örn. `properties/metadata` bloklarında alan yok | KR-081 | Recursive schema lint eklenmeli; nested object’lerde açık karar (false ya da bilinçli istisna) netleştirilmeli.
| MINOR | Dokümantasyon Yapı Tutarsızlığı | `docs/README.md` | Ağaçta `schemas/enums/` gösteriliyor; repo’da enum dosyaları kökte `enums/` altında | KR-081 | docs/README dizin ağacı güncellenmeli.

## C) KR/SSOT Uyum Matrisi (Contracts kapsamı)

| KR | Repo karşılığı | Test/Gate var mı? | Durum |
|---|---|---|---|
| KR-017 | `schemas/worker/analysis_job.v1.schema.json`, `api/platform_internal.v1.yaml` | Kısmi (schema/example testleri) | Kısmi uyum (CI hard gate eksikleri mevcut) |
| KR-018 / KR-082 | `schemas/platform/calibration_result.v1.schema.json`, `schemas/platform/qc_report.v1.schema.json` | Kısmi | Kısmi uyum |
| KR-041 | `CONTRACTS_VERSION.md`, `tools/pin_version.py`, `tools/breaking_change_detector.py`, workflow | Var ama yumuşak gate | UYUMSUZ (hard fail eksik) |
| KR-050 | Forbidden-field testleri + schema açıklamaları | Var | Kısmi uyum (workflow kapsamı dar) |
| KR-070/071/072/073 | `intake_manifest`, `quarantine_event`, event/result şemaları | Kısmi | Kısmi uyum |
| KR-081 | JSON Schema + OpenAPI + testler | Var | Kısmi uyum (recursive strictness ve CI enforcement eksik) |

## D) Önerilen Patch’ler (unified diff)

```diff
diff --git a/.github/workflows/contract_validation.yml b/.github/workflows/contract_validation.yml
@@
   pull_request:
     branches: [main, develop]
     paths:
       - 'schemas/**'
+      - 'enums/**'
       - 'api/**'
+      - 'docs/**'
+      - 'ssot/**'
+      - 'CONTRACTS_VERSION.md'
       - 'tools/**'
       - 'tests/**'
       - '.github/workflows/contract_validation.yml'
@@
   push:
     branches: [main]
     paths:
       - 'schemas/**'
+      - 'enums/**'
       - 'api/**'
+      - 'docs/**'
+      - 'ssot/**'
+      - 'CONTRACTS_VERSION.md'
@@
       - name: Check breaking changes
         if: steps.breaking.outputs.has_breaking == 'true'
         run: |
-          echo "::warning::Breaking changes detected! This PR requires MAJOR version bump."
-          echo "::warning::Please ensure this is intentional and coordinated with consumers."
-          # Don't fail - just warn
+          echo "::error::Breaking changes detected! MAJOR version bump and approval required."
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
-          npm install --include=dev --no-fund --no-audit
+
+      - name: Lint OpenAPI specs
+        run: |
+          npm run openapi:validate
+        continue-on-error: true
@@
       - name: Check for email/tckn/otp
         run: |
@@
-          if grep -r -i -E "\"($FORBIDDEN)\"" schemas/; then
+          if grep -r -i -E "\"($FORBIDDEN)\"" schemas/ docs/examples/ api/components/; then
             echo "::error::Forbidden fields found in schemas!"
@@
   summary:
@@
-    needs: [validate-schemas, test-schemas, detect-breaking-changes, check-forbidden-fields, check-draft-2020-12]
+    needs: [validate-schemas, test-schemas, detect-breaking-changes, verify-checksums, lint-openapi, check-forbidden-fields, check-draft-2020-12]
@@
           needs.check-forbidden-fields.result == 'failure' ||
-          needs.check-draft-2020-12.result == 'failure'
+          needs.check-draft-2020-12.result == 'failure' ||
+          needs.verify-checksums.result == 'failure' ||
+          needs.lint-openapi.result == 'failure'
```

## E) Risk kalır mı?

Evet. Önerilen patch’ler uygulanmadan mevcut durumda şu artık riskler sürer: (i) breaking değişikliklerin main’e yumuşak uyarıyla girmesi, (ii) checksum pin bypass, (iii) workflow trigger kapsamı dışında kalan contract materyali değişiklikleri, (iv) nested object strictness boşlukları nedeniyle sözleşme dışı alanların üretim ortamına sızma riski.
