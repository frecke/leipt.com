---
title: Information products and their realizations
date: 2026-10-09
description: An early research note on separating governed meaning from technical delivery.
draft: true
---

**Status: research note and working hypothesis.** This is a question I am exploring through [DataGovOps](https://github.com/frecke/datagovops), not a settled standard or an evaluated result.

Data-product conversations often combine two different things. One is the information an organisation intends to make available: its meaning, purpose, authority, obligations, and expected quality. The other is a particular technical way to deliver that information: a table, API, file, stream, or model on a platform.

They are closely related, but they do not necessarily change at the same pace. A technical implementation can move or be replaced while the information commitment remains. Conversely, a change in meaning can be significant even when the same table and endpoint still exist.

My working hypothesis is that a governed **information product** should be described independently of its **technical realizations**. A realization then points back to the information product and states how it satisfies the intended contract in a specific context.

This separation might help with several recurring problems:

1. **Portability.** A contract about meaning should not disappear merely because a platform changes.
2. **Multiple delivery forms.** One information product may need an API for an application and a dataset for analysis, with different technical guarantees.
3. **Accountability.** It should be possible to identify who is responsible for the information itself and who operates each delivery path.
4. **Change analysis.** A schema change, a semantic change, and a new snapshot are different events and may need different review.
5. **Evidence.** A consumer should be able to see which version, provenance, authority, and usage conditions supported a decision.

The model also creates risks. An abstract information-product layer could become another catalogue entry that nobody maintains. Separate version numbers can confuse rather than clarify. A relationship that looks clean in a diagram may be awkward for teams working under real delivery constraints.

Those risks are reasons to test the model, not reasons to assume it works. A useful evaluation would put the proposal against concrete cases: a source correction, a platform migration, a change in permitted use, and two delivery forms that must remain semantically consistent. I would want to know whether the model improves decisions and auditability without imposing more work than it saves.

The public repository records the current concepts and examples. I expect the terminology and boundaries to change as they meet counterexamples. That is part of the point of making the work inspectable.
