# PM-Bench score report

## Summary

Hit: 58 | Late: 0 | Miss: 23 | False alarms: 18 | Commission: 0 | Wrong-content: 10 | Dependency violations: 0 | Overkill steps: 13 | state query calls: 67 | check_time calls: 37 | Actions: 76
Exact-set: matches 53 | mismatches 31 | reward 22
Set micro: TP 58 | FP 18 | FN 23
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 71.6% | late 0.0% | miss 28.4% | false alarm/step 21.4% | commission 0.0% | wrong-content 12.3% | dependency/step 0.0% | overkill/step 15.5% | cross-day miss 0.0% | update miss 22.2% | precision_hit 76.3% | precision_any 76.3% | exact-set match rate 63.1% | exact-set avg reward 0.262 | set_precision 76.3% | set_recall 71.6% | set_f1 73.9%
Hit rates (by modality): event 73.2% | time 68.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T07:02:21.943Z |
| Finished (UTC) | 2026-09-14T07:15:17.880Z |
| Duration | 12m 55.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 58 |
| Late | 0 |
| Miss | 23 |
| False alarms | 18 |
| Commission | 0 |
| Wrong-content | 10 |
| Dependency violations | 0 |
| Overkill steps | 13 |
| State query calls | 67 |
| Check_time calls | 37 |
| Actions | 76 |
| Exact-set matches | 53 |
| Exact-set mismatches | 31 |
| Exact-set reward | 22 |
| Set TP | 58 |
| Set FP | 18 |
| Set FN | 23 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 1 |
| calendar | 2 |
| clock | 37 |
| course_portal | 6 |
| email | 5 |
| laundry_status | 2 |
| library_hold | 2 |
| price_tracker | 5 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 71.6% |
| Late rate | 0.0% |
| Miss rate | 28.4% |
| False alarm/step | 21.4% |
| Commission rate | 0.0% |
| Wrong-content rate | 12.3% |
| Dependency/step | 0.0% |
| Overkill/step | 15.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 76.3% |
| Precision any | 76.3% |
| Exact-set match rate | 63.1% |
| Exact-set avg reward | 0.262 |
| Set precision | 76.3% |
| Set recall | 71.6% |
| Set F1 | 73.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 56 | 73.2% |
| Time (time + time_check) | 17 | 25 | 68.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 20 | 0 | 21 | 41 | 48.8% | 48.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 17 | 0 | 8 | 25 | 68.0% | 68.0% |
| course_portal | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 3 | 4 | 25.0% | 25.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 15.4% | 15.4% | 80.0% | 75.0% | 100.0% | 60.0% | 76.9% | 0.538 | 77.8% | 77.8% | 77.8% |
| Tuesday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 18.2% | 9.1% | 75.0% | 100.0% | 100.0% | 66.7% | 72.7% | 0.455 | 83.3% | 83.3% | 83.3% |
| Wednesday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 28.6% | 14.3% | 60.0% | 50.0% | 75.0% | 40.0% | 71.4% | 0.429 | 55.6% | 55.6% | 55.6% |
| Thursday | 11 | 0 | 5 | 68.8% | 0.0% | 31.2% | 30.0% | 30.0% | 76.9% | 33.3% | 100.0% | 16.7% | 30.0% | -0.400 | 78.6% | 68.8% | 73.3% |
| Friday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 33.3% | 25.0% | 75.0% | 33.3% | 80.0% | 50.0% | 50.0% | 0.000 | 63.6% | 63.6% | 63.6% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 62.5% | 100.0% | 100.0% | 57.1% | 75.0% | 0.500 | 100.0% | 75.0% | 85.7% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 25.0% | 16.7% | 77.8% | 66.7% | 100.0% | 50.0% | 58.3% | 0.167 | 75.0% | 75.0% | 75.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 7 |
| Monday | email | 1 |
| Tuesday | appointment_portal | 1 |
| Tuesday | clock | 5 |
| Tuesday | email | 1 |
| Wednesday | appointment_portal | 2 |
| Wednesday | clock | 8 |
| Wednesday | email | 3 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 2 |
| Thursday | laundry_status | 1 |
| Thursday | price_tracker | 2 |
| Friday | calendar | 2 |
| Friday | clock | 4 |
| Friday | course_portal | 4 |
| Friday | price_tracker | 2 |
| Saturday | clock | 6 |
| Saturday | laundry_status | 1 |
| Saturday | price_tracker | 1 |
| Saturday | shipment_status | 3 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 5 |
| Sunday | course_portal | 2 |
| Sunday | library_hold | 2 |
