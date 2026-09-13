# Single sign-on

By default, people sign in to Search2o with an email and a password. With single sign-on
(SSO) they sign in through your company's identity provider instead — Microsoft Entra ID,
Okta, Google Workspace, or any provider that speaks OpenID Connect. The identity provider
checks who they are; Search2o still decides everything else — whether they are a member of
your account, what role they have, and how long their session lasts.

Search2o supports OpenID Connect. Password sign-in and SSO can be used **together**: an
account keeps its password sign-in while SSO is set up and proven, and can then turn password
sign-in off so SSO is the only way in — or leave both on for good. There is no separate
account to buy and no software to install; SSO is configured on the Authentication settings
page.

## What you need before you start

- An account at your identity provider where you can register an application (this is an
  administrator task at the provider, not in Search2o).
- The address your users open Search2o at — your agent server's UI, such as
  `https://search2o.example.com/ui`. You will register this at the provider and enter it in
  Search2o, and the two must match exactly.

## Step 1 — Register an application at your identity provider

At your identity provider, create a new application (providers call it an "app registration",
"client", or "application integration"). Set it up as a **web application** using the
**authorization code flow**. When it asks for a redirect URI — also called a callback or
sign-in return URL — enter your Search2o UI address, the same one your users open:

    https://search2o.example.com/ui

The provider then gives you two things you will need: a **client ID** and a **client
secret**. Note both. The secret is shown once by most providers, so copy it before you leave
the page.

You will also need the provider's **issuer URL**. It is the base address the provider
publishes its configuration under; the exact form differs by provider (see below).

## Step 2 — Enter the details in Search2o

On the Authentication settings page, choose OpenID Connect as the single sign-on method and
fill in:

| Field | What to enter | Required |
| --- | --- | --- |
| **Issuer** | The provider's issuer URL. Search2o reads everything else about the provider from `<issuer>/.well-known/openid-configuration`, so this one address is all it needs. | Yes |
| **Client ID** | The client ID from step 1. | Yes |
| **Client secret** | The client secret from step 1. It is encrypted and never shown again; leave it blank when you edit other settings to keep the stored one. | Yes, the first time |
| **Return address** | Your Search2o UI address — the same one you registered as the redirect URI at the provider. They must match exactly, or the provider refuses the sign-in. | Yes |
| **Scopes** | What Search2o asks the provider for. The default `openid profile email` is right for almost everyone; `openid` is always required, and `email` and `profile` are what let Search2o read the person's email and name. | Default is fine |
| **Require a verified email** | On by default. The provider must state that the email address is verified. Leave it on unless your provider does not send that signal. | Default on |
| **Email claim** | Which field of the provider's response holds the email address. The default is `email`. Some providers use a different field (see below). | Default is fine |
| **Name claim** | Which field holds the person's name. The default is `name`. | Default is fine |
| **Unknown users** | What happens when someone signs in successfully but has no Search2o account yet: **Reject** (the default — an administrator adds people first) or **Create user** (a Search2o user is created automatically, with the `user` role). | Default is Reject |
| **Allowed email domains** | If set, only addresses in these domains may sign in. Leave it empty to accept any address the provider vouches for. | Optional |

The client secret is stored encrypted and is never returned by Search2o — the settings page
shows it blank once saved. To replace it, type a new one; to change anything else, leave it
blank and the stored secret is kept.

## Step 3 — Test it, then decide about passwords

Keep password sign-in **on** while you test. Save the SSO settings, then open Search2o in a
new browser session: it should offer single sign-on alongside the password form. Sign in
through your provider and confirm you land in Search2o as the right person.

Only once that works, decide whether to turn password sign-in off:

- **Leave it on** to let people use either — useful during a rollout, and necessary for
  anyone who is not in your identity provider (outside contractors), and for scripts, which
  sign in with a password and have no SSO equivalent.
- **Turn it off** so SSO is the only way in. Search2o will not let you turn it off until SSO
  is configured, because that would leave no way to sign in. There is no password back door:
  if your provider is down, nobody signs in until it is back, so turn this off only once SSO
  is proven.

## Per-provider notes

The three fields that differ by provider are the issuer, and occasionally the email claim.

**Microsoft Entra ID.** Issuer is `https://login.microsoftonline.com/<tenant-id>/v2.0`, with
your tenant's id and the `/v2.0` on the end. Entra does not always send `email`; if sign-ins
are refused for a missing email, set the email claim to `preferred_username`. Register the
redirect URI under the "Web" platform.

**Okta.** Issuer is `https://<your-org>.okta.com`, or `https://<your-org>.okta.com/oauth2/default`
if you use the default authorization server. Create an "OIDC — Web Application" and enable
the authorization code grant.

**Google Workspace.** Issuer is `https://accounts.google.com`. Create an OAuth client of type
"Web application" in the Google Cloud console.

Any other OpenID Connect provider works the same way: register a web application with your
Search2o UI address as the redirect URI, and give Search2o the issuer, client ID and secret.

## What your users see

A person opening Search2o is sent to your identity provider to sign in, and comes straight
back signed in — they never type a Search2o password. If both sign-in methods are on, they
are offered the choice.

## Roles and membership

The identity provider only says who the person is. Their **role** is set in Search2o, as it
always has been. A user created automatically by "Create user" starts with the `user` role;
an administrator promotes them from the Users page. Signing in through the provider does not
change anyone's role.

## Removing people

Search2o and your identity provider are separate. Disabling someone at the identity provider
stops them starting a new Search2o session, but it does not end sessions they already have,
and it does not revoke any integration tokens they created. When someone leaves, remove them
in Search2o as well — from the Users page.

Signing out of Search2o ends the Search2o session only; it does not sign the person out of
your identity provider.

## What Search2o stores, and where the secret lives

Search2o stores, per user, the identity provider's permanent id for that person and the
issuer, so the same email can never be quietly reassigned to a different person. The client
secret is encrypted before it is written and is never sent back out. The exchange with your
identity provider happens in Search2o Cloud; your agent server never holds the secret and
never talks to the provider.
