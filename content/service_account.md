# Service accounts

A service account is a user that is a program rather than a person. A script, a scheduled job
or a back-end integration uses one to call the Search2o API on its own behalf, with a key
instead of a password.

A service account has its own **role** — user, developer or administrator — and can do what
that role allows. It cannot be an account owner. It is independent of how people sign in:
turning password sign-in off, or turning single sign-on on, does not affect it.

Service accounts are managed by administrators, on the **Service accounts** page under
**Admin** in the menu.

## Service accounts and integration tokens

Search2o has two kinds of long-lived credential. Use the one that matches what the program is.

| | Integration token | Service account |
| --- | --- | --- |
| Acts as | one person, in their name | itself, as a member of the account |
| Role | always `user` | its own role, chosen by an administrator |
| Created by | the person, from their Profile page | an administrator, on the Service accounts page |
| Typical use | a chat bot acting for the person who is chatting | a script, a scheduled job, a back-end integration |

## Add a service account

1. Open **Admin → Service accounts**.
2. Enter a **Name**. It identifies the service account on this page and must be unique in
   your account. Use letters and digits, with `_`, `-` or `.` between them, starting and
   ending with a letter or digit — for example `daily_sync`, `billing-export` or `ci.deploy`.
   Up to 64 characters.
3. Choose a **Role**: User, Developer or Administrator. Give it the least it needs; the role
   can be changed later.
4. Optionally enter an **Email**. If you leave it empty the service account is given
   `<name>@service` — for example `daily_sync@service` — which receives no mail. If you enter
   a real address, it must not already belong to a user.
5. Select **Create**.

The key appears in a highlighted panel at the top of the list, labelled with the service
account's name.

**Copy the key now. It is shown only this once and is stored nowhere in Search2o.** Select
**Copy key** and put it straight into wherever the program reads its secrets — a secret
manager, or an environment variable on the machine that runs it. Do not paste it into a chat
message, a ticket or source control.

The key stays on the page until you leave it, rotate another key, or delete that service
account. If it is lost, you cannot get it back: rotate the key instead (see below).

## Use the key

The program sends the key with **every** request, in an `Authorization` header:

    Authorization: Bearer <key>

There is no sign-in call and no session. Every call to your agent server's API is a `POST`
with a JSON body; for example, finding an agent for a question:

```
curl -X POST https://search2o.example.com/api/exec/search \
  -H "Authorization: Bearer $SEARCH2O_SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our travel expense policy?"}'
```

What the call may do is decided by the service account's role, exactly as it is for a person
with that role. A few things only a person can do — such as changing their own password —
are refused for a service account whatever its role.

A key does not expire. It stops working only when it is rotated or the service account is
deleted. A request with a key that no longer works is refused as unauthorized; if that
happens unexpectedly, check whether someone rotated the key.

A service account's calls count towards your account's usage like anyone else's.

## Change a service account's role

In the list, choose a new role in the service account's **Role** column. The change applies
to the next call the program makes. Any role except owner can be chosen.

## Rotate a key

Rotate a key when it has been lost, when it may have been exposed, or as routine hygiene.

1. In the list, select **Rotate key** on the service account's row.
2. Confirm. **The current key stops working immediately**, so anything still using it is
   refused until it is given the new one.
3. The new key appears in the panel, labelled **New key for** the service account. Copy it,
   as when the account was created, and update the program.

A service account has one key at a time. If a program must keep running without a gap,
update it as soon as you rotate.

## Delete a service account

1. In the list, select **Delete** on the service account's row.
2. Confirm. Its key stops working immediately, and the service account cannot be recovered.

If you need the program to work again later, create a new service account and give the
program the new key.

## Good practice

- Create one service account per program, so each can be rotated or deleted without
  affecting the others, and its role can be as small as that program needs.
- Keep keys in a secret manager, never in code.
- Rotate a key whenever someone who had access to it leaves, or if it may have been exposed.
- Removing a person from Search2o, or from your identity provider, does not affect service
  accounts. Review the Service accounts page when people with access to keys leave.
