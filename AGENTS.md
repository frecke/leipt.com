# Project instructions

Build `leipt.com` as a Markdown-first Hugo site. Keep templates small, semantic, accessible, fast, and dependency-light. Do not invent Fredrik's biography, affiliations, publications, talks, credentials, or contact details; mark gaps with `TODO` in content.

The intended source repository is public at `github.com/frecke/leipt.com`. Never commit secrets, unpublished private material, personal certificates, or client information. Use a branch and pull request for changes once the remote exists.

one.com is the production host. Treat its existing webspace as shared. Inspect and document the live layout before changing it. Do not change DNS, mail, certificates, or unrelated files. Never deploy to the web root or use blanket `rsync --delete` there. The preview deployment is confined to a verified `leipt-preview` directory and must fail if its ownership marker is absent. Promotion to the canonical root needs a separate reviewed migration plan and a backup of existing content.

For routine edits, run a Hugo build and inspect changed output. Keep content in Markdown and avoid introducing client-side frameworks.
