# one.com deployment plan

## Current state

The existing one.com webspace has **not yet been inventoried**. A read-only control-panel check on 2026-10-05 showed the `leipt.com` **Beginner** plan, SFTP enabled, and SSH unavailable. The SFTP connection details are available in the control panel; keep credentials out of this repository. The browser then reported an IP block, so File Manager, DNS, and Security & Compliance were not inspected. Public one.com documentation says SFTP starts in the public `httpd.www` folder, while SSH documentation calls the public folder `/www`; use the account's actual paths, not an assumed mapping. No deployment should run before checking the account.

## Read-only inventory first

In the one.com control panel, record the active site/webspace, domain mapping, hosting plan, SFTP host and username, and which directories and files occupy the public root. Do not expose credentials in issues, logs, or screenshots. Identify any WordPress/CMS installation and its database before contemplating a root change. Make a backup using one.com's supported method and verify it can be retrieved.

## Isolated preview

1. After the inventory, create a new empty `leipt-preview` directory directly under the SFTP login's public starting folder. Confirm it does not already hold unrelated content.
2. Put a file named `.leipt-deploy-root` in that directory containing exactly `leipt-preview-v1` and a newline. This marker is required by the deployment script; it is not created by CI.
3. In GitHub, create a `onecom-preview` environment and optionally restrict it to `main` and require a reviewer. Add environment secrets: `ONECOM_SFTP_HOST`, `ONECOM_SFTP_PORT` (usually `22`), `ONECOM_SFTP_USER`, `ONECOM_SFTP_PASSWORD`, and `ONECOM_SFTP_KNOWN_HOSTS` (an OpenSSH known-hosts line verified out of band).
4. Run the manual **Deploy one.com preview** workflow on `main`. It builds with a preview base URL and uploads only files from `public/` into the marked directory. It does not remove remote files.
5. Check the preview in a browser and compare it against the intended content. Keep the preview out of search results until launch.

The workflow's target is hardcoded as `leipt-preview` and rejects a missing or mismatched marker. It uses strict host-key checking. The generated preview includes `noindex`; canonical production metadata is reserved for the eventual root deployment.

## Production cutover, later

The canonical site belongs at `https://leipt.com/`, but publishing there could overwrite existing root files or routes. First map the exact path ownership and choose a migration strategy for the current site and other content. Review a file-level diff, preserve existing content and `/.well-known`, and take a verified backup. Add a separate production deployment procedure only after that plan is agreed. Do not point a generic mirror or `rsync --delete` at `/www`.
