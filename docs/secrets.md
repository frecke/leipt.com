# Secrets: age + GitHub CLI

age encrypts the local copy; GitHub environment secrets supply the manual preview deployment. Ordinary builds need no credentials or private keys. No secrets are provisioned by setup or CI.

## Key and encrypted file

Use an existing age identity or create a dedicated one outside this repository:

```sh
mkdir -p "$HOME/.config/age"
(umask 077; age-keygen -o "$HOME/.config/age/leipt-com.agekey")
export AGE_IDENTITY="$HOME/.config/age/leipt-com.agekey"
export AGE_RECIPIENT="$(age-keygen -y "$AGE_IDENTITY")"
```

Back up the private identity securely. Never commit or upload it to GitHub. Only the public recipient is needed for encryption. For an existing identity, set `AGE_IDENTITY` to its path and derive `AGE_RECIPIENT` as above. These variables are not loaded automatically into build commands.

Copy `.env.example` to the ignored `.env.onecom-preview`, restrict it with `chmod 600 .env.onecom-preview`, and fill it locally. Use dotenv quoting for values containing spaces or special characters, including the verified known-hosts line. Encrypt it:

```sh
just secrets-encrypt < .env.onecom-preview
```

This writes `secrets/onecom-preview.env.age`. Only ciphertext may be committed; review filenames and diffs before staging. Re-encrypt after editing values. Keep or remove the ignored plaintext source according to your local policy; the tooling does not delete it. Do not paste secret values into shell commands.

## Publish to GitHub

First complete the hosting inventory and environment setup in [deployment.md](deployment.md). Authenticate with `gh auth login`, then:

```sh
just secrets-sync
just secrets-list
```

Sync decrypts the entire file in memory before passing it to `gh secret set --env-file -`, explicitly scoped to `frecke/leipt.com` and `onecom-preview`. It writes no decrypted file and does not print values. A failed decryption prevents any GitHub call. GitHub updates are per secret: if an upload fails midway, rerun the sync. Removing a key from the file does not delete an existing GitHub secret.

Sync publishes credentials only; it does not trigger deployment. CI consumes GitHub secrets directly and never needs the age private key.
