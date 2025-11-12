# TODO: Fix Diagnostic Errors in cd.yml and Apply-Branch-Protection.ps1

## Steps to Complete

- [x] Edit `gravity-template-service/.github/workflows/cd.yml`:
  - [x] Replace `actions/create-release@v1` with `softprops/action-gh-release@v1`
  - [x] Change `release_name` to `name`
  - [x] Move `GITHUB_TOKEN` from `env` to `with` as `token`

- [x] Edit `scripts/Apply-Branch-Protection.ps1`:
  - [x] Remove assignment to `$ghStatus`
  - [x] Remove assignment to `$repoCheck`
  - [x] Remove assignment to `$apiResult`

- [ ] Verify workflow runs correctly after changes
- [ ] Test PowerShell script for runtime issues
