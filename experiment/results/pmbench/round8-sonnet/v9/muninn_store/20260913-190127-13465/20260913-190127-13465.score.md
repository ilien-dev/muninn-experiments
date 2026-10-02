# PM-Bench score report

## Summary

Hit: 79 | Late: 0 | Miss: 2 | False alarms: 0 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 0 | state query calls: 597 | check_time calls: 77 | Actions: 79
Exact-set: matches 79 | mismatches 1 | reward 78
Set micro: TP 79 | FP 0 | FN 2
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 9 | late 0 | miss 0 | canceled 2 | total 11 | violations 0
Rates: hit 97.5% | late 0.0% | miss 2.5% | false alarm/step 0.0% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 0.0% | cross-day miss 0.0% | update miss 0.0% | precision_hit 100.0% | precision_any 100.0% | exact-set match rate 98.8% | exact-set avg reward 0.975 | set_precision 100.0% | set_recall 97.5% | set_f1 98.8%
Hit rates (by modality): event 96.5% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:27.732Z |
| Finished (UTC) | 2026-09-14T01:13:39.462Z |
| Duration | 12m 11.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 79 |
| Late | 0 |
| Miss | 2 |
| False alarms | 0 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 0 |
| State query calls | 597 |
| Check_time calls | 77 |
| Actions | 79 |
| Exact-set matches | 79 |
| Exact-set mismatches | 1 |
| Exact-set reward | 78 |
| Set TP | 79 |
| Set FP | 0 |
| Set FN | 2 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 52 |
| bank_balance | 52 |
| calendar | 52 |
| clock | 77 |
| course_portal | 52 |
| email | 52 |
| laundry_status | 52 |
| library_hold | 52 |
| price_tracker | 52 |
| reservation_waitlist | 52 |
| shipment_status | 52 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 97.5% |
| Late rate | 0.0% |
| Miss rate | 2.5% |
| False alarm/step | 0.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 0.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 100.0% |
| Precision any | 100.0% |
| Exact-set match rate | 98.8% |
| Exact-set avg reward | 0.975 |
| Set precision | 100.0% |
| Set recall | 97.5% |
| Set F1 | 98.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 55 | 57 | 96.5% |
| Time (time + time_check) | 24 | 24 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 41 | 0 | 1 | 42 | 97.6% | 97.6% |
| proactive_monitoring_required | 38 | 0 | 1 | 39 | 97.4% | 97.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 3 | 0 | 0 | 3 | 100.0% | 100.0% |
| bank_balance | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| calendar | 3 | 0 | 0 | 3 | 100.0% | 100.0% |
| clock | 24 | 0 | 0 | 24 | 100.0% | 100.0% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| library_hold | 3 | 0 | 0 | 3 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 12 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Tuesday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Wednesday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Thursday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 77.8% | 100.0% | 87.5% | 75.0% | 90.9% | 0.818 | 100.0% | 83.3% | 90.9% |
| Friday | 12 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Saturday | 14 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Sunday | 9 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 10 |
| Monday | bank_balance | 10 |
| Monday | calendar | 10 |
| Monday | clock | 12 |
| Monday | course_portal | 10 |
| Monday | email | 10 |
| Monday | laundry_status | 10 |
| Monday | library_hold | 10 |
| Monday | price_tracker | 10 |
| Monday | reservation_waitlist | 10 |
| Monday | shipment_status | 10 |
| Tuesday | appointment_portal | 9 |
| Tuesday | bank_balance | 9 |
| Tuesday | calendar | 9 |
| Tuesday | clock | 12 |
| Tuesday | course_portal | 9 |
| Tuesday | email | 9 |
| Tuesday | laundry_status | 9 |
| Tuesday | library_hold | 9 |
| Tuesday | price_tracker | 9 |
| Tuesday | reservation_waitlist | 9 |
| Tuesday | shipment_status | 9 |
| Wednesday | appointment_portal | 9 |
| Wednesday | bank_balance | 9 |
| Wednesday | calendar | 9 |
| Wednesday | clock | 10 |
| Wednesday | course_portal | 9 |
| Wednesday | email | 9 |
| Wednesday | laundry_status | 9 |
| Wednesday | library_hold | 9 |
| Wednesday | price_tracker | 9 |
| Wednesday | reservation_waitlist | 9 |
| Wednesday | shipment_status | 9 |
| Thursday | clock | 11 |
| Friday | appointment_portal | 11 |
| Friday | bank_balance | 11 |
| Friday | calendar | 11 |
| Friday | clock | 12 |
| Friday | course_portal | 11 |
| Friday | email | 11 |
| Friday | laundry_status | 11 |
| Friday | library_hold | 11 |
| Friday | price_tracker | 11 |
| Friday | reservation_waitlist | 11 |
| Friday | shipment_status | 11 |
| Saturday | appointment_portal | 6 |
| Saturday | bank_balance | 6 |
| Saturday | calendar | 6 |
| Saturday | clock | 9 |
| Saturday | course_portal | 6 |
| Saturday | email | 6 |
| Saturday | laundry_status | 6 |
| Saturday | library_hold | 6 |
| Saturday | price_tracker | 6 |
| Saturday | reservation_waitlist | 6 |
| Saturday | shipment_status | 6 |
| Sunday | appointment_portal | 7 |
| Sunday | bank_balance | 7 |
| Sunday | calendar | 7 |
| Sunday | clock | 11 |
| Sunday | course_portal | 7 |
| Sunday | email | 7 |
| Sunday | laundry_status | 7 |
| Sunday | library_hold | 7 |
| Sunday | price_tracker | 7 |
| Sunday | reservation_waitlist | 7 |
| Sunday | shipment_status | 7 |
