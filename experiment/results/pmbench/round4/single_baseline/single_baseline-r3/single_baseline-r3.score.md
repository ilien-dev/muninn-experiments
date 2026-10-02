# PM-Bench score report

## Summary

Hit: 56 | Late: 2 | Miss: 23 | False alarms: 6 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 34 | check_time calls: 29 | Actions: 64
Exact-set: matches 53 | mismatches 27 | reward 26
Set micro: TP 56 | FP 8 | FN 25
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 1
Rates: hit 69.1% | late 2.5% | miss 28.4% | false alarm/step 7.5% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 7.5% | cross-day miss 0.0% | update miss 33.3% | precision_hit 87.5% | precision_any 90.6% | exact-set match rate 66.2% | exact-set avg reward 0.325 | set_precision 87.5% | set_recall 69.1% | set_f1 77.2%
Hit rates (by modality): event 68.4% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | n/a |
| Finished (UTC) | n/a |
| Duration | n/a |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 2 |
| Miss | 23 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 34 |
| Check_time calls | 29 |
| Actions | 64 |
| Exact-set matches | 53 |
| Exact-set mismatches | 27 |
| Exact-set reward | 26 |
| Set TP | 56 |
| Set FP | 8 |
| Set FN | 25 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 29 |
| email | 1 |
| library_hold | 1 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.1% |
| Late rate | 2.5% |
| Miss rate | 28.4% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 7.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 33.3% |
| Precision hit | 87.5% |
| Precision any | 90.6% |
| Exact-set match rate | 66.2% |
| Exact-set avg reward | 0.325 |
| Set precision | 87.5% |
| Set recall | 69.1% |
| Set F1 | 77.2% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 3 | 42 | 92.9% | 92.9% |
| proactive_monitoring_required | 17 | 2 | 20 | 39 | 43.6% | 48.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 17 | 1 | 6 | 24 | 70.8% | 75.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 10.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 87.5% | 63.6% | 73.7% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 18.2% | 18.2% | 77.8% | 33.3% | 87.5% | 25.0% | 63.6% | 0.273 | 80.0% | 66.7% | 72.7% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 10.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 91.7% | 78.6% | 84.6% |
| Sunday | 5 | 1 | 3 | 55.6% | 11.1% | 33.3% | 18.2% | 18.2% | 60.0% | 50.0% | 75.0% | 40.0% | 45.5% | -0.091 | 62.5% | 55.6% | 58.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 4 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 5 |
| Thursday | shipment_status | 1 |
| Friday | clock | 6 |
| Friday | email | 1 |
| Friday | library_hold | 1 |
| Saturday | clock | 5 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |
