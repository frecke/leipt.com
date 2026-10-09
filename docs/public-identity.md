# Public identity files

The contact page links to `static/foaf.ttl`, which Hugo copies to `/foaf.ttl`. The HTML head advertises it as Turtle. Keep the FOAF and schema.org Person records limited to confirmed public facts. Do not add `foaf:knows` without the other person's consent or assert unverified account ownership. Future project links or open-data files can live in `static/` and be linked from the contact page.

## Published OpenPGP key

The public key in `static/keys/fredrik-leipt-com-openpgp.asc` was retrieved from `keys.openpgp.org` by the public email address on 2026-10-09. It was parsed as a public key with the user ID `Fredrik Rundgren <fredrik@leipt.com>`, fingerprint `58097C53F37C2832D55D7F9D4A42823C584D1B87`, and expiry 2027-11-28. The local parser found no private-key material. Recheck the expiry and fingerprint before future publication or rotation. An email-address match in a directory is useful evidence; Fredrik should independently confirm the fingerprint before treating it as his active key.

## SSH public key

Fredrik supplied the Ed25519 public key in `static/keys/fredrik-leipt-com-ed25519.pub` on 2026-10-09. Its SHA-256 fingerprint, computed with `ssh-keygen`, is `SHA256:OzItSorkcz7Lq/2bdH+VsdwK9kmgoGBOkSzszAfcjFM`. Do not conflate this with the OpenPGP email key.

## OpenPGP rotation checklist

1. Obtain Fredrik's public key in ASCII-armored form (`.asc`). Export only the public key; never copy a secret key or private key block into this repository.
2. Inspect the user IDs and expiry date. Confirm the key includes `fredrik@leipt.com` and that Fredrik recognizes it as the key to publish.
3. Record the full fingerprint from the key itself. Put the `.asc` file in `static/keys/`, link it from `content/contact.md`, and display the full fingerprint beside the link.
4. Download the built file and check that its fingerprint matches the reviewed source. Consider a Web Key Directory later, after reviewing one.com's existing `/.well-known` paths and avoiding changes to unrelated files.

## S/MIME publication checklist

1. Obtain the public end-entity certificate only (`.cer`, `.crt`, or public-certificate PEM). Do not export or commit a `.p12`/`.pfx` bundle, a private key, or a PEM containing `PRIVATE KEY`.
2. Inspect subject, email addresses, issuer, validity dates, and key usage. Confirm the address and certificate are the ones Fredrik wants public. Decide whether to include an intermediate certificate separately; do not publish a chain by accident.
3. Record the certificate's SHA-256 fingerprint. Put the public certificate in `static/certs/`, link it from `content/contact.md`, and display the fingerprint and expiry date beside the link.
4. Download the built file and confirm its fingerprint matches the reviewed source. When rotating or revoking a certificate, update the page promptly and retain an accurate status note if an old link must remain.

The repository is public, so review the full contents of each file before committing. A public certificate can still reveal names, addresses, issuer details, and validity dates. The S/MIME certificate remains a TODO until its public file is provided and verified.
