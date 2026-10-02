# PM-Bench score report

## Summary

Hit: 76 | Late: 0 | Miss: 5 | False alarms: 0 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 0 | state query calls: 607 | check_time calls: 77 | Actions: 76
Exact-set: matches 76 | mismatches 4 | reward 72
Set micro: TP 76 | FP 0 | FN 5
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 0
Rates: hit 93.8% | late 0.0% | miss 6.2% | false alarm/step 0.0% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 0.0% | cross-day miss 0.0% | update miss 11.1% | precision_hit 100.0% | precision_any 100.0% | exact-set match rate 95.0% | exact-set avg reward 0.900 | set_precision 100.0% | set_recall 93.8% | set_f1 96.8%
Hit rates (by modality): event 91.2% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T14:42:53.539Z |
| Finished (UTC) | 2026-09-13T14:51:10.379Z |
| Duration | 8m 16.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 76 |
| Late | 0 |
| Miss | 5 |
| False alarms | 0 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 0 |
| State query calls | 607 |
| Check_time calls | 77 |
| Actions | 76 |
| Exact-set matches | 76 |
| Exact-set mismatches | 4 |
| Exact-set reward | 72 |
| Set TP | 76 |
| Set FP | 0 |
| Set FN | 5 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 53 |
| bank_balance | 53 |
| calendar | 53 |
| clock | 77 |
| course_portal | 53 |
| email | 53 |
| laundry_status | 53 |
| library_hold | 53 |
| price_tracker | 53 |
| reservation_waitlist | 53 |
| shipment_status | 53 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 93.8% |
| Late rate | 0.0% |
| Miss rate | 6.2% |
| False alarm/step | 0.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 0.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 100.0% |
| Precision any | 100.0% |
| Exact-set match rate | 95.0% |
| Exact-set avg reward | 0.900 |
| Set precision | 100.0% |
| Set recall | 93.8% |
| Set F1 | 96.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 52 | 57 | 91.2% |
| Time (time + time_check) | 24 | 24 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 4 | 42 | 90.5% | 90.5% |
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
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 75.0% | 75.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Friday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 0.0% | 0.0% | 87.5% | 100.0% | 83.3% | 100.0% | 91.7% | 0.833 | 100.0% | 91.7% | 95.7% |
| Saturday | 14 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Sunday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 80.0% | 100.0% | 75.0% | 100.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |

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
| Friday | appointment_portal | 12 |
| Friday | bank_balance | 12 |
| Friday | calendar | 12 |
| Friday | clock | 12 |
| Friday | course_portal | 12 |
| Friday | email | 12 |
| Friday | laundry_status | 12 |
| Friday | library_hold | 12 |
| Friday | price_tracker | 12 |
| Friday | reservation_waitlist | 12 |
| Friday | shipment_status | 12 |
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
