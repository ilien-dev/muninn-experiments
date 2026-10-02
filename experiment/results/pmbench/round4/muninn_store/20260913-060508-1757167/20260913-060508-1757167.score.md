# PM-Bench score report

## Summary

Hit: 73 | Late: 1 | Miss: 7 | False alarms: 3 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 597 | check_time calls: 77 | Actions: 77
Exact-set: matches 69 | mismatches 11 | reward 58
Set micro: TP 73 | FP 4 | FN 8
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 90.1% | late 1.2% | miss 8.6% | false alarm/step 3.8% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 5.0% | cross-day miss 0.0% | update miss 11.1% | precision_hit 94.8% | precision_any 96.1% | exact-set match rate 86.2% | exact-set avg reward 0.725 | set_precision 94.8% | set_recall 90.1% | set_f1 92.4%
Hit rates (by modality): event 86.0% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T12:05:08.898Z |
| Finished (UTC) | 2026-09-13T12:14:32.102Z |
| Duration | 9m 23.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 73 |
| Late | 1 |
| Miss | 7 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 597 |
| Check_time calls | 77 |
| Actions | 77 |
| Exact-set matches | 69 |
| Exact-set mismatches | 11 |
| Exact-set reward | 58 |
| Set TP | 73 |
| Set FP | 4 |
| Set FN | 8 |

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
| Hit rate | 90.1% |
| Late rate | 1.2% |
| Miss rate | 8.6% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 5.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 94.8% |
| Precision any | 96.1% |
| Exact-set match rate | 86.2% |
| Exact-set avg reward | 0.725 |
| Set precision | 94.8% |
| Set recall | 90.1% |
| Set F1 | 92.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 49 | 57 | 86.0% |
| Time (time + time_check) | 24 | 24 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 36 | 1 | 5 | 42 | 85.7% | 88.1% |
| proactive_monitoring_required | 37 | 0 | 2 | 39 | 94.9% | 94.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 3 | 0 | 0 | 3 | 100.0% | 100.0% |
| bank_balance | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| calendar | 2 | 0 | 1 | 3 | 66.7% | 66.7% |
| clock | 24 | 0 | 0 | 24 | 100.0% | 100.0% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| library_hold | 3 | 0 | 0 | 3 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 11 | 1 | 0 | 91.7% | 8.3% | 0.0% | 0.0% | 7.7% | 88.9% | 100.0% | 83.3% | 100.0% | 84.6% | 0.692 | 91.7% | 91.7% | 91.7% |
| Tuesday | 10 | 0 | 1 | 90.9% | 0.0% | 9.1% | 7.7% | 7.7% | 85.7% | 100.0% | 100.0% | 85.7% | 84.6% | 0.692 | 90.9% | 90.9% | 90.9% |
| Wednesday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 9.1% | 9.1% | 55.6% | 100.0% | 62.5% | 75.0% | 63.6% | 0.273 | 88.9% | 66.7% | 76.2% |
| Friday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 8.3% | 8.3% | 75.0% | 100.0% | 66.7% | 100.0% | 75.0% | 0.500 | 90.9% | 83.3% | 87.0% |
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
