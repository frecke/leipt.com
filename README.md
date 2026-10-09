# leipt.com

Fredrik's personal site, built with Hugo and Markdown. The intended public repository is `github.com/frecke/leipt.com`. The site is designed to run on existing one.com static hosting; no server runtime is needed.

## Local development

Install [mise](https://mise.jdx.dev/getting-started.html) and activate it in your shell, then:

```sh
mise trust
mise install
just setup
just doctor
just dev
```

Open the local address printed by Hugo. `mise.toml` pins Hugo Extended, Python, uv, just, age, and gh. uv owns the Python environment and committed `uv.lock`; the site itself remains Hugo and Markdown.

Run `just` to list commands. Use `just fmt` to format Python tooling, `just check` (or `just ci`) for the local/CI gate, and `just build` for production output in `public/`. `just preview` builds a noindex preview in `public-preview/` without uploading. Generated files and `.venv/` are ignored by Git. Without shell activation, use `mise exec -- just check`.

## Secrets

Use age for encrypted local secrets and `gh` for GitHub's `onecom-preview` environment secrets. See [the secrets workflow](docs/secrets.md). Keys stay outside the repository; secret values never belong in command arguments, commits, or logs.

## Editing

Pages live in `content/`. Replace TODOs only with verified facts. Add articles under `content/writing/`, research notes under `content/research/`, and talks under `content/speaking/`. Update `params.name`, page titles, metadata, and identity links when Fredrik approves the public wording. Keep unpublished or sensitive drafts outside this public repository.

Templates and CSS are deliberately local and small; there is no downloaded theme or JavaScript build chain. The color control is the only JavaScript.

## Build and hosting

GitHub Actions builds on pull requests and main. Deployment is a separate manual action, initially limited to a marked `leipt-preview` directory on one.com. It cannot deploy to the web root. See [deployment guide](docs/deployment.md) for host inspection, secrets, marker setup, and the later root cutover.

## Before publication

- Replace or remove every visible TODO and verify all links and claims.
- Confirm the exact public name, preferred language, contact channels, and identity links.
- Inspect one.com's current `/www` or `httpd.www` layout and back up the affected files.
- Confirm the preview URL and hosting plan's SFTP details. Set the GitHub environment secrets without adding values to Git.
