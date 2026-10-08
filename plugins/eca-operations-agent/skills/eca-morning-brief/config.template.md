# Morning brief configuration

Written at first run. Copy to `config.md` and fill it in, or let setup do it.

## Store
- **Brand name**: <as it should appear on the brief>
- **Shopify store**: <domain>
- **Timezone**: <from get-shop-info, confirmed with the member>
- **Currency**: <from get-shop-info>

## Connectors
- **Shopify**: required, verified <date>
- **Meta Ads**: connected / declined — ad account id: <id>, name: <name>
- **Gmail**: connected / declined — mailbox: <address>

> The ad account id is captured once and never guessed. Members routinely have dozens.

## Schedule
- **Runs at**: <time> local, <cron>
- Scheduled tasks run while the app is open. One due while it is closed runs at next launch.

## Slack
- **Mode**: off / draft-and-ask / automatic
- **Channel**: <only if automatic>

> Automatic means an unreviewed brief reaches everyone in that channel.

## Thresholds
- **Change worth mentioning**: 5%
- **Stock cover warning**: under 4 weeks
- **Dispatch backlog warning**: older than 48 hours
- **Low review rating**: 3 stars or under
- **Maximum actions in one brief**: 6

## Inbox noise filter
Senders and patterns to exclude from the "needs a reply" count. Add to this whenever a
notification sender slips through.
- `support@judge.me` — reviews, counted in the reviews section instead
- `notifications@*`, `noreply@*`, `no-reply@*`
- Anything whose labels include SENT
- Automatic replies: subject starting "Automatic reply" or "Out of office"
