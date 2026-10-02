# PM-Bench score report

## Summary

Hit: 58 | Late: 1 | Miss: 20 | False alarms: 3 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 3 | state query calls: 34 | check_time calls: 28 | Actions: 62
Exact-set: matches 56 | mismatches 20 | reward 36
Set micro: TP 58 | FP 4 | FN 21
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 73.4% | late 1.3% | miss 25.3% | false alarm/step 3.9% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 3.9% | cross-day miss 0.0% | update miss 22.2% | precision_hit 93.5% | precision_any 95.2% | exact-set match rate 73.7% | exact-set avg reward 0.474 | set_precision 93.5% | set_recall 73.4% | set_f1 82.3%
Hit rates (by modality): event 72.2% | time 76.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:12:43.079Z |
| Finished (UTC) | 2026-09-14T01:19:26.419Z |
| Duration | 6m 43.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 58 |
| Late | 1 |
| Miss | 20 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 3 |
| State query calls | 34 |
| Check_time calls | 28 |
| Actions | 62 |
| Exact-set matches | 56 |
| Exact-set mismatches | 20 |
| Exact-set reward | 36 |
| Set TP | 58 |
| Set FP | 4 |
| Set FN | 21 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 1 |
| clock | 28 |
| email | 1 |
| price_tracker | 2 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 73.4% |
| Late rate | 1.3% |
| Miss rate | 25.3% |
| False alarm/step | 3.9% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 3.9% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 93.5% |
| Precision any | 95.2% |
| Exact-set match rate | 73.7% |
| Exact-set avg reward | 0.474 |
| Set precision | 93.5% |
| Set recall | 73.4% |
| Set F1 | 82.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 54 | 72.2% |
| Time (time + time_check) | 19 | 25 | 76.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 19 | 1 | 19 | 39 | 48.7% | 51.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 19 | 1 | 5 | 25 | 76.0% | 80.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 0.0% | 0.0% | 71.4% | 75.0% | 100.0% | 50.0% | 75.0% | 0.500 | 100.0% | 72.7% | 84.2% |
| Tuesday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 10.0% | 10.0% | 77.8% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 90.9% | 76.9% | 83.3% |
| Wednesday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 0.0% | 0.0% | 57.1% | 66.7% | 100.0% | 33.3% | 70.0% | 0.400 | 100.0% | 60.0% | 75.0% |
| Thursday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 0.0% | 0.0% | 77.8% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 100.0% | 76.9% | 87.0% |
| Friday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 0.0% | 0.0% | 66.7% | 75.0% | 100.0% | 50.0% | 80.0% | 0.600 | 100.0% | 70.0% | 82.4% |
| Saturday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 8.3% | 8.3% | 62.5% | 100.0% | 83.3% | 50.0% | 75.0% | 0.500 | 87.5% | 70.0% | 77.8% |
| Sunday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 7.7% | 7.7% | 87.5% | 75.0% | 100.0% | 60.0% | 76.9% | 0.538 | 83.3% | 83.3% | 83.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | bank_balance | 1 |
| Monday | clock | 3 |
| Tuesday | clock | 2 |
| Tuesday | email | 1 |
| Wednesday | clock | 3 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 4 |
| Friday | clock | 5 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | clock | 6 |
| Sunday | clock | 5 |
| Sunday | shipment_status | 1 |
