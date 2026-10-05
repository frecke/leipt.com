# leipt.com

Fredrik's personal site, built with Hugo and Markdown. The intended public repository is `github.com/frecke/leipt.com`. The site is designed to run on existing one.com static hosting; no server runtime is needed.

## Local development

Install [Hugo Extended v0.167.0](https://github.com/gohugoio/hugo/releases/tag/v0.167.0), then:

```sh
hugo server -D
hugo --minify
```

Open the local address printed by Hugo. Generated files appear in `public/` and are ignored by Git.

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
