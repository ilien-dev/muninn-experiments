# PM-Bench score report

## Summary

Hit: 56 | Late: 3 | Miss: 22 | False alarms: 6 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 35 | check_time calls: 29 | Actions: 65
Exact-set: matches 52 | mismatches 28 | reward 24
Set micro: TP 56 | FP 9 | FN 25
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 4 | late 1 | miss 4 | canceled 2 | total 11 | violations 5
Rates: hit 69.1% | late 3.7% | miss 27.2% | false alarm/step 7.5% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 10.0% | cross-day miss 0.0% | update miss 44.4% | precision_hit 86.2% | precision_any 90.8% | exact-set match rate 65.0% | exact-set avg reward 0.300 | set_precision 86.2% | set_recall 69.1% | set_f1 76.7%
Hit rates (by modality): event 70.2% | time 66.7%

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
| Late | 3 |
| Miss | 22 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 35 |
| Check_time calls | 29 |
| Actions | 65 |
| Exact-set matches | 52 |
| Exact-set mismatches | 28 |
| Exact-set reward | 24 |
| Set TP | 56 |
| Set FP | 9 |
| Set FN | 25 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 29 |
| email | 3 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.1% |
| Late rate | 3.7% |
| Miss rate | 27.2% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 10.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 44.4% |
| Precision hit | 86.2% |
| Precision any | 90.8% |
| Exact-set match rate | 65.0% |
| Exact-set avg reward | 0.300 |
| Set precision | 86.2% |
| Set recall | 69.1% |
| Set F1 | 76.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 57 | 70.2% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 40 | 0 | 2 | 42 | 95.2% | 95.2% |
| proactive_monitoring_required | 16 | 3 | 20 | 39 | 41.0% | 48.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 16 | 2 | 6 | 24 | 66.7% | 75.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 23.1% | 23.1% | 57.1% | 25.0% | 100.0% | 14.3% | 46.2% | -0.077 | 62.5% | 45.5% | 52.6% |
| Wednesday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 40.0% | 80.0% | 0.600 | 100.0% | 72.7% | 84.2% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 9.1% | 18.2% | 88.9% | 33.3% | 100.0% | 25.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 0.0% | 75.0% | 75.0% | 100.0% | 50.0% | 75.0% | 0.500 | 90.0% | 75.0% | 81.8% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 10.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 91.7% | 78.6% | 84.6% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 18.2% | 60.0% | 75.0% | 75.0% | 60.0% | 54.5% | 0.091 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 5 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 1 |
| Friday | clock | 6 |
| Friday | email | 3 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 5 |
