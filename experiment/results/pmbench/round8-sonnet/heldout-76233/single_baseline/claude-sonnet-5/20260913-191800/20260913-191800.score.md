# PM-Bench score report

## Summary

Hit: 56 | Late: 3 | Miss: 20 | False alarms: 4 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 5 | state query calls: 33 | check_time calls: 24 | Actions: 63
Exact-set: matches 53 | mismatches 23 | reward 30
Set micro: TP 56 | FP 7 | FN 23
Cross-day: hit 6 | late 1 | miss 0 | total 7
Updates: hit 5 | late 1 | miss 3 | canceled 2 | total 11 | violations 3
Rates: hit 70.9% | late 3.8% | miss 25.3% | false alarm/step 5.3% | commission 0.0% | wrong-content 5.1% | dependency/step 0.0% | overkill/step 6.6% | cross-day miss 0.0% | update miss 33.3% | precision_hit 88.9% | precision_any 93.7% | exact-set match rate 69.7% | exact-set avg reward 0.395 | set_precision 88.9% | set_recall 70.9% | set_f1 78.9%
Hit rates (by modality): event 70.4% | time 72.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:18:00.229Z |
| Finished (UTC) | 2026-09-14T01:24:05.438Z |
| Duration | 6m 5.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 3 |
| Miss | 20 |
| False alarms | 4 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 5 |
| State query calls | 33 |
| Check_time calls | 24 |
| Actions | 63 |
| Exact-set matches | 53 |
| Exact-set mismatches | 23 |
| Exact-set reward | 30 |
| Set TP | 56 |
| Set FP | 7 |
| Set FN | 23 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 1 |
| calendar | 1 |
| clock | 24 |
| course_portal | 1 |
| email | 1 |
| laundry_status | 1 |
| price_tracker | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 70.9% |
| Late rate | 3.8% |
| Miss rate | 25.3% |
| False alarm/step | 5.3% |
| Commission rate | 0.0% |
| Wrong-content rate | 5.1% |
| Dependency/step | 0.0% |
| Overkill/step | 6.6% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 33.3% |
| Precision hit | 88.9% |
| Precision any | 93.7% |
| Exact-set match rate | 69.7% |
| Exact-set avg reward | 0.395 |
| Set precision | 88.9% |
| Set recall | 70.9% |
| Set F1 | 78.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 54 | 70.4% |
| Time (time + time_check) | 18 | 25 | 72.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 36 | 1 | 3 | 40 | 90.0% | 92.5% |
| proactive_monitoring_required | 20 | 2 | 17 | 39 | 51.3% | 56.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| clock | 18 | 2 | 5 | 25 | 72.0% | 80.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 8.3% | 8.3% | 71.4% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 88.9% | 72.7% | 80.0% |
| Tuesday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 0.0% | 0.0% | 77.8% | 75.0% | 100.0% | 50.0% | 80.0% | 0.600 | 100.0% | 76.9% | 87.0% |
| Wednesday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 10.0% | 0.0% | 71.4% | 66.7% | 75.0% | 66.7% | 80.0% | 0.600 | 87.5% | 70.0% | 77.8% |
| Thursday | 9 | 0 | 4 | 69.2% | 0.0% | 30.8% | 0.0% | 0.0% | 77.8% | 50.0% | 100.0% | 33.3% | 55.6% | 0.111 | 100.0% | 69.2% | 81.8% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 0.0% | 10.0% | 66.7% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 87.5% | 70.0% | 77.8% |
| Saturday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 8.3% | 8.3% | 62.5% | 100.0% | 83.3% | 50.0% | 75.0% | 0.500 | 87.5% | 70.0% | 77.8% |
| Sunday | 8 | 2 | 2 | 66.7% | 16.7% | 16.7% | 7.7% | 15.4% | 62.5% | 75.0% | 71.4% | 60.0% | 61.5% | 0.231 | 72.7% | 66.7% | 69.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | bank_balance | 1 |
| Monday | clock | 3 |
| Tuesday | clock | 2 |
| Tuesday | email | 1 |
| Wednesday | calendar | 1 |
| Wednesday | clock | 3 |
| Wednesday | laundry_status | 1 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 3 |
| Friday | clock | 4 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | clock | 4 |
| Saturday | course_portal | 1 |
| Sunday | clock | 5 |
