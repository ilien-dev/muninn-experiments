# PM-Bench score report

## Summary

Hit: 70 | Late: 0 | Miss: 9 | False alarms: 2 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 604 | check_time calls: 74 | Actions: 72
Exact-set: matches 66 | mismatches 10 | reward 56
Set micro: TP 70 | FP 2 | FN 9
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 88.6% | late 0.0% | miss 11.4% | false alarm/step 2.6% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 2.6% | cross-day miss 0.0% | update miss 11.1% | precision_hit 97.2% | precision_any 97.2% | exact-set match rate 86.8% | exact-set avg reward 0.737 | set_precision 97.2% | set_recall 88.6% | set_f1 92.7%
Hit rates (by modality): event 83.3% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:08:22.973Z |
| Finished (UTC) | 2026-09-14T01:17:44.327Z |
| Duration | 9m 21.4s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 70 |
| Late | 0 |
| Miss | 9 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 604 |
| Check_time calls | 74 |
| Actions | 72 |
| Exact-set matches | 66 |
| Exact-set mismatches | 10 |
| Exact-set reward | 56 |
| Set TP | 70 |
| Set FP | 2 |
| Set FN | 9 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 53 |
| bank_balance | 53 |
| calendar | 53 |
| clock | 74 |
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
| Hit rate | 88.6% |
| Late rate | 0.0% |
| Miss rate | 11.4% |
| False alarm/step | 2.6% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 2.6% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 97.2% |
| Precision any | 97.2% |
| Exact-set match rate | 86.8% |
| Exact-set avg reward | 0.737 |
| Set precision | 97.2% |
| Set recall | 88.6% |
| Set F1 | 92.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 45 | 54 | 83.3% |
| Time (time + time_check) | 25 | 25 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 35 | 0 | 5 | 40 | 87.5% | 87.5% |
| proactive_monitoring_required | 35 | 0 | 4 | 39 | 89.7% | 89.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 2 | 0 | 2 | 4 | 50.0% | 50.0% |
| bank_balance | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| calendar | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| clock | 25 | 0 | 0 | 25 | 100.0% | 100.0% |
| email | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| laundry_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| library_hold | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| price_tracker | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Tuesday | 12 | 0 | 1 | 92.3% | 0.0% | 7.7% | 10.0% | 10.0% | 88.9% | 100.0% | 85.7% | 100.0% | 80.0% | 0.600 | 92.3% | 92.3% | 92.3% |
| Wednesday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 0.0% | 0.0% | 85.7% | 100.0% | 75.0% | 100.0% | 90.0% | 0.800 | 100.0% | 90.0% | 94.7% |
| Thursday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 0.0% | 0.0% | 77.8% | 100.0% | 71.4% | 100.0% | 77.8% | 0.556 | 100.0% | 84.6% | 91.7% |
| Friday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 83.3% | 90.0% | 0.800 | 100.0% | 90.0% | 94.7% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 50.0% | 91.7% | 0.833 | 100.0% | 80.0% | 88.9% |
| Sunday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 7.7% | 7.7% | 75.0% | 100.0% | 85.7% | 80.0% | 76.9% | 0.538 | 90.9% | 83.3% | 87.0% |

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
| Sunday | clock | 12 |
