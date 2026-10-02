# PM-Bench score report

## Summary

Hit: 57 | Late: 2 | Miss: 22 | False alarms: 12 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 12 | state query calls: 52 | check_time calls: 33 | Actions: 71
Exact-set: matches 52 | mismatches 32 | reward 20
Set micro: TP 57 | FP 14 | FN 24
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 2 | miss 1 | canceled 2 | total 11 | violations 3
Rates: hit 70.4% | late 2.5% | miss 27.2% | false alarm/step 14.3% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 14.3% | cross-day miss 0.0% | update miss 11.1% | precision_hit 80.3% | precision_any 83.1% | exact-set match rate 61.9% | exact-set avg reward 0.238 | set_precision 80.3% | set_recall 70.4% | set_f1 75.0%
Hit rates (by modality): event 69.6% | time 72.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T07:20:22.532Z |
| Finished (UTC) | 2026-09-14T07:36:59.627Z |
| Duration | 16m 37.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 57 |
| Late | 2 |
| Miss | 22 |
| False alarms | 12 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 12 |
| State query calls | 52 |
| Check_time calls | 33 |
| Actions | 71 |
| Exact-set matches | 52 |
| Exact-set mismatches | 32 |
| Exact-set reward | 20 |
| Set TP | 57 |
| Set FP | 14 |
| Set FN | 24 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 1 |
| calendar | 2 |
| clock | 33 |
| course_portal | 5 |
| email | 1 |
| laundry_status | 1 |
| library_hold | 1 |
| price_tracker | 3 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 70.4% |
| Late rate | 2.5% |
| Miss rate | 27.2% |
| False alarm/step | 14.3% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 14.3% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 80.3% |
| Precision any | 83.1% |
| Exact-set match rate | 61.9% |
| Exact-set avg reward | 0.238 |
| Set precision | 80.3% |
| Set recall | 70.4% |
| Set F1 | 75.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 56 | 69.6% |
| Time (time + time_check) | 18 | 25 | 72.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 19 | 2 | 20 | 41 | 46.3% | 51.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 18 | 2 | 5 | 25 | 72.0% | 80.0% |
| course_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 23.1% | 23.1% | 60.0% | 75.0% | 75.0% | 60.0% | 61.5% | 0.231 | 66.7% | 66.7% | 66.7% |
| Tuesday | 8 | 2 | 2 | 66.7% | 16.7% | 16.7% | 0.0% | 18.2% | 75.0% | 50.0% | 100.0% | 33.3% | 63.6% | 0.273 | 80.0% | 66.7% | 72.7% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 14.3% | 7.1% | 60.0% | 100.0% | 75.0% | 80.0% | 78.6% | 0.571 | 77.8% | 77.8% | 77.8% |
| Thursday | 12 | 0 | 4 | 75.0% | 0.0% | 25.0% | 10.0% | 10.0% | 76.9% | 66.7% | 100.0% | 33.3% | 50.0% | 0.000 | 92.3% | 75.0% | 82.8% |
| Friday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 33.3% | 25.0% | 62.5% | 33.3% | 100.0% | 16.7% | 41.7% | -0.167 | 60.0% | 54.5% | 57.1% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 8.3% | 8.3% | 75.0% | 75.0% | 100.0% | 57.1% | 66.7% | 0.333 | 90.0% | 75.0% | 81.8% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 8.3% | 8.3% | 66.7% | 100.0% | 100.0% | 50.0% | 66.7% | 0.333 | 90.0% | 75.0% | 81.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 7 |
| Monday | email | 1 |
| Monday | shipment_status | 1 |
| Tuesday | clock | 5 |
| Tuesday | course_portal | 1 |
| Wednesday | appointment_portal | 3 |
| Wednesday | clock | 6 |
| Thursday | clock | 2 |
| Thursday | laundry_status | 1 |
| Thursday | price_tracker | 2 |
| Friday | calendar | 2 |
| Friday | clock | 3 |
| Friday | course_portal | 3 |
| Friday | price_tracker | 1 |
| Saturday | clock | 6 |
| Saturday | shipment_status | 1 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |
| Sunday | course_portal | 1 |
| Sunday | library_hold | 1 |
