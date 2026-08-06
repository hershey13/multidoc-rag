---
title: 'Global apps'
description: 'Documentation on Zendesk Global apps'
---

This guide covers the Zendesk apps currently used in the Global Zendesk instance.

## Advanced SAST App

<sup>*Introduced via [support-team-meta#6652](https://gitlab.com/gitlab-com/support/support-team-meta/-/issues/6652)*</sup>

The Advanced SAST App is a ticket app that enables a quick working of User requests for source code of LGPL-licensed components in GitLab Advanced SAST.

{{% alert title="Technical Details" color="primary" %}}

- Location: Ticket sidebar
- Restricted by Group:
  - Support AMER
  - Support APAC
  - Support EMEA
- This application was developed in-house and can be found [Advanced SAST App project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/advanced-sast-app).

{{% /alert %}}

## Advanced Search

Advanced Search is an app that provides a simple visual interface for constructing complex search queries against tickets, users, and organizations (orgs). It also enables you to export the search results in a CSV format.

{{% alert title="Technical Details" color="primary" %}}

- Location: Navbar
- This application was developed by [Zendesk](https://www.zendesk.com/marketplace/partners/zendesk/) and is available in the [Zendesk Marketplace](https://www.zendesk.com/marketplace/apps/support/198393/advanced-search/).

{{% /alert %}}

## GitLab Reminders App

<sup>*Introduced via [support-team-meta#3036](https://gitlab.com/gitlab-com/support/support-team-meta/-/issues/3036)*</sup>

The Reminders App appears in the navbar and allows the agent a more specialized view of tickets they are involved in. It currently shows:

- Tickets assigned to you with a pending/overdue task that are not in a Closed state
- Recent tickets you have viewed
- Tickets assigned to you that are not in a Closed state
- Tickets you are following that are not in a Closed state

It also allows you to quickly manage your tasks by seeing the notes you have left for said task, when it is due, and a button to quickly mark the task as done (remove the notes and due date).

{{% alert title="Technical Details" color="primary" %}}

- Location: Navbar
- This application was developed in-house and can be found [GitLab Reminders App project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/reminders-app).

{{% /alert %}}

## GitLab Super App

<sup>*Introduced via [support-team-meta#801](https://gitlab.com/gitlab-com/support/support-team-meta/-/issues/801)*</sup>

A plugin controlled app that can do several things GitLab related

The current plugins are:

- User Lookup
  > This lets you search gitlab.com for a username or email. It then displays information based on the results.
- Namespace Lookup
  > This lets you search gitlab.com for a namespace. It then displays information based on the results.
- Collaboration Project
This checks the organization for a collaboration project ID. If one exists, it then provides a link to said project.
- Email Suppressions
  > This searches mailgun for suppressions from bounces (note it does not do it on complaints or unsubscribes). It will display the results (with the message for the suppression).
  >
  > It also gives the option of removing the suppression (if one if found). Doing so deletes it from mailgun and adds an intenral comment on the ticket with the results of the suppression deletion.
- Fieldnotes
  > This app checks the [Fieldnotes project](https://gitlab.com/gitlab-com/support/fieldnotes/-/issues) for any existing Issues which reference the current Zendesk ticket ID. If no existing Issues are found, then agents are able to create a new Fieldnotes Issue from directly within the Zendesk ticket.
- Account Verification Helper
  > This creates a usable form to check if an account verification has passed based on the type of verification selected. It calculates the Risk Factor from the challenges passed and modifies it to reflect the passed challenges. It also allows for posting an internal note of what the form reflects.

{{% alert title="Technical Details" color="primary" %}}

- Location: Ticket sidebar
- Restricted by Group:
  - BPO
  - Support AMER
  - Support APAC
  - Support EMEA
- This application was developed in-house and can be found [GitLab Super App project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/gitlab-super-app).

{{% /alert %}}

## Glean

<sup>*Introduced via [issue-tracker#798](https://gitlab.com/gitlab-com/gl-security/corp/cust-support-ops/issue-tracker/-/work_items/798)*</sup>

Glean connects to and understands all your company's knowledge to bring you the answers you need while working in Zendesk. With Glean, teams improve customer experience with faster response times using state-of-the-art enterprise search and RAG technology to retrieve the most relevant, up-to-date information. Whether it is accessing ticket context, product experts, or customer information to respond to questions and unblock issues quickly, Glean generates highly personalized answers grounded in your company's unique enterprise knowledge graph.

Through Glean you can:

- Get a summary of the ticket
- Get suggested next steps
- Draft a response
- Perform a search across GitLab resources
- Use GitLab pre-defined prompts

{{% alert title="Technical Details" color="primary" %}}

- Locations:
  - Navbar
  - Ticket sidebar
- Restricted by Group:
  - Accounts Receivable
  - Billing
  - BPO
  - Support AMER
  - Support APAC
  - Support EMEA
- This application was developed by Glean and is available in the [Zendesk Marketplace](https://www.zendesk.com/marketplace/apps/support/922191/glean/).

{{% /alert %}}

## Notifications App

{{% alert title="Info" color="info" %}}

- This app is opt-in. This means nothing will happen unless you modify your user settings to receive notifications.

{{% /alert %}}

This app handles posting notifications at the top of the screen, depending on various conditions and user settings.

{{% alert title="Technical Details" color="primary" %}}

- Location: Top navbar
- Restricted by Group:
  - Support AMER
  - Support APAC
  - Support EMEA
  - Support Managers
  - Support Ops
- This application was developed in-house and can be found [Notifications App project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/notification-app).

{{% /alert %}}

### Current events that trigger the app

The following events will send data to the app for notification processing:

- Agent private comment made on ticket
- Agent public comment made on ticket
- Customer public comment made on ticket
- Emergency ticket created
- Escalated ticket created
- Tickets being STAR’d
- Tickets created by specific organizations

### User settings

The current user settings, which will determine what notifications you will (and will not) recieve are:

- Play notification sound
  - Checking this box tells the app to play the notification sound.
- Notify me for
  - This tells the app what kind of tickets to notify you for
  - Values:
    - Assigned tickets only
    - Followed tickets only
    - All tickets
- Notify me about
  - This tells the app what kind of events to notify you for
  - Values:
    - All public comments (agent and customer)
    - Only public comments from agents
    - Only public comments from customers
    - Only private comments
    - All types of comments
- Notify me only for tickets with priority
  - This tells the app which priorities to notify you on
  - Values:
    - at least Urgent
    - at least High
    - at least Medium
    - at least Low
  - Note: A blank value is assumed to be “all priorities”
- Also notify me for escalated ticket creation
  - This dictates if you want to be notified via the app when an escalated organization creates a ticket.
  - Note: This works independently of all other settings.
- Also notify me for emergency ticket creation
  - This dictates if you want to be notified via the app when an emergency ticket is created.
  - Note: This works independently of all other settings.
- Also notify me for STARs
- Also notify me for soon to breach tickets on
  - This dictates if you want to be notified via the app when a ticket is about to breach (within 2 hours)
  - Values:
    - Assigned tickets only
    - Followed tickets only
    - Tickets within my SGG only
    - All tickets
  - Note: This works independently of all other settings.
- Also notify me for tickets created via specific orgs
  - This dictates if you want to be notified via the app when a ticket is created by a specific organization
  - The list should be comma separated
    - Example: if you want to be notified for organizations 123, 456, and 789, use the value 123,456,789 or 123, 456, 789
  - Note: This works independently of all other settings.

For information on editing your personal user settings, please see [Zendesk’s documentation](https://support.zendesk.com/hc/en-us/articles/4408819930906-Editing-your-personal-settings-in-Zendesk-Chat-Support-accounts#topic_gfh_rqm_4fb).

## STAR

<sup>*Introduced via [support-team-meta#4694](https://gitlab.com/gitlab-com/support/support-team-meta/-/work_items/4694)*</sup>

Support Ticket Attention Requests (STAR) are the mechanism by which GitLab Team Members can request additional attention be placed on tickets. This is the app agents use in Zendesk to start a STAR process.

{{% alert title="Technical Details" color="primary" %}}

- Location: Ticket sidebar
- This application was developed in-house and can be found [STAR project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/star).

{{% /alert %}}

## Support Ops Super App

A plugin controlled app that can do several things Support Ops related

The current plugins are:

- Namespace Lookup
  > This lets you search gitlab.com for a namespace. It then displays information based on the results. This is related to the one in the GitLab Super App, but instead it shows less information and shows the SFDC IDs it is associated with.
- Project Lookup
  > This lets you search gitlab.com for a project. It then displays information based on the results.
- Attempt Association
  > On tickets where the product type is GitLab.com, clicking the button on the plugin will attempt to auto-associate the requester to an organizaiton. If that is not possible, it will detail why it was not possible.
- Associate User
  > On a Support Ops ticket, it will ask you for email addresses. It will then use the organization on the current ticket to associate said email addresses to that organization.
- Deassociate user
  > On a Support Ops ticket, it will ask you for email addresses. It will then use the organization on the current ticket to deassociate said email addresses from that organization.
- CMP Developers
  > Outputs a list of CMP developers (by email) for an organization (if it has a CMP)

{{% alert title="Technical Details" color="primary" %}}

- Location: Ticket sidebar
- Restricted by Role:
  - Admin
- This application was developed in-house and can be found [Support Ops Super App project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/support-ops-super-app).

{{% /alert %}}

## Zendesk Super App

<sup>*Introduced via [support-ops-project#801](https://gitlab.com/gitlab-com/support/support-ops/support-ops-project/-/issues/801)*</sup>

A plugin controlled app that can do several things Zendesk related

- Create new ticket
  > Allows an agent to create a new ticket using the same user as the ticket they are currently on.
- Due date picker
  > This allows you to customize what the Due Date for a Task ticket is set for. By default, Zendesk only allows setting the date. This enables you to set the date, time, and timezone.
  >
  > You can also set the Due Date Note and disable (or enable) task notifications using this app.
- Escalated tickets
  > This searches for tickets under the organization that have been escalated within the last 6 months.
- Related tickets
  > This looks for tickets related to the current one based off the category (or subcategory) the ticket is currently using. It then displays up to 5 of them (sorted by the update_at value of the ticket, descending).
- Attachments
  > Displays attachments present on the ticket.

{{% alert title="Technical Details" color="primary" %}}

- Location: Ticket sidebar
- Restricted by Group:
  - BPO
  - Support AMER
  - Support APAC
  - Support EMEA
- This application was developed in-house and can be found [Zendesk Super App project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/zendesk-super-app).

{{% /alert %}}

## ZenGuard

<sup>*Introduced via [issue-tracker#122](https://gitlab.com/gitlab-com/gl-security/corp/cust-support-ops/issue-tracker/-/issues/122)*</sup>

Implements a warning system into Zendesk to warn (or block) potentially dangerous actions. If a warning is bypassable, then a close button (X) appears to the right of it (and clicking said button removes the warning).

Current list of checks:

- Checks if making unapproved form changes

{{% alert title="Technical Details" color="primary" %}}

- Location: Ticket sidebar
- This application was developed in-house and can be found [ZenGuard project](https://gitlab.com/gitlab-support-readiness/zendesk-global/apps/zenguard).

{{% /alert %}}
