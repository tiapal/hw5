# AI Prompts

## Problem 1: Vibe coder prompts

**Initial prompt:**

> ok but in this newfolder make a new AI_prompts.md
>
> still do it by problem
>
> this for example is problem 1: vibe coder prompts

## Problem 2: Study the campus customs database

**Initial prompt:**

> open data/campus _customs.db and look through every table and its fields
>
> Copy the og file to data/campus_customs_new.db
>
> keep your eyes peeled and study those three open tickets to see how they link to other tables
>
> Start output/harness.md then for each table, list the fields and one short line on why that table matters for the agents
>
> write 3 mcp tools using fastmcp in `mcp_server/` for now.
>
> first, check the database at `data/campus_customs_new.db` and look at tickets 101, 102, and 103 to figure out what each one needs. don't guess or make up any data. only use what's actually in the database.
> create 3 tools with clear names that help resolve these tickets. each tool should read the relevant table and return the info needed to work on the ticket. I need you to make those tools because i tried opening the file and its gibberish eek
>
> also create `output/harness.md` and list all 3 tools. for each tool, include:
>
> * the tool name
> * which table it reads
> * which ticket it helps with (101, 102, or 103)
> * one sentence explaining exactly why it's useful for that ticket, based on the actual ticket details
>
> don't use vague explanations like "reads inventory". explain what specific information the tool provides and why that information is needed for that ticket.
>
> also create a short `mcp_server/README.md` explaining what the mcp server does, which database file it uses, and what the 3 tools are for.
>
> keep it simple and don't build anything beyond what's asked. don't modify the original database, don't invent data, and don't run or start the server.

## Problem 4: Add the MCP server to the vibe coder and test each tool

**Initial prompt:**

> problem 4: add the mcp server to the vibe coder and test each tool
>
> ok now i have to add the mcp server on here and test each tool so you can call each tool
>
> save the connection json text in .mcp.json at the project root or however you save local mcp server lists
>
> when the mcp server is connected , test each of the three tools and save the evidence in output/mcp_smoke.json
>
> for every tool include
> -the prompt i asked the vibe coder (you)--> i will need to do this individually so would be great if you could just prompt me to ask about each tool
> -the tool name
> -the tool output(must match values in data/campus_customs_new.db)

**Follow-up prompts:**

> for ticket 101 Use the campus-customs tool to check whether we have the Bulldog tee in size S for ticket 101, and tell me about the linked invoice

> im doing hw 5 of my vibe coding class Desktop/AI For Managers/HW 5. It has to be HW 5

> wait pause how do we start a session in there

> cd "/Users/bettinay.palang/Desktop/AI For Managers/HW 5" && claude
>
> it says claude not found

> Use the campus-customs tool to check whether we have the Bulldog tee in size S for ticket 101, and tell me about the linked invoice

> (Pasted the new session's reply: it could not call the campus-customs tool because the server was not connected.)

> ok
>
> im doing hw 5 of my vibe coding class Desktop/AI For Managers/HW 5. It has to be HW 5
>
> Use the campus-customs tool to check whether we have the Bulldog tee in size S for ticket 101, and tell me about the linked invoice

> i did start a new session but the campus-customs did not come up and when i pasted the ticket 101 prompt this is what it told me ^

> ok
>
> im doing hw 5 of my vibe coding class Desktop/AI For Managers/HW 5. It has to be HW 5
>
> Use the campus-customs tool to check whether we have the Bulldog tee in size S for ticket 101, and tell me about the linked invoice

> ok wait theen can you ask me for permission

> yay! did you log all the info that you need to (AI_prompts.md and also output/harness.md)

> oh woops!

> Use the campus-customs tool to check the rent notice on ticket 102. When is rent due, and do we have the cash?

> Use the campus-customs tool to check the hoodie bulk discount request on ticket 103. What’s the pricing, and do we have enough stock?

## Problem 5: Build the agent team and grow the MCP tools

**Initial prompt:**

> ok next problem 5 : build the agent team and grow the mcp tools
>
> ok so now we hustle onto agentic team we need to build this
>
> use pydanticAI: Boss, inventory. accounting, facilities, and cusotmer service
>
> include prompts, models, agent loops  so they can delegate  work to each other in full connectivity
>
> put the agent prompts in backend/prompts/[name of agent as file name and do one file per agent]
>
> put data types in backends/models.py and the agent files under backend/
>
> so i need to writeeach prompt in my own words  with the shop rules that the agent needsand it needs to be very detailed and cover all aspects of an agents work but lowk idk what to type so can you give me the first one as a sample i gen dont get what prompt to write

> ok so boss
>
> 1. Who you are: you are the boss you are very annoying and detailed because your employees (you ASSUME) are slackers. you like to be reading tickets, those shits are your poetry, you delegetae stuff because you like to have your shop be a well oiled machine like gen baby oiled
> 2. Your team: your team is you, and then inventory ina (so when you you get a ticket thats like "hey is this in stock" you go check with your man inventory ina and you go ORDER UP HOW MANY OF [this item] DO WE HAVE" and you delegate that to inventory ina (mom in tagalog) and inventory ina tells you after checking and then you put that out to the person who sent the ticket and they can also check stock by SKU and  SIZE, also inventory ina notices shortages and will find a vendor so you just have to approve that order and deny if its a ludicrous amount or unnecessary
>
> then you have accounting ama (dad in tag) who watches cash and invoices, checks margins, and preps payments or purchases orders for human approval. so when you get a ticket thats like how much cash do we have which invoice is this, you ask accounting ama and they just let you know and you report back to the "table" where you can communicate with the person asking. also if accounting daddy asks you for approval on a purchase ( usually when theres a shortage because inventory ina said so to accounting ama), you should ask a human  on the "Table" and human approval will be given or denied. if denied you do not let accounting ama do anything. if approved, you let accounting ama to use cash to make the purchase
>
> then we have facilities father and they handle she shop space side so when leases and rent come up on a ticket on the "table" you send them a request and they have to ask accounting ama to pay that based on the due date and allla dat so they schedule and send those requests to accounting ama when necessary they will also send you an approval when payment is finally to be made
>
> finally we have customer service jervis and hes da bulter and he writes out draft messages to customers so you dont even have to do that yourself! you get to ask them to do it based on all of your knowledge from facilities gather, acounting ama, and inventory ina and then you have all the thoughts circulating in your big boss brain and you say hey customer service jervis this is what i want to say and hes like your scribe man and then you take his parchment and you put it out for the customer to see
>
> 1. Your loop: so based on the ticket you direct it to the agent
>
> receive ticket and if the ticket is about size --> inventory ina --> inventory ina gives size to you --> you take note of this and you ask customer service jervis to draft a message based on your new knowledge --> csj sends you a draft message --> you send out an answer to the customer
>
> 1. Shop facts: things in the data it must always use. , "today" is 2026-08-31 from the `desk` table, not the real date. it is desk.date_today
> 2. Shop rules: never discount below unit cost, do not make up numbers to give to the customer, "today"  it is desk.date_today, vendor lead time comes from the vendors table , a vendor will not ship new products while they still have an open unpaid invoice, human approvl is necessary for ANY purchase, if a payment is made, make sure to update the relevant table, if there is not enough cashthe pay tool MUST REFUSE no negative balancs, we do not model revenue so cash only goes out in this case, before a full run to resolve the ttickets, make sure to reset the database to the originl values , DO NOT EMAIL REAL VENDORS or CUSTOMERS OR MAKE VENDOR CALLS everyhting stays on this board
> 3. Never do:  never invent numbers, do not go back and forth on a problem for more than 4 minutes, if its not working youre just wasting tokens and i will be poor
>
> BEFORE YOU RUN THIS CAN YOU TELL ME IF THIS IS OK? I FEEL LIKE IT GOES ON A BIT ABOUT WHAT THE OTHERS ARE DOING AND IDK IF THATS RIGHT

> ok wait can you try writing whats missing  and the trim

> ok yay now write the prompt for inventory ina

> draft all the rest, ill make small changes within the actual md file

> yes start on that

> do i need any tools to help my agentson the mcp server so they can work on open tickets
>
> shop facts come from the mcp server over data/campus_customs_new.db--do not invent a second shop-tools layer  that bypasses the MCP

> why not work

> where is venv

> yeah do dat

> ok now wire the agents so they append to output/audit_trail.json as they run: for each agent -loop step, record enough to audit later. append to this file --do not wipe it each run
>
>
> in output/harness.md , list each agent and each mcp tool(including ones you added in this problem )along with which table the tool uses, also add a really short safety section  so include the guardrails that are already there like the 4 limit rule you put in, but also include that we cannot use customers' money for any other purposes other than what they have purchased it for, and also we cannot share card details, and we cannot tell customers to do anything like input their ssn  or credit card details or passwords
>
> update mcp_server/README.md so the tool list matches what we have now

## Problem 6: Plan the three tickets

**Initial prompt:**

> ok problem 6: plan the three tickets
> build output/desk_tickets.html — a page i can double click open with one tab per ticket (101, 102, 103). also add empty Cash and Reflection tabs for later problems (leave them blank or put a short "coming later" note for now)
> on each ticket tab, fill an Expected section only (leave room for an Actual section i will fill after the agents actually run)
> for each ticket's expected section:
>
> * who the boss should call first and why
> * all the agent delegations you'd expect and why
> * which mcp tools you expect that run to use
>
> plans that send every specialist on every ticket score low. i will compare this plan to what actually happens when the agents resolve the tickets.
> use the real data, don't invent anything:
> ticket 101 — customer_order, Tauhid Zaman, Bulldog tee size S, qty 1, invoice 501
>
> stock size S is 0. invoice 501 is open $840 to Bulldog Print Co (vendor 1, apparel reprint, lead 5 days), due 2026-08-28 so it's already overdue. vendor won't ship new stuff while they have an open unpaid invoice. human approval needed for any payment.
> ticket 102 — rent_notice, Elm City Properties
>
> lease 1: Chapel Street shop, $2400/month, next due 2026-09-02 (today is 2026-08-31 so 2 days left). checking has $3400. human approval before rent gets paid.
> ticket 103 — price_override / bulk discount, Yale AI Club wants 20 navy hoodies size M
>
> unit cost $22, list $58 (never go below unit cost). we only have 8 in M so we're short 12.
> agent wiring from the team: Boss can ask Ina / Ama / Father / Jervis + the human. Ina can ask Ama. Father can ask Ama. Jervis and Ama don't ask anyone.
> tools are the real ones from the mcp server (get_ticket, get_stock, list_vendors, get_vendor_invoices, get_invoice, get_cash, get_pricing, get_lease, get_today, list_payments, record_approval, pay_invoice, pay_rent, order_stock etc). don't make up tools.
> boss loop reminder: stock/order stuff → Ina first (Ama if shortage or open invoice). rent → Father first (Ama for cash / payment prep). price/bulk → Ama for margins + Ina for stock. always end with Jervis drafting the customer message when the customer needs a reply. money only moves after human approval at the Table.
> keep the html self-contained so i can just double click it. don't run the agents, don't touch the db, don't invent data. just the one file output/desk_tickets.html.

> ok skimmed the tabs. a few fixes on the judgment calls:
>
> -ticket 101
> two separate human approvals is right — pay invoice 501 first ($840) so the vendor is clear, then order the 1 tee (~$8). cash path $3400 → $2560 → $2552 is fine. keep that.
>
> -ticket 102
> leave Jervis out. requester is the landlord (Elm City Properties), not a customer, so no customer message. Father → Ama → human → Ama pays rent. that's it.
>
> -ticket 103
> Ama first is fine (it's a price_override). stock check with Ina after.
> baseline path = **no restock, no human approval, no payment** — the ticket only asks for a bulk discount, not "order more." mark the Ina→Ama / restock stuff as optional/conditional only if Boss decides we should fill the full 20.
> don't invent a discount %. just say: price must stay ≥ unit cost ($22), Boss picks a price in that range, we can only promise the 8 we actually have in M unless we restock.
>
> tee unit cost $8 / list $28 from pricing is fine, leave it.
>
> update the Expected sections on those three tabs to match the above. don't touch Cash or Reflection. don't run agents, don't touch the db.

## Problem 7: Backend routes

**Initial prompt:**

> ok problem 7: backend routes
> the react frontend dashboard (the next problem) needs a backend it can call. in backend/main.py, use fastapi and add routes that do the following:
>
> * return the three tickets and whether each is open or resolved
> * take a ticket id and run your agent team on that ticket
> * return recent agent events which is what each agent said and which tools they used so the board can refresh
> * approve a payment or purchase after a human clicks approve (agents only prepare the pay; this route is what actually changes cash)
> * return the current checking balance from cash_accounts
> * reset the database to the original values when you want to try a fresh run
>
> from the backend/ folder, start the server with:
> uvicorn main:app --reload --port 8000
> that turns on the backend at http://localhost:8000 so the frontend dashboard can call it.
> in output/harness.md list each route in one line (what url / what it does).
> wire it to the existing stuff :  team.py, shop_db.py, the mcp server, audit trail, etc. DO NOTTT invent a second shop layer. keep it simple, don't build anything beyond what's asked. don't touch the frontend yet, that's next yar yar now do this bru

## Problem 8: Agent dashboard

**Initial prompt:**

> ok problem 8: agent dashboard
> build the frontend dashboard in frontend/ with react + vite + typescript. the page should call the routes we made in problem 7 (backend at http://localhost:8000).
> at minimum the board should:
>
> * list all three tickets
> * let you pick one ticket and start the agent team on it
> * show each agent and what they are saying / doing while the ticket runs
> * mark a ticket resolved when the run finishes
> * show a short summary of what each agent did on that ticket
> * let a human approve a pay or purchase when asked
> * show the checking balance (it should drop after an approved pay)
>
> tell the frontend to talk to the backend at http://localhost:8000. on the backend, allow the vite page origin (usually http://localhost:5173) so the browser is allowed to call those routes.
> start the board with:
> npm run dev
> this opens the React desk in the browser so you can pick tickets and watch agents.
> write output/design.md with what you chose for the dashboard look (layout, how agents read differently, how resolved tickets and cash show up) and why,  including the creative choices that make it feel special and something a human would actually enjoy using.
> be creative with the look and feel — campus customs is a small campus shop, not a boring admin panel. make the agents feel like real people at a desk (boss, ina, ama, father, jervis), make the live run readable, and make approve / cash / resolved feel clear and obvious. don't invent new backend routes; only use what problem 7 already has. keep it simple enough that npm run dev just works.
>
> i also want each agent to have a distinct color and avatar with their name plate , so theyre like a dysfunctional family: - overall feel: New England home office / warm shop desk — wood tones, calm light, not a corporate. reference vibe: https://theinspiredroom.net/dream-house-tour-new-england-style/
> - each agent has a distinct color + simple avatar/nameplate so they read as a dysfunctional family at a desk:
>   - Boss = old grandfather / Succession patriarch energy, oak color (same as the table)
>   - Ina = 50-year-old woman with glasses, navy blue
>   - Ama = glasses, rounder face, red
>   - Father = grumpy older man (younger than Boss), stubble, big nose, green; has a coffee cup that is steamy only while he is working
>   - Jervis = formal butler, mustache, bald, grey
> - avatars can be simple illustrations or stylized icons (no real photos, no external image APIs)
> - make the live run readable, and make approve / cash / resolved feel clear and obvious

## Problem 9: Resolve the tickets

**Initial prompt:**

> ok problem 9: resolve the tickets
> before testing the agents on a full run over the three tickets, reset the working database data/campus_customs_new.db again so you start clean. note the starting checking balance. then run all three tickets on the board (101, 102, 103) until each is resolved.
> open output/desk_tickets.html from problem 6. on each ticket tab, fill the Actual section from this run: which agents worked, what they delegated, and which tools they used. keep your Expected section so you can compare the two.
> on the Cash tab of the same output/desk_tickets.html, itemize the money:
> -starting checking balance (after the reset)
> -for each ticket: how cash changed when that ticket resolved, and why (which pay / purchase, dollar amount)
> -ending checking balance - it must match cash_accounts in the working database
> wrong cash math loses points even if the board shows every ticket resolved. also save:
> -output/resolved_tickets.json - for each ticket: id, final status, short outcome, what each agent contributed, and any human approvals
> -output/resolved_board.html - a page you can double-click with a screenshot of your React board for
> -each resolved ticket (101, 102, and 103)
> append real runs to output/audit_trail.json. finish output/harness.md so it covers tables, MCP tools, the five agents, API routes, the dashboard, and safety rules.
> dont invent numbers - only use what the tools and the database actually return. if a pay gets refused or denied, record that honestly in Actual and in the cash tab. like be real about it.

> small fixes:
>
> -the tickets sometimes trail off and just do an elipsis, make sure the full ticket text can be seen at least on the sidebar ticket thing
> -jarvis doesnt need to tell the customer everything. if something  is out of stock leave it at Hello, The Classic Bulldog Tee in white, size S (SKU CC-TEE-WHITE), is currently unavailable because we have no stock.We'll be restocking soon! please wait for alerts
> -make a deny button for requests for the human and make the approve button and thte deny button netural grays

## Problem 10: Reflection

**Initial prompt:**

> ok problem 10: reflection
> open output/desk_tickets.html and fill the Reflection tab. use the Expected vs Actual sections already on the ticket tabs and the Cash tab numbers as evidence. every answer has to point at something real from this app - a ticket id, an agent name, a tool, a dollar amount, a delegation that happened or didnt. put my answers on there
> How would you evaluate the performance of the agents on each ticket and why?
> I like how it did !! so good, im proud of my bots. On ticket 101 the Boss called Ina first for CC-TEE-WHITE size S (0 on hand), invoice 501 got paid ($840) then the $8 tee order went through, and Father stayed out of it like he should. On 102 Father got the lease right ($2400 due 2026-09-02) and rent paid, cash 2552 → 152. On 103 the price floor ($22) and the 8-of-20 stock gap showed up correctly. I didnt like Jervis original response so annoyingly i had to write that part myself, but look at the little guys they look so cute on the board
>
> For each ticket, how did Actual compare to the Expected plan you wrote earlier?
> The agents under the Boss sometimes didnt know how to talk to each other. On 101 and 102 the plan said Ina → Ama or Father → Ama, but in the Actual runs Ina and Ama mostly deferred upward, so the Boss had to ask Ama directly in parallel (those Boss → Ama calls were not in Expected). On 101 the rest matched: pay invoice 501 then order the tee, Father not called. On 102 the plan said no Jervis (requester is the landlord), but the Boss still called him anyway. So Expected was mostly right on who owns what, Actual showed the Boss doing extra solo asks because the specialists werent chatting sideways as much
>
> What would have been simpler as one agent with tools - and why?
> With one agent it wouldve been easier and cost less tokens. Accounting Ama exists because no one else can read cash (get_cash, pay_invoice, pay_rent, order_stock), so every money question burns extra tokens bouncing through him. But that split is also safer because when cash went 3400 → 2560 → 2552 on 101 and then 2552 → 152 on 102, i can point at Ama (and the backend approve route that actually called the pay tools) instead of blaming big ai for ruining my career
>
> Three new problems this agent team could solve with the tools you built
> 1. Rush of orders during orientation so same path as 101 and 103: get_ticket, get_stock, get_pricing, draft a reply with Jervis, human approve if anything needs ordering
> 2. Shop closure from rain, flood, or earthquake  tickets come in like the open ones on the board, agents read them with get_ticket and reply with what stock is still on the shelves
> 3. Rent payment apps go bust or mail isnt working,  landlord sends a rent_notice like ticket 102, Father pulls the lease, Ama checks cash, human approves, pay_rent runs
> 4.
>
> Three new problems this team could not solve, and what youd need
> 1. Directing where to place stock at the supplier, right now order_stock only pays and notes lead_days. We dont tell the vendor a warehouse or storage unit. Would need a tool that sends put-away location to the vendor and maybe a receiving agent that owns it
> 2. Updating customers when a shipment will actually arrive - we have lead_days from list_vendors but no email or sms tool. Would need a notify_customer tool and Jervis (or a new agent) allowed to send it unlike boss sending it out each time
> 3. Auto-updating inventory spreadsheets so inventory only moves when someone runs tools by hand. Would need a tool that watches a folder for a new spreadsheet and writes into the inventory table.

> ok this is how the file for hw5 should be lookin
> (Pasted a screenshot of the expected hw5/ file layout: AI_prompts.md, requirements.txt, .env.example, .gitignore, .mcp.json, README.md, data/{campus_customs.db, campus_customs_new.db}, mcp_server/{server.py, README.md}, frontend/, backend/{main.py, models.py, prompts/{boss,inventory,accounting,facilities,customer_service}.md}, output/{harness.md, mcp_smoke.json, desk_tickets.html, design.md, resolved_tickets.json, resolved_board.html, audit_trail.json, github_url.txt}. README should explain: copy original DB to the working copy when you need a clean run, start MCP server, start FastAPI backend, start the React board, reset the DB before a full three-ticket run.)

## Problem 11: Submit to GitHub

**Initial prompt:**

> oh btw this is problem 11: submit to github

> ok now recheck, what else is needed

> but if i upload this onto git do i still need git, yeah delete.venv

> i wanna drag everything in though

> wait can we try running this stuff again so i can retry ticket 101

> wait like i wanna do it without changing any of the recorded files
> i just wanna see new jervis reply

> can you open it up

> no i wanna see the little agents

> ugh cant i get the actual table again
