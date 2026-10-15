# Campus Customs Desk: design notes

The dashboard is meant to feel like walking into a small shop's back office in New England: warm wood, soft light, a brass nameplate on every chair. It is not an admin panel. You are the human at the Table, and the agents are a slightly dysfunctional family who run the shop around you.

## Look and feel

- **Palette:** cream walls with faint wood-panel lines, a dark walnut top bar, oak for the table, brass for nameplates and the drawer. Georgia-style serif headings (like a ledger), a soft sans for body text.
  *Why:* calm light and wood is the home-office feel you asked for, and a serif ledger voice suits a shop that deals in invoices and rent.
- **One loud colour, campus pink:** pink is used only for things that need you or just got finished ("needs your OK", the Resolved stamp, money leaving the drawer). Everything else is quiet wood and cream. The Approve and Deny buttons are deliberately neutral grey (see below).
  *Why:* the rest of the project uses black and pink. Keeping pink as the one accent means your eye goes straight to the thing that matters, and it ties the desk back to the shop's look.

## Layout: three columns, like a real desk

1. **Left, the ticket pile.** The three tickets as paper slips on the desk. Pick one by clicking it.
2. **Middle, the desk.** The ticket's title and the big **Start the team** button, a status banner, any approval slip, then the oak table with the five agents sitting at it, and below it a "Who did what" summary.
3. **Right, the ticket tape.** A running transcript of the conversation, newest at the bottom, auto-scrolling, with a small typing indicator while the team is working.

*Why:* you pick on the left, watch in the middle, and read the detail on the right. The tape is the precise record; the table is the at-a-glance picture of who is busy.

## How the agents read differently

Each agent has their own colour, a hand-drawn SVG portrait (no photos, no image services) and a brass nameplate. Their colour also shows up on their speech bubble, their tape entries and their summary card, so you can follow one person across the whole page without reading names.

| Agent | Colour | Portrait |
|---|---|---|
| The Boss | oak | old patriarch: bald on top, white tufts, bushy brows, oak jacket (the same oak as the table, so he looks like part of the furniture) |
| Inventory Ina | navy | fifties, round glasses, hair in a bun with a grey streak, navy cardigan |
| Accounting Ama | red | rounder face, rectangular glasses, red sweater |
| Facilities Father | green | grumpy, stubble, big nose, green flannel; his coffee mug **only steams while he is working** |
| Jervis | grey | bald butler, handlebar moustache, waistcoat and bow tie |

*Why:* a dysfunctional family is easier to remember than five boxes. Distinct silhouettes (glasses, bun, moustache, stubble) mean you can tell them apart at a glance, even greyed out.

## Making the live run readable

- **Seats show state.** An agent who is working lifts slightly, breathes, glows in their colour and wears an "at work" badge. Agents who are done get a "done" badge. Agents who were never called fade to a dim, desaturated look and say "not called". You can see at once that a ticket did not need the whole family.
- **Speech bubbles** over each head show that agent's latest line in plain English ("Please prepare the rent payment...", "is checking the cash..."), cut to four lines.
- **The tape shows full text.** Nothing on the ticket tape is cut off with an ellipsis; only the small speech bubbles over the agents' heads are clamped, and they show everything when you hover.
- **The tape translates plumbing into words.** Tool names become verbs (`get_cash` becomes "is checking the cash..."). A delegation reads as "The Boss → Facilities Father" with the question. Raw prompts and tool results are hidden; each agent's final answer is boiled down to one sentence.
- **"Who did what on this ticket"** cards give a short summary per agent: their final answer, who they asked, and which MCP tools they used. Agents who were not needed say so, in dashed grey cards.

## Approve: impossible to miss, impossible to do by accident

When the Boss asks for approval, a cream slip with a dashed pink border appears above the table. It says what would be paid, to whom and how much, repeats that "the agents only prepared this", and has two buttons side by side, **Approve & pay** and **Deny**. Both are the same neutral grey so neither one nudges you; the slip's pink dashed border is what grabs your eye. The ticket card also gets a pulsing pink "needs your OK" chip. Nothing moves until you press Approve (the backend's approve route is the only thing that changes cash). Deny pays nothing and is remembered, so the Boss will not ask for the same thing again. After you press it, a toast tells you what happened, either the amount paid and the new balance, or why it was refused.

## Cash

The **cash drawer** sits in the top bar in a dark walnut box with a brass edge, so it is always visible. The balance counts down smoothly when money leaves and a pink "-$2,400.00" chip pops next to it for a few seconds. A refused payment shows as a red toast and the drawer does not change.
*Why:* the number you care most about should never need scrolling, and the animation makes a payment feel like something that happened.

## Resolved

A resolved ticket gets a pink **RESOLVED** rubber stamp slammed onto its slip (with a small stamp animation) and a "Filed in the drawer" banner above the table, along with the Boss's decision. A ticket that is not resolved but has been paid says "Payment made. Start the team again so the Boss can finish this ticket", because the backend only marks a ticket resolved when a run ends with nothing waiting on a human.

## Small touches

- Tickets tilt slightly when you hover, like slips on a desk.
- The **Fresh start** button resets the shop; it asks first and is disabled while the team is working.
- If the backend is not running, a banner tells you the exact command to start it.
- The board polls every second while a run is going, and every two and a half seconds otherwise.

## What the board uses

The problem 7 routes (`GET /tickets`, `POST /tickets/{id}/run`, `GET /events`, `POST /approvals/{id}/approve`, `GET /cash`, `POST /reset`) plus `POST /approvals/{id}/deny`, which was added later for the Deny button.
