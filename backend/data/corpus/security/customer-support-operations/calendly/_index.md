---
title: 'Calendly'
description: 'Documentation on Calendly'
---

## Understanding Calendly

### What is Calendly

Calendly is an online appointment scheduling tool that GitLab uses.

## Calendly webhooks

### Listing all webhooks

To do this, you will want to use the [List Webhook Subscriptions](https://developer.calendly.com/api-docs/faac832d7c57d-list-webhook-subscriptions) to get that information. This requires you to specify a scope and the organization itself. This might look like (assuming you URL encode the values, which isn't "required" but helpful):

```bash
curl -ss --request GET \
  --url 'https://api.calendly.com/webhook_subscriptions?organization=https%3A%2F%2Fapi.calendly.com%2Forganizations%2FAAAAAAAAAAAAAAAA&scope=organization' \
  --header 'Authorization: Bearer TOKEN_GOES_HERE' \
  --header 'Content-Type: application/json'
```

### Creating a webhook

To create a webhook in Calendly, you have to use the API.

The very *first* thing you are going to need to do is determine our Organization's information, as it will be required for the webhook's creation.

To do this, you are going to need to use the [Get current user](https://developer.calendly.com/api-docs/005832c83aeae-get-current-user) API endpoint, like so:

```bash
curl --request GET \
  --url https://api.calendly.com/users/me \
  --header 'Authorization: Bearer TOKEN_GOES_HERE' \
  --header 'Content-Type: application/json'
```

This will produce output that contains our organization's information (as you are part of our organization). The exact entry you are wanting is the `current_organization` value. If using something like [jq](https://jqlang.github.io/jq/), you can run the entire command like so:

```bash
curl -ss --request GET --url https://api.calendly.com/users/me \
  --header 'Authorization: Bearer TOKEN_GOES_HERE' \
  --header 'Content-Type: application/json' \
  | jq '.resource.current_organization'
```

You will also need your user reference URL, which you can get from the same endpoint. In this case, you'll need `uri` value from the output. Using something like [jq](https://jqlang.github.io/jq/), you can run the entire command like so:

```bash
curl -ss --request GET --url https://api.calendly.com/users/me \
  --header 'Authorization: Bearer TOKEN_GOES_HERE' \
  --header 'Content-Type: application/json' \
  | jq '.resource.uri'
```

With that, you can now create the webhook itself. To do this, you will use the [Create Webhook Subscription](https://developer.calendly.com/api-docs/c1ddc06ce1f1b-create-webhook-subscription) API endpoint. This is going to require some very specific information to work correct, so let's break it down item by item:

- `url`
  - This is the URL the payload from Calendly is being sent to.
- `events`
  - An array of items the webhook will trigger for. The options currently are:
    - `invitee.created`
    - `invitee.canceled`
    - `invitee_no_show.created`
    - `routing_form_submission.created`
- `organization`
  - The URL for your organization. See above to get this value.
  - **NOTE** The *full* URL should be used.
- `user`
  - Your user reference URL. See above to get this value
  - **NOTE** The *full* URL should be used.
- `scope`
  - The scope this runs on. It can either be `user` or `organization`.

Putting this all together, you will make a POST request, with the data being in JSON format. To accomplish this, we recommend making a JSON file containing the parameters to send, verifying it via [jq](https://jqlang.github.io/jq/), and then making your API call. An example of what this might look like is:

```bash
echo '{' >> temp.json
echo '"url": "https://blah.foo/bar",' >> temp.json
echo '  "events": [' >> temp.json
echo '    "invitee.created",' >> temp.json
echo '    "invitee.canceled",' >> temp.json
echo '    "invitee_no_show.created"' >> temp.json
echo '  ],' >> temp.json
echo '  "organization": "https://api.calendly.com/organizations/AAAAAAAAAAAAAAAA",' >> temp.json
echo '  "user": "https://api.calendly.com/users/BBBBBBBBBBBBBBBB",' >> temp.json
echo '  "scope": "user"' >> temp.json
echo '}' >> temp.json
$ cat temp.json | jq
{
  "url": "https://blah.foo/bar",
  "events": [
    "invitee.created",
    "invitee.canceled",
    "invitee_no_show.created"
  ],
  "organization": "https://api.calendly.com/organizations/AAAAAAAAAAAAAAAA",
  "user": "https://api.calendly.com/users/BBBBBBBBBBBBBBBB",
  "scope": "user"
}

curl -ss --request POST \
  --url https://api.calendly.com/webhook_subscriptions \
  --header 'Authorization: Bearer TOKEN_GOES_HERE' \
  --header 'Content-Type: application/json' \
  --data @temp.json
```

The response you get back from this need to be verified, but it should mirror a lot of the information you just used in your parameters. Once you have verified it all looks correct, the webhook is live.

## Calendly Events to gCal Events

{{% alert title="Technical Details" color="primary" %}}

- Deployment type: `Ad-hoc`
- Project repo: [Calendly Events to gCal Events](https://gitlab.com/gitlab-support-readiness/calendly-events-to-gcal-events)

{{% /alert %}}

### What is Calendly Events to gCal Events

The Calendly Events to gCal Events is a setup that takes payloads from Calendly webhooks (fired at the organization level when events are created) and translates them to Google calendar entries.

### How it works

Via a Calendly webhook (implemented at the organization level), when an event is created a payload is sent to the process (via a pipeline trigger). This results in the execution of the `bin/process` script, which does the following:

- Verifies there is a payload present
- Reads data from the Support Team YAML files
- Checks if the event is a Support US Government event or a Support Global event
  - It is a Support US Government event if it meets all of the following criteria:
    - the assignee is a US Government Support agent
    - the name of the scheduled event contains one of the following strings:
      - `US Federal`
      - `US Government`
  - It is a Support Global event if it meets all of the following criteria:
    - it is not a Support US Government event
    - the name of the scheduled event contains the string `Support` (case insensitive)
- If it is a Support US Government event, a Google calendar event is added to the `US Government Support` calendar
- If it is a Support Global event, a Google calendar event is added to the `GitLab Support` calendar
- If it neither type of event, it exits with a status code of 0

### Changing Calendly Events to gCal Events

{{% alert title="Note" color="primary" %}}

- This requires at least `Developer` access to the [Calendly Events to gCal Events](https://gitlab.com/gitlab-support-readiness/calendly-events-to-gcal-events) project.
- This should only be done if there is a corresponding request issue (Feature Request, Administrative, Bug, etc.). If one does not exist, you should first create one (and let it go through the standard process before working it).

{{% /alert %}}

To make changes to the Calendly Events to gCal Events, you will need to create a MR in the project repo. The exact changes being made will depend on the request itself.

After a peer reviews and approves your MR, you can merge the MR (which will have them applied on the next scheduled run).

## Common issues and troubleshooting

This is a living section that will have items added to it as needed.
