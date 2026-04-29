# Restore and Sanitization

## Restore Strategy

A production-like ERPNext Helpdesk backup was restored into an isolated personal AWS staging environment.

## Restored Data

- Database backup
- Public files backup
- Site configuration backup

Private file attachments were intentionally excluded because they may contain sensitive company data.

## Safety Controls

After restore, the following were disabled:

- Incoming email accounts
- Outgoing email accounts
- Webhooks
- Notifications
- Scheduler

This prevents the staging environment from sending real emails or triggering production integrations.
