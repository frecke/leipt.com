---
title: The maintenance phase is the design
date: 2026-10-09
description: Why the real test of a data platform begins after the first successful delivery.
draft: true
---

A data platform can be impressive on launch day. The first pipeline runs, the dashboard loads, and the team can tell a coherent story about the architecture. The more revealing question comes later: can someone who did not build it understand a failed run, decide whether a dataset is fit for use, and change a contract without surprising everyone downstream?

That later period is often called maintenance, as though the interesting design work has ended. For data systems, it is where many design choices finally become visible.

Consider a fairly ordinary change. A source team renames a field and changes how it handles missing values. The ingestion job still succeeds. A report still opens. Yet the meaning of one measure has shifted. If the platform cannot show the change, identify the consumers, and make the expected meaning explicit, the problem is not merely operational. It is architectural.

This is why I think about analytics as a service rather than a sequence of deliveries. A useful service needs more than an available endpoint or a finished dashboard. It needs a way to answer:

- Who is responsible for this information and for this implementation?
- What does the data mean, and for which purposes is it suitable?
- Which checks are automated, and which decisions require a person?
- How will a change be detected, reviewed, communicated, and reversed?
- What evidence will remain when someone asks why a decision was made?

None of these questions has a universal tool-shaped answer. A contract can make expectations explicit, but it cannot decide whether those expectations are appropriate. Monitoring can show that a value changed, but it cannot alone determine whether the change matters to a decision. Governance can define responsibility, but it only helps if that responsibility is connected to the work people do.

The practical work is to make these connections visible. Put the specification close enough to the pipeline that it can be checked. Record decisions in a form the next team can find. Give operators useful signals rather than a wall of green and red lights. Treat an incident or a disputed metric as feedback on the system's design, not simply as a reason to tell people to be more careful.

This also changes how I judge success. A delivery can be on time and still leave an organisation with fragile knowledge concentrated in a few people. A smaller solution that a team can explain and improve may create more lasting value.

The point is not to slow every project down until every possible future has been documented. It is to design for the next responsible change. If the people inheriting the system can see its purpose, limits, ownership, and evidence, they can keep it useful. That is where a data project starts becoming a data capability.
