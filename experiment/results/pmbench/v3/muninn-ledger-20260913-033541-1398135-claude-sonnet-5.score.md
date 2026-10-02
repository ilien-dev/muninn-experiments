# PM-Bench score report

## Summary

Hit: 34 | Late: 1 | Miss: 46 | False alarms: 7 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 5 | state query calls: 3 | check_time calls: 3 | Actions: 42
Exact-set: matches 44 | mismatches 36 | reward 8
Set micro: TP 34 | FP 8 | FN 47
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 2 | late 0 | miss 7 | canceled 2 | total 11 | violations 5
Rates: hit 42.0% | late 1.2% | miss 56.8% | false alarm/step 8.8% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 6.2% | cross-day miss 100.0% | update miss 77.8% | precision_hit 81.0% | precision_any 83.3% | exact-set match rate 55.0% | exact-set avg reward 0.100 | set_precision 81.0% | set_recall 42.0% | set_f1 55.3%
Hit rates (by modality): event 49.1% | time 25.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T09:35:40.681Z |
| Finished (UTC) | 2026-09-13T09:54:11.923Z |
| Duration | 18m 31.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 34 |
| Late | 1 |
| Miss | 46 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 5 |
| State query calls | 3 |
| Check_time calls | 3 |
| Actions | 42 |
| Exact-set matches | 44 |
| Exact-set mismatches | 36 |
| Exact-set reward | 8 |
| Set TP | 34 |
| Set FP | 8 |
| Set FN | 47 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 3 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 42.0% |
| Late rate | 1.2% |
| Miss rate | 56.8% |
| False alarm/step | 8.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 6.2% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 77.8% |
| Precision hit | 81.0% |
| Precision any | 83.3% |
| Exact-set match rate | 55.0% |
| Exact-set avg reward | 0.100 |
| Set precision | 81.0% |
| Set recall | 42.0% |
| Set F1 | 55.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 28 | 57 | 49.1% |
| Time (time + time_check) | 6 | 24 | 25.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 28 | 0 | 14 | 42 | 66.7% | 66.7% |
| proactive_monitoring_required | 6 | 1 | 32 | 39 | 15.4% | 17.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 6 | 0 | 18 | 24 | 25.0% | 25.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 7.7% | 7.7% | 55.6% | 66.7% | 83.3% | 33.3% | 69.2% | 0.385 | 87.5% | 58.3% | 70.0% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 23.1% | 15.4% | 57.1% | 50.0% | 100.0% | 28.6% | 53.8% | 0.077 | 66.7% | 54.5% | 60.0% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 20.0% | 10.0% | 33.3% | 50.0% | 50.0% | 20.0% | 50.0% | 0.000 | 66.7% | 36.4% | 47.1% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 0.0% | 0.0% | 66.7% | 0.0% | 75.0% | 0.0% | 63.6% | 0.273 | 100.0% | 50.0% | 66.7% |
| Friday | 3 | 1 | 8 | 25.0% | 8.3% | 66.7% | 8.3% | 8.3% | 25.0% | 25.0% | 33.3% | 16.7% | 41.7% | -0.167 | 60.0% | 25.0% | 35.3% |
| Saturday | 4 | 0 | 10 | 28.6% | 0.0% | 71.4% | 0.0% | 0.0% | 40.0% | 0.0% | 50.0% | 0.0% | 40.0% | -0.200 | 100.0% | 28.6% | 44.4% |
| Sunday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 0.0% | 0.0% | 80.0% | 0.0% | 100.0% | 0.0% | 63.6% | 0.273 | 100.0% | 44.4% | 61.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | (none) | 0 |
| Wednesday | (none) | 0 |
| Thursday | (none) | 0 |
| Friday | clock | 1 |
| Saturday | (none) | 0 |
| Sunday | clock | 1 |
