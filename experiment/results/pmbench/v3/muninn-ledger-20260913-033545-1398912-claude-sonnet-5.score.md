# PM-Bench score report

## Summary

Hit: 37 | Late: 0 | Miss: 44 | False alarms: 6 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 2 | check_time calls: 1 | Actions: 43
Exact-set: matches 42 | mismatches 38 | reward 4
Set micro: TP 37 | FP 6 | FN 44
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 4 | late 0 | miss 5 | canceled 2 | total 11 | violations 4
Rates: hit 45.7% | late 0.0% | miss 54.3% | false alarm/step 7.5% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 7.5% | cross-day miss 100.0% | update miss 55.6% | precision_hit 86.0% | precision_any 86.0% | exact-set match rate 52.5% | exact-set avg reward 0.050 | set_precision 86.0% | set_recall 45.7% | set_f1 59.7%
Hit rates (by modality): event 54.4% | time 25.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T09:35:44.680Z |
| Finished (UTC) | 2026-09-13T09:54:15.526Z |
| Duration | 18m 30.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 37 |
| Late | 0 |
| Miss | 44 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 2 |
| Check_time calls | 1 |
| Actions | 43 |
| Exact-set matches | 42 |
| Exact-set mismatches | 38 |
| Exact-set reward | 4 |
| Set TP | 37 |
| Set FP | 6 |
| Set FN | 44 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 45.7% |
| Late rate | 0.0% |
| Miss rate | 54.3% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 7.5% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 55.6% |
| Precision hit | 86.0% |
| Precision any | 86.0% |
| Exact-set match rate | 52.5% |
| Exact-set avg reward | 0.050 |
| Set precision | 86.0% |
| Set recall | 45.7% |
| Set F1 | 59.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 31 | 57 | 54.4% |
| Time (time + time_check) | 6 | 24 | 25.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 31 | 0 | 11 | 42 | 73.8% | 73.8% |
| proactive_monitoring_required | 6 | 0 | 33 | 39 | 15.4% | 15.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 6 | 0 | 18 | 24 | 25.0% | 25.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 15.4% | 15.4% | 57.1% | 50.0% | 100.0% | 28.6% | 53.8% | 0.077 | 75.0% | 54.5% | 63.2% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 10.0% | 10.0% | 44.4% | 0.0% | 66.7% | 0.0% | 40.0% | -0.200 | 80.0% | 36.4% | 50.0% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 0.0% | 0.0% | 66.7% | 0.0% | 75.0% | 0.0% | 63.6% | 0.273 | 100.0% | 50.0% | 66.7% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 8.3% | 8.3% | 50.0% | 25.0% | 66.7% | 16.7% | 41.7% | -0.167 | 83.3% | 41.7% | 55.6% |
| Saturday | 4 | 0 | 10 | 28.6% | 0.0% | 71.4% | 10.0% | 10.0% | 40.0% | 0.0% | 50.0% | 0.0% | 30.0% | -0.400 | 80.0% | 28.6% | 42.1% |
| Sunday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 9.1% | 9.1% | 80.0% | 0.0% | 100.0% | 0.0% | 54.5% | 0.091 | 80.0% | 44.4% | 57.1% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | (none) | 0 |
| Wednesday | bank_balance | 1 |
| Thursday | (none) | 0 |
| Friday | (none) | 0 |
| Saturday | (none) | 0 |
| Sunday | (none) | 0 |
