# PM-Bench score report

## Summary

Hit: 59 | Late: 2 | Miss: 20 | False alarms: 12 | Commission: 0 | Wrong-content: 9 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 56 | check_time calls: 35 | Actions: 73
Exact-set: matches 58 | mismatches 26 | reward 32
Set micro: TP 59 | FP 14 | FN 22
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 72.8% | late 2.5% | miss 24.7% | false alarm/step 14.3% | commission 0.0% | wrong-content 11.1% | dependency/step 0.0% | overkill/step 10.7% | cross-day miss 0.0% | update miss 11.1% | precision_hit 80.8% | precision_any 83.6% | exact-set match rate 69.0% | exact-set avg reward 0.381 | set_precision 80.8% | set_recall 72.8% | set_f1 76.6%
Hit rates (by modality): event 73.2% | time 72.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T07:47:22.065Z |
| Finished (UTC) | 2026-09-14T08:03:02.651Z |
| Duration | 15m 40.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 2 |
| Miss | 20 |
| False alarms | 12 |
| Commission | 0 |
| Wrong-content | 9 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 56 |
| Check_time calls | 35 |
| Actions | 73 |
| Exact-set matches | 58 |
| Exact-set mismatches | 26 |
| Exact-set reward | 32 |
| Set TP | 59 |
| Set FP | 14 |
| Set FN | 22 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 5 |
| calendar | 2 |
| clock | 35 |
| course_portal | 4 |
| email | 2 |
| laundry_status | 2 |
| library_hold | 1 |
| price_tracker | 3 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 72.8% |
| Late rate | 2.5% |
| Miss rate | 24.7% |
| False alarm/step | 14.3% |
| Commission rate | 0.0% |
| Wrong-content rate | 11.1% |
| Dependency/step | 0.0% |
| Overkill/step | 10.7% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 80.8% |
| Precision any | 83.6% |
| Exact-set match rate | 69.0% |
| Exact-set avg reward | 0.381 |
| Set precision | 80.8% |
| Set recall | 72.8% |
| Set F1 | 76.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 56 | 73.2% |
| Time (time + time_check) | 18 | 25 | 72.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 20 | 2 | 19 | 41 | 48.8% | 53.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| clock | 18 | 1 | 6 | 25 | 72.0% | 76.0% |
| course_portal | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 15.4% | 15.4% | 80.0% | 75.0% | 100.0% | 60.0% | 76.9% | 0.538 | 77.8% | 77.8% | 77.8% |
| Tuesday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 18.2% | 9.1% | 75.0% | 50.0% | 100.0% | 33.3% | 63.6% | 0.273 | 72.7% | 66.7% | 69.6% |
| Wednesday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 28.6% | 14.3% | 60.0% | 50.0% | 75.0% | 40.0% | 71.4% | 0.429 | 55.6% | 55.6% | 55.6% |
| Thursday | 12 | 0 | 4 | 75.0% | 0.0% | 25.0% | 20.0% | 20.0% | 76.9% | 66.7% | 100.0% | 33.3% | 50.0% | 0.000 | 85.7% | 75.0% | 80.0% |
| Friday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 8.3% | 8.3% | 75.0% | 66.7% | 100.0% | 50.0% | 66.7% | 0.333 | 80.0% | 72.7% | 76.2% |
| Saturday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 71.4% | 83.3% | 0.667 | 100.0% | 83.3% | 90.9% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 8.3% | 8.3% | 66.7% | 100.0% | 100.0% | 50.0% | 66.7% | 0.333 | 90.0% | 75.0% | 81.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 7 |
| Monday | email | 1 |
| Tuesday | appointment_portal | 1 |
| Tuesday | clock | 5 |
| Tuesday | email | 1 |
| Wednesday | appointment_portal | 4 |
| Wednesday | clock | 6 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 3 |
| Thursday | laundry_status | 1 |
| Thursday | price_tracker | 1 |
| Friday | calendar | 2 |
| Friday | clock | 3 |
| Friday | course_portal | 3 |
| Friday | price_tracker | 2 |
| Saturday | clock | 6 |
| Saturday | laundry_status | 1 |
| Saturday | shipment_status | 1 |
| Sunday | clock | 5 |
| Sunday | course_portal | 1 |
| Sunday | library_hold | 1 |
