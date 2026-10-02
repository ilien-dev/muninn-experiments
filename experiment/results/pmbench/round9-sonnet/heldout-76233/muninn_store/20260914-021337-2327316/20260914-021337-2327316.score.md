# PM-Bench score report

## Summary

Hit: 70 | Late: 0 | Miss: 9 | False alarms: 2 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 584 | check_time calls: 74 | Actions: 72
Exact-set: matches 65 | mismatches 11 | reward 54
Set micro: TP 70 | FP 2 | FN 9
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 88.6% | late 0.0% | miss 11.4% | false alarm/step 2.6% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 2.6% | cross-day miss 0.0% | update miss 22.2% | precision_hit 97.2% | precision_any 97.2% | exact-set match rate 85.5% | exact-set avg reward 0.711 | set_precision 97.2% | set_recall 88.6% | set_f1 92.7%
Hit rates (by modality): event 83.3% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T08:13:37.656Z |
| Finished (UTC) | 2026-09-14T08:21:42.046Z |
| Duration | 8m 4.4s |

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
| State query calls | 584 |
| Check_time calls | 74 |
| Actions | 72 |
| Exact-set matches | 65 |
| Exact-set mismatches | 11 |
| Exact-set reward | 54 |
| Set TP | 70 |
| Set FP | 2 |
| Set FN | 9 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 51 |
| bank_balance | 51 |
| calendar | 51 |
| clock | 74 |
| course_portal | 51 |
| email | 51 |
| laundry_status | 51 |
| library_hold | 51 |
| price_tracker | 51 |
| reservation_waitlist | 51 |
| shipment_status | 51 |

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
| Update miss rate | 22.2% |
| Precision hit | 97.2% |
| Precision any | 97.2% |
| Exact-set match rate | 85.5% |
| Exact-set avg reward | 0.711 |
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
| no_proactive_monitoring | 33 | 0 | 7 | 40 | 82.5% | 82.5% |
| proactive_monitoring_required | 37 | 0 | 2 | 39 | 94.9% | 94.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 4 | 0 | 0 | 4 | 100.0% | 100.0% |
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
| Monday | 10 | 0 | 1 | 90.9% | 0.0% | 9.1% | 0.0% | 0.0% | 85.7% | 100.0% | 80.0% | 100.0% | 91.7% | 0.833 | 100.0% | 90.9% | 95.2% |
| Tuesday | 13 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Wednesday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 0.0% | 0.0% | 85.7% | 100.0% | 75.0% | 100.0% | 90.0% | 0.800 | 100.0% | 90.0% | 94.7% |
| Thursday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 0.0% | 0.0% | 77.8% | 100.0% | 71.4% | 100.0% | 77.8% | 0.556 | 100.0% | 84.6% | 91.7% |
| Friday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 83.3% | 90.0% | 0.800 | 100.0% | 90.0% | 94.7% |
| Saturday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 0.0% | 0.0% | 87.5% | 100.0% | 83.3% | 100.0% | 91.7% | 0.833 | 100.0% | 90.0% | 94.7% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 15.4% | 15.4% | 62.5% | 100.0% | 71.4% | 80.0% | 61.5% | 0.231 | 81.8% | 75.0% | 78.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 12 |
| Monday | bank_balance | 12 |
| Monday | calendar | 12 |
| Monday | clock | 11 |
| Monday | course_portal | 12 |
| Monday | email | 12 |
| Monday | laundry_status | 12 |
| Monday | library_hold | 12 |
| Monday | price_tracker | 12 |
| Monday | reservation_waitlist | 12 |
| Monday | shipment_status | 12 |
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
| Saturday | appointment_portal | 4 |
| Saturday | bank_balance | 4 |
| Saturday | calendar | 4 |
| Saturday | clock | 12 |
| Saturday | course_portal | 4 |
| Saturday | email | 4 |
| Saturday | laundry_status | 4 |
| Saturday | library_hold | 4 |
| Saturday | price_tracker | 4 |
| Saturday | reservation_waitlist | 4 |
| Saturday | shipment_status | 4 |
| Sunday | clock | 12 |
