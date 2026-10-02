# PM-Bench score report

## Summary

Hit: 77 | Late: 0 | Miss: 4 | False alarms: 3 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 877 | check_time calls: 77 | Actions: 80
Exact-set: matches 74 | mismatches 6 | reward 68
Set micro: TP 77 | FP 3 | FN 4
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 95.1% | late 0.0% | miss 4.9% | false alarm/step 3.8% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 2.5% | cross-day miss 0.0% | update miss 11.1% | precision_hit 96.2% | precision_any 96.2% | exact-set match rate 92.5% | exact-set avg reward 0.850 | set_precision 96.2% | set_recall 95.1% | set_f1 95.7%
Hit rates (by modality): event 93.0% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T13:03:19.323Z |
| Finished (UTC) | 2026-09-13T13:12:50.731Z |
| Duration | 9m 31.4s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 77 |
| Late | 0 |
| Miss | 4 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 877 |
| Check_time calls | 77 |
| Actions | 80 |
| Exact-set matches | 74 |
| Exact-set mismatches | 6 |
| Exact-set reward | 68 |
| Set TP | 77 |
| Set FP | 3 |
| Set FN | 4 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 80 |
| bank_balance | 80 |
| calendar | 80 |
| clock | 77 |
| course_portal | 80 |
| email | 80 |
| laundry_status | 80 |
| library_hold | 80 |
| price_tracker | 80 |
| reservation_waitlist | 80 |
| shipment_status | 80 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 95.1% |
| Late rate | 0.0% |
| Miss rate | 4.9% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 2.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 96.2% |
| Precision any | 96.2% |
| Exact-set match rate | 92.5% |
| Exact-set avg reward | 0.850 |
| Set precision | 96.2% |
| Set recall | 95.1% |
| Set F1 | 95.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 53 | 57 | 93.0% |
| Time (time + time_check) | 24 | 24 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 40 | 0 | 2 | 42 | 95.2% | 95.2% |
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
| email | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| library_hold | 3 | 0 | 0 | 3 | 100.0% | 100.0% |
| shipment_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 12 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Tuesday | 10 | 0 | 1 | 90.9% | 0.0% | 9.1% | 0.0% | 0.0% | 85.7% | 100.0% | 100.0% | 85.7% | 92.3% | 0.846 | 100.0% | 90.9% | 95.2% |
| Wednesday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Thursday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 9.1% | 9.1% | 88.9% | 100.0% | 87.5% | 100.0% | 81.8% | 0.636 | 91.7% | 91.7% | 91.7% |
| Friday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 16.7% | 8.3% | 75.0% | 100.0% | 83.3% | 83.3% | 75.0% | 0.500 | 83.3% | 83.3% | 83.3% |
| Saturday | 14 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Sunday | 9 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 13 |
| Monday | bank_balance | 13 |
| Monday | calendar | 13 |
| Monday | clock | 12 |
| Monday | course_portal | 13 |
| Monday | email | 13 |
| Monday | laundry_status | 13 |
| Monday | library_hold | 13 |
| Monday | price_tracker | 13 |
| Monday | reservation_waitlist | 13 |
| Monday | shipment_status | 13 |
| Tuesday | appointment_portal | 13 |
| Tuesday | bank_balance | 13 |
| Tuesday | calendar | 13 |
| Tuesday | clock | 12 |
| Tuesday | course_portal | 13 |
| Tuesday | email | 13 |
| Tuesday | laundry_status | 13 |
| Tuesday | library_hold | 13 |
| Tuesday | price_tracker | 13 |
| Tuesday | reservation_waitlist | 13 |
| Tuesday | shipment_status | 13 |
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
| Thursday | appointment_portal | 11 |
| Thursday | bank_balance | 11 |
| Thursday | calendar | 11 |
| Thursday | clock | 11 |
| Thursday | course_portal | 11 |
| Thursday | email | 11 |
| Thursday | laundry_status | 11 |
| Thursday | library_hold | 11 |
| Thursday | price_tracker | 11 |
| Thursday | reservation_waitlist | 11 |
| Thursday | shipment_status | 11 |
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
| Saturday | appointment_portal | 10 |
| Saturday | bank_balance | 10 |
| Saturday | calendar | 10 |
| Saturday | clock | 9 |
| Saturday | course_portal | 10 |
| Saturday | email | 10 |
| Saturday | laundry_status | 10 |
| Saturday | library_hold | 10 |
| Saturday | price_tracker | 10 |
| Saturday | reservation_waitlist | 10 |
| Saturday | shipment_status | 10 |
| Sunday | appointment_portal | 11 |
| Sunday | bank_balance | 11 |
| Sunday | calendar | 11 |
| Sunday | clock | 11 |
| Sunday | course_portal | 11 |
| Sunday | email | 11 |
| Sunday | laundry_status | 11 |
| Sunday | library_hold | 11 |
| Sunday | price_tracker | 11 |
| Sunday | reservation_waitlist | 11 |
| Sunday | shipment_status | 11 |
