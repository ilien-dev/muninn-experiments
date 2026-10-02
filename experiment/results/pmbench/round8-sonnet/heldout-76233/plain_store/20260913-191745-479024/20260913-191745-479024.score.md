# PM-Bench score report

## Summary

Hit: 72 | Late: 0 | Miss: 7 | False alarms: 1 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 1 | state query calls: 734 | check_time calls: 74 | Actions: 73
Exact-set: matches 69 | mismatches 7 | reward 62
Set micro: TP 72 | FP 1 | FN 7
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 91.1% | late 0.0% | miss 8.9% | false alarm/step 1.3% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 1.3% | cross-day miss 0.0% | update miss 11.1% | precision_hit 98.6% | precision_any 98.6% | exact-set match rate 90.8% | exact-set avg reward 0.816 | set_precision 98.6% | set_recall 91.1% | set_f1 94.7%
Hit rates (by modality): event 87.0% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:17:45.728Z |
| Finished (UTC) | 2026-09-14T01:25:33.905Z |
| Duration | 7m 48.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 72 |
| Late | 0 |
| Miss | 7 |
| False alarms | 1 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 1 |
| State query calls | 734 |
| Check_time calls | 74 |
| Actions | 73 |
| Exact-set matches | 69 |
| Exact-set mismatches | 7 |
| Exact-set reward | 62 |
| Set TP | 72 |
| Set FP | 1 |
| Set FN | 7 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 66 |
| bank_balance | 66 |
| calendar | 66 |
| clock | 74 |
| course_portal | 66 |
| email | 66 |
| laundry_status | 66 |
| library_hold | 66 |
| price_tracker | 66 |
| reservation_waitlist | 66 |
| shipment_status | 66 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 91.1% |
| Late rate | 0.0% |
| Miss rate | 8.9% |
| False alarm/step | 1.3% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 1.3% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 98.6% |
| Precision any | 98.6% |
| Exact-set match rate | 90.8% |
| Exact-set avg reward | 0.816 |
| Set precision | 98.6% |
| Set recall | 91.1% |
| Set F1 | 94.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 47 | 54 | 87.0% |
| Time (time + time_check) | 25 | 25 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 35 | 0 | 5 | 40 | 87.5% | 87.5% |
| proactive_monitoring_required | 37 | 0 | 2 | 39 | 94.9% | 94.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 2 | 0 | 2 | 4 | 50.0% | 50.0% |
| bank_balance | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| calendar | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| clock | 25 | 0 | 0 | 25 | 100.0% | 100.0% |
| email | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| laundry_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| library_hold | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| price_tracker | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| shipment_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Tuesday | 13 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Wednesday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 0.0% | 0.0% | 85.7% | 100.0% | 75.0% | 100.0% | 90.0% | 0.800 | 100.0% | 90.0% | 94.7% |
| Thursday | 12 | 0 | 1 | 92.3% | 0.0% | 7.7% | 0.0% | 0.0% | 88.9% | 100.0% | 85.7% | 100.0% | 88.9% | 0.778 | 100.0% | 92.3% | 96.0% |
| Friday | 10 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Saturday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 0.0% | 0.0% | 62.5% | 100.0% | 83.3% | 50.0% | 83.3% | 0.667 | 100.0% | 70.0% | 82.4% |
| Sunday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 7.7% | 7.7% | 75.0% | 100.0% | 71.4% | 100.0% | 76.9% | 0.538 | 90.9% | 83.3% | 87.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 6 |
| Monday | bank_balance | 6 |
| Monday | calendar | 6 |
| Monday | clock | 11 |
| Monday | course_portal | 6 |
| Monday | email | 6 |
| Monday | laundry_status | 6 |
| Monday | library_hold | 6 |
| Monday | price_tracker | 6 |
| Monday | reservation_waitlist | 6 |
| Monday | shipment_status | 6 |
| Tuesday | appointment_portal | 8 |
| Tuesday | bank_balance | 8 |
| Tuesday | calendar | 8 |
| Tuesday | clock | 10 |
| Tuesday | course_portal | 8 |
| Tuesday | email | 8 |
| Tuesday | laundry_status | 8 |
| Tuesday | library_hold | 8 |
| Tuesday | price_tracker | 8 |
| Tuesday | reservation_waitlist | 8 |
| Tuesday | shipment_status | 8 |
| Wednesday | appointment_portal | 10 |
| Wednesday | bank_balance | 10 |
| Wednesday | calendar | 10 |
| Wednesday | clock | 10 |
| Wednesday | course_portal | 10 |
| Wednesday | email | 10 |
| Wednesday | laundry_status | 10 |
| Wednesday | library_hold | 10 |
| Wednesday | price_tracker | 10 |
| Wednesday | reservation_waitlist | 10 |
| Wednesday | shipment_status | 10 |
| Thursday | appointment_portal | 8 |
| Thursday | bank_balance | 8 |
| Thursday | calendar | 8 |
| Thursday | clock | 9 |
| Thursday | course_portal | 8 |
| Thursday | email | 8 |
| Thursday | laundry_status | 8 |
| Thursday | library_hold | 8 |
| Thursday | price_tracker | 8 |
| Thursday | reservation_waitlist | 8 |
| Thursday | shipment_status | 8 |
| Friday | appointment_portal | 9 |
| Friday | bank_balance | 9 |
| Friday | calendar | 9 |
| Friday | clock | 10 |
| Friday | course_portal | 9 |
| Friday | email | 9 |
| Friday | laundry_status | 9 |
| Friday | library_hold | 9 |
| Friday | price_tracker | 9 |
| Friday | reservation_waitlist | 9 |
| Friday | shipment_status | 9 |
| Saturday | appointment_portal | 12 |
| Saturday | bank_balance | 12 |
| Saturday | calendar | 12 |
| Saturday | clock | 12 |
| Saturday | course_portal | 12 |
| Saturday | email | 12 |
| Saturday | laundry_status | 12 |
| Saturday | library_hold | 12 |
| Saturday | price_tracker | 12 |
| Saturday | reservation_waitlist | 12 |
| Saturday | shipment_status | 12 |
| Sunday | appointment_portal | 13 |
| Sunday | bank_balance | 13 |
| Sunday | calendar | 13 |
| Sunday | clock | 12 |
| Sunday | course_portal | 13 |
| Sunday | email | 13 |
| Sunday | laundry_status | 13 |
| Sunday | library_hold | 13 |
| Sunday | price_tracker | 13 |
| Sunday | reservation_waitlist | 13 |
| Sunday | shipment_status | 13 |
