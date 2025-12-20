# SignPath Code Signing Setup - TODO

## Status: ⏳ Waiting for Approval

**Applied:** December 20, 2025
**Email sent to:** oss-support@signpath.org
**Expected response:** 1-3 business days

---

## When Approved, Do These Steps:

### Step 1: Get Credentials
- [ ] Log in to https://app.signpath.io
- [ ] Note your **Organization ID**
- [ ] Generate an **API Token**

### Step 2: Install GitHub App
- [ ] Go to https://github.com/apps/signpath-io
- [ ] Install on `bokiko/pingdiff` repository

### Step 3: Add Secret to GitHub
```bash
gh secret set SIGNPATH_API_TOKEN
# Paste the API token when prompted
```

### Step 4: Update Workflow
Edit `.github/workflows/build-windows.yml`:
1. Uncomment the SignPath signing steps (lines 71-89)
2. Replace `YOUR_ORG_ID` with your actual Organization ID
3. Commit and push

### Step 5: Test
- Create a new tag: `git tag v1.10.1 && git push origin v1.10.1`
- Check GitHub Actions for successful signing
- Download and verify the installer is signed

---

## Why This Matters
- ✅ Removes Windows SmartScreen warning
- ✅ Users can install without "Unknown publisher" message
- ✅ Builds trust with users

---

## Files Modified for SignPath
- `.github/workflows/build-windows.yml` - Signing steps added (commented out)

## Contact
SignPath Support: oss-support@signpath.org
