# CPL PRACTICE 2.0 — DATABASE BACKUP & DISASTER RECOVERY POLICY (Feature D6)

## 1. Executive Summary
This document outlines the backup, retention, and disaster recovery strategy for **CPL Practice 2.0 — DGCA Commercial Pilot Licence Examination Preparation Platform**.

The database houses critical DGCA examination assets, including:
- 959 authoritative DGCA questions across 6 core aeronautical subjects.
- 95 syllabus chapters and topics with 285 tracking milestones.
- Student authentication credentials, profiles, and study streaks.
- Examination attempt histories, student answers, and zero-repeat exposure tables.
- Mistake notebook entries and Leitner-spaced repetition queues.

---

## 2. Backup Frequency & Retention Architecture

| Tier | Frequency | Retention Window | Storage Medium | Verification Mode |
|---|---|---|---|---|
| **Real-Time WAL Archiving** | Continuous (Every commit) | 7 Days (Point-In-Time) | PostgreSQL WAL Storage | Automated checksum |
| **Automated Daily Snapshot** | Daily at 02:00 UTC | 30 Days | Encrypted Cloud Object Storage | SHA-256 Manifest Check |
| **Monthly Milestone Archive** | 1st of each calendar month | 12 Months | Cold Glacier / Offsite Archive | Dry-run staging restore |
| **Pre-Migration Snapshot** | Prior to any schema migration | Indefinite | Version-Controlled Repository | Hash-verified JSON/SQL |

---

## 3. Automated Backup Script

An automated export script is provided in `scripts/backup_database.py`.

### Execution:
```bash
python scripts/backup_database.py
```

### Outputs Generated:
- `backups/cpl_practice_backup_<timestamp>.json`
- `backups/MANIFEST.txt` (Maintains cryptographic SHA-256 verification hashes for every dump)

---

## 4. Disaster Recovery & Restoration Procedure

In the event of database corruption, accidental deletion, or disaster recovery, follow this protocol:

### Step 1: Isolate the Incident
1. Temporarily place the application in maintenance mode or route traffic to offline fallback bundles (`cpl-exam-direct.html`).
2. Identify the target restoration point (e.g. timestamp before the anomaly).

### Step 2: Validate Target Backup Manifest
Verify the SHA-256 hash of the chosen backup file against `backups/MANIFEST.txt`:
```bash
certutil -hashfile backups/cpl_practice_backup_YYYYMMDD_HHMMSS.json SHA256
```

### Step 3: Execute Controlled Staging Restore
Never restore directly into production without verifying in a staging container or schema:
```bash
# Seed local or staging database
psql -h <host> -U postgres -d cpl_practice_staging -f supabase/schema.sql
psql -h <host> -U postgres -d cpl_practice_staging -f supabase/seed.sql
```

### Step 4: Run Post-Restoration Verification Suite
Execute the automated test runner to ensure zero question or relationship defects:
```bash
python scripts/test_phase1_5_features.py
python scripts/test_phase3_features.py
python scripts/test_phase4_features.py
```

### Step 5: Switch DNS / Promote Staging to Production
Once all test assertions report `[PASS]`, update connection strings and resume normal flight training operations.

---

## 5. Recovery Limitations
- **Free-Tier Limits:** Standard hosted Supabase projects on the free tier provide daily backups with 7-day retention. Point-In-Time-Recovery (PITR) requires Supabase Pro (WAL archiving enabled) or a dedicated self-hosted PostgreSQL instance.
- **Client Cache Independence:** Student examination answers in progress are safely preserved in browser local storage (`cpl_active_session`), ensuring zero in-flight data loss during transient database outages.
