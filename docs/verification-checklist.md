# Pre-Deploy Verification Checklist

**What**: Complete verification process before deploying crm-admin-stability changes.  
**Who**: Maintainers preparing a production release.  
**When**: After all PRs are merged, before deploying to production.  
**Time**: ~5-10 minutes (automated) + manual checks.

## Quick Path

```bash
# Run all automated checks
./scripts/verify-all.sh

# If exit 0 → deploy. If exit ≠ 0 → see "When Something Fails" below.
```

## What Gets Verified

| Suite | Command | Success Criteria | Duration |
|-------|---------|------------------|----------|
| Backend tests | `cd backend && make test-db-up && poetry run pytest --cov=app --cov-fail-under=60` | All tests pass, coverage ≥60% | ~30s |
| Frontend unit tests | `cd frontend && pnpm vitest run` | 72 tests pass (7 files) | ~7s |
| Frontend type check | `cd frontend && pnpm astro check` | 0 errors (4 pre-existing image_url errors are non-blocking) | ~5s |
| Smoke tests | 8 endpoints via curl | All return HTTP 200 | ~10s |

**Total automated time**: ~52 seconds

## Manual Checks (Before Automated)

- [ ] All 4 PRs merged to main (slice-1-backend, slice-2-frontend, slice-3-proxy, slice-4-process)
- [ ] No uncommitted changes in working directory
- [ ] Docker daemon running (for test DB)
- [ ] Network access to api.elrincondeharco.com (for smoke tests)

## Step-by-Step Process

### 1. Prepare Environment

```bash
# Ensure you're on main with all slices merged
git checkout main
git pull origin main

# Verify Docker is running
docker ps

# Install dependencies (if needed)
cd backend && poetry install
cd ../frontend && pnpm install
cd ..
```

### 2. Run Automated Verification

```bash
./scripts/verify-all.sh
```

**Expected output**:
```
[PASS] Backend tests passed (coverage ≥60%)
[PASS] Frontend unit tests passed
[PASS] Type check passed (or warning about 4 pre-existing errors)
[PASS] Smoke tests passed (8/8 endpoints)
[PASS] Verification complete: 4 suites passed
```

### 3. Verify Coverage Report (Optional)

```bash
cd backend
poetry run pytest --cov=app --cov-report=html
open htmlcov/index.html
```

**Target**: ≥60% coverage (current: 63.36%)

### 4. Manual Smoke Test (Optional)

Open in browser:
- https://www.rincom.es/admin (dashboard loads with 8 cards)
- https://api.elrincondeharco.com/docs (Swagger UI)

### 5. Deploy

If all checks pass → proceed with deployment.

## The 8 Dashboard Endpoints

These endpoints are smoke-tested by `verify-all.sh`:

| # | Endpoint | Purpose | Expected Status |
|---|----------|---------|-----------------|
| 1 | `/api/v1/projects/` | List all projects | 200 |
| 2 | `/api/v1/sectors/` | List all sectors | 200 |
| 3 | `/api/v1/testimonials/all` | List all testimonials | 200 |
| 4 | `/api/v1/showrooms/` | List all showrooms | 200 |
| 5 | `/api/v1/stacks/` | List all tech stacks | 200 |
| 6 | `/api/v1/heroes/latest/` | Latest hero content | 200 |
| 7 | `/api/v1/abouts/latest/` | Latest about content | 200 |
| 8 | `/api/v1/experience/latest/` | Latest experience content | 200 |

**Note**: `/api/v1/testimonials/all` has NO trailing slash (bug-1 fix: trailing slash triggers 307 → mixed content).

## When Something Fails

### Backend Tests Fail

**Symptom**: `pytest` exits with non-zero status or coverage <60%.

**Diagnosis**:
```bash
cd backend
make test-db-up  # Ensure test DB is running
poetry run pytest -v  # Verbose output
```

**Common causes**:
- Test DB not running → `make test-db-up`
- Missing dependencies → `poetry install`
- Test regression → check recent commits

**Fix**: Re-run failed tests locally, fix code, commit, re-verify.

### Frontend Tests Fail

**Symptom**: `vitest run` exits with non-zero status.

**Diagnosis**:
```bash
cd frontend
pnpm vitest run --reporter=verbose
```

**Common causes**:
- Missing dependencies → `pnpm install`
- Test regression → check recent commits
- Environment issue → clear node_modules: `rm -rf node_modules && pnpm install`

**Fix**: Re-run failed tests locally, fix code, commit, re-verify.

### Type Check Fails (Unexpected Errors)

**Symptom**: `astro check` reports errors beyond the 4 known image_url errors.

**Diagnosis**:
```bash
cd frontend
pnpm astro check 2>&1 | grep "error"
```

**Known non-blocking errors** (safe to ignore):
- `src/components/sections/Projects.astro:29` — image_url vs image_urls
- `src/components/sections/Projects.astro:30` — image_url vs image_urls
- `src/components/ui/ProjectCard.astro:46` — image_url vs image_urls
- `src/components/ui/ProjectCard.astro:50` — image_url vs image_urls

**If OTHER errors appear**: Fix them before deploying.

### Smoke Tests Fail

**Symptom**: One or more endpoints return non-200 status.

**Diagnosis**:
```bash
# Test individual endpoint
curl -I https://api.elrincondeharco.com/api/v1/projects/

# Test all 8 endpoints
for ep in projects sectors testimonials/all showrooms stacks heroes/latest abouts/latest experience/latest; do
  echo -n "$ep: "
  curl -s -L -o /dev/null -w "%{http_code}" "https://api.elrincondeharco.com/api/v1/$ep/"
  echo
done
```

**Common causes**:
- Backend down → check backend deployment
- Network issue → retry in 30 seconds
- Endpoint renamed → check dashboard.ts for canonical URLs

**Fix**: Verify backend is running, check logs, retry.

## Regression Map

Each of the 5 original bugs has corresponding tests:

| Bug | Test File(s) | What It Catches |
|-----|--------------|-----------------|
| 1. /testimonials/all/ 307→http mixed content | `backend/tests/test_api.py` (TestPublicTestimonialsAPI), `frontend/tests/lib/dashboard.test.ts` | Trailing slash redirect trap |
| 2. Drag-drop navigates to file:/// | `frontend/tests/lib/uploads.test.ts`, `frontend/tests/e2e/drop-guard.spec.ts` (skipped) | DataTransfer file filtering |
| 3. 401 on writes (cookie cross-domain) | `frontend/tests/lib/config.test.ts`, `backend/tests/conftest.py` (admin_override) | credentials:include assertion |
| 4. Proxy strips trailing slash → 422/405 | `frontend/tests/lib/api-proxy.test.ts` | Slash/query/cookie preservation |
| 5. 422 with single image upload | `backend/tests/test_api.py` (TestProjectsUploadAPI) | 1/N/0 file upload scenarios |

## Post-Deployment Verification

After deploying to production:

- [ ] Visit https://www.rincom.es/admin → dashboard loads with 8 cards
- [ ] Create/edit a project → image upload works (1 file, multiple files)
- [ ] Drag-drop images on project editor → no file:// navigation
- [ ] Check browser console → no 401/422/405 errors
- [ ] Verify testimonials load → no mixed content warnings

## Rollback Plan

If production issues arise:

```bash
# Revert the merge commit
git revert -m 1 <merge-commit-hash>
git push origin main

# Redeploy
```

**Rollback scope**: All test infrastructure is additive. Helper extraction (dashboard.ts, uploads.ts, fetch-interceptor.ts) is behavior-neutral — revert restores inline logic.

## References

- **Automated script**: `scripts/verify-all.sh`
- **Backend tests**: `backend/tests/test_api.py`, `backend/tests/conftest.py`
- **Frontend tests**: `frontend/tests/lib/*.test.ts`
- **Design decisions**: See SDD design artifact (D1-D8)
- **Spec requirements**: REQ-TESTDB, REQ-AUTH-TESTS, REQ-IMG-UPLOAD, REQ-SLASH-API, REQ-PROXY, REQ-TS-EXTRACTION, REQ-VERIFY, REQ-REGRESSION-MAP
